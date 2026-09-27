import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.optimize import minimize
from scipy.interpolate import PchipInterpolator


# PATHS
ref_file = Path("Daten/Analysis and Interpretation/Ref Spectrum/Reference_Data_Fig_4_4.csv")
data_folder = Path("Daten/Experiment with Data Acquisition/messreihe")

delays = [-150, -100, -50, 0, 50, 100, 150, 200, 300, 400, 600, 800]
delay_names = ["min150 fs", "min100 fs", "min50 fs", "0 fs", "50 fs", "100 fs", "150 fs", "200 fs", "300 fs", "400 fs", "600 fs", "800 fs"]

# LOAD REFERENCE DATA
ref = pd.read_csv(ref_file)

energy_ref = ref["emission energy"].values
states = ["singlet", "doublet", "triplet", "quartet", "quintet"]
plot_states = ["singlet", "doublet", "triplet", "quartet", "quintet"]
plot_indices = [states.index(s) for s in plot_states]
FIT_STATES = ["singlet", "doublet", "triplet", "quartet", "quintet"]
FIT_MODELS = {"all states":         [ "singlet", "doublet", "triplet", "quartet", "quintet"],
              "without quartet":    [ "singlet", "doublet", "triplet", "quintet"],
              "triplet + quintet":  ["singlet", "triplet", "quintet"]}

ref_spectra = np.array([ref[state].values for state in states]).T
# shape:
# (number of energy points, 5)

# FUNCTION TO LOAD MEASUREMENT
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

# INTERPOLATE REFERENCE SPECTRA ONTO MEASUREMENT ENERGY GRID
def interpolate_reference(energy):
    ref_interp = np.zeros((len(energy), len(states)))
    for i, state in enumerate(states):
        f = interp1d(
            energy_ref,
            ref_spectra[:, i],
            bounds_error=False,
            fill_value=0
        )
        ref_interp[:, i] = f(energy)
    return ref_interp

# ============================================================
# FIT FUNCTIONS
# ============================================================

def prepare_fit_matrix(energy, fit_states):
    """
    Creates the difference-spectrum matrix relative to singlet.
    Model:ΔI = Σ p_i * (R_i - R_singlet)
    Singlet is treated as the ground state and is therefore
    not an independent fit parameter.
    """

    A = interpolate_reference(energy)

    singlet_index = states.index("singlet")

    fit_indices = [
        states.index(state)
        for state in fit_states
        if state != "singlet"
    ]

    B = A[:, fit_indices] - A[:, singlet_index, None]

    return A, B, fit_indices


def fit_spectrum(energy, delta_intensity, sigma, fit_states):
    """
    Fit a spectrum using the selected electronic states.

    Parameters
    ----------
    energy : array
        Measurement energy grid.

    delta_intensity : array
        Measured difference spectrum.

    sigma : array
        Uncertainty used for weighted fitting.

    fit_states : list
        States included in the fit, e.g.
        ["singlet", "triplet", "quintet"]

    Returns
    -------
    populations : array
        Populations in the order of `states`.

    fitted : array
        Total fitted difference spectrum.

    result : scipy optimization result

    A : array
        Reference spectra interpolated onto measurement grid.
    """

    # --------------------------------------------------------
    # Prepare fit matrix
    # --------------------------------------------------------

    A, B, fit_indices = prepare_fit_matrix(
        energy,
        fit_states
    )

    n_parameters = len(fit_indices)

    # --------------------------------------------------------
    # Objective function
    # --------------------------------------------------------

    def objective(p):

        fitted = B @ p

        residuals = (
            fitted - delta_intensity
        ) / sigma

        return np.sum(residuals**2)

    # --------------------------------------------------------
    # Initial guess
    # --------------------------------------------------------

    x0 = np.ones(n_parameters) * 0.1

    # --------------------------------------------------------
    # Bounds
    # --------------------------------------------------------

    bounds = [
        (0, 1)
        for _ in range(n_parameters)
    ]

    # --------------------------------------------------------
    # Total population <= 1
    # --------------------------------------------------------

    constraints = {
        "type": "ineq",
        "fun": lambda p: 1 - np.sum(p)
    }

    # --------------------------------------------------------
    # Fit
    # --------------------------------------------------------

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={
            "ftol": 1e-12,
            "maxiter": 2000
        }
    )

    p_fit = result.x

    # --------------------------------------------------------
    # Construct complete population array
    # --------------------------------------------------------

    populations = np.zeros(len(states))

    for parameter, index in zip(
        p_fit,
        fit_indices
    ):
        populations[index] = parameter

    # Singlet = remaining population
    singlet_index = states.index("singlet")

    populations[singlet_index] = (
        1 - np.sum(p_fit)
    )

    # --------------------------------------------------------
    # Final fit
    # --------------------------------------------------------

    fitted = B @ p_fit

    return populations, fitted, result, A

