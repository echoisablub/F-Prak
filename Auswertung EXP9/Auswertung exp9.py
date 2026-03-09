import numpy as np
import matplotlib as plt


epsilon_x = ...
epsilon_y = ...

data = np.loadtxt("data/...")
z_pos = data[:, 0] #in cm
x_rms = data[:, 1] #in mm
y_rms = data[:, 2] #in mm

x_rms_m2 = (x_rms * 10**(-3))**2 #in m
y_rms_m2 = (y_rms * 10**(-3))**2 #in m

x_rms_new = np.array(...) + x_rms_m2 #hier wert von Qscan einfügen
y_rms_new = np.array(...) + y_rms_m2 #hier punkt

beta_x_func = x_rms_new/epsilon_x
beta_y_func = y_rms_new/epsilon_y

plt