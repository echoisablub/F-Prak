import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.optimize import minimize, curve_fit
from scipy.special import erfc
plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 14,
    "axes.labelsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "legend.title_fontsize": 14,
})

def load_spectrum(file):
    data = np.loadtxt(
        file,
        #sep=r'\s+',
        comments="#"
    )
    number = data[:, 0]
    energy = data[:, 1]
    intensity = data[:, 2]

    return energy, intensity

def load_reference_spectra(ref_file):

    data = np.loadtxt(
        ref_file,
        delimiter=",",
        comments="#",
        skiprows=1
    )

    energy_ref = data[:, 0]
    reference_spectra = data[:, 1:6]

    return energy_ref, reference_spectra

def build_deltaI_matrix_from_folders(
    data_folder: Path,
    delays,
    delay_names,
    load_spectrum,
):
    all_means = []
    all_sigmas = []
    t_fs_list = []

    energy_common = None

    for delay, delay_name in zip(delays, delay_names):
        folder = data_folder / delay_name
        files = sorted(folder.glob("*"))

        spectra_interp = []
        energies = []

        #print(f"Delay: {delay} fs")

        for file in files:
            energy, intensity = load_spectrum(file)
            energies.append(energy)

        #common energy grid
        energy_common = energies[0]
        spectra = []

        #interpolate to common grid
        for file in files:
            energy, intensity = load_spectrum(file)
            f = interp1d(energy, intensity, bounds_error=False, fill_value=np.nan)
            spectra.append(f(energy_common))

        spectra = np.array(spectra)  # (n_shots, NE)

        mean_intensity = np.nanmean(spectra, axis=0)  # (NE,)
        std_intensity = np.nanstd(spectra, axis=0, ddof=1)

        n_shots = np.sum(~np.isnan(spectra[:, 0]))  

        #assume same n_shots across bins:
        sem_intensity = std_intensity / np.sqrt(len(spectra))

        #avoid sigma=0 bc no dividing by zero
        sigma = sem_intensity.copy()
        positive_sigma = sigma[sigma > 0]
        minimum_sigma = np.min(positive_sigma) if len(positive_sigma) > 0 else 1.0
        sigma[sigma <= 0] = minimum_sigma

        all_means.append(mean_intensity)
        all_sigmas.append(sigma)
        t_fs_list.append(delay)

    dI_mean = np.array(all_means)
    sigma = np.array(all_sigmas)
    t_fs = np.array(t_fs_list)

    return t_fs, energy_common, dI_mean, sigma

def fit_difference_spectrum(energy, difference, sigma, reference_spectra, fixed_amplitude=None):
    """Fit S1 through S5 with L_off = S1.
    D(E) = A * (L_on(E) - L_off(E)) with
    L_on = f_5 S_5 + f_4 S_4 + f_3 S_3 + f_2 S_2 + (1 - f_5 - f_4 - f_3 - f_2) S_1
    """
    ground_state = reference_spectra[:, 0]

    def model(parameters):
        amplitude = fixed_amplitude
        excited_populations = parameters

        singlet_population = 1.0 - np.sum(excited_populations)
        populations = np.concatenate(([singlet_population], excited_populations))
        fitted = amplitude * (reference_spectra @ populations - ground_state)
        return fitted, populations

    def objective(parameters):
        fitted, _ = model(parameters)
        return np.sum(((difference - fitted) / sigma) ** 2)

    x0 = np.array([0.1, 0.1, 0.1, 0.1])
    bounds = [(0.0, 1.0)] * 4
    population_parameters = lambda parameters: parameters

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints={"type": "ineq", "fun": lambda parameters: 1.0 - np.sum(population_parameters(parameters))},
        options={"ftol": 1e-12, "maxiter": 2000},
    )

    amplitude = fixed_amplitude
    fitted, populations = model(result.x)
    return amplitude, populations, fitted, result

def fit_amplitude_for_pure_quintet(difference, sigma, reference_spectra):
    """Determine A assuming the calibration spectrum is entirely S5."""
    quintet_difference = reference_spectra[:, 4] - reference_spectra[:, 0]
    weights = 1.0 / sigma**2
    denominator = np.sum(weights * quintet_difference**2)
    amplitude = np.sum(weights * difference * quintet_difference) / denominator
    residuals = (difference - amplitude * quintet_difference) / sigma

    # stuff for error
    degrees_of_freedom = difference.size - 1
    chi2 = np.sum(residuals**2)
    reduced_chi2 = chi2 / degrees_of_freedom
    formal_uncertainty = np.sqrt(1.0 / denominator)
    scaled_uncertainty = formal_uncertainty * np.sqrt(reduced_chi2)
    
    return amplitude, scaled_uncertainty, formal_uncertainty, reduced_chi2

