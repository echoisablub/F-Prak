import numpy as np
from scipy.interpolate import UnivariateSpline, interp1d
from scipy.stats import linregress
from scipy.signal import argrelextrema
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# 1. Daten einlesen
def load_data(filepath):
    data = np.loadtxt(filepath)
    positions = data[:, 0]
    measurements = data[:, 1:20]  # N Spalten mit Messwerten
    return positions, measurements

def average_measurements(measurements):
    return np.mean(measurements, axis=1)

def interpolate(x, y, factor=10): #für x positions und y avergae_measurements
    f_interpol = interp1d(x, y, kind='cubic')
    x_new = np.linspace(x.min(), x.max(), len(x)*factor)
    y_new = f_interpol(x_new)
    return x_new, y_new, f_interpol

def find_extrema(y):
    peaks = argrelextrema(y, np.greater)[0]
    troughs = argrelextrema(y, np.less)[0]
    return peaks, troughs

def linear_fit(extrema):
    r = np.linspace(0, len(extrema)-1, len(extrema))
    fit = linregress(r, extrema)
    return r, fit

'''def reinterpolate(x_korr, y, num_points=1000):
    f = interp1d(x_korr, y, kind='cubic')
    x_new = np.linspace(x_korr.min(), x_korr.max(), num_points)
    y_new = f(x_new)
    return x_new, y_new
'''

def compute_spectrum(y, delta_t):
    n = len(y)
    y_f = fft(y)
    x_f = fftfreq(n, d=delta_t)[:n//2] #[:n//2] um nur die positiven Frequenzen zu haben
    spectrum = 2.0/n * np.abs(y_f[:n//2]) #skalierung der Amplitude
    return x_f, spectrum


# Analyse der Laser-Daten:
file_path = "data/Filter 1/Data Channel 2.dat"
positions, measurements = load_data(file_path)
mean_data_laser = average_measurements(measurements)

# Erste Interpolation der Laser-Daten
x_new, y_new, f_interpol = interpolate(positions, mean_data_laser, factor=10)

plt.plot(positions, mean_data_laser, '.', color='green', label="Datenpunkte")
plt.plot(x_new, y_new, '-', color='red', label="Interpolation")
plt.xlabel("Motorposition")
plt.ylabel("Signal")
plt.title("Laser-Daten: Interpolation vs. Originaldaten")
plt.legend()
plt.show()



# Bestimmung der Extrema
peaks, troughs = find_extrema(y_new)
maxima_positions = x_new[peaks]

plt.plot(x_new, y_new, '-', color='red', label="Interpolation")
plt.plot(maxima_positions, f_interpol(maxima_positions), 'x', color='green', label="Maxima")
plt.xlabel("Motorposition")
plt.ylabel("Signal")
plt.title("Laser-Daten: Interpolation mit Maxima")
plt.legend()
plt.show()

# Kalibrierfunktion bestimmen
r, fit = linear_fit(maxima_positions)

plt.plot(r, maxima_positions, 'x', color='orange', label="Maxima")
plt.plot(r, fit.intercept + fit.slope*r, '-', color='blue', label="Lineare Anpassung")
plt.xlabel("Maxima")
plt.ylabel("Motorposition")
plt.title("Kalibrierfunktion: Lineare Anpassung der Maxima")
plt.legend()
plt.show()

P_soll = np.empty(len(maxima_positions), dtype=int)
P_ist = maxima_positions
for i in range(len(maxima_positions)):
    P_soll[i] = fit.intercept + fit.slope*i
delta = P_soll - P_ist
delta_interpolate = UnivariateSpline(P_ist, delta, k=4)

plt.plot(P_ist, delta, 'x', color='red', label="Daten")
plt.plot(x_new, delta_interpolate(x_new), '-', color='blue', label="Interpolation der Korrektur")
plt.xlabel("Motorposition")
plt.ylabel("Korrektur (Soll - Ist)")
plt.title("Korrektur der Motorpositionen")
plt.legend()
plt.show()

# Ortskorrektur
x= np.linspace(-5000, 5000, 10000)
x_korr = x + delta_interpolate(x)
x_korr_eq = np.arange(min(x_korr), max(x_korr), (max(x_korr)-min(x_korr))/len(x_korr))

# Neue Interpolation nach Korrektur
laser_interpolate_func = UnivariateSpline(x_korr, mean_data_laser, k=4)
laser_interpolate_korr = laser_interpolate_func(x_korr_eq)

#vergleich der Interpolation vor und nach Korrektur
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Vergleich')
ax1.plot(x_korr_eq, laser_interpolate_korr, '-', color='red', label="Korrigierte Interpolation")
ax1.set_xlabel("Motorposition")
ax1.set_ylabel("Signal")
ax1.legend()
ax2.plot(x_new, y_new, '-', color='green', label="Ursprüngliche Interpolation")
ax2.set_xlabel("Motorposition")
ax2.set_ylabel("Signal")
ax2.legend()
plt.show()

# Ort zu Zeit Trafo
delta_s = x_korr*101*10**(-5)/fit.slope
c = 3*10**8  # Lichtgeschwindigkeit in m/s
delta_t = delta_s / c # Zeit in Sekunden

# Fourier Transformation
#T_sample= ((max(delta_t)-min(delta_t))/len(delta_t))*1e9 #in pentasec

freq, spectrum = compute_spectrum(laser_interpolate_korr, delta_t)

plt.plot(freq, spectrum, color='purple')
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude")
plt.title("Laser Spektrum")
plt.show()

# umrechnung frequenz zu wellenlänge

#Todo: optische dichte und so
