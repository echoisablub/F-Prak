import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# -----------------------------
# Messdaten
# -----------------------------
I_pos = np.array([0.923, 1.023, 1.121, 1.221, 1.316, 1.419,
                  1.519, 1.621, 1.724, 1.812, 1.919])

x_rms_qscan = np.array([0.638175, 0.516351, 0.434130, 0.388772,
                        0.363201, 0.388798, 0.439333, 0.494053,
                        0.544843, 0.535492, 0.505021])

x_ms_qscan = x_rms_qscan**2


I_neg = np.array([-0.908, -1.004, -1.104, -1.206, -1.306, -1.404,
                  -1.509, -1.607, -1.709, -1.802, -1.902])

y_rms_qscan = np.array([0.775577, 0.832959, 0.693442, 0.604762,
                        0.554150, 0.576056, 0.644182, 0.742516,
                        0.871134, 0.976145, 1.160084])

y_ms_qscan = y_rms_qscan**2
print(y_ms_qscan)

# -----------------------------
# Interpolation
# -----------------------------

# x-Richtung
x_spline = CubicSpline(I_pos, x_ms_qscan)

I_pos_interp = np.linspace(I_pos.min(), I_pos.max(), 500)
x_ms_interp = x_spline(I_pos_interp)

# y-Richtung

sort_idx = np.argsort(I_neg)

I_neg_sorted = np.array(I_neg)[sort_idx]
y_ms_sorted = np.array(y_ms_qscan)[sort_idx]

y_spline = CubicSpline(I_neg_sorted, y_ms_sorted)

I_neg_interp = np.linspace(I_neg_sorted.min(), I_neg_sorted.max(), 500)
y_ms_interp = y_spline(I_neg_interp)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(8, 5))

# Messpunkte
plt.plot(I_pos, x_ms_qscan, '.', color='red',
         markersize=7, label=r'$\sigma_x^2(I)$ Messwerte')

plt.plot(I_neg, y_ms_qscan, '.', color='blue',
         markersize=7, label=r'$\sigma_y^2(I)$ Messwerte')

# interpolierte Kurven
plt.plot(I_pos_interp, x_ms_interp, color='red',
         label=r'$\sigma_x^2(I)$ Interpolation')

plt.plot(I_neg_interp, y_ms_interp, color='blue',
         label=r'$\sigma_y^2(I)$ Interpolation')

# Achsen
plt.xlabel('Quadrupolstrom [A]')
plt.ylabel('Strahlengröße $\sigma^2$  [mm$^2$]')
plt.title(r'$\sigma_x^2(I)$ bzw. $\sigma_y^2(I)$')

plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(r"Auswertung EXP9/output/emittanz plot.png")

plt.show()

