data = np.loadtxt("data/...")
z_pos = data[:, 0] #in cm
x_rms = data[:, 1] #in mm
y_rms = data[:, 2] #in mm

x_rms_new = x_rms * 10**(-3) #in m
y_rms_new = y_rms * 10**(-3) #in m
