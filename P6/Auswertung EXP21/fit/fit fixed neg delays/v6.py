import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.optimize import minimize
from matplotlib.colors import to_rgba
'''plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 14,
    "axes.labelsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "legend.title_fontsize": 14,
})'''

def load_spectrum(file):
    data = np.loadtxt(file, comments="#")
    number = data[:, 0]
    energy = data[:, 1]
    intensity = data[:, 2]
    return energy, intensity

def load_reference_spectra(ref_file):
    data = np.loadtxt(ref_file, delimiter=",", comments="#", skiprows=1)
    energy_ref = data[:, 0]
    reference_spectra = data[:, 1:6]
    return energy_ref, reference_spectra

def build_deltaI_matrix_from_folders(data_folder: Path, delays, delay_names, load_spectrum):
    all_means = []
    all_sigmas = []
    t_fs_list = []

    energy_common = None

    for delay, delay_name in zip(delays, delay_names):
        folder = data_folder / delay_name
        files = sorted(folder.glob("*"))
        spectra_interp = []
        energies = []

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

        spectra = np.array(spectra)
        mean_intensity = np.nanmean(spectra, axis=0)
        std_intensity = np.nanstd(spectra, axis=0, ddof=1)

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

def fit_difference_spectrum(energy, difference, sigma, reference_spectra):
    #Fit D(E) = A * (sum(a_M * S_M(E)) - S_1(E))
    ground_state = reference_spectra[:, 0]

    def model(parameters):
        amplitude = parameters[0]
        excited_populations = parameters[1:]
        singlet_population = 1.0 - np.sum(excited_populations)
        populations = np.concatenate(([singlet_population], excited_populations))
        return amplitude * (reference_spectra @ populations - ground_state), populations

    def objective(parameters):
        fitted, _ = model(parameters)
        return np.sum(((difference - fitted) / sigma) ** 2)

    # für alle states
    #x0 = np.array([1.0, 0.1, 0.1, 0.1, 0.1])
    x0 = np.array([0.1, 1.0, 0.1, 0.1, 0.0])
    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=[(0.0, None), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)],
        constraints={"type": "ineq", "fun": lambda parameters: 1.0 - np.sum(parameters[1:])},
        options={"ftol": 1e-12, "maxiter": 2000},
    )

    amplitude = result.x[0]
    fitted, populations = model(result.x)
    return amplitude, populations, fitted, result

def fit_negative_delays_soft(differences, sigmas, reference_spectra, regularization_strength=10.0,):
    """Fit separate populations while softly keeping them near one baseline."""
    ground_state = reference_spectra[:, 0]
    number_of_delays = differences.shape[0]
    population_parameter_count = 4 * number_of_delays

    def unpack(parameters):
        excited_populations = parameters[:population_parameter_count].reshape(number_of_delays, 4)
        baseline = parameters[population_parameter_count:population_parameter_count + 4]
        amplitudes = parameters[population_parameter_count + 4:]
        populations = np.column_stack((1.0 - np.sum(excited_populations, axis=1), excited_populations))
        baseline_population = np.concatenate(([1.0 - np.sum(baseline)], baseline))
        return populations, baseline_population, amplitudes

    def residuals(parameters):
        populations, baseline_population, amplitudes = unpack(parameters)
        spectral_shapes = reference_spectra @ populations.T - ground_state[:, None]
        fitted = amplitudes[:, None] * spectral_shapes.T
        data_residuals = ((differences - fitted) / sigmas).ravel()
        population_residuals = np.sqrt(regularization_strength) * (populations[:, 1:] - baseline_population[1:]).ravel()
        return np.concatenate((data_residuals, population_residuals))

    initial_amplitudes = np.maximum(np.max(np.abs(differences), axis=1), 1.0)
    initial_populations = np.zeros((number_of_delays, 4))
    x0 = np.concatenate((initial_populations.ravel(), np.zeros(4), initial_amplitudes))
    bounds = ([(0.0, 1.0)] * population_parameter_count + [(0.0, 1.0)] * 4 + [(0.0, None)] * number_of_delays)

    def population_constraints(parameters):
        populations, baseline_population, _ = unpack(parameters)
        return np.concatenate((populations[:, 0], [baseline_population[0]]))

    result = minimize(
        lambda parameters: np.sum(residuals(parameters) ** 2),
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints={"type": "ineq", "fun": population_constraints},
        options={"ftol": 1e-12, "maxiter": 2000},
    )

    populations, baseline_population, amplitudes = unpack(result.x)
    spectral_shapes = reference_spectra @ populations.T - ground_state[:, None]
    fitted = amplitudes[:, None] * spectral_shapes.T

    jacobian = np.empty((residuals(result.x).size, result.x.size))
    for parameter_index, parameter in enumerate(result.x):
        step = np.sqrt(np.finfo(float).eps) * max(1.0, abs(parameter))
        shifted_plus = result.x.copy()
        shifted_minus = result.x.copy()
        shifted_plus[parameter_index] += step
        shifted_minus[parameter_index] -= step
        jacobian[:, parameter_index] = (residuals(shifted_plus) - residuals(shifted_minus)) / (2 * step)

    covariance = np.linalg.pinv(jacobian.T @ jacobian)
    population_uncertainties = np.empty((number_of_delays, 5))
    for delay_index in range(number_of_delays):
        covariance_block = covariance[4 * delay_index:4 * delay_index + 4,
                                      4 * delay_index:4 * delay_index + 4]
        population_transform = np.vstack((-np.ones(4), np.eye(4)))
        population_covariance = population_transform @ covariance_block @ population_transform.T
        population_uncertainties[delay_index] = np.sqrt(
            np.maximum(np.diag(population_covariance), 0.0)
        )

    return amplitudes, populations, fitted, population_uncertainties, result

