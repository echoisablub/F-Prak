import numpy as np

file_lon = "Data/HS1 Tag 1/FITS/20260907-133042_TPI-CSCAN_LON-VIRA_03#_01#_t1.txt"
file_lat = "Data/HS1 Tag 1/FITS/20260907-133622_TPI-CSCAN_LAT-VIRA_03#_02#_t1.txt"
data_lon = np.loadtxt(file_lon, skiprows=3)
data_lat = np.loadtxt(file_lat, skiprows=3)

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
#lat
data_lat_l_n = data_lat_l/T_sys_l
data_lat_r_n = data_lat_r/T_sys_r
#lon
data_lon_l_n = data_lon_l/T_sys_l
data_lon_r_n = data_lon_r/T_sys_r

# big ?
'''T_sys_lat_l_eff = T_sys_l - data_lat_l_n
T_sys_lat_r_eff = T_sys_r - data_lat_r_n
T_sys_lon_l_eff = T_sys_l - data_lon_l_n
T_sys_lon_r_eff = T_sys_r - data_lon_r_n'''

#PLOT
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# T'_sys als Funktion der Elevation
axes[0].plot(data_lat_el, data_lat_l_n, "o-", label="linke Polarisation")
axes[0].plot(data_lat_el, data_lat_r_n, "o-", label="rechte Polarisation")

axes[0].set_xlabel("Elevation [deg]")
axes[0].set_ylabel(r"$T'_{h_n} = P/T_'{\mathrm{sys}}$")
axes[0].set_title(r"$T'_{h_n}$ als Funktion der Elevation")
axes[0].set_ylim(5,35)
axes[0].grid(True)
axes[0].legend()

# T'_sys als Funktion des Azimuts
axes[1].plot(data_lon_az, data_lon_l_n, "o-", label="linke Polarisation")
axes[1].plot(data_lon_az, data_lon_r_n, "o-", label="rechte Polarisation")

axes[1].set_xlabel("Azimut [deg]")
axes[1].set_ylabel(r"$T'_{h_n} = P/T_'{\mathrm{sys}}$")
axes[1].set_title(r"$T'_{h_n}$ als Funktion des Azimuts")
axes[1].set_ylim(5,35)
axes[1].grid(True)
axes[1].legend()

plt.tight_layout()
plt.show()


