import numpy as np
from scipy.interpolate import UnivariateSpline, interp1d
from scipy.stats import linregress
from scipy.signal import argrelextrema
from scipy.constants import c
from scipy.fft import fft, fftfreq, fftshift
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# 1. Daten einlesen
def load_data(filepath):
    data = np.loadtxt(filepath)
    positions = data[:, 0]
    measurements = data[:, 1:20]  # N Spalten mit Messwerten
    return positions, measurements

def average_measurements(measurements):
    return np.mean(measurements, axis=1)

def interpolate(x, y, factor=10): #für x positions und y avergae_measurements
    f_interpol = UnivariateSpline(x, y, k=4)
    x_new = np.linspace(x.min(), x.max(), len(x)*factor)
    y_new = f_interpol(x_new)
    return x_new, y_new, f_interpol

'''def interpolate(x, y, factor=10): #für x positions und y avergae_measurements
    f_interpol = interp1d(x, y, kind='cubic')
    x_new = np.linspace(x.min(), x.max(), len(x)*factor)
    y_new = f_interpol(x_new)
    return x_new, y_new, f_interpol'''

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

'''# Analyse für das Weißlicht- oder Jod-Interferogramm
file_path_led = "Auswertung KV6/data/Filter 1/Data Channel 0.dat"
positions_led, measurements_led = load_data(file_path_led)
mean_data_led = average_measurements(measurements_led)'''

# Dateipfade
path_jod = "data/Iod 1/Data Channel 0.dat"
path_ref = "data/Iod 1/Data Channel 1.dat"

# Einlesen und Mittelwertbildung
pos_jod, meas_jod = load_data(path_jod)
mean_jod = average_measurements(meas_jod)

pos_ref, meas_ref = load_data(path_ref)
mean_ref = average_measurements(meas_ref)


# Erste Interpolation der Laser-Daten
x_new, y_new, f_interpol = interpolate(positions, mean_data_laser, factor=10)

'''plt.plot(positions, mean_data_laser, '.', color='green', label="Datenpunkte")
plt.plot(x_new, y_new, '-', color='red', label="Interpolation")
plt.xlabel("Motorposition")
plt.ylabel("Signal")
plt.title("Laser-Daten: Interpolation vs. Originaldaten")
plt.legend()
plt.show()'''


# Bestimmung der Extrema
peaks, troughs = find_extrema(y_new)
maxima_positions = x_new[peaks]

'''plt.plot(x_new, y_new, '-', color='red', label="Interpolation")
plt.plot(maxima_positions, f_interpol(maxima_positions), 'x', color='green', label="Maxima")
plt.xlabel("Motorposition")
plt.ylabel("Signal")
plt.title("Laser-Daten: Interpolation mit Maxima")
plt.legend()
plt.show()'''

# Kalibrierfunktion bestimmen
r, fit = linear_fit(maxima_positions)

'''plt.plot(r, maxima_positions, 'x', color='orange', label="Maxima")
plt.plot(r, fit.intercept + fit.slope*r, '-', color='blue', label="Lineare Anpassung")
plt.xlabel("Maxima")
plt.ylabel("Motorposition")
plt.title("Kalibrierfunktion: Lineare Anpassung der Maxima")
plt.legend()
plt.show()'''

P_soll = np.empty(len(maxima_positions), dtype=int)
P_ist = maxima_positions
for i in range(len(maxima_positions)):
    P_soll[i] = fit.intercept + fit.slope*i
delta = P_soll - P_ist
delta_interpolate = UnivariateSpline(P_ist, delta, k=4)

'''plt.plot(P_ist, delta, 'x', color='red', label="Daten")
plt.plot(x_new, delta_interpolate(x_new), '-', color='blue', label="Interpolation der Korrektur")
plt.xlabel("Motorposition")
plt.ylabel("Korrektur (Soll - Ist)")
plt.title("Korrektur der Motorpositionen")
plt.legend()
plt.show()
'''
'''# Erzeugen der korrigierten Ortsachse für die Weißlicht-Daten
# x sind die ursprünglichen Motorpositionen
x_korr_led = positions_led + delta_interpolate(positions_led)

# Erzeugen einer äquidistanten Achse für die FFT
x_korr_eq = np.linspace(x_korr_led.min(), x_korr_led.max(), len(x_korr_led))

# Erneute Interpolation auf das äquidistante Gitter
led_interpolate_func = UnivariateSpline(x_korr_led, mean_data_led, k=4)
led_interferogram_korr = led_interpolate_func(x_korr_eq)'''

