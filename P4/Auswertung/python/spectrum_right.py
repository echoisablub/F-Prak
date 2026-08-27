###==========================================================================
###PYTHON SCRIPT TO ANALYSE HI SPECTRA FROM THE KRT3 RADIO TELESCOPE
###VERSION OF 20220124 (YYYYMMDD)
###==========================================================================
from astropy import units as u
from astropy.coordinates import LSR
from astropy.coordinates import ICRS
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation
import sys
from astropy.io import fits as pyfits
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore', category=UserWarning, append=True)

filename_spectrum = sys.argv[1]
try:
    xoption = sys.argv[2]
except IndexError:
    xoption = 'vlsr'
try:
    baseline = float(sys.argv[3])
except IndexError:
    baseline = None
try:
    filename_lab = sys.argv[4]
    lab = np.loadtxt(filename_lab, comments='%')
except IndexError:
    filename_lab = None

if baseline == None:
    baseline_subtract = 0
else:
    baseline_subtract = baseline

hambobs = EarthLocation.from_geodetic(lat=53.5*u.deg, lon=10.25*u.deg, height=40*u.m)
#hambobs = EarthLocation.from_geodetic(lat=38.*u.deg, lon=-80.*u.deg, height=40*u.m)

hdulist = pyfits.open(filename_spectrum)

# print column information
# print(hdulist[1].data)

# get to the data part (in extension 1)
scidata = hdulist[1].data
# print('Hier')

obstime = scidata[0][0]
l = scidata[0][5]
b = scidata[0][6]
sc = SkyCoord(l=l*u.deg, b=b*u.deg, frame='galactic')
#barycorr = sc.radial_velocity_correction(obstime=Time(obstime,format='jd'), location=hambobs)
barycorr = sc.radial_velocity_correction(kind='barycentric', obstime=Time(obstime,format='jd'), location=hambobs)
print('barycorr=', barycorr.to(u.km/u.s))
icrs = ICRS(sc.icrs.ra, sc.icrs.dec, distance=1000*u.pc, pm_ra_cosdec=0*u.mas/u.yr, pm_dec=0*u.mas/u.yr, radial_velocity=barycorr.to(u.km/u.s))
#icrs = ICRS(sc.icrs.ra, sc.icrs.dec, distance=1.*u.pc, pm_ra_cosdec=0*u.mas/u.yr, pm_dec=0*u.mas/u.yr, radial_velocity=0.*(u.km/u.s))
#print('LSR= ', icrs.transform_to(LSR))
radial_velocity = icrs.transform_to(LSR()).radial_velocity
#print('LSR =', icrs.transform_to(LSR()))

print('======================================================')
print('++++++++++++ANALYSIS OF KRT3 HI SPECTRA+++++++++++++++')
print('======================================================')
print('HEADER INFORMATION')
print('icrs = ', sc.icrs.to_string('hmsdms'))
print('icrs = ', sc.icrs.to_string())
print('time = ', Time(obstime,format='jd').isot)

delta_vlsr = -radial_velocity 

print ('delta_vlsr = ', "{:.1f}".format(delta_vlsr))


#print('obstime =', obstime)

print ('Galactic longitude = ', '{:.1f}'.format(l), 'degree')
print ('Galactic latitude = ', '{:.1f}'.format(b), 'degree')


observations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
observations = [7, 8, 9]

left = range(0, 1024)
right = range(0, 1024)

cal_left = 1./5e7 * 0.7 * 20.
cal_right = cal_left

line_free = range(400,450)


print('======================================================')
for i in observations:
    left = left + scidata[i*3][8] - scidata[i*3+1][8]
    right = right + scidata[i*3][8] - scidata[i*3+1][8]
    left_obs = scidata[i*3][8] - scidata[i*3+1][8]
    right_obs = scidata[i*3][8] - scidata[i*3+1][8]
    
    print('On-Off Messung:', "{:02d}".format(i), 'rms_left =', int(round(np.std(cal_left * len(observations) * left_obs[line_free] - baseline_subtract))), 'K; rms_right = ', int(round(np.std(cal_right * len(observations) * right_obs[line_free] - baseline_subtract))), 'K')
print('======================================================')    

mean_left = np.mean(left[366:381])
mean_right = np.mean(right[366:381])
base_left = np.mean(left[line_free])
base_right = np.mean(right[line_free])

print('Normalisation left/right = ', '{:.1f}'.format((mean_left-base_left)/(mean_right-base_right)))

if (mean_left-base_left)/(mean_right-base_right) > 0.:
    cal_right = (mean_left-base_left)/(mean_right-base_right) * cal_left
else:
    cal_right = cal_left

rms_left = np.std(cal_left * left[line_free] - base_left)
rms_right = np.std(cal_right * right[line_free] - base_right)

#for i in observations:
#    right = right + scidata[i*3][8] - scidata[i*3+1][8]


#continuum = []
#for i in range(10):
#    continuum.append(np.average(left_time[i]))




freq_left = []
freq_right = []
for i in range(1024):
#    freq_left.append(1397.75 + i*62.5/1024)
#    freq_right.append(1397.75 + (i-1)*62.5/1024)
#    freq_left.append(1397.65 + i*62.5/1024)
#    freq_right.append(1397.65 + (i-1)*62.5/1024)
#    freq_left.append(1397.55 + i*62.5/1024)
#    freq_right.append(1397.55 + (i-1)*62.5/1024)
    freq_left.append(1397.57 + (i-1)*62.5/1024)
    freq_right.append(1397.57 + (i-1)*62.5/1024)

#print(freq_left)

chan = []
for i in range(1024):
    chan.append(i)

#for i in range(1024):
#    freq.append(1398.0 + 62.5/1024./2. + i*62.5/1024.)
    