def estimate_population_uncertainties(result, difference, sigma, reference_spectra):
    parameters = result.x
    ground_state = reference_spectra[:, 0]

    def weighted_residuals(parameters):
        amplitude = parameters[0]
        excited_populations = parameters[1:]
        singlet_population = 1.0 - np.sum(excited_populations)
        populations = np.concatenate(([singlet_population], excited_populations))
        fitted = amplitude * (reference_spectra @ populations - ground_state)
        return (difference - fitted) / sigma

    # Numerical Jacobian of the weighted residuals at the optimum
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
    population_transform = np.zeros((5, 5))
    population_transform[0, 1:] = -1.0
    population_transform[1:, 1:] = np.eye(4)
    population_covariance = population_transform @ covariance @ population_transform.T
    return np.sqrt(np.maximum(np.diag(population_covariance), 0.0))

def poisson_counts_for_negative_delays(t_fs, population_uncertainties, state_names, maximum_delay_fs=50,):
    """Calculate N = (Delta N)^2 up to a selected delay."""
    negative_delays = t_fs <= maximum_delay_fs
    poisson_counts = population_uncertainties[negative_delays] ** 2
    return t_fs[negative_delays], poisson_counts

#---lets try it out---yippieyippieyippie
ref_file = Path("Daten/Analysis and Interpretation/Ref Spectrum/Reference_Data_Fig_4_4.csv")
data_folder = Path("Daten/Experiment with Data Acquisition/messreihe")

delays = [-150, -100, -50, 0, 50, 100, 150, 200, 250, 300, 350, 400, 600, 800]
delay_names = ["min150 fs", "min100 fs", "min50 fs", "0 fs", "50 fs", "100 fs", "150 fs", "200 fs", "250 fs", "300 fs", "350 fs", "400 fs", "600 fs", "800 fs"]

# deltaI matrix aus measurements
t_fs, energy_common, dI_mean, sigma = build_deltaI_matrix_from_folders(data_folder=data_folder, delays=delays, delay_names=delay_names, load_spectrum=load_spectrum)
# load and interpolate all five reference spectra
energy_ref, reference_ref = load_reference_spectra(ref_file)
reference_spectra = np.column_stack([interp1d(energy_ref, reference_ref[:, state], bounds_error=False, fill_value=np.nan)(energy_common)
    for state in range(reference_ref.shape[1])])
valid = (np.isfinite(dI_mean).all(axis=0) & np.isfinite(sigma).all(axis=0) 
         & np.isfinite(reference_spectra).all(axis=1) & (sigma > 0).all(axis=0))

energy_fit = energy_common[valid]
dI_fit = dI_mean[:, valid]
sigma_fit = sigma[:, valid]
reference_fit = reference_spectra[valid]

amplitudes = []
populations = []
population_uncertainties = []
fitted_spectra = []

