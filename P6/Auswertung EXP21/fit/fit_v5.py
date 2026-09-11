import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 13,
    "axes.labelsize": 13,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "legend.fontsize": 13,
    "legend.title_fontsize": 13,
})

from pathlib import Path
from scipy.interpolate import interp1d
from scipy.optimize import minimize
from scipy.signal import fftconvolve

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
    x0 = np.array([0.1, 1.0, 0.1, 0.1, 0.0])
    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=[(0.0, None), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)],
        constraints={"type": "ineq", "fun": lambda parameters: 1.0 - np.sum(parameters[1:])},
        options={"ftol": 1e-12, "maxiter": 2000},
    )

    '''# für alle außer quartet
    x0 = np.array([0.3, 1.0, 0.1, 0.0])
    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=[(0.0, None),(0.0, 1.0),(0.0, 1.0),(0.0, 1.0),],
        constraints={"type": "ineq","fun": lambda parameters: 1.0 - np.sum(parameters[1:])},
        options={"ftol": 1e-12, "maxiter": 2000},
    )'''

    amplitude = result.x[0]
    fitted, populations = model(result.x)
    return amplitude, populations, fitted, result


#---lets try it out---yippieyippieyippie
ref_file = Path("Daten/Analysis and Interpretation/Ref Spectrum/Reference_Data_Fig_4_4.csv")
data_folder = Path("Daten/Experiment with Data Acquisition/messreihe")

delays = [-150, -100, -50, 0, 50, 100, 150, 200, 300, 400, 600, 800]
delay_names = ["min150 fs", "min100 fs", "min50 fs", "0 fs", "50 fs", "100 fs", "150 fs", "200 fs", "300 fs", "400 fs", "600 fs", "800 fs"]

# deltaI matrix aus measurements
t_fs, energy_common, dI_mean, sigma = build_deltaI_matrix_from_folders(data_folder=data_folder, delays=delays, delay_names=delay_names, load_spectrum=load_spectrum)
# load and interpolate all five reference spectra
energy_ref, reference_ref = load_reference_spectra(ref_file)
reference_spectra = np.column_stack([
    interp1d(energy_ref, reference_ref[:, state], bounds_error=False, fill_value=np.nan)(energy_common)
    for state in range(reference_ref.shape[1])
])
'''reference_spectra = np.column_stack([
    interp1d(energy_ref, reference_ref[:, state], bounds_error=False, fill_value=np.nan)(energy_common)
    for state in [0, 1, 2, 4]
])'''

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
fitted_spectra = []
for delay, difference, uncertainty in zip(t_fs, dI_fit, sigma_fit):
    amplitude, population, fitted, result = fit_difference_spectrum(
        energy_fit, difference, uncertainty, reference_fit
    )
    amplitudes.append(amplitude)
    populations.append(population)
    fitted_spectra.append(fitted)
    print(f"{delay:>5.0f} fs: A = {amplitude:.5g}, populations = {population}")

amplitudes = np.array(amplitudes)
populations = np.array(populations)
fitted_spectra = np.array(fitted_spectra)

plt.figure(figsize=(7, 4.5))
state_names = ["singlet", "doublet", "triplet", "quartet", "quintet"]
#state_names = ["singlet", "doublet", "triplet", "quintet"]
for index, state_name in enumerate(state_names):
    plt.plot(t_fs, populations[:, index], "o-", label=state_name)
plt.xlabel("Time delay [fs]")
plt.ylabel("Population $a_M$")
plt.ylim(-0.02, 1.02)
plt.legend()
plt.tight_layout()
plt.savefig("Auswertung EXP21/fit/fit_with_quarlets.png")
plt.show()