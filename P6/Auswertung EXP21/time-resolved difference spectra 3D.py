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

# 3D false-color plot

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Normalize delay for colormap
norm = Normalize(vmin=delays.min(), vmax=delays.max())
cmap = cm.turbo

selected_delays = [400, 800]

energy_mask = (energy_grid >= 7030) & (energy_grid <= 7080)
energy_plot = energy_grid[energy_mask]*0.001 #energy is converted to keV for better readability
# energy_plot = energy_plot[::-1]

for delay, spectrum in zip(delays, all_spectra):

    color = cmap(norm(delay))

    ax.plot(
        [delay] * len(energy_plot),
        energy_plot,
        spectrum[energy_mask],
        color=cmap(norm(delay)),
        linewidth=1.5
    )

    # Standard deviation leider nicht in 3d so machbar 
    # need to find workaround 
    # aber in 2d gehts :)
    '''if delay in selected_delays:
        ax.fill_between(
            energy_plot,
            spectrum[energy_mask] - sd[energy_mask],
            spectrum[energy_mask] + sd[energy_mask],
            color=color,
            alpha=0.2
        )'''

ax.set_xlabel("Time delay [fs]")
ax.set_ylabel("Energy [keV]")
ax.set_zlabel("Difference Emission Intensity [a.u.]") # *10^5

ax.set_ylim(7.030, 7.080)

# Colorbar
sm = cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])

cbar = fig.colorbar(sm, ax=ax, pad=0.1)
cbar.mappable.set_clim(min(delays) - 50, max(delays) + 50) # Extend the range for better color representation
cbar.ax.plot([0.115] *len(delays), delays, ">", color='k', markersize=5, label="Selected Delays")
cbar.set_label("Time delay [fs]")

'''ax.view_init(
    elev=20,
    azim=130
)'''

plt.tight_layout()

ax.grid(True)

for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis._axinfo["grid"]["color"] = (0, 0, 0, 0.2)
    axis._axinfo["grid"]["linewidth"] = 0.5

# Very transparent panes
ax.xaxis.pane.set_alpha(0.05)
ax.yaxis.pane.set_alpha(0.05)
ax.zaxis.pane.set_alpha(0.05)

plt.savefig(
    "Daten/Analysis and Interpretation/Time_resolved_spectrum_3D.png",
    dpi=300
)

plt.show()

# aber hier anderer weg zu plotten mit plotly, was echt cooles tool für sowas ist
# mach dann ne datei auf, in der man rumslicen kann und alles mögliche
'''import plotly.graph_objects as go

fig = go.Figure()

for delay, spectrum in zip(delays, all_spectra):

    fig.add_trace(
        go.Scatter3d(
            x=np.full_like(energy_grid, delay),
            y=energy_grid,
            z=spectrum,
            mode='lines',
            line=dict(width=3),
            name=f'{delay} fs'
        )
    )

fig.update_layout(
    scene=dict(
        xaxis_title='Time delay [fs]',
        yaxis_title='Energy [eV]',
        zaxis_title='Mean Intensity',

        yaxis=dict(
            range=[7030, 7080]
        )
    ),
    width=1000,
    height=700
)

fig.show()'''