def estimate_population_uncertainties(result, difference, sigma, reference_spectra, amplitude=None):
    """Estimate uncertainties for populations [S1, S2, S3, S4, S5]."""
    parameters = result.x
    ground_state = reference_spectra[:, 0]

    def weighted_residuals(parameters):
        fit_amplitude = amplitude
        excited_populations = parameters

        singlet_population = 1.0 - np.sum(excited_populations)
        populations = np.concatenate(([singlet_population], excited_populations))
        fitted = fit_amplitude * (reference_spectra @ populations - ground_state)
        return (difference - fitted) / sigma

    jacobian = np.empty((difference.size, parameters.size))
    for parameter_index, parameter in enumerate(parameters):
        step = np.sqrt(np.finfo(float).eps) * max(1.0, abs(parameter))
        shifted_plus = parameters.copy()
        shifted_minus = parameters.copy()
        shifted_plus[parameter_index] += step
        shifted_minus[parameter_index] -= step
        jacobian[:, parameter_index] = (
            weighted_residuals(shifted_plus) - weighted_residuals(shifted_minus)
        ) / (2 * step)

    covariance = np.linalg.pinv(jacobian.T @ jacobian)
    population_transform = np.zeros((5, 4))
    population_transform[0, :] = -1.0
    population_transform[1:, :] = np.eye(4)

    population_covariance = population_transform @ covariance @ population_transform.T
    return np.sqrt(np.maximum(np.diag(population_covariance), 0.0))

def fit_singlet_transition(time_fs, singlet_population, singlet_uncertainty):
    """
    Fit a falling Gaussian-CDF edge and return t0 and its width (CDF: cumulative distribution function)
    f(t)= f_after + 0.5 * ∆f * erf((t - t_0)/(sigma_time * sqrt(2)))
    t0 is the midpoint of the population drop. 
    sigma_time is the standard deviation of the Gaussian temporal response (not the FWHM)
    """
    time_fs = np.asarray(time_fs, dtype=float)
    singlet_population = np.asarray(singlet_population, dtype=float)
    singlet_uncertainty = np.asarray(singlet_uncertainty, dtype=float)

    def model(time, population_after, population_drop, t0, sigma_time):
        return population_after + 0.5 * population_drop * erfc((time - t0) / (np.sqrt(2.0) * sigma_time))

    # init param: population_after aus dem letzten messwert [0,1], population_drop aus erstem minus letztem Messwert [0,1], t0 [at f_1 nearest 0.5], sigma_time [time range/5, 1]
    initial_parameters = [np.clip(singlet_population[-1], 0.0, 1.0), np.clip(singlet_population[0] - singlet_population[-1], 0.0, 1.0), time_fs[np.argmin(np.abs(singlet_population - 0.5))], max(np.ptp(time_fs) / 5.0, 1.0)]
    # bounds: population_after [0,1], population_drop [0,1], t0 [can be slightly out of mesured range], sigma_time [>0, max 10*time range]
    parameter_bounds = ([0.0, 0.0, np.min(time_fs) - np.ptp(time_fs), 1e-6], [1.0, 1.0, np.max(time_fs) + np.ptp(time_fs), 10.0 * np.ptp(time_fs)])

    fit_parameters, covariance = curve_fit(
        model,
        time_fs,
        singlet_population,
        p0=initial_parameters,
        sigma=singlet_uncertainty,
        absolute_sigma=True,
        bounds=parameter_bounds,
        maxfev=100000,
    )
    parameter_uncertainties = np.sqrt(np.maximum(np.diag(covariance), 0.0))
    return model, fit_parameters, parameter_uncertainties

#---lets try it out---yippieyippieyippie
ref_file = Path("Daten/Analysis and Interpretation/Ref Spectrum/Reference_Data_Fig_4_4.csv")
data_folder = Path("Daten/Experiment with Data Acquisition/messreihe")

delays = [-150, -100, -50, 0, 50, 100, 150, 200, 250, 300, 350, 400, 600, 800]
delay_names = ["min150 fs", "min100 fs", "min50 fs", "0 fs", "50 fs", "100 fs", "150 fs", "200 fs", "250 fs", "300 fs", "350 fs", "400 fs", "600 fs", "800 fs"]

# deltaI matrix aus measurements
t_fs, energy_common, dI_mean, sigma = build_deltaI_matrix_from_folders(data_folder=data_folder, delays=delays, delay_names=delay_names, load_spectrum=load_spectrum)

# load and interpolate all five reference spectra
energy_ref, reference_ref = load_reference_spectra(ref_file)
reference_spectra = np.column_stack([
    interp1d(energy_ref, reference_ref[:, state], bounds_error=False, fill_value=np.nan)(energy_common)
    for state in range(reference_ref.shape[1])])

valid = (
    np.isfinite(dI_mean).all(axis=0)
    & np.isfinite(sigma).all(axis=0)
    & np.isfinite(reference_spectra).all(axis=1)
    & (sigma > 0).all(axis=0)
)

