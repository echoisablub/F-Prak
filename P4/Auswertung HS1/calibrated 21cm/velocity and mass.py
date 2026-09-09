import numpy as np
import matplotlib.pyplot as plt

filepath="Auswertung HS1/calibrated 21cm/cm21_tab.txt"
data = np.loadtxt(filepath, skiprows=1)
l = data[:,0]
R = data[:,1]
R_err = data[:,2]
v_max = data[:,3]
v_max_err = data[:,4]

R_0 = 8.5 #kpc
omeg_0 = 220/R_0 #s-1 w\e-16
M_sun = 1.98e30 #kg

v_R = []
v_R_err = []
M_R = []
M_R_err = []
v_d = []
v_d_err = []
M_d = []
M_d_err = []
M_dm = []
M_dm_err = []

for i in range(len(l)):
    # velocity (radian)
    v_R_i = v_max[i] + omeg_0 * R[i] #R = R_0 * np.sin(l) R=[kpc] v_R=[kms-1]
    # v_R_i = v_max[i] + 220 * np.sin([l])
    v_R_err_i = np.sqrt(v_max_err[i]**2 + R_err[i]**2)

    # mass (in solar masses)
    M_R_i = 0.234e10 * (v_R_i / 100)**2 * R[i] #in Sonnenmassen (M_sun = 1.98e30 kg)
    # M_R_err_i = np.sqrt(2*234e6 * v_R_i * R[i] * v_R_err_i**2 + 0.234e10 * (v_R_i / 100)**2 * R_err[i]**2)
    M_R_err_i = 2*v_R_err_i/v_R_i * M_R_i

    # baryonic velocity
    f_R = (1 - (R[i] / 2 + 1) * np.exp(-R[i] / 2)) / R[i]
    df_dR = (np.exp(-R[i] / 2) * (1 / R[i]**2 + 1 / 4 + 1 / (2 * R[i])) - 1 / R[i]**2)
    dv_dR = 452 / (2 * np.sqrt(f_R)) * df_dR

    v_d_i = 452 * np.sqrt(f_R)
    v_d_err_i = abs(dv_dR) * R_err[i]

    # baryonic mass
    M_d_i = 0.234e10 * (v_d_i / 100)**2 * R[i] #in Sonnenmassen (M_sun = 1.98e30 kg)
    M_d_err_i = 2*v_d_err_i/v_d_i * M_d_i

    # dark matter mass
    M_dm_i = M_R_i - M_d_i
    M_dm_err_i = M_R_err_i - M_d_err_i

    v_R.append(v_R_i)
    v_R_err.append(v_R_err_i)
    M_R.append(M_R_i)
    M_R_err.append(M_R_err_i)
    v_d.append(v_d_i)
    v_d_err.append(v_d_err_i)
    M_d.append(M_d_i)
    M_d_err.append(M_d_err_i)
    M_dm.append(M_dm_i)
    M_dm_err.append(M_dm_err_i)

v_R = np.array(v_R)
v_R_err = np.array(v_R_err)
M_R = np.array(M_R)
M_R_err = np.array(M_R_err)
v_d = np.array(v_d)
v_d_err = np.array(v_d_err)
M_d = np.array(M_d)
M_d_err = np.array(M_d_err)
M_dm = np.array(M_dm)
M_dm_err = np.array(M_dm_err)

# für M_DM(R_0) -> R=R_0 bzw l=90°
M_dm_0 = M_dm[8]


data_new = np.column_stack((data, v_R, v_R_err, M_R, M_R_err, v_d, v_d_err, M_dm, M_dm_err))
filepath_newdata="Auswertung HS1/calibrated 21cm/cm21_tab_newdata.txt"
np.savetxt(
    filepath_newdata,
    data_new,
    header="l[deg] R[kpc] R_err v_max[kms-1] v_max_err v_R[kms-1] M_R[M_sun] M_R_err v_d[kms-1] v_d_err M_DM[M_sun] M_DM_err",
    comments="",
    fmt=["%.0f", "%.2f", "%.2f", "%.2f", "%.2f", "%.2f", "%.2f", "%.2f", "%.2f", "%.2f", "%.2f", "%.2f", "%.2f"]
)

plt.errorbar(
    R[1:],
    v_R[1:],
    yerr=v_R_err[1:],
    fmt="x",
    capsize=3,
    label=r"$v_R$ mit Fehlerbalken"
)

plt.errorbar(
    R[1:],
    v_d[1:],
    yerr=v_d_err[1:],
    fmt="x",
    capsize=3,
    label=r"$v_d$ mit Fehlerbalken"
)

plt.xlabel(r"$R$ [kpc]")
plt.ylabel(r"velocity [kms^{-1}]")
plt.title("Velocities (radian + bayronic) at each distance R")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.errorbar(
    R[1:],
    M_R[1:],
    yerr=M_R_err[1:],
    fmt="x",
    capsize=3,
    label=r"$M_R$ mit Fehlerbalken"
)

plt.errorbar(
    R[1:],
    M_d[1:],
    yerr=M_d_err[1:],
    fmt="x",
    capsize=3,
    label=r"$M_d$ mit Fehlerbalken"
)

plt.errorbar(
    R[1:],
    M_dm[1:],
    yerr=abs(M_dm_err[1:]),
    fmt="x",
    capsize=3,
    label=r"$M_{DM}$ mit Fehlerbalken"
)

plt.xlabel(r"$R$ [kpc]")
plt.ylabel(r"$M_R$ [solar masses]")
plt.title("Enclosed mass of the Milky Way ($M_R, M_d, M_{DM}$) at each distance R")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
