from matplotlib.pylab import norm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from matplotlib import cm
from matplotlib.colors import Normalize
import plotly.graph_objects as go
from scipy.ndimage import gaussian_filter
from scipy.interpolate import RectBivariateSpline


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
all_spectra = all_spectra[sort_idx]

# 3D false-color plot

'''fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Normalize delay for colormap
norm = Normalize(vmin=delays.min(), vmax=delays.max())
cmap = cm.turbo

selected_delays = [400, 800]

energy_mask = (energy_grid >= 7030) & (energy_grid <= 7080)
energy_plot = energy_grid[energy_mask]

for delay, spectrum in zip(delays, all_spectra):

    color = cmap(norm(delay))

    ax.plot(
        [delay] * len(energy_plot),
        energy_plot,
        spectrum[energy_mask],
        color=cmap(norm(delay)),
        linewidth=1.5
    )

    if delay in selected_delays:
        ax.fill_between(
            energy_plot,
            spectrum[energy_mask] - sd[energy_mask],
            spectrum[energy_mask] + sd[energy_mask],
            color=color,
            alpha=0.2
        )

ax.set_xlabel("Time delay [fs]")
ax.set_ylabel("Energy [eV]")
ax.set_zlabel("Mean Intensity")

ax.set_ylim(7030, 7080)

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

plt.show()'''


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


fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection='3d')

energy_mask = (energy_grid >= 7030) & (energy_grid <= 7080)
energy_plot = energy_grid[energy_mask]

X, Y = np.meshgrid(delays, energy_plot, indexing='ij')
Z = all_spectra[:, energy_mask]
Z_smooth = gaussian_filter(
    Z,
    sigma=(2.0, 1.5)
)


# More points in delay direction
delay_dense = np.linspace(
    delays.min(),
    delays.max(),
    1000
)

# More points in energy direction
energy_dense = np.linspace(
    energy_plot.min(),
    energy_plot.max(),
    1000
)

# Cubic interpolation to create a smooth surface

spline = RectBivariateSpline(
    delays,
    energy_plot,
    Z_smooth,
    kx=3,
    ky=3,
    s=0
)

Z_dense = spline(
    delay_dense,
    energy_dense
)

# Meshgrid for plotting
X_dense, Y_dense = np.meshgrid(
    delay_dense,
    energy_dense,
    indexing='ij'
)

# Color according to delay

norm = Normalize(
    vmin=Z_dense.min(),
    vmax=Z_dense.max()
)
colors = cm.hsv(norm(Z_dense))

surf = ax.plot_surface(
    X_dense,
    Y_dense,
    Z_dense,
    facecolors=colors,
    linewidth=0,
    antialiased=True,
    shade=False
)

ax.set_xlabel("Time delay [fs]")
ax.set_ylabel("Energy [eV]")
ax.set_zlabel("Mean Intensity")

ax.set_ylim(7030, 7080)

sm = cm.ScalarMappable(norm=norm, cmap=cm.hsv)
sm.set_array(Z_dense)

cbar = fig.colorbar(sm, ax=ax, pad=0.1)
cbar.set_label("Mean Intensity")

plt.tight_layout()
plt.show()