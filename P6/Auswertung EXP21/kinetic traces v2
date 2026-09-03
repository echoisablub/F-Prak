import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import curve_fit
from scipy.special import erf

folder = Path("Daten/Experiment with Data Acquisition/messreihe")

folders = sorted(folder.glob("*"))

all_spectra = []
delays = []

# Common energy grid
energy_grid= np.linspace(7000, 7110, 1000)

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

# KINETIC TRACES
intensity = all_spectra

# Smooth only in TIME direction
intensity_smooth = gaussian_filter1d(intensity,sigma=1.0,axis=0)

# Plot the four kinetic traces
fig, ax = plt.subplots(figsize=(10, 6))

selected_energies = [
    7045.0,
    7053.7,
    7057.8,
    7060.5
]

# Find the closest available energy-grid point
selected_indices_manuel = [
    np.argmin(np.abs(energy_grid - E))
    for E in selected_energies
]
print(selected_indices_manuel)

for idx in selected_indices_manuel:
    trace = intensity_smooth[:, idx]

    # Invert selected traces
    if np.isclose(energy_grid[idx], 7053.7, atol=0.1) or \
       np.isclose(energy_grid[idx], 7057.8, atol=0.1):
        trace = -trace

    # Normalize ?
    trace_norm = trace / np.max(np.abs(trace)) # For comparing timing/shape:
    # trace_norm = trace / np.max(np.abs(intensity_smooth)) # For comparing actual magnitude of the diff-Intensity:

    ax.plot(
        delays,
        trace_norm,
        marker="o",
        markersize=4,
        linewidth=1.5,
        label=f"{energy_grid[idx]:.1f} eV"
    )

ax.set_xlabel("Time delay [fs]")
ax.set_ylabel("Normalized $\Delta$ Signal Intensity [a.u.]")
ax.set_title("Kinetic traces at selected emission energies")
ax.legend(title="Emission energy")
ax.grid(True, alpha=0.2)
plt.savefig(
    "Daten/Analysis and Interpretation/Kinetic traces.png",
    dpi=300
)

# Choose the energy that represents the excited-state population
target_energy = 7045 #? oder eher 7053,6? 
# TODO: find out welcher fit

# Rise time by 10-90% fit (bis Zeile 230)
idx = np.argmin(
    np.abs(energy_grid - target_energy)
)
trace = intensity_smooth[:, idx]
# Invert if necessary
# trace = -trace
# Normalize
trace = trace / np.max(np.abs(trace))

# Baseline: average of measurements before time zero
pre_mask = delays < 0
baseline = np.mean(trace[pre_mask])
# Final population: average of the last few measurements
final_value = np.mean(trace[-2:])

# 10 % and 90 % of the population rise
level_10 = baseline + 0.10 * (final_value - baseline)
level_90 = baseline + 0.90 * (final_value - baseline)

'''print("Rise time of excited-state population")
print(f"Emission energy: {energy_grid[idx]:.2f} eV")
print(f"Baseline:        {baseline:.3f}")
print(f"Final value:     {final_value:.3f}")
print(f"10 % level:      {level_10:.3f}")
print(f"90 % level:      {level_90:.3f}")
'''
# Find crossing of 10 % and 90 %

# Only consider times after time zero
post_mask = delays >= 0

t = delays[post_mask]
I = trace[post_mask]

def find_crossing_time(t, I, level):
    # Find first point above the requested level
    crossing_indices = np.where(I >= level)[0]

    if len(crossing_indices) == 0:
        return np.nan

    i = crossing_indices[0]

    # If the first point is already above the level
    if i == 0:
        return t[0]

    # Linear interpolation between the two surrounding points
    t1 = t[i - 1]
    t2 = t[i]

    I1 = I[i - 1]
    I2 = I[i]

    t_cross = t1 + ((level - I1)/ (I2 - I1)* (t2 - t1))

    return t_cross


t10 = find_crossing_time(t, I, level_10)
t90 = find_crossing_time(t, I, level_90)
rise_time = t90 - t10

# Plot
plt.figure(figsize=(10, 6))

plt.plot(
    delays,
    trace,
    "o-",
    #label=f"{energy_grid[idx]:.1f} eV"
    label=f"Fit, rise time = {rise_time:.1f} fs"
)

# 10 % and 90 % levels
plt.axhline(level_10,linestyle="--",alpha=0.6,label=f"10 %  ({t10:.1f} fs)")
plt.axhline(level_90,linestyle="--",alpha=0.6,label=f"90 %  ({t90:.1f} fs)")

# Vertical lines at crossing times
plt.axvline(t10,linestyle=":",alpha=0.6)
plt.axvline(t90,linestyle=":",alpha=0.6)

plt.xlabel("Time delay [fs]")
plt.ylabel("Normalized Δ Emission Intensity")
plt.legend()
plt.title(
    f"Rise time (10-90%-Fit) at {energy_grid[idx]:.1f} eV"
)
plt.savefig(
    "Daten/Analysis and Interpretation/population rise time at 7045eV_1090fit.png",
    dpi=300)

# Rise function with Sigmoid-Fit
def rise_function(t, A, t0, sigma, B):
    return (B+ A * 0.5 *(1 + erf((t - t0) / (np.sqrt(2) * sigma))))

# Fit
p0 = [
    1.0,     # A
    200.0,   # t0
    150.0,   # sigma
    0.0      # B
]
popt, pcov = curve_fit(rise_function,delays,trace,p0=p0,maxfev=20000)
A, t0, sigma, B = popt

# Calculate 10-90 % rise time
# For an error-function rise:
# 10 %  -> -1.28155 sigma
# 90 %  -> +1.28155 sigma
# Therefore:

rise_time = 2 * 1.28155 * sigma

print(f"Energy: {energy_grid[idx]:.1f} eV")
print(f"t0          = {t0:.2f} fs")
print(f"sigma       = {sigma:.2f} fs")
print(f"Rise time   = {rise_time:.2f} fs")

# Plot fit
t_dense = np.linspace(delays.min(),delays.max(),1000)
fit = rise_function(t_dense,*popt)

plt.figure(figsize=(10, 6))
plt.plot(delays,trace,"o",label="Measurement")
plt.plot(t_dense,fit,linewidth=2,label=f"Fit, rise time = {rise_time:.1f} fs")

plt.xlabel("Time delay [fs]")
plt.ylabel("Normalized Δ Emission Intensity")
plt.title(
    f"Rise time (Sigmoid-Fit) at {energy_grid[idx]:.1f} eV"
)

plt.legend()
plt.grid(True, alpha=0.2)
plt.savefig(
    "Daten/Analysis and Interpretation/population rise time at 7045eV_sigmoidfit.png",
    dpi=300)

plt.tight_layout()
plt.show()