# Korrektur der ursprünglichen Ortsachsen
x_korr_jod = pos_jod + delta_interpolate(pos_jod)
x_korr_ref = pos_ref + delta_interpolate(pos_ref)

# Erzeugen eines gemeinsamen, äquidistanten Gitters für die FFT
# Wichtig: Benutze für beide das exakt gleiche Gitter!
x_min = max(x_korr_jod.min(), x_korr_ref.min())
x_max = min(x_korr_jod.max(), x_korr_ref.max())
x_eq = np.linspace(x_min, x_max, 10000)

# Interpolation für Jod und Referenz
interpol_jod = UnivariateSpline(x_korr_jod, mean_jod, k=4)
interpol_ref = UnivariateSpline(x_korr_ref, mean_ref, k=4)

y_eq_jod = interpol_jod(x_eq)
y_eq_ref = interpol_ref(x_eq)

'''# Ortskorrektur Laser
x= np.linspace(-5000, 5000, 10000)
x_korr = x + delta_interpolate(x)
x_korr_eq = np.arange(min(x_korr), max(x_korr), (max(x_korr)-min(x_korr))/len(x_korr))

# Neue Interpolation nach Korrektur
laser_interpolate_func = UnivariateSpline(x_korr, mean_data_laser, k=4)
laser_interpolate_korr = laser_interpolate_func(x_korr_eq)'''

#vergleich der Interpolation vor und nach Korrektur
'''fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Vergleich')
ax1.plot(x_korr_eq, laser_interpolate_korr, '-', color='red', label="Korrigierte Interpolation")
ax1.set_xlabel("Motorposition")
ax1.set_ylabel("Signal")
ax1.legend()
ax2.plot(x_new, y_new, '-', color='green', label="Ursprüngliche Interpolation")
ax2.set_xlabel("Motorposition")
ax2.set_ylabel("Signal")
ax2.legend()
plt.show()'''

# Ort zu Zeit Trafo

# old code
'''delta_s = x_korr*101*10**(-5)/fit.slope
c = 3*10**8  # Lichtgeschwindigkeit in m/s
delta_t = delta_s / c # Zeit in Sekunden

# Fourier Transformation
#T_sample= ((max(delta_t)-min(delta_t))/len(delta_t))*1e12 #in pentasec

freq, spectrum = compute_spectrum(laser_interpolate_korr, delta_t)

plt.plot(freq, spectrum, color='purple')
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude")
plt.title("Laser Spektrum")
plt.show()
'''

#delta_s_laser = x_korr_eq*532*10**(-9)/fit.slope #: andere Gruppe
#delta_t_laser = delta_s_laser / c
#d_laser = delta_t_laser
delta_s_led = x_eq * 532e-9 / fit.slope 
delta_t_led = delta_s_led / c
d_led = delta_t_led
#print(len(delta_s_led))

# FFT
# compute_spectrum liefert Frequenzachse und Amplituden
# freq_axis, spectrum_jod = compute_spectrum(y_eq_jod, d_led[3] - d_led)
# _, spectrum_ref = compute_spectrum(y_eq_ref, d_led[3] - d_led)

# lambda_all = c / (freq_axis + 1e-12) * 1e9

# FT 
'''T_sample_laser= ((max(d_laser)-min(d_laser))/len(d))*1e12 #Ps
f_max_laser=1/T_sample_laser
L_laser=len(d_laser)
f_Ny=f_max/2
w=np.linspace(-f_Ny,f_Ny,L_laser)
W=abs(fftshift(fft(laser_interpolate_korr/L)))
W_imp=W/max(W) # normierung, weil?
'''
T_sample_led= ((max(d_led)-min(d_led))/len(d_led))*1e12 #Ps
f_max_led=1/T_sample_led
L_led=len(d_led)
f_Ny=f_max_led/2
freq_axis=np.linspace(-f_Ny,f_Ny,L_led)
spectrum_jod=abs(fftshift(fft(y_eq_jod/L_led)))
spectrum_ref=abs(fftshift(fft(y_eq_ref/L_led)))
spectrum_jod_norm=spectrum_jod/max(spectrum_jod)
spectrum_ref_norm=spectrum_ref/max(spectrum_ref)


