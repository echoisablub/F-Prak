import numpy as np
import matplotlib.pyplot as plt

rho_Fe = 7.874       # g/cm^3
d_Fe = 54.6e-7       # cm, 54.6 nm

# Energy range
E_water = np.array([7000, 7020, 7040, 7060, 7080, 7100, 7112, 7120, 7140, 7160, 7180, 7200])
mu_rho_water = np.array([15.4905, 15.3585, 15.2280, 15.0990, 14.9714, 14.8452, 14.7700, 14.7205, 14.5972, 14.4752, 14.3546, 14.2354])
T_water = np.array([0.962014, 0.962332, 0.962646, 0.962956, 0.963263, 0.963567, 0.963748, 0.963868, 0.964165, 0.964459, 0.964750, 0.965037])

# Iron data
E_Fe = np.array([7000, 7050, 7100, 7111, 7112, 7150, 7200])
mu_rho_Fe = np.array([55.57, 54.49, 53.45, 53.24, 407.60, 404.23, 397.08])

# Calculate transmission of Fe foil
# T = 10^(-mu/rho * rho * d)
T_Fe = 10**(-mu_rho_Fe * rho_Fe * d_Fe)


#PLOT
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(E_water,T_water * 100,'o-',label=r'$\mathrm{H_2O}$, $d=25\,\mu$m')
ax.plot(E_Fe,T_Fe * 100,'s-',label=r'Fe foil, $d=54.6$ nm')

# Fe K-edge
ax.axvline(7112,linestyle='--',linewidth=1,label='Fe K-edge')

# Labels
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Transmission (%)')
ax.set_title('X-ray transmission of water and equivalent Fe foil')

ax.set_xlim(7000, 7200)
ax.set_ylim(96, 100)

ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig('Daten/Preperatory Estimates/Transmission Iron vs Water.png', dpi=300)
plt.show()