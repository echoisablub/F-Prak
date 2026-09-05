import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.optimize import least_squares

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


#for finding kinetic populations
def kinetics_direct(t, k):
    #P1 = e^{-k t}, P5 = 1 - e^{-k t} <-- gewünschte form der populations funktionen
    #hier der direkte zerfall von 1MLCT -> 5T2 mit rate k
    P1 = np.exp(-k * t)
    P5 = 1.0 - P1
    return P1, P5

def kinetics_cascade(t, k1, k2):
    # 1MLCT -> 3T1 (k1), 3T1 -> 5T2 (k2)
    #hier der indirekte zerfall von 1MLCT -> 3T1 -> 5T2 mit rates k1, k2
    eps = 1e-12
    if np.abs(k2 - k1) < eps:
        k2 = k1 + eps

    P1 = np.exp(-k1 * t)
    PT = (k1 / (k2 - k1)) * (np.exp(-k1 * t) - np.exp(-k2 * t))
    P5 = 1.0 + (k1 * np.exp(-k2 * t) - k2 * np.exp(-k1 * t)) / (k2 - k1)
    return P1, PT, P5

#residuen definieren für least squares fitting
def residual_direct(params, t_ps, dI, sigma):
    k, dt0 = params
    k = np.abs(k)
    t = t_ps - dt0

    P1, P5 = kinetics_direct(t, k)

    # Build design matrix X(t) = [P1, P5, 1]  -> Nt x 3
    X = np.column_stack([P1, P5, np.ones_like(t)])  # (Nt,3)

    Nt, NE = dI.shape
    res_list = []

    # Weighted residuals:
    # For each energy E_m, solve linear least squares for amplitudes: dI[:,m] ≈ X @ a(E_m)  with weights 1/sigma[:,m]
    #weighted least squares by scaling rows:
    for m in range(NE):
        y = dI[:, m]
        w = 1.0 / sigma[:, m] #weights per time
        Xw = X * w[:, None] #scale rows
        yw = y * w

        # linear solve
        a, *_ = np.linalg.lstsq(Xw, yw, rcond=None)  # a=[A1,A5,C]
        yfit = X @ a

        r = (y - yfit) / sigma[:, m]
        res_list.append(r)

    # stack into (Nt*NE,)
    return np.concatenate(res_list)


def residual_cascade(params, t_ps, dI, sigma):
    #this assumes the cascade transition with 3T1 as intermediate between 1MLCT and 5T2, with rates k1, k2 and time offset dt0
    k1, k2, dt0 = params
    k1 = np.abs(k1)
    k2 = np.abs(k2)

    t = t_ps - dt0

    P1, PT, P5 = kinetics_cascade(t, k1, k2)

    X = np.column_stack([P1, PT, P5, np.ones_like(t)])  # Nt x 4

    Nt, NE = dI.shape
    res_list = []

    for m in range(NE):
        y = dI[:, m]
        w = 1.0 / sigma[:, m]
        Xw = X * w[:, None]
        yw = y * w

        a, *_ = np.linalg.lstsq(Xw, yw, rcond=None)  # [A1, AT, A5, C]
        yfit = X @ a
        r = (y - yfit) / sigma[:, m]
        res_list.append(r)

    return np.concatenate(res_list)


# Fit wrappers, again with the two versions
def fit_direct_target_analysis(t_fs, energy, dI_mean, sigma, dt0_guess_fs=0.0, dt0_bounds_fs=20.0):
    t_ps = t_fs / 1000.0
    dt0_guess = dt0_guess_fs / 1000.0
    dt0_max = dt0_bounds_fs / 1000.0

    # initial guess: k ~ 1/ps
    x0 = np.array([1.0, dt0_guess])
    bounds = ([0.0, -dt0_max], [np.inf, dt0_max])

    res = least_squares(
        residual_direct, x0,
        args=(t_ps, dI_mean, sigma),
        bounds=bounds,
        verbose=2,
        max_nfev=400
    )
    k_fit, dt0_fit = res.x
    return {"k": k_fit, "dt0": dt0_fit, "result": res}


def fit_cascade_target_analysis(t_fs, energy, dI_mean, sigma, dt0_guess_fs=0.0, dt0_bounds_fs=20.0):
    t_ps = t_fs / 1000.0
    dt0_guess = dt0_guess_fs / 1000.0
    dt0_max = dt0_bounds_fs / 1000.0

    x0 = np.array([1.0, 0.2, dt0_guess])  # [k1,k2,dt0] in ps^-1, ps
    bounds = ([0.0, 0.0, -dt0_max], [np.inf, np.inf, dt0_max])

    res = least_squares(
        residual_cascade, x0,
        args=(t_ps, dI_mean, sigma),
        bounds=bounds,
        verbose=2,
        max_nfev=600
    )
    k1_fit, k2_fit, dt0_fit = res.x
    return {"k1": k1_fit, "k2": k2_fit, "dt0": dt0_fit, "result": res}


