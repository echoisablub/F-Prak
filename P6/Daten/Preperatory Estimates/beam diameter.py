import numpy as np
import matplotlib.pyplot as plt

# Constants
c_sol = 0.308           # mol/L
N_A = 6.022e23          # 1/mol
d_jet = 100e-6           # m
lambda_laser = 400e-9   # m
h = 6.626e-34           # J s
c_light = 2.998e8       # m/s
# Photon energy
E_photon = h * c_light / lambda_laser

# Beam diameter
d_beam = np.linspace(20, 300, 500)  # µm
d_beam_m = d_beam * 1e-6

# Effective Gaussian beam area: A_eff = 1.133 * d_FWHM^2
A_eff = 1.133 * d_beam_m**2

# Illuminated volume
V_eff = A_eff * d_jet   # m^3
# convert m^3 -> L
V_eff_L = V_eff * 1000

# Number of molecules
N_molecules = c_sol * N_A * V_eff_L

# Critical pulse energy:
# N_photons = N_molecules
E_critical = N_molecules * E_photon
E_critical_uJ = E_critical * 1e6

# Comparison points
beam_sizes = np.array([50, 75, 100])   # µm

A = 1.133 * (beam_sizes * 1e-6)**2
V = A * d_jet * 1000    # L
N = c_sol * N_A * V
E = N * E_photon * 1e6  # µJ

# Plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(d_beam,E_critical_uJ,linewidth=2,label='Critical pulse energy')

# Available laser pulse energy
ax.axhline(50,linestyle='--',linewidth=1.5,label='Maximum available: 50 µJ')
ax.scatter(beam_sizes,E,s=60,zorder=3)
offsets = [
    (-20, 20),    # 50 µm
    (-20, 15),    # 75 µm
    (-20, 15),    # 100 µm
]
for d, e, n, offset in zip(beam_sizes, E, N, offsets):
    ax.annotate(f'{d}µm, {e:.1f}µJ\nN={n:.2e}',(d, e),xytext=offset,textcoords='offset points',fontweight='bold', fontsize=8)

# Your selected beam size
d_selected = 75
# Calculate corresponding values
A_75 = 1.133 * (75e-6)**2
V_75 = A_75 * d_jet * 1000
N_75 = c_sol * N_A * V_75
E_75 = N_75 * E_photon * 1e6

ax.scatter(d_selected,E_75,s=70,zorder=3,label=f'75 µm → {E_75:.1f} µJ')
ax.set_xlabel('Beam diameter $d_{FWHM}$ ($\mu m$)')
ax.set_ylabel('Critical pulse energy ($\mu J$)')
ax.set_title('Critical laser pulse energy vs. beam size\n'r'$\lambda = 400$ nm, $d_{jet}=100\,\mu$m')

ax.set_xlim(20, 150)
ax.set_ylim(0, 200)
ax.grid(True, alpha=0.3)
ax.legend()
plt.savefig('Daten/Preperatory Estimates/beam_diameter.png', dpi=300)
plt.tight_layout()
plt.show()

