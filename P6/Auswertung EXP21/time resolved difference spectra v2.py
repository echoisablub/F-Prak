import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from matplotlib import cm
from matplotlib.colors import Normalize

folder = Path("Daten/Experiment with Data Acquisition/messreihe")
folders = sorted(folder.glob("*"))

all_spectra = []  # mean per delay on E_ref
all_sd = []        # sd per delay on E_ref
all_Eref = []      # raw energy grid per delay (chosen from first file)
delays = []

for subfolder in folders:

    y_interp_list = []
    E_ref = None

    # exactly 10 files
    files = sorted(subfolder.glob("*"))
    if len(files) == 0:
        continue

    for file in files:
        df = pd.read_table(
            file,
            sep=r'\s+',
            comment='#',
            header=None,
            names=['Number', 'Energy', 'Intensity']
        )

        E = df["Energy"].to_numpy()
        y = df["Intensity"].to_numpy()

        # Ensure increasing E for interp1d
        idx = np.argsort(E)
        E = E[idx]
        y = y[idx]

        if E_ref is None:
            E_ref = E  # choose raw measured energies from first file

        interp_func = interp1d(
            E, y,
            kind="cubic",
            bounds_error=False,
            fill_value=np.nan
        )
        y_interp_list.append(interp_func(E_ref))

    if E_ref is None or len(y_interp_list) == 0:
        continue

    spectra_interp = np.array(y_interp_list) 
    y_average = np.nanmean(spectra_interp, axis=0)
    sd = np.nanstd(spectra_interp, axis=0, ddof=1)

    # Convert folder name to numerical delay
    name = subfolder.name.lower().replace("fs", "").strip()
    delay = (
        -float(name.replace("min", "").strip())
        if name.startswith("min")
        else float(name)
    )

    delays.append(delay)
    all_spectra.append(y_average)
    all_sd.append(sd)
    all_Eref.append(E_ref)

delays = np.array(delays)
sort_idx = np.argsort(delays)

all_spectra = np.array(all_spectra)
all_sd = np.array(all_sd)
all_Eref = np.array(all_Eref)

delays = delays[sort_idx]
all_spectra = all_spectra[sort_idx]
all_sd = all_sd[sort_idx]
all_Eref = all_Eref[sort_idx]

all_spectra = all_spectra * 1e-5 # for better readability
all_sd = all_sd * 1e-5

# 3d color plot
fig, ax = plt.subplots(figsize=(10, 7))

norm = Normalize(vmin=delays.min(), vmax=delays.max())
cmap = cm.turbo

# option to sparsify error bars so it doesn’t become unreadable
num_points = len(E_ref)

for delay, E_ref, spectrum, sd in zip(delays, all_Eref, all_spectra, all_sd):
    color = cmap(norm(delay))

    inds = np.linspace(0, len(E_ref) - 1, num_points, dtype=int)

    # error bars on raw measured points
    ax.errorbar(
        E_ref[inds] * 0.001,      # keV
        spectrum[inds],
        yerr=sd[inds],
        fmt="none",
        ecolor=color,
        elinewidth=1.0,
        capsize=2,
        alpha=0.9
    )

    # optional: plot the mean curve
    ax.plot(E_ref * 0.001, spectrum, color=color, linewidth=1.2, alpha=0.7)

ax.set_xlabel("Energy [keV]")
ax.set_ylabel("Difference Emission Intensity [a.u.]")
ax.set_xlim(7.030, 7.080)
ax.set_title("Time-resolved difference spectra")

sm = cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, pad=0.1)
cbar.mappable.set_clim(min(delays) - 50, max(delays) + 50)
cbar.set_label("Time delay [fs]")

plt.tight_layout()
plt.grid()

plt.savefig(
    "Daten/Analysis and Interpretation/Time_resolved_spectrum_errbars.png",
    dpi=300
)

plt.show()
