import numpy as np

file_lon = "Data/HS1 Tag 1/FITS/20260907-133042_TPI-CSCAN_LON-VIRA_03#_01#_t1.txt"
file_lat = "Data/HS1 Tag 1/FITS/20260907-133622_TPI-CSCAN_LAT-VIRA_03#_02#_t1.txt"
data_lon = np.loadtxt(file_lon, skiprows=3)
data_lat = np.loadtxt(file_lat, skiprows=3)

filepath="Data/HS1 Tag 1/onoff/sun_onoff_final.txt"
data = np.loadtxt(filepath, skiprows=1, usecols=(1,2,3))

data_l = data[:5]
data_r = data[5:]
P_off_l = data_l[:,1]
P_off_l_mean = np.mean(P_off_l)
P_off_r = data_r[:,1]
P_off_r_mean = np.mean(P_off_r)

# data Lat
data_lat_el = data_lat[:,0]
data_lat_l = data_lat[:,1]
data_lat_r = data_lat[:,2]
# data Lon
data_lon_az = data_lon[:,0]
data_lon_l = data_lon[:,1]
data_lon_r = data_lon[:,2]

# T_sys berechnet aus Sonnendaten (on_off) + errors
T_sys_l  = 98.76 #K
T_sys_l_err = 2.54 #K
T_sys_r = 107.80 #K
T_sys_r_err = 31.65 #K

# normierung über t_sys (is that right??)
# aber nicht in K, sonder counts/K
#lat
data_lat_l_n = data_lat_l*T_sys_l / P_off_l_mean
data_lat_r_n = data_lat_r*T_sys_r / P_off_r_mean
#lon
data_lon_l_n = data_lon_l*T_sys_l / P_off_l_mean
data_lon_r_n = data_lon_r*T_sys_r / P_off_r_mean

# Fehlerbalken
sigma_lat_l = np.std(data_lat_l_n[2:13])
sigma_lat_r = np.std(data_lat_r_n[2:13])
sigma_lon_l = np.std(data_lon_l_n[2:13])
sigma_lon_r = np.std(data_lon_r_n[2:13])

sigma_data = np.column_stack((sigma_lat_l, sigma_lat_r, sigma_lon_l, sigma_lon_r))
filepath="Auswertung HS1/angular resolution/sigma_l_r_background"
np.savetxt(
    filepath,
    sigma_data,
    header="lat_l lat_r lon_l lon_r",
    comments="",
    fmt=["%.3f", "%.3f", "%.3f", "%.3f"]
)

#PLOT
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# T'_sys als Funktion der Elevation
axes[0].errorbar(data_lat_el, data_lat_l_n, yerr=sigma_lat_l, fmt="o-", capsize=3, label="left circular polarisation")
axes[0].errorbar(data_lat_el, data_lat_r_n, yerr=sigma_lat_r, fmt="o-", capsize=3, label="right circular polarisation")

axes[0].set_xlabel("Elevation [deg]")
axes[0].set_ylabel(r"$T_{h_n} = TPI \cdot T'_{\mathrm{sys}} / \overline{P_{off}}$ [K]")
axes[0].set_title(r"$T_{h_n}$ as a function of elevation")
axes[0].set_ylim(75,300)
axes[0].grid(True)
axes[0].legend()

# T'_sys als Funktion des Azimuts
axes[1].errorbar(data_lon_az, data_lon_l_n, yerr=sigma_lon_l, fmt="o-", capsize=3, label="left circular polarisation")
axes[1].errorbar(data_lon_az, data_lon_r_n, yerr=sigma_lon_r, fmt="o-", capsize=3, label="right circular polarisation")

axes[1].set_xlabel("Azimuth [deg]")
axes[1].set_ylabel(r"$T_{h_n} = TPI \cdot T'_{\mathrm{sys}} / \overline{P_{off}}$ [K]")
axes[1].set_title(r"$T_{h_n}$ as a function of azimuth")
axes[1].set_ylim(75,300)
axes[1].grid(True)
axes[1].legend()

plt.tight_layout()
plt.show()

# extrapolation of elevation
# nur niedrige Elevationen für die Extrapolation verwenden
low_elevation = data_lat_el <= 16

# lineare Fits für beide Polarisationen
fit_l = np.polyfit(data_lat_el[low_elevation], data_lat_l_n[low_elevation], 1)
fit_r = np.polyfit(data_lat_el[low_elevation], data_lat_r_n[low_elevation], 1)

# Werte bei Elevation 0 Grad
T_h_l_0 = np.polyval(fit_l, 0)
T_h_r_0 = np.polyval(fit_r, 0)

# Referenzwert bei hoher Elevation, z. B. 50 Grad
T_h_l_ref = np.mean(data_lat_l_n[data_lat_el >= 40])
T_h_r_ref = np.mean(data_lat_r_n[data_lat_el >= 40])

increase_l = T_h_l_0 - T_h_l_ref
increase_r = T_h_r_0 - T_h_r_ref

print(f"T'_h,left(0°)  = {T_h_l_0:.2f}")
print(f"T'_h,right(0°) = {T_h_r_0:.2f}")
print(f"Increase left  = {increase_l:.2f}")
print(f"Increase right = {increase_r:.2f}")

plt.figure(figsize=(7, 5))

plt.errorbar(data_lat_el, data_lat_l_n, yerr=sigma_lat_l, fmt="o-", capsize=3, label="left")
plt.errorbar(data_lat_el, data_lat_r_n, yerr=sigma_lat_r, fmt="o-", capsize=3, label="right")

elevation_fit = np.linspace(0, max(data_lat_el), 200)
plt.plot(elevation_fit,np.polyval(fit_l, elevation_fit),"--",label="linear fit, left")
plt.plot(elevation_fit,np.polyval(fit_r, elevation_fit),"--",label="linear fit, right")

plt.scatter(0, T_h_l_0, marker="x", s=80)
plt.scatter(0, T_h_r_0, marker="x", s=80)
plt.xlim(0,45)
plt.ylim(0,700)

plt.xlabel("Elevation [deg]")
plt.ylabel(r"$T'_h [K]$")
plt.title(r"Extrapolation of $T'_h$ to $0^\circ$")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
