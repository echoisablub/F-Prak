from scipy.signal import find_peaks
from matplotlib.pylab import norm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from matplotlib import cm
from matplotlib.colors import Normalize
import plotly.graph_objects as go

folder = Path("Daten/Experiment with Data Acquisition/messreihe")

folders = sorted(folder.glob("*"))

all_spectra = []
delays = []

# Common energy grid
energy_grid = np.linspace(7000, 7110, 1000)

for subfolder in folders:

    spectra = []

    for file in subfolder.glob("*"):

        df = pd.read_table(
            file,
            sep=r'\s+',
            comment='#',
            header=None,
            names=['Number', 'Energy', 'Intensity']
        )

        E = df['Energy'].to_numpy()
        y = df['Intensity'].to_numpy()

        # Interpolate onto common energy grid
        interp_func = interp1d(
            E,
            y,
            kind='cubic',
            bounds_error=False,
            fill_value=np.nan
        )

        y_interp = interp_func(energy_grid)

        spectra.append(y_interp)

    spectra = np.array(spectra)

    # Mean over the 20 measurements
    y_average = np.nanmean(spectra, axis=0)

    # Standard deviation over the 20 measurements
    sd = np.nanstd(spectra, axis=0, ddof=1)

    all_spectra.append(y_average)

    # Convert folder name to numerical delay
    name = subfolder.name.lower().replace("fs", "").strip()
    delay = (
        -float(name.replace("min", "").strip())
        if name.startswith("min")
        else float(name)
    )
    delays.append(delay)

all_spectra = np.array(all_spectra)
delays = np.array(delays)

# Sort by delay
sort_idx = np.argsort(delays)

delays = delays[sort_idx]
print(delays)
all_spectra = all_spectra[sort_idx]*1e-5 #Intensity is in a.u., so it is scaled down for better readability in the plot (*10^5)

# Find peaks in the spectra

spectrum = np.nanmean(all_spectra, axis=0)  # Average spectrum across all delays
peaks, properties = find_peaks(spectrum, 
                               prominence=0.01*np.nanmax(spectrum),
                               distance=20)  # find peaks in the spectrum
minima,properties = find_peaks(-spectrum, 
                                prominence=0.01*np.nanmax(spectrum),
                               distance=20)


plt.figure(figsize=(10, 6))
plt.plot(energy_grid, spectrum, label='$\Delta$ Emission Intensity', color='blue')
plt.plot(energy_grid[peaks], spectrum[peaks], "x", label='Detected Peaks', color='red')
plt.plot(energy_grid[minima], spectrum[minima], "x", label='Detected Minima',color='green')

for p in peaks:
    plt.annotate(
        f"{energy_grid[p]:.1f} eV",
        (energy_grid[p], spectrum[p]),
        xytext=(0, 8),
        textcoords="offset points",
        ha="center"
    )


for m in minima:
    plt.annotate(
        f"{energy_grid[m]:.1f} eV",
        (energy_grid[m], spectrum[m]),
        xytext=(0, 8),
        textcoords="offset points",
        ha="center"
    )

plt.title('$\Delta$ Emission Intensity vs Energy')
plt.xlabel('Energy [eV]')
plt.ylabel('$\Delta$ Emission Intensity [a.u.]')
plt.legend()
plt.grid(True)
plt.show()