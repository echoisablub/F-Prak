import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.stats import linregress
from scipy.constants import c
from scipy.fft import fft, fftshift

# Daten einlesen
data_laser = np.loadtxt('data/Filter 1/Data Channel 2.dat')

# Messwerte mitteln
relevante_spalten = data_laser[:, 1:20]
zeilen_mittelwerte = np.mean(relevante_spalten, axis=1)

erste_spalte_data_laser = data_laser[:, 0]
mean_data_laser = np.column_stack((erste_spalte_data_laser, zeilen_mittelwerte))
#print(mean_data_laser[:,1])


# Interpolation
x= np.linspace(-5000, 5000, 10000)
y= mean_data_laser[:,1]

mean_laser_interpolate = UnivariateSpline(x,y, k=4)
x_new=np.linspace(-5000,5000,100000)

'''plt.plot(x,y,'.',color='green')
plt.plot(x_new, mean_laser_interpolate(x_new), '-', color='red')
plt.xlabel("Position")
plt.ylabel("Signal")
plt.show()'''

# Bestimmung der Position der Maxima (ggf. auch Minima)
mean_laser_interpolate_deriv1= mean_laser_interpolate.derivative(1)

#print("deriv: ", mean_laser_interpolate_deriv1)

'''plt.plot(x_new, mean_laser_interpolate(x_new), '-', color='black')
plt.plot(x_new, mean_laser_interpolate_deriv1(x_new), color='blue', label="Extrema")
plt.xlabel("Position")
plt.ylabel("Signal")
plt.legend()
plt.show()'''

# Kalibrierfunktion

# bc curved, lets make it lin: roots()
deriv_lin = mean_laser_interpolate_deriv1.roots()
#print(len(deriv_lin))

r= np.linspace(0, len(deriv_lin)-1, len(deriv_lin))
fit=linregress(r, deriv_lin)

'''plt.plot(r, deriv_lin, '+',color='orange', label="data")
plt.plot(r, fit.intercept + fit.slope*r, color='blue', label="linear fit")
plt.xlabel("Extrema")
plt.ylabel("Position")
plt.legend()
plt.show()'''


# Korrektur + # Erneute Interpolation der korrigierten Daten
P_soll = np.empty(len(deriv_lin), dtype=int)
for i in range(len(deriv_lin)):
    P_soll[i] = fit.intercept + fit.slope*i
P_ist = deriv_lin
delta = P_soll - P_ist
delta_interpolate = UnivariateSpline(P_ist, delta, k=4)


'''plt.plot(P_ist, delta, '+', color='red', label="data")
plt.plot(x_new, delta_interpolate(x_new), color='blue', label="interpolation")
plt.xlabel("Position")
plt.ylabel("Signal")
plt.legend()
plt.show()'''


# Ortskorrektur
x= np.linspace(-5000, 5000, 10000)
y= mean_data_laser[:,1]
x_korr = x + delta_interpolate(x)

x_korr_eq = np.arange(min(x_korr), max(x_korr), (max(x_korr)-min(x_korr))/len(x_korr))

laser_interpolate_func = UnivariateSpline(x_korr, y, k=4)
laser_interpolate_korr = laser_interpolate_func(x_korr_eq)

'''plt.plot(x_korr_eq, laser_interpolate_korr, '-', color='red', label="data")
plt.xlabel("Position")
plt.ylabel("Signal")
plt.legend()
plt.show()

# Vergleich von laser-interpolation-korr mit laser-interpolation
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Vergleich')
ax1.plot(x_korr_eq, laser_interpolate_korr, '-', color='red', label="data")
ax1.set_xlabel("Position")
ax1.set_ylabel("Signal")
ax2.plot(x_new, mean_laser_interpolate(x_new), '-', color='green')
ax2.set_xlabel("Position")
ax2.set_ylabel("Signal")

#plt.plot(x_korr_eq, laser_interpolate_korr, '-', color='red', label="data")
plt.plot(x_new, mean_laser_interpolate(x_new), '-', color='green')
plt.xlabel("Position")
plt.ylabel("Signal")
#plt.legend()
plt.show()'''

# Umrechnen der Ortsachse in eine Zeitachse
delta_s = x_korr*101*10**(-5)/fit.slope
delta_t = delta_s / c
d=delta_t
#print(delta_t)

# FT 
T_sample= ((max(d)-min(d))/len(d))*1e12 #ps
f_max=1/T_sample
L=len(d)
f_Ny=f_max/2
w=np.linspace(-f_Ny,f_Ny,L)

W=abs(fftshift(fft(laser_interpolate_korr/L)))

plt.plot(w,W/max(W), color='purple')
plt.xlim(0,1000)
plt.ylim(0,1)
plt.show()

# 
