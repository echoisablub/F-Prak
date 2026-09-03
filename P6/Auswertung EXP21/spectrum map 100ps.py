import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from matplotlib import cm
from matplotlib.colors import Normalize

energy_grid = np.linspace(7000, 7110, 1000) #common energy grid

file = Path("Daten/Experiment with Data Acquisition/diff 100 ps spektrum/acc_1min_GotthardVonHamos 26-09-02 19-10-44")
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

spectrum = y_interp*1e-5 #Intensity is in a.u., so it is scaled down for better readability in the plot (*10^5)

fig, ax = plt.subplots(figsize=(10, 7))

ax.set_xlabel("Energy [eV]")
ax.set_ylabel("Emission Intensity [a.u.]")

plt.xlim(7030, 7080)

plt.plot(energy_grid, spectrum, color='blue', label="Accumulated transient spectrum 100 ps delay", linewidth=2)
plt.title("Accumulated transient spectrum 100 ps delay")
plt.tight_layout()
plt.grid()

plt.savefig(
    "Daten/Analysis and Interpretation/100ps diff spektrum.png",
    dpi=300
)

plt.show()