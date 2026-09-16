import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from pathlib import Path
import pandas as pd

folder = Path("Daten/(Experiment with Data Acquisition/Kb1 spektrum VonHamos/data kb1 spectrum/pink_new/")
files = sorted(folder.glob("*"))

spectra = []

# ---- define common grid ONCE (use global energy range) ----
E0 = 0  # your E_0
mins, maxs = [], []

for file in files:
    df = pd.read_table(
        file,
        sep=r'\s+',
        comment='#',
        header=None,
        names=['Number', 'Energy', 'Intensity']
    )
    dE = df['Energy'].to_numpy() - E0
    mins.append(dE.min())
    maxs.append(dE.max())

energy_grid = np.linspace(min(mins), max(maxs), 1000)

# ---- interpolate all spectra onto this grid ----
for file in files:
    df = pd.read_table(
        file,
        sep=r'\s+',
        comment='#',
        header=None,
        names=['Number', 'Energy', 'Intensity']
    )

    E = df['Energy'].to_numpy()
    y = df['Intensity'].to_numpy()

    dE = E - E0

    # (optional but recommended) ensure sorted x for interp1d
    sort_idx = np.argsort(dE)
    dE_sorted = dE[sort_idx]
    y_sorted = y[sort_idx]

    interp_func = interp1d(dE_sorted, y_sorted, kind='cubic', bounds_error=False, fill_value=np.nan)
    y_interp = interp_func(energy_grid)

    spectra.append(y_interp)

spectra = np.array(spectra)

# average ignoring NaNs (from out-of-range cubic interpolation)
y_average = np.nanmean(spectra, axis=0)

# ---- plot averaged spectrum ----
plt.figure(figsize=(8, 5))
plt.plot(energy_grid, y_average, label="Average")

# FWHM
i_max = np.nanargmax(y_average)
E_peak = energy_grid[i_max]
I_max = y_average[i_max]

I_half = I_max / 2

left_indices = np.where(y_average[:i_max] < I_half)[0]
right_indices = np.where(y_average[i_max:] < I_half)[0]

if len(left_indices) > 0 and len(right_indices) > 0:
    i_left = left_indices[-1]
    i_right = i_max + right_indices[0]

    E_left = np.interp(
        I_half,
        [y_average[i_left], y_average[i_left + 1]],
        [energy_grid[i_left], energy_grid[i_left + 1]]
    )

    E_right = np.interp(
        I_half,
        [y_average[i_right - 1], y_average[i_right]],
        [energy_grid[i_right - 1], energy_grid[i_right]]
    )

    FWHM = E_right - E_left

    print(f"Peak energy: {E_peak + E0:.2f} eV")
    print(f"FWHM: {FWHM:.2f} eV")
else:
    print("Could not determine FWHM.")
    FWHM = np.nan
    E_left = E_right = np.nan

plt.axhline(I_half, linestyle='--', label="Half maximum")
plt.axvline(E_left, linestyle=':', label=f"FWHM = {FWHM:.2f} eV")
plt.axvline(E_right, linestyle=':')
plt.axvline(E_peak, linestyle='--', alpha=0.5)
plt.hlines(I_half, E_left, E_right, linewidth=3)

plt.xlabel("Energy [eV]")
plt.ylabel("Intensity [arb. units]")
plt.title("Averaged Kb1 spectrum")
plt.grid(True)
plt.xlim(7000, 7100)
plt.legend()
plt.savefig("Daten/Experiment with Data Acquisition/Kb1 spektrum VonHamos/kb1_spectrum_new.png", dpi=300)
plt.show()