fit_until_50_fs = t_fs <= 50
(negative_amplitudes, negative_populations, negative_fitted_spectra, negative_uncertainties, negative_result,
 ) = fit_negative_delays_soft(dI_fit[fit_until_50_fs], sigma_fit[fit_until_50_fs], reference_fit, regularization_strength=10.0)
negative_index = 0

for delay, difference, uncertainty in zip(t_fs, dI_fit, sigma_fit):
    if delay <= 50:
        amplitude = negative_amplitudes[negative_index]
        population = negative_populations[negative_index]
        fitted = negative_fitted_spectra[negative_index]
        population_uncertainty = negative_uncertainties[negative_index]
        negative_index += 1
    else:
        amplitude, population, fitted, result = fit_difference_spectrum(energy_fit, difference, uncertainty, reference_fit)
        population_uncertainty = estimate_population_uncertainties(result, difference, uncertainty, reference_fit)
    amplitudes.append(amplitude)
    populations.append(population)
    population_uncertainties.append(population_uncertainty)
    fitted_spectra.append(fitted)
    # print(f"{delay:>5.0f} fs: A = {amplitude:.5g}, populations = {population}")

amplitudes = np.array(amplitudes)
populations = np.array(populations)
population_uncertainties = np.array(population_uncertainties)
fitted_spectra = np.array(fitted_spectra)

state_names = ["singlet", "doublet", "triplet", "quartet", "quintet"]
state_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"][:len(state_names)]
negative_delays, poisson_counts = poisson_counts_for_negative_delays(t_fs, population_uncertainties, state_names, maximum_delay_fs=50)

# MAIN PLOT
plt.figure(figsize=(7, 4.5))
for index, state_name in enumerate(state_names):
    plt.errorbar(
        t_fs,
        populations[:, index],
        yerr=population_uncertainties[:, index],
        fmt="o-",
        capsize=3,
        color=state_colors[index],
        ecolor=(*to_rgba(state_colors[index])[:3], 0.5),
        label=state_name,
    )
plt.xlabel("Time delay [fs]")
plt.ylabel("Population $a_M$")
#plt.ylim(-0.02, 1.02)
plt.legend()
plt.tight_layout()
plt.savefig("Auswertung EXP21/fit/fit fixed neg delays/fit_try_to_fix_lol.png")
plt.show()

'''# PLOT COUNTS AT NEGATIVE DELAYS (über Fehlerbalken/Poisson Statistik)
number_of_negative_delays = len(negative_delays)
number_of_columns = 2
number_of_rows = int(np.ceil(number_of_negative_delays / number_of_columns))
fig, axes = plt.subplots(
    number_of_rows,
    number_of_columns,
    figsize=(12, 3.5 * number_of_rows),
    sharey=True,
    squeeze=False,
)
axes = axes.ravel()

negative_indices = np.flatnonzero(t_fs <= 50)
for panel_index, (delay, counts, fit_index) in enumerate(zip(negative_delays, poisson_counts, negative_indices)):
    bars = axes[panel_index].bar(state_names, counts, color=state_colors)
    axes[panel_index].set_title(
        f"{delay:.0f} fs, A = {amplitudes[fit_index]:.5g}"
    )
    axes[panel_index].set_ylabel(r"$N = (\Delta N)^2$")
    axes[panel_index].tick_params(axis="x", rotation=35)
    axes[panel_index].grid(axis="y", alpha=0.25)
    axes[panel_index].bar_label(bars, fmt="%.4g", padding=3)
    axes[panel_index].set_ylim(0.0,0.9)

for axis in axes[number_of_negative_delays:]:
    axis.set_visible(False)

fig.tight_layout()
fig.savefig("Auswertung EXP21/fit/fit fixed neg delays/counts_negative_delays_per_delay_try_to_fix.png", dpi=200)
plt.show()'''

# Poisson-Statistik
# Beim Zählen von Photonen mit einem Detektor misst man
# eine Intensität über die Anzahl der gezählten Ereignisse N
# Für diese Verteilung gilt eine fundamentale Eigenschaft:
# Varianz = Mittelwert (σ² = N)
# Da der Fehlerbalken Δ N der Standardabweichung σ entspricht, gilt: 
# Delta N = \sqrt{N}
# Quadriert man den Fehlerbalken, erhält man die gemessene Anzahl (Intensität): 
# (Delta N)^2 = N

