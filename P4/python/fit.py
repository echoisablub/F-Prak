import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x=[]
y=[]
sigma_y = []
filename = sys.argv[1]

with open(filename) as inf:
    for line in inf:
        if not line.startswith('#'):
            parts= line.split()
            x.append(float(parts[0]))
            y.append(float(parts[1]))
            sigma_y.append(float(parts[2]))


def f(x, a, b):
    return a*x + b

# Initial guess.
initial    = np.array([1., 1.])

popt, pcov = curve_fit(f, np.asarray(x), np.asarray(y), initial, np.asarray(sigma_y))

print('=====Best-fitting results======================================')
print('a =', popt[0], '+/-', pcov[0,0]**0.5, 'cm')
print('b =', popt[1], '+/-', pcov[1,1]**0.5, 'cm')
model = f(np.asarray(x),popt[0],popt[1])
r = np.asarray(y) - model
chisq = np.sum((r/np.asarray(sigma_y))**2)
df = len(y) - 2.0
print('Reduced chisq = ',chisq/df)
print('Degrees of freedom = ', df)
print('===============================================================')

x_model = np.arange(np.amin(x),np.amax(x), (np.amax(x)-np.amin(x)) / 100.)
model_plot = f(x_model,popt[0],popt[1])

plt.errorbar(x, y, sigma_y, marker='_', color='r', fmt='o', markersize = 5, capsize = 2.5, label='Messwerte')
plt.plot(x_model, model_plot, label='Fit')
plt.legend(loc='lower right')
plt.title('Buch Dicke gegen Seiten')
plt.xlabel('Seitenzahl')
plt.ylabel('Dicke (cm)')
plt.show()
