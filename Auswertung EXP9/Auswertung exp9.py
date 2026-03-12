import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.optimize import fsolve
import scipy.constants as const

# ---Tag 1---

# Energiemessung
'''Messung: <y>(I)'''
dy_dI = 14.4384e-3 # in m/A
sigma_dy_dI = (14.4384 - 14.2273)/2 # 1 sigma berechnung durch (value-lower)/2 mit value und lower 2 sigma fehler
kappa = 7.64e-6 # in Tm/A, Eigenschaft des Dipols
L = 0.52 # in m
e_lad = const.elementary_charge
e_mass = const.electron_mass
c_vak = const.speed_of_light
E_0 = 511 # in keV
beta_gamma = (e_lad*kappa*L)/(e_mass*c_vak*dy_dI) #result: 0.16142780000890825 ~= beta
gamma = np.sqrt(1+beta_gamma**2) #result: 1.0129456720948642 --> also fast klassisch
Ekin = E_0*(gamma-1) #result: 6.6152384404756015 keV
p = E_0/c_vak*np.sqrt(gamma**2-1) #result: p=2.7515570723447654e-07 keV/c

# Energiemessung Fehlerfortpflanzung
# fehlerbehaftete Größen: L, Steigung bzw. dy_dI
# todo: ekin fehler, beta fehler, impuls fehler


# Emittanzbestimmung duch Q-Scan
'''zwei Messreihen, eine horizontal (x_RMS(I)), eine vertikal (y_RMS(I))'''
I_pos = [0.923, 1.023, 1.121, 1.221, 1.316, 1.419, 1.519, 1.621, 1.724, 1.812, 1.919]
x_rms_qscan = [0.638175, 0.516351, 0.434130, 0.388772, 0.363201, 0.388798, 0.439333, 0.494053, 0.544843, 0.535492, 0.505021]
I_neg = [-0.908, -1.004, -1.104, -1.206, -1.306, -1.404, -1.509, -1.607, -1.709, -1.802, -1.902]
y_rms_qscan = [0.775577, 0.832959, 0.693442, 0.604762, 0.554150, 0.576056, 0.644182, 0.742516, 0.871134, 0.976145, 1.160084]
A = np.array([[0.0293, -0.1312,  0.1470], [0.0874, -0.2237,  0.1432], [0.1755, -0.3129,  0.1395], [0.2927, -0.3989,  0.1359], [0.4384, -0.4816,  0.1323], [0.6116, -0.5613,  0.1288], [0.8115, -0.6379,  0.1253], [1.0375, -0.7115,  0.1220], [1.2887, -0.7821,  0.1187], [1.5643, -0.8497,  0.1154], [1.8637, -0.9145,  0.1122]])
#A=A_x=A_y in diesem  Fall
x_vect_x = 1.0e-05 * np.array([0.0421, 0.0869, 0.3054])
x_vect_y = 1.0e-05 * np.array([0.1615, 0.2779, 0.7218])

epsilon_x = np.sqrt(x_vect_x[0]*x_vect_x[2]-x_vect_x[1]**2) #result: 7.284044206345813e-07 m rad = 0.72867 mm mrad
epsilon_y = np.sqrt(x_vect_y[0]*x_vect_y[2]-x_vect_y[1]**2) #result: 1.9834890975248643e-06 m rad = 1.98349 mm mrad

# Emittanz Fehlerfortpflanzung
# Fehlerfortpflanzung wurde in situ gemacht:
sigma_epsilon_x = 0.097674*epsilon_x #result: 7.11461733810621e-08 m rad = 0.07115 mm mrad
sigma_epsilon_y = 0.045431*epsilon_y #result: 9.011189318965211e-08 m rad = 0.09011 mm mrad

# Beta Funktions Messung
'''Messungen x_rms, y_rms an den verschiedenen schirmen an z_pos'''
z_pos = np.array([176.5, 233, 288, 343.5]) # in cm
x_rms_beta = np.array([1.469368, 1.675064, 1.885123, 0.416260]) # in mm
y_rms_beta = np.array([3.270433, 3.765737, 1.381060, 2.914094]) # in mm

x_rms_m2 = (x_rms_beta * 10**(-3))**2 # in m
y_rms_m2 = (y_rms_beta * 10**(-3))**2 # in m

x_rms_new = x_vect_x[0] + x_rms_m2 # hier wert von Q-Scan einfügen als 5. punkt
y_rms_new = x_vect_y[0] + y_rms_m2 
z_pos_new = np.array([140]) + z_pos

beta_x_func = x_rms_new/epsilon_x
beta_y_func = y_rms_new/epsilon_y

plt.plot(z_pos_new, beta_x_func, '.', color='red', label="$\\beta_x$")
plt.plot(z_pos_new, beta_y_func, '.', color='blue', label="$\\beta_y$")
plt.xlabel("Z Position [cm]")
plt.ylabel("$\\beta$-Funktion")
plt.title("$\\beta$-Funktionen in Abhängigkeit der z-Achse")
plt.legend()
plt.show()

