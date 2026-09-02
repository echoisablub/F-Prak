import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from matplotlib import cm
from matplotlib.colors import Normalize

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
all_spectra = all_spectra[sort_idx]

# 3D false-color plot

#fig, ax = plt.subplots(figsize=(10, 7))
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Normalize delay for colormap
norm = Normalize(vmin=delays.min(), vmax=delays.max())
cmap = cm.viridis

selected_delays = [400, 800]

for delay, spectrum in zip(delays, all_spectra):

    color = cmap(norm(delay))

    ax.plot(
        energy_grid,
        spectrum,
        zs=delay,
        zdir='z',
        color=cmap(norm(delay)),
        linewidth=1.5
    )

    if delay in selected_delays:
        ax.fill_between(
            energy_grid,
            spectrum - sd,
            spectrum + sd,
            color=color,
            alpha=0.2
        )

ax.set_xlabel("Energy [eV]")
ax.set_ylabel("Mean Intensity")
ax.set_zlabel("Time delay [fs]")

ax.set_xlim(7000, 7110)

# Colorbar
sm = cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])

cbar = fig.colorbar(sm, ax=ax, pad=0.1)
cbar.set_label("Time delay [fs]")

plt.tight_layout()
plt.grid()

plt.savefig(
    "Daten/Analysis and Interpretation/Time_resolved_spectrum_3D.png",
    dpi=300
)

#plt.show()