import numpy as np
from scipy.constants import k

filepath="Data/HS1 Tag 1/onoff/sun_onoff_final.txt"
data = np.loadtxt(filepath, skiprows=1, usecols=(1,2,3))

data_left = data[:5]
data_right = data[5:]

P_on_left = data_left[:,0]
P_off_left = data_left[:,1]
P_cal_left = data_left[:,2]

P_on_right = data_right[:,0]
P_off_right = data_right[:,1]
P_cal_right = data_right[:,2]

P_on_left_mean = np.mean(P_on_left)
P_off_left_mean = np.mean(P_off_left)
P_cal_left_mean = np.mean(P_cal_left)

P_on_right_mean = np.mean(P_on_right)
P_off_right_mean = np.mean(P_off_right)
P_cal_right_mean = np.mean(P_cal_right)

P_on_left_std = np.std(P_on_left, ddof=1)
P_off_left_std = np.std(P_off_left, ddof=1)
P_cal_left_std = np.std(P_cal_left, ddof=1)

P_on_right_std = np.std(P_on_right, ddof=1)
P_off_right_std = np.std(P_off_right, ddof=1)
P_cal_right_std = np.std(P_cal_right, ddof=1)

print(f"P_on_left_mean  = {P_on_left_mean:.2f} ± {P_on_left_std:.2f}")
print(f"P_off_left_mean = {P_off_left_mean:.2f} ± {P_off_left_std:.2f}")
print(f"P_cal_left_mean = {P_cal_left_mean:.2f} ± {P_cal_left_std:.2f}")

print(f"P_on_right_mean  = {P_on_right_mean:.2f} ± {P_on_right_std:.2f}")
print(f"P_off_right_mean = {P_off_right_mean:.2f} ± {P_off_right_std:.2f}")
print(f"P_cal_right_mean = {P_cal_right_mean:.2f} ± {P_cal_right_std:.2f}")

T_cal = 170 #K
T_sys_left = T_cal * P_off_left_mean / (P_cal_left_mean - P_off_left_mean)
T_sys_right = T_cal * P_off_right_mean / (P_cal_right_mean - P_off_right_mean)

T_sun_left = T_sys_left * (P_on_left_mean - P_off_left_mean) / P_off_left_mean
T_sun_right = T_sys_right * (P_on_right_mean - P_off_right_mean) / P_off_right_mean

def temperatur_mit_std(P_on, P_off, P_cal, T_cal=170):
    on = np.mean(P_on)
    off = np.mean(P_off)
    cal = np.mean(P_cal)

    on_std = np.std(P_on, ddof=1) / np.sqrt(len(P_on))
    off_std = np.std(P_off, ddof=1) / np.sqrt(len(P_off))
    cal_std = np.std(P_cal, ddof=1) / np.sqrt(len(P_cal))

    denominator = cal - off

    T_sys = T_cal * off / denominator

    T_sys_std = np.sqrt(
        (T_cal * cal / denominator**2 * off_std)**2
        + (T_cal * off / denominator**2 * cal_std)**2
    )

    return T_sys, T_sys_std

T_sys_left, T_sys_left_std= temperatur_mit_std(
    P_on_left, P_off_left, P_cal_left
)

T_sys_right, T_sys_right_std = temperatur_mit_std(
    P_on_right, P_off_right, P_cal_right
)

print(f"T_sys_left  = {T_sys_left:.2f} ± {T_sys_left_std:.2f} K")
print(f"T_sys_right = {T_sys_right:.2f} ± {T_sys_right_std:.2f} K")

def antenna_temperature(P_on, P_off, P_cal, T_cal=170):
    # Systemtemperatur für jedes BBC
    T_sys_bbc = T_cal * P_off / (P_cal - P_off)

    # Antennentemperatur der Sonne für jedes BBC
    T_sun_bbc = T_sys_bbc * (P_on - P_off) / P_off

    # Mittelwert und Standardabweichung
    T_sun_mean = np.mean(T_sun_bbc)
    T_sun_std = np.std(T_sun_bbc, ddof=1)

    return T_sys_bbc, T_sun_bbc, T_sun_mean, T_sun_std

T_sys_left_bbc, T_sun_left_bbc, T_sun_left_mean, T_sun_left_std = antenna_temperature(P_on_left, P_off_left, P_cal_left)
T_sys_right_bbc, T_sun_right_bbc, T_sun_right_mean, T_sun_right_std = antenna_temperature(P_on_right, P_off_right, P_cal_right)

print(f"T_sun_left  = {T_sun_left_mean:.2f} +- {T_sun_left_std:.2f} K")
print(f"T_sun_right = {T_sun_right_mean:.2f} +- {T_sun_right_std:.2f} K")

# Antennentemp Theorie
S_nu=76e-22
A_e=1.125*np.pi
k_B= k
T_A = S_nu*A_e/(2*k_B)

print(f"T_A = {T_A:.3f} K")