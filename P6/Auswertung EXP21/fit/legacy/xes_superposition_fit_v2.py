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
plot_states = ["doublet", "triplet", "quintet"]
plot_indices = [states.index(s) for s in plot_states]

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

# FIT
def fit_spectrum(energy, delta_intensity, sigma):
    # Reference spectra on measurement grid
    A = interpolate_reference(energy)

    # FIT Model: ΔI = Σ p_i A_i - A_singlet
    # with:
    # p_i >= 0
    # Σ p_i = 1

    A_ground = A[:, 0]
    # We fit 6 parameters:
    # pS, pD, pT, pQ, p5, background?

    def objective(params):
        populations = params[:5]
        background = params[5]
        fitted = A @ populations - A_ground + background
        residuals = (fitted - delta_intensity) / sigma
        return np.sum(residuals**2)

    # Initial guess
    x0 = np.array([
        0.0,    # singlet
        0.0,    # doublet
        0.1,    # triplet
        0.0,    # quartet
        0.9,    # quintet
        0.0     # background
    ])

    # Population constraints
    bounds = [
        (0, 1),       # singlet
        (0, 1),       # doublet
        (0, 1),       # triplet
        (0, 1),       # quartet
        (0, 1),       # quintet
        (-np.inf, np.inf)  # background
    ]

    constraints = {"type": "eq","fun": lambda params: np.sum(params[:5]) - 1}
    result = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=constraints)
    coefficients = result.x
    populations = coefficients[:5]
    background = coefficients[5]

    fitted = A @ populations - A_ground + background

    return populations, background, fitted, result, A

def fit_spectrum_without_background(energy, delta_intensity, sigma):

    # Reference spectra on measurement grid
    A = interpolate_reference(energy)

    # Ground-state reference
    A_ground = A[:, 0]

    # Model: ΔI = A @ populations - A_ground
    # p_i >= 0, sum(p_i) = 1, NO BACKGROUND

    def objective(populations):
        fitted = A @ populations - A_ground
        residuals = (fitted - delta_intensity) / sigma
        return np.sum(residuals**2)

    # Initial guess
    x0 = np.array([
        0.0,    # singlet
        0.0,    # doublet
        0.1,    # triplet
        0.0,    # quartet
        0.9     # quintet
    ])

    # populations >= 0
    bounds = [
        (0, 1),    # singlet
        (0, 1),    # doublet
        (0, 1),    # triplet
        (0, 1),    # quartet
        (0, 1)     # quintet
    ]

    # sum(populations) = 1
    constraints = {
        "type": "eq",
        "fun": lambda p: np.sum(p) - 1
    }

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    populations = result.x

    # Final fit
    fitted = A @ populations - A_ground

    return populations, fitted, result, A

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
    #populations, background, fitted, result, A = fit_spectrum(energy, mean_intensity, sigma)
    populations, fitted, result, A = fit_spectrum_without_background(energy, mean_intensity, sigma)

    # Store
    all_mean_spectra.append(mean_intensity)
    all_std_spectra.append(std_intensity)
    all_fit_spectra.append(fitted)
    all_populations.append(populations)
    all_fit_matrices.append(A)
    #all_fit_coefficients.append(np.concatenate([populations, [background]]))

# convert to arrays
all_populations = np.array(all_populations)
all_mean_spectra = np.array(all_mean_spectra)
all_std_spectra = np.array(all_std_spectra)
all_fit_spectra = np.array(all_fit_spectra)

# PLOT POPULATIONS VS DELAY
plt.figure(figsize=(9, 6))

delay_fine = np.linspace(min(delays), max(delays), 500)

for i in plot_indices:
    state = states[i]
    population = all_populations[:, i]

    # interpolation (cubic vs pchip)
    f = interp1d(delays,population,kind="cubic")
    #f = PchipInterpolator(delays,population)
    population_fine = f(delay_fine)

    plt.plot(delay_fine,population_fine,linewidth=2,label=state)
    plt.plot(delays,population,"o")
    #plt.errorbar(delays,all_populations[:, i],marker="o",capsize=3,label=state)

plt.xlabel("Delay (fs)")
plt.ylabel("Population")
plt.legend()
plt.grid(alpha=0.3)


# PLOT ONE DELAY: MEAN + STD + FIT + INDIVIDUAL CONTRIBUTIONS
plot_delay = 3
# Index: 0 -> -150 fs, 1 -> -100 fs, 2 -> -50 fs, 3 -> 0 fs, 4 -> 50 fs, ...

energy_plot = energy
mean_plot = all_mean_spectra[plot_delay]
std_plot = all_std_spectra[plot_delay]
fit_plot = all_fit_spectra[plot_delay]
A = all_fit_matrices[plot_delay]
#coefficients = all_fit_coefficients[plot_delay]
populations_plot = all_populations[plot_delay]

contributions = []
for i in plot_indices:
    state = states[i]
    contribution = (A[:, i] * populations_plot[i])
    # Ground-state bleach
    if i == 0:
        contribution -= A[:, 0]
    contributions.append(contribution)
contributions = np.array(contributions)

plt.figure(figsize=(10, 6))
plt.stackplot(energy_plot, contributions,labels=plot_states,alpha=0.35)
#plt.errorbar(energy_plot, mean_plot, yerr=std_plot, fmt="o", markersize=3, capsize=2, label="Mean ± STD", alpha=0.7)
# Jede Contribution einzeln plotten
for contribution, state in zip(contributions, plot_states):
    plt.plot(energy_plot, contribution, linestyle="--", linewidth=1.5, label=f"{state} contribution")
plt.plot(energy_plot, fit_plot, linewidth=2.5, label="Total fit")

#background = coefficients[5]
#plt.axhline(background, linestyle=":", linewidth=1.5, label="Background" )

plt.xlabel("Energy (eV)")
plt.ylabel("Intensity")
plt.xlim(7000, 7110)

plt.title(f"Spectral fit/decomposition at {delays[plot_delay]} fs")
plt.legend()

plt.tight_layout()
plt.show()