def compare_fits(
    energy,
    intensity,
    sigma,
    fit_models
):

    results = {}

    for name, fit_states in fit_models.items():

        populations, fitted, result, A = fit_spectrum(
            energy,
            intensity,
            sigma,
            fit_states
        )

        chi2 = result.fun

        n_data = len(intensity)
        n_parameters = len(fit_states) - 1

        degrees_of_freedom = (
            n_data - n_parameters
        )

        reduced_chi2 = (
            chi2 / degrees_of_freedom
        )

        results[name] = {
            "states": fit_states,
            "populations": populations,
            "fitted": fitted,
            "result": result,
            "A": A,
            "chi2": chi2,
            "reduced_chi2": reduced_chi2
        }

    return results

# 4. LOOP OVER ALL DELAYS
all_populations = []
all_errors = []
all_mean_spectra = []
all_std_spectra = []
all_fit_spectra = []
all_fit_matrices = []
all_fit_coefficients = []

for delay, delay_name in zip(delays, delay_names):

    folder = data_folder / delay_name
    files = sorted(folder.glob("*"))
    populations = []

    print(f"\nDelay: {delay} fs")

    # 1. Alle 10 Spektren laden
    energies = []
    intensities = []

    for file in files:
        energy, intensity = load_spectrum(file)
        energies.append(energy)
        intensities.append(intensity)

    # Make sure all spectra use the same energy grid
    energy = energies[0]
    spectra = []

    for e, intensity in zip(energies, intensities):
        f = interp1d(e, intensity, bounds_error=False, fill_value=np.nan)
        spectra.append(f(energy))

    spectra = np.array(spectra)

    # 2. Mean spectrum
    mean_intensity = np.mean(spectra, axis=0)

    # 3. Standard deviation
    std_intensity = np.std(spectra, axis=0, ddof=1)


    n_shots = len(spectra)
    sem_intensity = (
        std_intensity /
        np.sqrt(n_shots)
    )

    # Avoid sigma = 0
    # Otherwise the weighted fit would divide by zero.

    sigma = sem_intensity.copy()
    positive_sigma = sigma[sigma > 0]

    if len(positive_sigma) > 0:
        minimum_sigma = np.min(positive_sigma)
    else:
        minimum_sigma = 1.0

    sigma[sigma <= 0] = minimum_sigma

    # 4. Fit mean spectrum
    populations, fitted, result, A = fit_spectrum(energy, mean_intensity, sigma, FIT_STATES)

    fit_results = compare_fits(energy, mean_intensity, sigma, FIT_MODELS)
    for name, result in fit_results.items():
        print(f"{name:20s} "f"χ²_red = {result['reduced_chi2']:.3f}")
        
    all_model_populations = {
        model_name: []
        for model_name in FIT_MODELS
    }

    # Store
    all_mean_spectra.append(mean_intensity)
    all_std_spectra.append(std_intensity)
    all_fit_spectra.append(fitted)
    all_populations.append(populations)
    all_fit_matrices.append(A)

# convert to arrays
all_populations = np.array(all_populations)
all_mean_spectra = np.array(all_mean_spectra)
all_std_spectra = np.array(all_std_spectra)
all_fit_spectra = np.array(all_fit_spectra)

# PLOT POPULATIONS VS DELAY
plt.figure(figsize=(9, 6))

#delay_fine = np.linspace(min(delays), max(delays), 500)

for i, state in enumerate(plot_states):
    state = states[i]
    population = all_populations[:, i]

    # interpolation (cubic vs pchip)
    #f = interp1d(delays,population,kind="cubic")
    #f = PchipInterpolator(delays,population)
    #population_fine = f(delay_fine)

    plt.plot(delays,population, "o-", linewidth=2, markersize=6, label=state)
    #plt.errorbar(delays,all_populations[:, i],marker="o",capsize=3,label=state)

plt.xlabel("Delay (fs)")
plt.ylabel("Population")
plt.ylim(-0.02, 1.02)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# PLOT ONE DELAY: MEAN + STD + FIT + INDIVIDUAL CONTRIBUTIONS
plot_delay = 4
# Index: 0 -> -150 fs, 1 -> -100 fs, 2 -> -50 fs, 3 -> 0 fs, 4 -> 50 fs, ...

energy_plot = energy
mean_plot = all_mean_spectra[plot_delay]
std_plot = all_std_spectra[plot_delay]
fit_plot = all_fit_spectra[plot_delay]
A = all_fit_matrices[plot_delay]
populations_plot = all_populations[plot_delay]

#plt.errorbar(energy_plot, mean_plot, yerr=std_plot, fmt="o", markersize=3, capsize=2, label="Mean ± STD", alpha=0.7)
for i, state in enumerate(states[1:], start=1):
    contribution = (populations_plot[i] * (A[:, i] - A[:, 0]))
    plt.plot(energy_plot, contribution, linewidth=2, label=f"{state} contribution")
plt.stackplot(energy_plot, contribution,labels=plot_states,alpha=0.35)
plt.plot(energy_plot, fit_plot, linewidth=2.5, label="Total fit")

#plt.axhline(background, linestyle=":", linewidth=1.5, label="Background" )

plt.xlabel("Energy (eV)")
plt.ylabel("Intensity")
plt.xlim(7000, 7110)

plt.title(f"Spectral decomposition at {delays[plot_delay]} fs")
plt.legend()
plt.tight_layout()
plt.show()