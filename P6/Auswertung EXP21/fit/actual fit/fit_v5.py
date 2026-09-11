import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.optimize import minimize
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

def poisson_counts_for_negative_delays(t_fs, population_uncertainties, state_names):
    """Calculate N = (Delta N)^2 from population error bars at t < 0."""
    negative_delays = t_fs <= 0
    poisson_counts = population_uncertainties[negative_delays] ** 2

    for delay, counts in zip(t_fs[negative_delays], poisson_counts):
        print(f"{delay:>5.0f} fs: gemessene Anzahl/Intensität")
        for state_name, count in zip(state_names, counts):
            print(f"  {state_name:>8}: N = {count:.6g}")

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
reference_spectra = np.column_stack([
    interp1d(energy_ref, reference_ref[:, state], bounds_error=False, fill_value=np.nan)(energy_common)
    for state in range(reference_ref.shape[1])
])

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

amplitudes = []
populations = []
population_uncertainties = []
fitted_spectra = []
for delay, difference, uncertainty in zip(t_fs, dI_fit, sigma_fit):
    amplitude, population, fitted, result = fit_difference_spectrum(energy_fit, difference, uncertainty, reference_fit)
    amplitudes.append(amplitude)
    populations.append(population)
    population_uncertainties.append(estimate_population_uncertainties(result, difference, uncertainty, reference_fit))
    fitted_spectra.append(fitted)
    print(f"{delay:>5.0f} fs: A = {amplitude:.5g}, populations = {population}")

amplitudes = np.array(amplitudes)
populations = np.array(populations)
population_uncertainties = np.array(population_uncertainties)
fitted_spectra = np.array(fitted_spectra)

normalized_residuals = (dI_fit - fitted_spectra) / sigma_fit

state_names = ["singlet", "doublet", "triplet", "quartet", "quintet"]
negative_delays, poisson_counts = poisson_counts_for_negative_delays(t_fs,population_uncertainties,state_names)

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
plt.ylabel("Population $a_M$")
plt.ylim(-0.02, 1.02)
plt.legend()
plt.tight_layout()
plt.savefig("Auswertung EXP21/fit/actual fit/fit_all.png")
plt.show()

plt.figure(figsize=(7, 4.5))
for index, state_name in enumerate(state_names):
    plt.plot(
        negative_delays,
        poisson_counts[:, index],
        "o-",
        label=state_name,
    )
plt.xlabel("Time delay [fs]")
plt.ylabel(r"Measured intensity $N = (\Delta N)^2$")
plt.legend()
plt.tight_layout()
plt.savefig("Auswertung EXP21/fit/actual fit/poisson_counts_negative_delays.png")
plt.show()

# RESIDUEN UND SPEKTREN FÜR -150 BIS 50 fs
selected_indices = np.flatnonzero(t_fs <= 50)
selected_delays = t_fs[selected_indices]

number_of_delays = len(selected_delays)
number_of_columns = 2
number_of_rows = int(np.ceil(number_of_delays / number_of_columns))

fig, axes = plt.subplots(number_of_rows, number_of_columns, figsize=(14, 3.8 * number_of_rows), sharex=True, squeeze=False)
axes = axes.ravel()

for panel_index, fit_index in enumerate(selected_indices):
    delay = t_fs[fit_index]
    residual_axis = axes[panel_index]

    # Normierte Residuen auf der linken y-Achse
    residual_axis.plot(
        energy_fit,
        normalized_residuals[fit_index],
        color="black",
        linewidth=0.8,
        label="Normierte Residuen")
    residual_axis.axhline(
        0,
        color="tab:red",
        linestyle="--",
        linewidth=1)
    residual_axis.axhline(
        1,
        color="gray",
        linestyle=":",
        linewidth=0.8)
    residual_axis.axhline(
        -1,
        color="gray",
        linestyle=":",
        linewidth=0.8)

    residual_axis.set_title(f"{delay:.0f} fs")
    residual_axis.set_ylabel(r"$(I_\mathrm{mess}-I_\mathrm{fit})/\sigma$")
    residual_axis.grid(alpha=0.25)

    # Spektren auf der rechten y-Achse
    spectrum_axis = residual_axis.twinx()
    measured_line, = spectrum_axis.plot(energy_fit, dI_fit[fit_index], color="tab:blue", linewidth=1, label="Messung")
    fitted_line, = spectrum_axis.plot(energy_fit, fitted_spectra[fit_index], color="tab:orange", linewidth=1.2, label="Fit")
    spectrum_axis.set_ylabel(r"$\Delta \, I [a.u.]$")

    # Gemeinsame Legende aus beiden Achsen
    residual_lines, residual_labels = residual_axis.get_legend_handles_labels()
    spectrum_lines, spectrum_labels = spectrum_axis.get_legend_handles_labels()
    residual_axis.legend(residual_lines + spectrum_lines, residual_labels + spectrum_labels, loc="upper right", fontsize=10)
for axis in axes[number_of_delays:]:
    axis.set_visible(False)

for axis in axes[-number_of_columns:]:
    axis.set_xlabel("Energy [eV]")

fig.tight_layout()
fig.savefig("Auswertung EXP21/fit/actual fit/residuals_and_spectra_minus150_to_50fs.png",dpi=200)
plt.show()

# COUNTS AT NEG DELAYS (ÜBER FEHLERBALKEN)
state_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"][:len(state_names)]
number_of_negative_delays = len(negative_delays)
number_of_columns = 2
number_of_rows = int(np.ceil(number_of_negative_delays / number_of_columns))
fig, axes = plt.subplots(number_of_rows, number_of_columns, figsize=(12, 3.5 * number_of_rows), sharey=True, squeeze=False)
axes = axes.ravel()

negative_indices = np.flatnonzero(t_fs <= 0)
for panel_index, (delay, counts, fit_index) in enumerate(zip(negative_delays, poisson_counts, negative_indices)):
    bars = axes[panel_index].bar(state_names, counts, color=state_colors)
    axes[panel_index].set_title(f"{delay:.0f} fs, A = {amplitudes[fit_index]:.5g}")
    axes[panel_index].set_ylabel(r"$N = (\Delta N)^2$")
    axes[panel_index].tick_params(axis="x", rotation=35)
    axes[panel_index].grid(axis="y", alpha=0.25)
    axes[panel_index].bar_label(bars, fmt="%.4g", padding=3)
    axes[panel_index].set_ylim(0.0,40)

for axis in axes[number_of_negative_delays:]:
    axis.set_visible(False)

fig.tight_layout()
fig.savefig("Auswertung EXP21/fit/actual fit/counts_negative_delays_per_delay.png", dpi=200)
plt.show()


# Poisson-Statistik
# Beim Zählen von Photonen mit einem Detektor misst man
# eine Intensität über die Anzahl der gezählten Ereignisse N
# Für diese Verteilung gilt eine fundamentale Eigenschaft:
# Varianz = Mittelwert (σ² = N)
# Da der Fehlerbalken Δ N der Standardabweichung σ entspricht, gilt: 
# Delta N = \sqrt{N}
# Quadriert man den Fehlerbalken, erhält man die gemessene Anzahl (Intensität): 
# (Delta N)^2 = N

