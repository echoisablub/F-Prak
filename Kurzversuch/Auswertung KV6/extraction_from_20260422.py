# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:22:45 2026

@author: wieland
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 14:37:15 2026

@author: wieland
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline,make_interp_spline
from scipy.stats import linregress
from scipy.signal import argrelextrema
from scipy.signal import find_peaks, savgol_filter
from scipy.constants import c
from scipy.fft import fft, fftshift
from scipy.interpolate import interp1d


# 1. Daten einlesen
def load_data(filepath):
    data = np.loadtxt(filepath)
    positions = data[:, 0]
    measurements = data[:, 1:20]  # N Spalten mit Messwerten
    return positions, measurements

def average_measurements(measurements):
    return np.mean(measurements, axis=1)

def interpolate(x, y, factor=10): #für x positions und y avergae_measurements
    f_interpol = make_interp_spline(x, y, k=3)
    #f_interpol = UnivariateSpline(x, y, k=3)
    x_new = np.linspace(x.min(), x.max(), len(x)*factor)
    y_new = f_interpol(x_new)
    return x_new, y_new

def find_extrema(y):
    # peaks = argrelextrema(y, np.greater)[0]
    # troughs = argrelextrema(y, np.less)[0]
    # extrema_list = []
    # for i, j in zip(peaks, troughs):
    #     extrema_list.append(i)
    #     extrema_list.append(j)

    # extrema_array=np.array(extrema_list)

    #return extrema_array, peaks

    # Laser-Signal glätten vor der Peak-Suche
    # smooth_laser = savgol_filter(mean_data_laser, window_length=51, polyorder=3)
    # Robuste Peaks finden (nur die großen Maxima der Laser-Fringes)
    # peaks, _ = find_peaks(smooth_laser, distance=50, prominence=0.01)
    
    extrema_array = np.sort(np.append(argrelextrema(y,np.greater),argrelextrema(y,np.less)))
    
    return extrema_array


def linear_fit(extrema):
    r = np.linspace(0, len(extrema)-1, len(extrema))
    fit = linregress(r, extrema)
    return r, fit

def korrekturfunktion(data):
    # Analyse der Laser-Daten:
    file_path = "data/"+data+"/Data Channel 2.dat"
    positions, measurements = load_data(file_path)
    mean_data_laser = average_measurements(measurements)
    
    # Erste Interpolation der Laser-Daten
    x_new, y_new = interpolate(positions, mean_data_laser, factor=10)

    # Bestimmung der Extrema
    #smooth_laser = savgol_filter(mean_data_laser, window_length=51, polyorder=3)
    #peaks, _ = find_peaks(smooth_laser, distance=50, prominence=0.01)
    #maxima_positions = x_new[peaks]
    #_, extrema_array = find_extrema(y_new)
    extrema_array = find_extrema(y_new)
    maxima_positions = x_new[extrema_array]
    print("maxima menge = ",len(maxima_positions))
    
    # Kalibrierfunktion bestimmen
    r, fit = linear_fit(maxima_positions)

    P_soll = np.empty(len(maxima_positions), dtype=int)
    P_ist = maxima_positions
    for i in range(len(maxima_positions)):
        P_soll[i] = fit.intercept + fit.slope*i
    delta = P_soll - P_ist
    delta_interpolate = make_interp_spline(P_ist, delta, k=3)
    #delta_interpolate = UnivariateSpline(P_ist, delta, k=3)

    return delta_interpolate, fit.slope, positions, mean_data_laser, maxima_positions

dataset = "Iod 2"

# Korrekturfunktion für Datensatz
delta_func, laser_slope, position, mean_data_laser, maxima_positions = korrekturfunktion(dataset)

#Ortskorrektur
# Ursprüngliche Achse korrigieren
x_korr = position + delta_func(position)

# Erzeugen eines äquidistanten Gitters für die FFT
x_eq = np.linspace(x_korr.min(), x_korr.max(), len(x_korr))

# Erneute Interpolation auf das neue Gitter
f_int = make_interp_spline(x_korr, mean_data_laser, k=3)
#f_int = interp1d(x_korr, mean_data_laser, kind='slinear', fill_value='extrapolate')
y_eq_laser = f_int(x_eq)

def fft_spectrum(x_eq, y_eq, laser_slope):
    """
    Führt die Ort-zu-Zeit Transformation und die FFT durch.
    
    Parameter:
    x_eq: Äquidistante Ortsachse (Motorschritte)
    y_eq: Interpolierte Signalwerte (Kanal 0, 1 oder 2)
    laser_slope: Steigung aus der Laserkalibrierung (Schritte pro Maximum)
    """
    # Ort zu Zeit Transformation
    #lambda_half = 266e-9 
    delta_s = (x_eq * 266e-9) / laser_slope
    delta_t_axis = delta_s / c

    # Sampling-Parameter für die FFT
    # Wir benötigen das Zeitintervall T_sampl als Skalar für die Frequenzachse.
    L = len(delta_t_axis)
    t_range = np.max(delta_t_axis) - np.min(delta_t_axis)
    
    # Tsampl oft in Ts angegeben (Faktor 1e12), um handliche Frequenzwerte zu erhalten.
    T_sampl = (t_range / L)  * 1e12
    f_max = 1 / T_sampl
    f_ny = f_max / 2
    
    # Frequenzachse erzeugen
    # Die FFT liefert ein symmetrisches Signal um die Frequenz 0.
    freq_axis = np.linspace(-f_ny, f_ny, L)
    
    # Apodisation: Korrekturfaktor zum "Ausschmieren" des Rechteckfensters, das durch das endliche Zeitintervall entsteht
    # Ziel: Dämpfen der hochfrequenten Überschwinger, die aus der FFT der Rechteckfunktion resultieren
    apo = np.hanning(len(delta_t_axis))

    # FFT berechnen und verschieben
    # Division durch L reduziert die Signalamplitude auf physikalisch sinnvolle Werte.
    spectrum_raw = fft(y_eq / L*apo)
    spectrum_shifted = fftshift(spectrum_raw)
    spectrum_abs = np.abs(spectrum_shifted)

    return freq_axis, spectrum_abs

freq_green, spec_laser_green = fft_spectrum(x_eq, y_eq_laser, laser_slope)

path_jod = f"data/{dataset}/Data Channel 0.dat"
pos_jod, meas_jod = load_data(path_jod)
mean_jod = average_measurements(meas_jod)
# Interpolation auf das neue Gitter
f_int_jod = make_interp_spline(x_korr, mean_jod, k=3)
y_eq_jod = f_int_jod(x_eq)

freq_jod, spec_jod = fft_spectrum(x_eq, y_eq_jod, laser_slope)