#---lets try it out---yippieyippieyippie
ref_file = Path("Daten/Analysis and Interpretation/Ref Spectrum/Reference_Data_Fig_4_4.csv")
data_folder = Path("Daten/Experiment with Data Acquisition/messreihe")

delays = [-150, -100, -50, 0, 50, 100, 150, 200, 300, 400, 600, 800]
delay_names = ["min150 fs", "min100 fs", "min50 fs", "0 fs", "50 fs", "100 fs", "150 fs", "200 fs", "300 fs", "400 fs", "600 fs", "800 fs"]


t_fs, energy_common, dI_mean, sigma = build_deltaI_matrix_from_folders(
    data_folder=data_folder,
    delays=delays,
    delay_names=delay_names,
    load_spectrum=load_spectrum
)

# Fit (a) direct
fit_a = fit_direct_target_analysis(
    t_fs, energy_common, dI_mean, sigma,
    dt0_guess_fs=0.0,
    dt0_bounds_fs=20.0
)
print("Direct fit:", fit_a["k"], "ps^-1 ; dt0 =", fit_a["dt0"], "ps")

# Fit (b) cascade
fit_b = fit_cascade_target_analysis(
    t_fs, energy_common, dI_mean, sigma,
    dt0_guess_fs=0.0,
    dt0_bounds_fs=20.0
)
print("Cascade fit:", fit_b["k1"], fit_b["k2"], "ps^-1 ; dt0 =", fit_b["dt0"], "ps")

def populations_direct(t_ps, k):
    P1 = np.exp(-k * t_ps)
    P5 = 1.0 - P1
    return P1, P5

def populations_cascade(t_ps, k1, k2):
    eps = 1e-12
    if abs(k2 - k1) < eps:
        k2 = k1 + eps

    P1 = np.exp(-k1 * t_ps)
    PT = (k1 / (k2 - k1)) * (np.exp(-k1 * t_ps) - np.exp(-k2 * t_ps))
    P5 = 1.0 + (k1*np.exp(-k2 * t_ps) - k2*np.exp(-k1 * t_ps)) / (k2 - k1)
    return P1, PT, P5

def plot_populations_direct_separate(t_fs, fit_a):
    t_ps = t_fs / 1000.0
    k = fit_a["k"]
    dt0_ps = fit_a.get("dt0", 0.0)

    t_eff = t_ps - dt0_ps

    P1, P5 = populations_direct(t_eff, k)

    plt.figure(figsize=(7, 4.5))
    plt.plot(t_fs, P1, lw=2, label='Singlet MLCT')
    plt.plot(t_fs, P5, lw=2, label='Quintet 5T2')
    plt.axvline(0, color='k', lw=0.8, alpha=0.4)
    plt.xlabel("Time delay [fs]")
    plt.ylabel("Population [arb. units]")
    plt.title(f"(a) Direct model: k = {k:.3g} ps-1^{{-1}}-1")
    plt.ylim(-0.05, 1.05)
    plt.legend()
    plt.tight_layout()

    plt.show()

def plot_populations_cascade_separate(t_fs, fit_b):
    t_ps = t_fs / 1000.0
    k1 = fit_b["k1"]
    k2 = fit_b["k2"]
    dt0_ps = fit_b.get("dt0", 0.0)

    t_eff = t_ps - dt0_ps

    P1, PT, P5 = populations_cascade(t_eff, k1, k2)

    plt.figure(figsize=(7, 4.5))
    plt.plot(t_fs, P1,  lw=2, label='Singlet MLCT')
    plt.plot(t_fs, PT,  lw=2, label='Triplet 3T1')
    plt.plot(t_fs, P5,  lw=2, label='Quintet 5T2')
    plt.axvline(0, color='k', lw=0.8, alpha=0.4)
    plt.xlabel("Time delay [fs]")
    plt.ylabel("Population [arb. units]")
    plt.title(f"(b) Cascade model: k1 = {k1:.3g}, k2 = {k2:.3g} ps-1^{{-1}}-1")
    plt.ylim(-0.05, 1.05)
    plt.legend()
    plt.tight_layout()

    plt.show()

# After fitting:
# fit_a = fit_direct_target_analysis(...)
# fit_b = fit_cascade_target_analysis(...)
plot_populations_direct_separate(t_fs, fit_a)
plot_populations_cascade_separate(t_fs, fit_b)