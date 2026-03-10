import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

'''# Emittanzbestimmung duch Q-Scan


epsilon_x = ...
epsilon_y = ...

# Beta Funktions Messung

data = np.loadtxt("data/...")
z_pos = data[:, 0] # in cm
x_rms = data[:, 1] # in mm
y_rms = data[:, 2] # in mm

x_rms_m2 = (x_rms * 10**(-3))**2 # in m
y_rms_m2 = (y_rms * 10**(-3))**2 # in m

x_rms_new = np.array(...) + x_rms_m2 # hier wert von Q-Scan einfügen
y_rms_new = np.array(...) + y_rms_m2 # hier punkt
z_pos_new = np.array(...) + z_pos

beta_x_func = x_rms_new/epsilon_x
beta_y_func = y_rms_new/epsilon_y

plt.plot(z_pos_new, beta_x_func, '.', color='red', label="$\\beta_x$")
plt.plot(z_pos_new, beta_y_func, '.', color='blue', label="$\\beta_y$")
plt.xlabel("Z Position [m]")
plt.ylabel("$\\beta$-Funktion")
plt.title("$\\beta$$-Funktionen in Abhängigkeit der z-Achse")
plt.legend()
plt.show()'''

# Strahl
x_1 = [-7.715350, 10.871612]
i_1 = [-2.303, 0.501]
x_2 = [-4.931521, 9.554739]
i_2 = [-2.816, 1.192]

i_1_neu = np.linspace(-1.3, 0.5)
fct = linregress(i_1, x_1)
i_2_neu = np.linspace(-2.9, 1.2)
fct2 = linregress(i_2, x_2)
fct_neu = fct.intercept + fct.slope*i_1_neu
fct2_neu = fct2.intercept + fct2.slope*i_2_neu

plt.plot(i_1_neu, fct_neu, 'r')
plt.plot(i_2_neu, fct2_neu, 'b')
plt.show()