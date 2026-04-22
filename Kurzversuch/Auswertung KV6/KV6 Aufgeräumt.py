import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline,make_interp_spline
from scipy.stats import linregress
from scipy.signal import argrelextrema
from scipy.signal import find_peaks, savgol_filter
from scipy.constants import c
from scipy.fft import fft, fftshift


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
    peaks = argrelextrema(y, np.greater)[0]
    troughs = argrelextrema(y, np.less)[0]
    extrema_list = []
    for i, j in zip(peaks, troughs):
        extrema_list.append(i)
        extrema_list.append(j)

    extrema_array=np.array(extrema_list)

    return extrema_array, peaks

    # Laser-Signal glätten vor der Peak-Suche
    # smooth_laser = savgol_filter(mean_data_laser, window_length=51, polyorder=3)
    # Robuste Peaks finden (nur die großen Maxima der Laser-Fringes)
    # peaks, _ = find_peaks(smooth_laser, distance=50, prominence=0.01)


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
    _, extrema_array = find_extrema(y_new)
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

    return delta_interpolate, fit.slope

def find_extrema_robust(y, prominence=0.01, distance=20):
    """
    Findet Maxima und Minima robust gegenüber Rauschen.
    """
    # Maxima finden
    peaks, _ = find_peaks(y, prominence=prominence, distance=distance)
    # Minima finden (durch Invertieren des Signals)
    troughs, _ = find_peaks(-y, prominence=prominence, distance=distance)
    
    # Kombinieren und sortieren
    extrema = np.sort(np.concatenate((peaks, troughs)))
    return extrema

def korrekturfunktion_neu(data_name):
    # 1. Laser-Daten laden (Kanal 2)
    file_path = f"data/{data_name}/Data Channel 2.dat"
    positions, measurements = load_data(file_path)
    mean_data_laser = average_measurements(measurements)
    
    # 2. Glättung des Laser-Signals (entscheidend gegen Rauschen)
    # (Hinweis: savgol_filter ist eine externe Funktion aus scipy.signal)
    smooth_laser = savgol_filter(mean_data_laser, window_length=51, polyorder=3)
    
    # 3. Robuste Extrema finden
    extrema_indices = find_extrema_robust(smooth_laser)
    pos_extrema = positions[extrema_indices]
    
    # 4. Fit der Extrema zur Bestimmung der laser_slope
    r, fit = linear_fit(extrema_indices)
    laser_slope = fit.slope
    
    # 5. Delta-Berechnung für die Ortskorrektur
    # Theoretische (lineare) Positionen vs. reale Peak-Positionen
    theoretical_pos = fit.intercept + fit.slope * r
    deltas = theoretical_pos - pos_extrema
    
    # 6. Kontinuierliche Korrekturfunktion via Spline
    # 's' glättet den Spline zusätzlich
    delta_func = UnivariateSpline(pos_extrema, deltas, s=1.0)
    
    return delta_func, laser_slope

def ortskorrektur(positions, values, delta_interpolate):
    # Ursprüngliche Achse korrigieren
    x_korr = positions + delta_interpolate(positions)
    
    # Erzeugen eines äquidistanten Gitters für die FFT
    x_eq = np.linspace(x_korr.min(), x_korr.max(), len(x_korr))
    
    # Erneute Interpolation auf das neue Gitter
    f_int = make_interp_spline(x_korr, values, k=3)
    # f_int = UnivariateSpline(x_korr, values, k=3)
    y_eq = f_int(x_eq)
    # y_eq = np.interp(x_eq, x_korr, values)

    return x_eq, y_eq

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
    delta_s = (x_eq * 532e-9) / laser_slope
    delta_t_axis = delta_s / c

    # Sampling-Parameter für die FFT
    # Wir benötigen das Zeitintervall T_sampl als Skalar für die Frequenzachse.
    L = len(delta_t_axis)
    t_range = np.max(delta_t_axis) - np.min(delta_t_axis)
    
    # Tsampl oft in Ts angegeben (Faktor 1e12), um handliche Frequenzwerte zu erhalten.
    T_sampl = (t_range / L) * 1e12 
    f_max = 1 / T_sampl
    f_ny = f_max / 2
    
    # Frequenzachse erzeugen
    # Die FFT liefert ein symmetrisches Signal um die Frequenz 0.
    freq_axis = np.linspace(-f_ny, f_ny, L)

    # FFT berechnen und verschieben
    # Division durch L reduziert die Signalamplitude auf physikalisch sinnvolle Werte.
    spectrum_raw = fft(y_eq / L)
    spectrum_shifted = fftshift(spectrum_raw)
    spectrum_abs = np.abs(spectrum_shifted)

    return freq_axis, spectrum_abs

