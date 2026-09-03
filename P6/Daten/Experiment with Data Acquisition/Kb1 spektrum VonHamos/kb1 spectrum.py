import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from pathlib import Path
import pandas as pd

#folder = Path("Daten/Experiment with Data Acquisition/Kb1 spektrum VonHamos/dif spectrum kb1/pink_acc/")
folder = Path("Daten/(Experiment with Data Acquisition/Kb1 spektrum VonHamos/data kb1 spectrum/pink_new/")


files = sorted(folder.glob("*"))   # all files in folder

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

spectra = []

plt.figure(figsize=(8, 5))

'''for file in files[1:5]:

    df = pd.read_table(
        file,
        sep=r'\s+',
        comment='#',
        header=None,
        names=['Number', 'Energy', 'Intensity']
    )
    #E_0=7400
    E = df['Energy'].to_numpy()
    y = df['Intensity'].to_numpy()

    plt.plot(E, y, '--', alpha=0.7, label=file.name)

    plt.xlabel("Energy [eV]")
    plt.ylabel("Intensity [arb. units]")
    plt.title("Single-shot X-ray spectra")
    plt.grid(True)
    #plt.xlim(-50, 50)
    plt.legend()
    plt.savefig(f"Daten/Experiment with Data Acquisition/Kb1 spektrum VonHamos/dif spectrum kb1/kb1_spectrum_acc_5min.png", dpi=300)
    plt.show()

'''
for file in files:

    # Load data
    df = pd.read_table(
        file,
        sep=r'\s+',
        comment='#',
        header=None,
        names=['Number', 'Energy', 'Intensity']
    )
    #E_0=7400  
    E_0 = 0
    E = df['Energy'].to_numpy()
    y = df['Intensity'].to_numpy()

    # Interpolate to common energy grid
    dE = E-E_0
    energy_grid = np.linspace(dE.min(), dE.max(), 1000)

    interp_func = interp1d(
        dE,
        y,
        kind='cubic'
    )

    y_interp = interp_func(energy_grid)
    spectra.append(y_interp)

spectra = np.array(spectra)
y_average = np.mean(spectra, axis=0)

# Plot averaged spectrum
# plt.figure(figsize=(8, 5))
plt.plot(
    energy_grid,
    y_average,
    label="Average"
)

# FWHM

# Maximum of averaged spectrum
i_max = np.argmax(y_average)

E_peak = energy_grid[i_max]
I_max = y_average[i_max]

# Half maximum
I_half = I_max / 2

# Find left crossing
left_indices = np.where(y_average[:i_max] < I_half)[0]

# Find right crossing
right_indices = np.where(y_average[i_max:] < I_half)[0]

if len(left_indices) > 0 and len(right_indices) > 0:

    i_left = left_indices[-1]
    i_right = i_max + right_indices[0]

    # Interpolate between points to get more accurate crossings
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

    print(f"Peak energy: {E_peak + E_0:.2f} eV")
    print(f"FWHM: {FWHM:.2f} eV")

else:
    print("Could not determine FWHM.")

# FWHM lines
plt.axhline(
    I_half,
    linestyle='--',
    label=f"Half maximum"
)

plt.axvline(
    E_left,
    linestyle=':',
    label=f"FWHM = {FWHM:.2f} eV"
)

plt.axvline(
    E_right,
    linestyle=':'
)

plt.axvline(
    E_peak,
    linestyle='--',
    alpha=0.5
)

# Horizontal line showing actual FWHM width
plt.hlines(
    I_half,
    E_left,
    E_right,
    linewidth=3
)


plt.xlabel("Energy [eV]")
plt.ylabel("Intensity [arb. units]")
plt.title("Averaged Kb1 spectrum")
plt.grid(True)
plt.xlim(7000, 7100)
plt.legend()
plt.savefig("Daten/Experiment with Data Acquisition/Kb1 spektrum VonHamos/kb1_spectrum_new.png", dpi=300)
plt.show()


