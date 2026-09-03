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
all_sd = []
all_Eref = []
all_yref = []

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

        all_Eref.append(E)  # Store the energy reference for each measurement
        all_yref.append(y)  # Store the intensity reference for each measurement

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

    # Mean over the 10 measurements
    y_average = np.nanmean(spectra, axis=0)

    # Standard deviation over the 10 measurements
    sd = np.nanstd(spectra, axis=0, ddof=1)
    all_sd.append(sd)

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
all_sd = np.array(all_sd)
all_Eref = np.array(all_Eref)
all_yref = np.array(all_yref)

# Sort by delay
sort_idx = np.argsort(delays)

delays = delays[sort_idx]

all_spectra = all_spectra[sort_idx]*1e-5 #Intensity is in a.u., so it is scaled down for better readability in the plot (*10^5)
all_sd = all_sd[sort_idx]*1e-5 #Intensity is in a.u., so it is scaled down for better readability in the plot (*10^5)   
all_Eref = all_Eref[sort_idx]
all_yref = all_yref[sort_idx]*1e-5 #Intensity is in


# 3D false-color plot

fig, ax = plt.subplots(figsize=(10, 7))

# Normalize delay for colormap
norm = Normalize(vmin=delays.min(), vmax=delays.max())
cmap = cm.turbo

# Plot all mean spectra (lines)
for delay, E_ref, y_ref, spectrum, sd in zip(delays, all_Eref, all_yref, all_spectra, all_sd):
    color = cmap(norm(delay))

    '''ax.errorbar(
        E_ref*0.001,  #energy in keV
        y_ref,
        yerr=sd,
        fmt='none',
        ecolor=color,
        elinewidth=1.0,
        capsize=2,
        alpha=0.9
    )'''

    ax.plot(
        energy_grid * 0.001, #Energie in keV
        spectrum,
        color=color,
        linewidth=1.5,
        alpha=0.95
    )

# Add colormapped error bars for selected energy points
num_points = 420
energy_indices = np.linspace(0, len(energy_grid) - 1, num_points, dtype=int)

ax.set_xlabel("Energy [keV]")
ax.set_ylabel("Difference Emission Intensity [a.u.]")

ax.set_xlim(7.030, 7.080)
ax.set_title("Time-resolved difference spectra (colormapped error bars)")

# Colorbar
sm = cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])

cbar = fig.colorbar(sm, ax=ax, pad=0.1)
cbar.mappable.set_clim(min(delays) - 50, max(delays) + 50)
cbar.set_label("Time delay [fs]")

plt.tight_layout()
plt.grid()
plt.show()

'''# 3D false-color plot

fig, ax = plt.subplots(figsize=(10, 7))

# Normalize delay for colormap
norm = Normalize(vmin=delays.min(), vmax=delays.max())
cmap = cm.turbo

selected_delays = [400, 800]

for delay, spectrum in zip(delays, all_spectra):

    color = cmap(norm(delay))

    ax.plot(
        energy_grid*0.001, #energy is converted to keV for better readability
        spectrum,
        color=cmap(norm(delay)),
        linewidth=1.5
    )

ax.set_xlabel("Energy [keV]")
ax.set_ylabel("Difference Emission Intensity [a.u.]")

ax.set_xlim(7.030, 7.080)

ax.set_title("Time-resolved difference spectra")


# Colorbar
sm = cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])  

cbar = fig.colorbar(sm, ax=ax, pad=0.1)
cbar.mappable.set_clim(min(delays) - 50, max(delays) + 50) # Extend the range for better color representation
cbar.ax.plot([0.115] *len(delays), delays, ">", color='k', markersize=5, label="Selected Delays", clip_on=False)
cbar.set_label("Time delay [fs]")

plt.tight_layout()
plt.grid()

plt.savefig(
    "Daten/Analysis and Interpretation/Time_resolved_spectrum_new.png",
    dpi=300
)

plt.show()'''