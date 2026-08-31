import numpy as np
import matplotlib.pyplot as plt

E = np.linspace(7000, 7200, 1000)  # Energiebereich in eV
E_edge = 7112.0                    # Fe K-Absorptionskante in eV

# Geometrie & Probenpräparation
d_h2o = 25e-4                      # 25 µm Wasserstrahl-Dicke in cm
rho_h2o = 1.0                      # Dichte von flüssigem Wasser in g/cm^3

d_fe = 54.6e-7                     # 54.6 nm äquivalente Eisendicke in cm
rho_fe = 7.874                     # Dichte von reinem Eisenmetall in g/cm^3

# MASSENSCHWÄCHUNGSKOEFFIZIENTEN (NIST/CXRO)
# Wasser (H2O):
mu_rho_h2o = 15.49 * (7000.0 / E)**3.008

# Eisen (Fe):
mu_rho_fe = np.zeros_like(E)
# Unterhalb der K-Kante (K-Schalen-Wechselwirkung energetisch verboten)
mu_rho_fe[E < E_edge] = 55.57 * (7000.0 / E[E < E_edge])**2.743
# Oberhalb der K-Kante (K-Kanten-Photoeffekt dominiert abrupt)
mu_rho_fe[E >= E_edge] = 407.6 * (7112.0 / E[E >= E_edge])**2.563

# 3. BERECHNUNG DER ABSORBANCE & TRANSMISSION
# Optische Dichte (Absorbanz): A = (mu/rho) * rho * d
A_h2o = mu_rho_h2o * rho_h2o * d_h2o
A_fe = mu_rho_fe * rho_fe * d_fe
A_total = A_h2o + A_fe

# Transmission: T = exp(-A)
T_h2o = np.exp(-A_h2o)
T_fe = np.exp(-A_fe)
T_total = np.exp(-A_total)
# 4. Umrechnung in prozentuale Absorption
Abs_h2o = (1.0 - T_h2o) * 100.0
Abs_fe = (1.0 - T_fe) * 100.0
Abs_total = (1.0 - T_total) * 100.0

# 4. KONTROLLAUSGABE FÜR DIE TABELLEN IM PROTOKOLL
for E_target in E:
    idx = np.abs(E - E_target).argmin()
    print(f"\n--- Werte bei {E_target} eV ---")
    print(f"Wasser: T = {T_h2o[idx]*100:.2f} %, Absorbance = {A_h2o[idx]:.4f}")
    print(f"Eisen (äquiv.): T = {T_fe[idx]*100:.2f} %, Absorbance = {A_fe[idx]:.4f}")
    print(f"Gesamt-Jet: T = {T_total[idx]*100:.2f} %, Absorbance = {A_total[idx]:.4f}")
    contrib_fe = (A_fe[idx] / A_total[idx]) * 100
    print(f"Relativer Dämpfungsbeitrag des Eisens: {contrib_fe:.1f} %")

# 5. PLOT
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Vergleich der Röntgen-Abschwächung im wässrigen Jet (EXP21)\n'
             r'Wasserstrahl ($25\ \mu\mathregular{m}$) vs. Eisen-Äquivalent ($54.6\ \mathregular{nm}$)', 
             fontsize=14, fontweight='bold')

# --- Linker Plot: Transmission ---
ax1.plot(E / 1000.0, T_h2o * 100, label='Reines Wasser (25 µm)', color='#2ca02c', linestyle='--', linewidth=2)
ax1.plot(E / 1000.0, T_fe * 100, label='Eisen-Äquivalent (54.6 nm)', color='#d62728', linestyle=':', linewidth=2)
ax1.plot(E / 1000.0, T_total * 100, label='Gesamtsystem (Wasser + Eisen)', color='#1f77b4', linewidth=2.5)
ax1.axvline(E_edge / 1000.0, color='gray', linestyle='-', alpha=0.5, label='Fe K-Kante (7.112 keV)')

ax1.set_title('Transmission (%)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Photonenenergie (keV)', fontsize=11)
ax1.set_ylabel('Transmission $I/I_0$ (%)', fontsize=11)
ax1.set_ylim(92, 100.5)
ax1.legend(loc='lower left', frameon=True)
ax1.grid(True, which='both', linestyle=':', alpha=0.5)

# --- Rechter Plot: Absorbance ---
ax2.plot(E / 1000.0, A_h2o, label='Reines Wasser (25 µm)', color='#2ca02c', linestyle='--', linewidth=2)
ax2.plot(E / 1000.0, A_fe, label='Eisen-Äquivalent (54.6 nm)', color='#d62728', linestyle=':', linewidth=2)
ax2.plot(E / 1000.0, A_total, label='Gesamtsystem (Wasser + Eisen)', color='#1f77b4', linewidth=2.5)
ax2.axvline(E_edge / 1000.0, color='gray', linestyle='-', alpha=0.5)

# Kennzeichnung der quantitativen Punkte aus Aufgabe 12d
E_targets=[7050,7150]
for E_target, color in zip(E_targets, ['darkorange', 'purple']):
    idx = np.abs(E - E_target).argmin()
    ax2.scatter(E_target / 1000.0, A_total[idx], color=color, s=50, zorder=5)
    ax2.annotate(f"Dämpfungsbeitrag Fe\nbei {E_target} eV: {(A_fe[idx]/A_total[idx])*100:.1f}%", 
                 xy=(E_target / 1000.0, A_total[idx]),
                 xytext=(0, 10), 
                 textcoords='offset points',
                 #arrowprops=dict(arrowstyle="->", color=color),
                 color=color, fontweight='bold', fontsize=9)

ax2.set_title('Absorbanz / Natürliche Optische Dichte', fontsize=12, fontweight='bold')
ax2.set_xlabel('Photonenenergie (keV)', fontsize=11)
ax2.set_ylabel(r'Absorbanz $A = \ln(I_0/I)$', fontsize=11)
ax2.set_ylim(-0.005, 0.07)
ax2.legend(loc='upper left', frameon=True)
ax2.grid(True, which='both', linestyle=':', alpha=0.5)

# Speichern und Anzeigen
plt.tight_layout()
plt.savefig('Daten/Preperatory Estimates/attenuation-comparison-plot.png', dpi=150, bbox_inches='tight')
plt.show()