def plot_final_results(freq, spec_ref, spec_probe, label_probe="Iod 2"):
    # 1. Vorbereitung: Nur positive Frequenzen betrachten (FFT ist symmetrisch)
    # Da freq von -f_nyquist bis +f_nyquist läuft, nehmen wir nur die rechte Hälfte
    mask = freq > 0
    f_pos = freq[mask]
    s_ref_pos = spec_ref[mask]
    s_probe_pos = spec_probe[mask]

    # PLOT 1: FREQUENZSPEKTRUM
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(f_pos, s_ref_pos / np.max(s_ref_pos), label="Referenz (normiert)", color="gray", alpha=0.5)
    plt.plot(f_pos, s_probe_pos / np.max(s_ref_pos), label=f"{label_probe} (normiert)", color="darkred")
    plt.xlabel("Frequenz $f$ [THz]")
    plt.ylabel("Spektrale Energiedichte $W(f)$")
    plt.title("Iod Spektrum im Frequenzraum")
    plt.xlim(350, 750) # Bereich für sichtbares Licht (ca. 0.35 - 0.75 PHz) [2]
    plt.ylim(0, 0.0005)
    plt.legend()
    plt.grid(True)

    # UMRECHNUNG IN WELLENLÄNGE UND NEU-ÄQUIDISTANZEN
    # Formel: lambda = c / f. Da f in THz (1e12 Hz) vorliegt:
    # lambda [nm] = (c [m/s] / (f [THz] * 1e12)) * 1e9 [nm/m]
    wl_raw = (c / (f_pos)) * 1e-3
    wl_equi = np.linspace(400, 800, 5000) # 400nm bis 800nm [3]
    
    # Interpolation der Spektren auf das neue Wellenlängen-Gitter
    f_interp_ref = make_interp_spline(wl_raw[::-1], s_ref_pos[::-1], k=3)
    f_interp_probe = make_interp_spline(wl_raw[::-1], s_probe_pos[::-1], k=3)
    #f_interp_ref = UnivariateSpline(wl_raw[::-1], s_ref_pos[::-1], k=3, s=0)
    #f_interp_probe = UnivariateSpline(wl_raw[::-1], s_probe_pos[::-1], k=3, s=0)


    s_ref_wl = f_interp_ref(wl_equi)
    s_probe_wl = f_interp_probe(wl_equi)

    # PLOT 2: WELLENLÄNGENSPEKTRUM
    plt.subplot(1, 2, 2)
    plt.plot(wl_equi, s_ref_wl / np.max(s_ref_wl), label="Referenz", color="gray", alpha=0.5)
    plt.plot(wl_equi, s_probe_wl / np.max(s_ref_wl), label=label_probe, color="blue")
    plt.xlabel("Wellenlänge $\lambda$ [nm]")
    plt.ylabel("Amplitude")
    plt.title("Wellenlängenspektren - Iod")
    plt.xlim(400, 800)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # BERECHNUNG DER OPTISCHEN DICHTE (OD)
    epsilon = 1e-10 # Vermeidung DivByZero
    od = -np.log10((s_probe_wl + epsilon) / (s_ref_wl + epsilon))
    
    plt.figure(figsize=(10, 4))
    plt.plot(wl_equi, od, color="green")
    plt.xlabel("Wellenlänge $\lambda$ [nm]")
    plt.ylabel("Optische Dichte (OD)")
    plt.title(f"Absorptionsprofil: {label_probe} (OD)")
    plt.xlim(500, 700) # Fokus auf Iod-Übergänge
    plt.ylim(0,0.7)
    plt.grid(True)
    plt.show()
    
