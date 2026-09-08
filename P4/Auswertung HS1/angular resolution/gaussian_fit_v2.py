import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


filename_lon = sys.argv[1]
filename_lat = sys.argv[2]


def read_scan(filename):
    data = np.loadtxt(filename, skiprows=3)
    angle = data[:, 0]
    left = data[:, 1]
    right = data[:, 2]
    return angle, left, right


x_lon, y_lon_l, y_lon_r = read_scan(filename_lon)
x_lat, y_lat_l, y_lat_r = read_scan(filename_lat)


# Kalibrierungsdaten für Normierung
calibration_file = ("/Users/leonielanz/Library/CloudStorage/OneDrive-Persönlich/Anwendungen/remotely-save/Studium/F-Prak/F-Prak/P4/Data/HS1 Tag 1/onoff/sun_onoff_final.txt")
data = np.loadtxt(calibration_file, skiprows=1, usecols=(1, 2, 3))
data_l = data[:5]
data_r = data[5:]
P_off_l_mean = np.mean(data_l[:, 1])
P_off_r_mean = np.mean(data_r[:, 1])

# Normierung auf die Sonnen-Antennentemperatur
T_A_sun = 972.753  # K
y_lon_l = y_lon_l * T_A_sun / (P_off_l_mean * 10)
y_lon_r = y_lon_r * T_A_sun / (P_off_r_mean * 10)

y_lat_l = y_lat_l * T_A_sun / (P_off_l_mean * 10)
y_lat_r = y_lat_r * T_A_sun / (P_off_r_mean * 10)


def gaussian(angle, amplitude, sigma, offset):
    return offset + amplitude * np.exp(-angle**2 / (2 * sigma**2))

def fit_scan(angle, signal):
    signal_error = np.std(signal)

    parameters, covariance = curve_fit(
        gaussian,
        angle,
        signal,
        p0=[
            max(signal) - min(signal),
            1.0,
            min(signal)
        ],
        sigma=signal_error,
        absolute_sigma=True
    )

    amplitude, sigma, offset = parameters
    sigma_error = np.sqrt(covariance[1, 1])

    fwhm = 2 * np.sqrt(2 * np.log(2)) * sigma
    fwhm_error = 2 * np.sqrt(2 * np.log(2)) * sigma_error

    return parameters, fwhm, fwhm_error

fit_lon_l, fwhm_lon_l, fwhm_lon_l_error = fit_scan(x_lon, y_lon_l)
fit_lon_r, fwhm_lon_r, fwhm_lon_r_error = fit_scan(x_lon, y_lon_r)
fit_lat_l, fwhm_lat_l, fwhm_lat_l_error = fit_scan(x_lat, y_lat_l)
fit_lat_r, fwhm_lat_r, fwhm_lat_r_error = fit_scan(x_lat, y_lat_r)

# Korrektur des Longitude-Winkels
ELV = 42.0
correction = np.cos(np.deg2rad(ELV))
fwhm_lon_l_corrected = fwhm_lon_l * correction
fwhm_lon_r_corrected = fwhm_lon_r * correction
fwhm_lon_l_corrected_error = fwhm_lon_l_error * correction
fwhm_lon_r_corrected_error = fwhm_lon_r_error * correction

# Plot
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

def plot_scan(axis, angle, signal, parameters, fwhm, label):
    amplitude, sigma, offset = parameters
    angle_model = np.linspace(angle.min(), angle.max(), 300)
    signal_model = gaussian(angle_model, *parameters)

    half_max = offset + amplitude / 2

    axis.errorbar(
        angle,
        signal,
        yerr=np.std(signal),
        fmt="o",
        color="red",
        capsize=2,
        label=label
    )

    axis.plot(
        angle_model,
        signal_model,
        color="black",
        label=fr"Fit, FWHM = {fwhm:.2f} deg"
    )

    axis.axhline(
        half_max,
        color="gray",
        linestyle="--",
        label="Half maximum"
    )

    axis.set_xlabel("Winkel [deg]")
    axis.set_ylabel(r"$T_A$ [K]")
    axis.grid(True)
    axis.legend()


'''plot_scan(
    axes[0],
    x_lon,
    y_lon_l,
    fit_lon_l,
    fwhm_lon_l_corrected,
    label="Left polarised longitude scan"
)

plot_scan(
    axes[1],
    x_lat,
    y_lat_l,
    fit_lat_l,
    fwhm_lat_l,
    label="Left polarised latitude scan"
)'''

plot_scan(
    axes[0],
    x_lon,
    y_lon_r,
    fit_lon_r,
    fwhm_lon_r_corrected,
    label="Right polarised longitude scan"
)

plot_scan(
    axes[1],
    x_lat,
    y_lat_r,
    fit_lat_r,
    fwhm_lat_r,
    label="Right polarised latitude scan"
)

axes[0].set_title("Longitude")
axes[1].set_title("Latitude")

plt.tight_layout()
plt.show()

# python3 gaussian_fit_v2.py 20260907-104625_TPI-CSCAN_LON-SUN_01#_01#_t1.txt 20260907-105053_TPI-CSCAN_LAT-SUN_01#_02#_t1.txt