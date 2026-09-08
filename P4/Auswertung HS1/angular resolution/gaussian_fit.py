import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x=[]
y_lon_l=[]
y_lon_r=[]
y_lat_l=[]
y_lat_r=[]
sigma_y = []
filename_1 = sys.argv[1]
filename_2 = sys.argv[2]

# open Lon data
with open(filename_1) as inf:
    for line in inf:
        if not line.startswith('#'):
            parts= line.split()
            x.append(float(parts[0]))
            y_lon_l.append(float(parts[1]))
            y_lon_r.append(float(parts[2]))

# open Lat data
with open(filename_2) as inf:
    for line in inf:
        if not line.startswith('#'):
            parts= line.split()
            x.append(float(parts[0]))
            y_lat_l.append(float(parts[1]))
            y_lat_r.append(float(parts[2]))

# Calibration
filepath="/Users/leonielanz/Library/CloudStorage/OneDrive-Persönlich/Anwendungen/remotely-save/Studium/F-Prak/F-Prak/P4/Data/HS1 Tag 1/onoff/sun_onoff_final.txt"
data = np.loadtxt(filepath, skiprows=1, usecols=(1,2,3))
data_l = data[:5]
data_r = data[5:]
P_off_l = data_l[:,1]
P_off_l_mean = np.mean(P_off_l)
P_off_r = data_r[:,1]
P_off_r_mean = np.mean(P_off_r)

# gaussian model
def f(x, amplitude, sigma, offset):
    return offset + amplitude * np.exp(-x**2 / (2 * sigma**2))

T_A_sun = 972.753  # K

# normierung über T_A_sun + sigma
y_l = np.asarray(y_l)*T_A_sun / (P_off_l_mean * 10)
print(y_l)
y_r = np.asarray(y_r)*T_A_sun / (P_off_r_mean * 10)
sigma_y_l = np.std(y_l)
sigma_y_r = np.std(y_r)

# fit parameter
popt_l, pcov_l = curve_fit(f, np.asarray(x), y_l, p0=[max(y_l), 1.0, min(y_l)], sigma=sigma_y_l, absolute_sigma=True)
popt_r, pcov_r = curve_fit(f, np.asarray(x), y_r, p0=[max(y_r), 1.0, min(y_r)], sigma=sigma_y_r, absolute_sigma=True)

amplitude_lat, sigma_lat, offset_lat = popt_l
amplitude_lon, sigma_lon, offset_lon = popt_r

sigma_lat_err = np.sqrt(pcov_l[1, 1])
sigma_lon_err = np.sqrt(pcov_r[1, 1])

fwhm_lat = 2 * np.sqrt(2 * np.log(2)) * sigma_lat
fwhm_lat_err = 2 * np.sqrt(2 * np.log(2)) * sigma_lat_err

fwhm_lon = 2 * np.sqrt(2 * np.log(2)) * sigma_lon
fwhm_lon_err = 2 * np.sqrt(2 * np.log(2)) * sigma_lon_err

ELV = 42 #in deg at time of recording der sonne
#ELV = 47 + 56 / 60 + 18 / 3600 #für virA
correction = np.cos(np.deg2rad(ELV))

fwhm_lon_corrected = fwhm_lon * correction
fwhm_lon_corrected_err = fwhm_lon_err * correction

x_model = np.linspace(min(x), max(x), 100)
model_plot = f(x_model, amplitude_lat, sigma_lat, offset_lat)

# plot fwhm
half_max = offset_lat + amplitude_lat / 2

plt.axhline(half_max, color="gray", linestyle="--", label=f"FWHM = {fwhm_lat:.2f}°")
plt.axvline(-fwhm_lat / 2, color="blue", linestyle=":")
plt.axvline(fwhm_lat / 2, color="blue", linestyle=":")

# plot fit + daten (mit errors)
plt.errorbar(x, y_l, yerr=sigma_y_l, fmt="o", color="r", markersize=5, capsize=2.5, label="Messwerte")
plt.plot(x_model, model_plot, label=fr"Fit: $\sigma = {sigma_lat:.2f} \pm {sigma_lat_err:.2f}$")

plt.xlabel("Angle [°]")
plt.ylabel("Relative intensity")
plt.legend()
plt.tight_layout()
plt.show()