def plot_filter_analysis(freq, spec_ref, spec_filt):
    # Nur positive Frequenzen (Sichtbarer Bereich ca. 400-800 THz)
    mask = freq > 0
    f_pos = freq[mask]
    s_ref = spec_ref[mask]
    s_filt = spec_filt[mask]

    # PLOT 1: FREQUENZSPEKTRUM
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plt.plot(f_pos, s_ref / np.max(s_ref), label="Weißlicht (Ref)", color="gray")
    plt.plot(f_pos, s_filt / np.max(s_ref), label="Filter 2", color="orange")
    plt.xlabel("Frequenz $f$ [THz]")
    plt.ylabel("Normierte Intensität")
    plt.title("Spektren im Frequenzraum")
    plt.xlim(350, 750)
    plt.ylim(0, 0.0008)
    plt.legend()
    plt.grid(True)

    # 2. WELLENLÄNGEN-TRANSFORMATION & INTERPOLATION
    # Umrechnung: lambda = c / f
    wl_raw_filt = (c / (f_pos * 1e12)) * 1e9
    wl_equi_filt = np.linspace(400, 800, 5000) # Neues äquidistantes nm-Gitter
    print(len(wl_raw_filt))
    
    interp_ref = make_interp_spline(wl_raw_filt[::-1], s_ref[::-1], k=3)
    interp_filt = make_interp_spline(wl_raw_filt[::-1], s_filt[::-1], k=3)    
    #interp_ref = UnivariateSpline(wl_raw[::-1], s_ref[::-1], k=3, s=0)
    #interp_filt = UnivariateSpline(wl_raw[::-1], s_filt[::-1], k=3, s=0)
    
    s_ref_nm = interp_ref(wl_equi_filt)
    s_filt_nm = interp_filt(wl_equi_filt)

    # PLOT 2: ÄQUIDISTANTES WELLENLÄNGENSPEKTRUM
    plt.subplot(1, 2, 2)
    plt.plot(wl_equi_filt, s_ref_nm / np.max(s_ref_nm), label="Weißlicht (Ref)", color="gray")
    plt.plot(wl_equi_filt, s_filt_nm / np.max(s_ref_nm), label="Filter 2", color="blue")
    plt.xlabel("Wellenlänge $\lambda$ [nm]")
    plt.ylabel("Intensität")
    plt.title("Äquidistante Wellenlängenspektren")
    plt.xlim(400, 800)
    plt.legend()
    plt.grid(True)
    plt.show()

    # DIFFERENTIELLE TRANSMISSION (DOT)
    # Formel: (I - I0) / I0
    dot = (s_filt_nm - s_ref_nm) / (s_ref_nm + 1e-10)
    
    plt.figure(figsize=(10, 4))
    plt.plot(wl_equi_filt, dot, color="darkorange", lw=1.5)
    plt.axhline(0, color='black', linestyle='--')
    plt.xlabel("Wellenlänge $\lambda$ [nm]")
    plt.ylabel("DOT")
    plt.title("Differentielle Transmission des Filters (2)")
    plt.xlim(450, 650) # Fokus auf den Absorptionsbereich des Filters
    plt.ylim(-1,1)
    plt.grid(True)
    plt.show()

dataset = "Iod 2"
dataset_filter= "Filter 2"

# Korrekturfunktion für Datensatz
delta_func, laser_slope = korrekturfunktion(dataset)
delta_func_filt, slope_filt = korrekturfunktion(dataset_filter)

# Grüner Laser (Kanal 2)
path_laser_green = f"data/{dataset}/Data Channel 2.dat"
pos_laser_green, meas_laser_green = load_data(path_laser_green)
mean_laser_green = average_measurements(meas_laser_green)
x_eq_green, y_eq_green = ortskorrektur(pos_laser_green, mean_laser_green, delta_func)