# Beta-Funktion Fehlerfortpflanzung

# ---TAG 2---

# Strahlbasierte Justage
#x_werte
# I_Q_1:-0.344
x_1 = [2.381327, 1.701390, 0.543287, -0.559225, -1.598436, -2.668805, -3.962848, -5.083899, -6.339732, -7.617045, -9.388490]
i_x_1 = [-1.568, -1.492, -1.407, -1.309, -1.192, -1.096, -0.989, -0.891, -0.789, -0.694, -0.505]

# I_Q_2: 0.657
x_2 = [-8.137709, -6.398327, -4.906813, -3.324318, -1.858580, -0.200311, 1.271396, 1.971100]
i_x_2 = [-0.806, -0.904, -1.009, -1.101, -1.194, -1.294, -1.394, -1.455]

#I_D0: -1.236
x_2_2=[-1.470172, -1.435137, -1.547972, -1.603483, -1.400256, -1.516494,-1.363436,	-1.541525,	-1.455577,	-1.573190,	-1.319472]
i_x_2_2=[-0.342, -0.247, -0.149, -0.046,0.056, 0.151, 0.254, 0.352, 0.444, 0.547, 0.657]

#y_werte
# I_Q_1: 1.685
y_1=[10.871612, 9.889948, 8.801943, 7.534783, 6.131194, 4.694049, 3.211998, 1.706693, 0.281157, -1.190804, -2.742777, -4.065295, -5.466554, -6.642288, -7.936796, -7.715350]
i_y_1=[0.501, 0.305, 0.149, -0.056, -0.259, -0.457, -0.657 ,-0.852, -1.060, -1.258, -1.458, -1.661, -1.861, -2.054, -2.254, -2.303]
# I_Q_2: 2.703
y_2=[-2.816, -2.615, -2.410, -2.208, -2.022, -1.812, -1.619, -1.414, 1.454827, 2.047659, 2.478990, 3.106047, 3.716454, 4.340098, 4.959453, 5.699637, 6.337515, 7.170582, 7.937646, 8.636715, 9.554739]
i_y_2=[	-4.931521, -3.839596, -3.017802, -2.195475, -1.261315, -0.548561, 	0.172940, 0.648720, -1.214, -1.018, -0.825, -0.613, -0.425, -0.220, -0.002, 0.186, 0.393, 0.586, 0.789, 0.987, 1.192]

#I_D0: -0.7773577667316248
y_2_2=[2.742641,2.801394,2.779676, 2.791666,2.826833,2.808116,2.835512,2.855125,2.802748, 2.883961,2.794510,2.875665]
i_y_2_2=[1.685	,1.773	,1.900	,1.966	,2.095	,2.176	,2.281	,2.376	,2.469	,2.567	,2.681,	2.703	]

i_x_1_neu = np.linspace(-9.4, 2.4)
fct_x = linregress(i_x_1, x_1)
i_x_2_neu = np.linspace(-8.2, 2)
fct2_x = linregress(i_x_2, x_2)
fct_x_neu = fct_x.intercept + fct_x.slope*i_x_1_neu
fct2_x_neu = fct2_x.intercept + fct2_x.slope*i_x_2_neu

i_x_2_2_neu = np.linspace(-0.4, 0, 11)

x_intersection = (fct2_x.intercept-fct_x.intercept)/(fct_x.slope-fct2_x.slope)
#print(x_intersection)

plt.plot(i_x_1_neu, fct_x_neu, 'r')
plt.plot(i_x_2_neu, fct2_x_neu, 'b')
plt.title("X-Ausrichtung")
plt.show()

plt.plot(i_x_2_2_neu, x_2_2, 'x')
plt.title("Überprüfung X")
plt.show()

i_y_1_neu = np.linspace(-9.4, 2.4)
fct_y = linregress(i_y_1, y_1)
i_y_2_neu = np.linspace(-8.2, 2)
fct2_y = linregress(i_y_2, y_2)
fct_y_neu = fct_y.intercept + fct_y.slope*i_y_1_neu
fct2_y_neu = fct2_y.intercept + fct2_y.slope*i_y_2_neu

i_y_2_2_neu = np.linspace(-0.4, 0, 12)

y_intersection = (fct2_y.intercept-fct_y.intercept)/(fct_y.slope-fct2_y.slope)
#print(y_intersection)

plt.plot(i_y_1_neu, fct_y_neu, 'r')
plt.plot(i_y_2_neu, fct2_y_neu, 'b')
plt.title("Y-Ausrichtung")
plt.show()

plt.plot(i_y_2_2_neu, y_2_2, 'x')
plt.title("Überprüfung Y")
plt.show()

# Strahltransport
# hat keine rechnerische Auswertung :)