# f_peak, _ = find_peaks(W_imp, prominence=0.15)
# print(f_peak)
# von w den 6889 index -> w_postion von +peak = 563.6648002224845
# mittelpunkt peak = 0.14915713157506616
# w_postion von -peak = -563.3664859593342
# print(w[5000])

# f_mittelwert_laser = 563.515643091*10**12
# lambda_f =c/f_mittelwert_laser
# print(lambda_f)
# =5.320037902684942e-07 =532nm yaaay

'''plt.plot(w,W_imp, color='purple')
plt.xlim(0,1000)
plt.ylim(0,0.25)
plt.xlabel("Frequenz [PHz]")
plt.ylabel("Amplitude")
plt.title("Laser Spektrum")
plt.show()'''

# umrechnung frequenz zu wellenlänge
# lambda_laser = c/(w*10**(12-9))
lambda_led= c / (freq_axis * 1e-12) * 1e9

#f_peak, _ = find_peaks(spectrum_jod_norm)
#print(f_peak)
#von w den 6889 index -> w_postion von +peak = 563.6648002224845
#mittelpunkt peak = 0.14915713157506616
# w_postion von -peak = -563.3664859593342
# print(w[5000])

#plt.plot(w,W_imp,color='purple')
#plt.plot(freq_axis,spectrum_jod_norm, color='purple', label='jod')
#plt.plot(freq_axis,spectrum_ref_norm, color='orange', label='ref')
plt.plot(lambda_led,spectrum_ref_norm, color='orange', label='ref')
plt.plot(lambda_led,spectrum_jod_norm, color='purple',label='jod')
#plt.xlim(350,700)
#plt.ylim(0,0.00052)
plt.xlim(2e26, 10e26)
plt.ylim(0, 0.00052)
plt.xlabel("Wellenlänge [nm]")
#plt.xlabel("Frequenz [PHz]")
plt.ylabel("Amplitude")
#plt.title("Laser Spektrum, Wellenlänge")
plt.title("LED Spektrum, Wellenlänge")
#plt.title("Led Spektrum, Frequenz")
plt.legend()
plt.show()


#Todo: optische dichte und so

#Um subtile Details in den gemessenen Spektren sichtbar zu machen, ist es sinnvoll, die Daten mit
#einem Referenzspektrum zu korrigieren. Dazu wird typischerweise die optische Dichte OD =
#−log(I/I0) oder aber auch die differentielle optische Transmission (I −I0)/I0 berechnet. I0
#bezieht sich dabei auf das Referenzspektrum. Berechnen Sie wahlweise die OD oder DOT aus
#den Spektren der Jod- und Referenzprobe

# 1. Berechnung der Optischen Dichte (OD)
# Formel: OD = -log10(I / I0)
# Wir nutzen np.log10, da OD im physikalischen Kontext meist dekadisch ist.
# Ein kleines epsilon verhindert Division durch Null.
epsilon = 1e-12
od = -np.log10((spectrum_jod + epsilon) / (spectrum_ref))

# 2. Berechnung der Differentiellen Optischen Transmission (DOT)
# Formel: DOT = (I - I0) / I0
dot = (spectrum_jod - spectrum_ref) / (spectrum_ref)


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
# Darstellung der Optischen Dichte (OD)
ax1.plot(lambda_led, od, color='darkred', label='Optische Dichte (OD)')
ax1.set_ylabel("OD")
ax1.set_title("Absorptionsspektrum der Jod-Probe (OD)")
ax1.grid(True)
ax1.legend()
# Darstellung der Differentiellen Transmission (DOT)
ax2.plot(lambda_led, dot, color='blue', label='Diff. Transmission (DOT)')
ax2.set_xlabel("Wellenlänge [nm]")
#ax2.set_xlabel("Frequenz [PHz]")
ax2.set_ylabel("DOT")
ax2.set_title("Spektrum: Differentielle Transmission (DOT)")
ax2.grid(True)
ax2.legend()
# Bereich auf den interessanten Teil begrenzen (z.B. 450nm bis 650nm für Jod)
# plt.xlim(450, 700) 
plt.tight_layout()
plt.show()