vlsr_left = []
vlsr_right = []
for i in range(1024):
    vlsr_left.append((1420.405752 - freq_left[i]) / 1420.405752 * 2.99792e5 - delta_vlsr.value)
    vlsr_right.append((1420.405752 - freq_right[i]) / 1420.405752 * 2.99792e5 - delta_vlsr.value)
    



line_free_left = []
rfi_left = []
for i in range(400, 450):
    if (abs(cal_left * (2.*left[i]-left[i-1]-left[i+1]) - 0.) < 5.*rms_left):
        line_free_left.append(i)
    else:
        rfi_left.append(i)

line_free_right = []
rfi_right = []
if baseline == None:
    baseline_subtract = 0
else:
    baseline_subtract = baseline
for i in range(400, 450):
    if (abs(cal_right * (2.*right[i]-right[i-1]-right[i+1]) - 0.) < 5.*rms_right):
        line_free_right.append(i)
    else:
        rfi_right.append(i)
        

replace = 0
#left[342] = (replace + baseline_subtract) / cal_left
#left[383] = (replace + baseline_subtract) / cal_left
#left[384] = (replace + baseline_subtract) / cal_left

#right[343] = (replace + baseline_subtract) / cal_right
#right[384] = (replace + baseline_subtract) / cal_right
#right[385] = (replace + baseline_subtract) / cal_right

#left[384] = (left[383] + left[385])/.2
#right[385] = (left[384] + left[386])/.2

        
base_left = np.mean(cal_left * left[line_free_left])
base_right = np.mean(cal_right * right[line_free_right])
rms_left = np.std(cal_left * left[line_free_left] - base_left)
rms_right = np.std(cal_right * right[line_free_right] - base_right)
print ('base_left =', '{:.1f}'.format(base_left), 'K')
print ('base_right =', '{:.1f}'.format(base_right), 'K')


#if baseline == None:
#    baseline = np.average(cal * left[line_free] - baseline_subtract)
#    print ('Fitted baseline =', baseline, 'K')


if len(line_free_left) <= 25 or len(line_free_right) <= 25:
    print ('More than half of the line free channels rejected. Check baseline.')
    
if len(line_free_left) <= 25:
    rms_left = 1.e10

if len(line_free_right) <= 25:
    rms_right = 1.e10
    

tp = []
left_help = []
right_help = []
for i in range(0, 1024):
    if (i < 1023):
        left_help.append(cal_left * left[i+1] - base_left)
        right_help.append(cal_right * right[i+1] - base_right)
    else:
        left_help.append(cal_left * left[i] - base_left)
        right_help.append(cal_right * right[i] - base_right)
    if i+1 in rfi_left or i+1 in rfi_right:
        if i+1 in rfi_right and i in rfi_left:
                tp.append(0.)
        else:
            if i+1 in rfi_right:
                tp.append(left_help[i])
            if i in rfi_left:
                tp.append(right_help[i])
    else:
        if abs(left_help[i]-right_help[i])>30. and (abs(left_help[i]/right_help[i])<1./3. or abs(left_help[i]/right_help[i])>3. or left_help[i]/right_help[i]<0.):
            tp.append(0.)


        else:
            tp.append((1./rms_left**2*left_help[i]+1./rms_right**2*right_help[i])/(1./rms_left**2+1./rms_right**2)-baseline_subtract)

 

rms = np.std(tp[400:450])
print('HI spectrum noise')
print ('rms_left =', '{:.1f}'.format(rms_left), 'K')
print ('rms_right =', '{:.1f}'.format(rms_right), 'K')
print ('rms =', '{:.1f}'.format(rms), 'K')
print('===============================================> DONE!')
             
x_coordinates = [-1000, 1000]
if (xoption == 'chan'):
    x_coordinates = [0, 1023]
if (xoption == 'freq'):
    x_coordinates = [1400, 1460]
y_coordinates = [3.*rms, 3.*rms]
y2_coordinates = [0, 0]

if (xoption == 'chan'):
    xaxis_left = chan
    xaxis_right = chan
if (xoption == 'freq'):
    xaxis_left = freq_left
    xaxis_right = freq_right
if (xoption == 'vlsr'):
    xaxis_left = vlsr_left
    xaxis_right = vlsr_right


#print('len(left_help)=', len(left_help))

#============================================================================
#CHANGE HERE THIS TO BE PLOTTED    
plt.errorbar(xaxis_left, tp, rms, marker='o', label='KRT3')
#plt.errorbar(xaxis_left, left_help, rms_left,marker='.', label='KRT3 left')
#plt.errorbar(xaxis_right, right_help, rms_left,marker='+', label='KRT3 right')
#============================================================================
    

if (filename_lab != None):
    plt.plot(lab[:,0],lab[:,1],label='LAB')

if (xoption == 'chan'):
    plt.xlabel('Channel')
    plt.plot(x_coordinates, y2_coordinates, color='black', label=r'$T_{\rm A} = 0~\rm K$')
elif (xoption == 'freq'):
    plt.xlabel('Frequency (MHz)')
else:
    plt.xlabel(r'$V_{\rm LSR}~[\rm km\, s^{-1}]$')

plt.plot(x_coordinates, y_coordinates, label=r'$3\sigma$')
plt.fill_between(x_coordinates, y_coordinates-rms, y_coordinates+rms, alpha=0.2)
plt.plot(x_coordinates, y2_coordinates, color='black', label=r'$T_{\rm A} = 0~\rm K$')



plt.ylabel(r'$T_{\rm A}~[K]$')
plt.title(r'${\rm Galactic~HI~at}~l =$'+str(int(l))+r'$^{\circ}~b =$'+str(int(b))+r'$^{\circ}$')  
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