# JOD-PROBE (Kanal 0)
path_jod = f"data/{dataset}/Data Channel 0.dat"
pos_jod, meas_jod = load_data(path_jod)
mean_jod = average_measurements(meas_jod)
x_final, y_jod_final = ortskorrektur(pos_jod, mean_jod, delta_func)

# REFERENZ (Kanal 1)
path_ref = f"data/{dataset}/Data Channel 1.dat"
pos_ref, meas_ref = load_data(path_ref)
mean_ref = average_measurements(meas_ref)
x_final, y_ref_final = ortskorrektur(pos_ref, mean_ref, delta_func)

# FILTER-DATEN laden (Kanal 0)
path_filt = f"data/{dataset_filter}/Data Channel 0.dat"
pos_filt, meas_filt = load_data(path_filt)
mean_filt = average_measurements(meas_filt)
x_final_f, y_filt_corr = ortskorrektur(pos_filt, mean_filt, delta_func_filt)

# REFERENZ-DATEN laden (Kanal 1)
path_ref_filt = f"data/{dataset_filter}/Data Channel 1.dat"
pos_ref_f, meas_ref_f = load_data(path_ref_filt)
mean_ref_f = average_measurements(meas_ref_f)
x_final_f, y_ref_f_corr = ortskorrektur(pos_ref_f, mean_ref_f, delta_func_filt)

# FFT BERECHNEN
freq_green, spec_laser_green = fft_spectrum(x_eq_green, y_eq_green, laser_slope)
freq, spec_ref = fft_spectrum(x_final, y_ref_final, laser_slope)
freq, spec_jod = fft_spectrum(x_final, y_jod_final, laser_slope)
freq_f, spec_ref_f = fft_spectrum(x_final_f, y_ref_f_corr, slope_filt)
freq_f, spec_filt_f = fft_spectrum(x_final_f, y_filt_corr, slope_filt)

# Plots
plot_final_results(freq, spec_ref, spec_jod, label_probe="Iod-Küvette")
plot_filter_analysis(freq_f, spec_ref_f, spec_filt_f)
#plot_laser_green_analysis(freq_green, spec_laser_green)

# Stuff ausprobieren
def plot_laser_green_analysis(freq_green, spec_laser_green):
    mask = freq_green > 0
    f_pos = freq_green[mask]
    s_laser_pos = spec_laser_green[mask]

    # Plotten
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plt.plot(f_pos, s_laser_pos/np.max(s_laser_pos), color='green', label="Spektrum Grüner Laser")
    plt.xlabel("Frequenz [THz]")
    plt.ylabel("Intensität [a.u.]")
    plt.title("Laserspektrum (Channel 2)")
    plt.xlim(540,590)
    plt.ylim(0,0.4)
    plt.grid(True)
    plt.legend()

    # Umrechnung: Frequenz (Hz) -> Wellenlänge (nm)
    lambda_green_nm = (c / f_pos) * 1e-3
    # wl_equi_green = np.linspace(400, 800, 5000) # Neues äquidistantes nm-Gitter
    # interp_laser_green = make_interp_spline(lambda_green_nm[::-1], s_laser_pos[::-1], k=3)    
    #interp_laser_green = UnivariateSpline(lambda_green_nm[::-1], s_laser_pos[::-1], k=3, s=0)
    # s_green_nm = interp_laser_green(wl_equi_green)

    # Plotten des Spektrums um 532 nm
    plt.subplot(1, 2, 2)
    plt.plot(lambda_green_nm, s_laser_pos/np.max(s_laser_pos), color='green', label="Laser-Referenz (532 nm)")
    plt.xlabel("Wellenlänge [nm]")
    plt.ylabel("Intensität [a.u.]")
    plt.title(f"Wellenlängenspektrum des grünen Lasers ({dataset})")
    plt.xlim(510, 555)  # Zoom auf den Bereich um 532 nm
    plt.ylim(0,0.4)
    plt.grid(True)
    plt.legend()
    plt.show()

plot_laser_green_analysis(freq_green, spec_laser_green)