energy_fit = energy_common[valid]
dI_fit = dI_mean[:, valid]
sigma_fit = sigma[:, valid]
reference_fit = reference_spectra[valid]

# A wird einmal aus der 800-fs-Messung bestimmt und danach festgehalten.
# Für 100 ps müsste dieser Wert auf 100_000 gesetzt werden und der entsprechende Messordner in delays/delay_names vorhanden sein.
calibration_delay_fs = 800
calibration_indices = np.flatnonzero(t_fs == calibration_delay_fs)
calibration_index = calibration_indices[0]
(   calibration_amplitude,
    calibration_amplitude_uncertainty,
    calibration_formal_uncertainty,
    calibration_reduced_chi2,
) = fit_amplitude_for_pure_quintet(
    dI_fit[calibration_index],
    sigma_fit[calibration_index],
    reference_fit,
)
print(
    f"Kalibrierung bei {calibration_delay_fs:g} fs als reines Quintett: "
    f"A = {calibration_amplitude:.5g} +/- {calibration_amplitude_uncertainty:.3g} "
    f"(formal: {calibration_formal_uncertainty:.3g}, "
    f"reduced chi2: {calibration_reduced_chi2:.3g})")

# jtz ist kein prep mehr
amplitudes = []
populations = []
population_uncertainties = []
fitted_spectra = []
for delay, difference, uncertainty in zip(t_fs, dI_fit, sigma_fit):
    amplitude, population, fitted, result = fit_difference_spectrum(
        energy_fit,
        difference,
        uncertainty,
        reference_fit,
        fixed_amplitude=calibration_amplitude,
    )
    amplitudes.append(amplitude)
    populations.append(population)
    population_uncertainties.append(
        estimate_population_uncertainties(
            result,
            difference,
            uncertainty,
            reference_fit,
            amplitude=calibration_amplitude,
        )
    )
    fitted_spectra.append(fitted)
    print(f"{delay:>5.0f} fs: populations = {population}")

amplitudes = np.array(amplitudes)
populations = np.array(populations)
population_uncertainties = np.array(population_uncertainties)
fitted_spectra = np.array(fitted_spectra)
normalized_residuals = (dI_fit - fitted_spectra) / sigma_fit

# plot
state_names = ["singlet", "doublet", "triplet", "quartet", "quintet"]

plt.figure(figsize=(7, 4.5))
for index, state_name in enumerate(state_names):
    plt.errorbar(
        t_fs,
        populations[:, index],
        yerr=population_uncertainties[:, index],
        fmt="o-",
        capsize=3,
        label=state_name,
    )
plt.xlabel("Time delay [fs]")
plt.ylabel("Population $f_s$")
plt.ylim(-0.02, 1.02)
plt.legend()
plt.tight_layout()
plt.savefig("Auswertung EXP21/fit/actual fit/population_fit.png")
#plt.show()

# t0 aus dem Abfall der Singulettpopulation bestimmen
singlet_model, singlet_fit_parameters, singlet_fit_uncertainties = fit_singlet_transition(t_fs, populations[:, 0], population_uncertainties[:, 0])
population_after, population_drop, t0_fs, sigma_time_fs = singlet_fit_parameters
t0_uncertainty_fs = singlet_fit_uncertainties[2]
sigma_time_uncertainty_fs = singlet_fit_uncertainties[3]
fwhm_time_fs = 2.0 * np.sqrt(2.0 * np.log(2.0)) * sigma_time_fs
fwhm_uncertainty_fs = 2.0 * np.sqrt(2.0 * np.log(2.0)) * sigma_time_uncertainty_fs

print(
    f"Singulett-Flanke: t0 = {t0_fs:.2f} +/- {t0_uncertainty_fs:.2f} fs, "
    f"sigma_t = {sigma_time_fs:.2f} +/- {sigma_time_uncertainty_fs:.2f} fs, "
    f"FWHM = {fwhm_time_fs:.2f} +/- {fwhm_uncertainty_fs:.2f} fs"
)

time_dense_fs = np.linspace(np.min(t_fs), np.max(t_fs), 500)
plt.figure(figsize=(7, 4.5))
plt.errorbar(
    t_fs,
    populations[:, 0],
    yerr=population_uncertainties[:, 0],
    fmt="o",
    capsize=3,
    label="singlet data",
)
plt.plot(
    time_dense_fs,
    singlet_model(time_dense_fs, *singlet_fit_parameters),
    color="tab:red",
    label=rf"Gaussian-CDF fit, $t_0={t0_fs:.1f}\,\mathrm{{fs}}$",
)
plt.axvline(t0_fs, color="tab:red", linestyle="--", linewidth=1)
plt.xlabel("Time delay [fs]")
plt.ylabel("Singlet population $f_1$")
plt.ylim(-0.02, 1.02)
plt.legend()
plt.tight_layout()
plt.savefig("Auswertung EXP21/fit/actual fit/singlet_transition_fit.png")
#plt.show()
