#############################################################################
###SCRIPT TO EXTRACT THE VALUES FROM THE KRT FILES
###VOLKER HEESEN, FEBRUARY 2017, changed last March 2018
############################################################################

#!/usr/bin/python

import math
import numpy
import sys

###NUMBER OF DATA POINTS
N = 0

###READ THE FILES IN
time=[]
time_format=[]
int_read=[]
int2_read=[]

filename = sys.argv[1]


beam_option = 'blah'
if sys.argv[2:]:
   beam_option = sys.argv[2]

bmsw = False
if str(beam_option) == 'bmsw':
    bmsw = True


with open(filename) as inf:
    for line in inf:
        if not line.startswith("*"):
            N = N + 1
            time.append(8*N)
            parts= line.split() # split line into parts
            nof = int(parts[8])
            freq = float(parts[5])
            delta_freq = float(parts[6])


intensity = numpy.empty((N, nof), dtype=object)


i=0
vlsr=[]
rest_frame = False
with open(filename) as inf:
    for line in inf:
        if not line.startswith("*"):
            parts= line.split() # split line into parts
            time_format.append(parts[0])
            for j in range (0, nof):
                intensity[i, j] = (float(parts[j+9]))
            i = i + 1
            if len(parts) == nof + 11:
                vlsr.append(float(parts[j+11]))
                rest_frame = True
           


bad_channels = [32, 78, 124]

average = []
sigma = []
V_LSR = []

beam_on = []
beam_off = []
sigma_beam_on = []
sigma_beam_off = []
beam_counter_on = 0
beam_counter_off = 0

for i in range(0, N):
    sum = []
    counter = 0
    for j in range(8, nof-8):
        if j not in bad_channels:
            sum.append(intensity[i, j])
            counter = counter + 1
#            print 'counter_continuum=', j, counter, intensity[i, j]
    average.append(numpy.average(sum))
    sigma.append(numpy.std(sum)/math.sqrt(len(sum)))
    if i%2 == 0:
        beam_on.append(numpy.average(sum))
        sigma_beam_on.append(numpy.std(sum)/math.sqrt(len(sum)))
        beam_counter_on = beam_counter_on + 1
    if i%2 == 1:
        beam_off.append(numpy.average(sum))
        sigma_beam_off.append(numpy.std(sum)/math.sqrt(len(sum)))
        beam_counter_off = beam_counter_off + 1


beam_counter = [beam_counter_on, beam_counter_off]

difference = []
sigma_difference = []
difference_beam_1 = []
difference_beam_2 = []
nob = numpy.min(beam_counter)
for k in range(0, nob):
    difference.append(beam_on[k] - beam_off[k])
    sigma_difference.append(sigma_beam_on[k]+sigma_beam_off[k])
    if k%2 == 0:
         difference_beam_1.append(beam_on[k] - beam_off[k])
    if k%2 == 1:
         difference_beam_2.append(beam_on[k] - beam_off[k])

spectrum = []
sigma_spectrum = []
frequency = []
velocity = []
hi_frequency = 1420.405752e6
c = 299790e3
if rest_frame == True:
    vlsr_mean = (vlsr[0]+vlsr[N-1])/2.
    v = (hi_frequency - freq * 1.e6) / hi_frequency * c - (vlsr_mean * 1.e3)
    v = v / 1.e3
for j in range(0, nof):
    sum = []
    counter = 0
    for i in range(0, N):
        sum.append(intensity[i, j])
        counter = counter + 1
#        print 'counter=', counter, j, intensity[i, j]
    spectrum.append(numpy.average(sum))
    sigma_spectrum.append(numpy.std(sum)/math.sqrt(len(sum)))
    frequency.append(freq)
    if rest_frame == True:
        velocity.append(v)
        v = (hi_frequency - freq * 1.e6) / hi_frequency * c - (vlsr_mean * 1.e3)
        v = v / 1.e3
    freq = freq + delta_freq

for j in range(0, nof):
    if j in bad_channels:
        spectrum[j] = (spectrum[j-1]+spectrum[j+1]) / 2.
        sigma_spectrum[j] = (sigma_spectrum[j-1]+sigma_spectrum[j+1]) / 2.

f1 = open('continuum.dat', 'w')
f2 = open('spectrum.dat', 'w')
f3 = open('beamsw1.dat', 'w')
f4 = open('beamsw2.dat', 'w')

f1.write ('###Time scan time(s) T_A(K) Delta T_A(K)\n')
for i in range(0,N):
    f1.write (str(time_format[i])+' '+str(i)+' '+ str(time[i])+' '+str(average[i])+' '+str(sigma[i])+'\n')
if rest_frame == True:
   f2.write ('###Time channel nu(MHz) VLSR(km/s) T_A(K) Delta T_A(K)\n')
   for j in range(0,nof):
      f2.write (str(time_format[0])+' '+str(j)+' '+ str(frequency[j])+' '+str(velocity[j])+' '+ str(spectrum[j])+' '+str(sigma_spectrum[j])+'\n')
else:
   f2.write ('###Time channel nu(MHz) T_A(K) Delta T_A(K)\n')
   for j in range(0,nof):
      f2.write (str(time_format[0])+' '+str(j)+' '+ str(frequency[j])+' '+ str(spectrum[j])+' '+str(sigma_spectrum[j])+'\n')

f3.write ('###k T(ON)-T(OFF) Delta(T(ON)-T(OFF)) Delta(T(ON)) Delta(T(OFF))\n')      
f4.write ('###k T(ON)-T(OFF) Delta(T(ON)-T(OFF)) Delta(T(ON)) Delta(T(OFF))\n')      
for k in range(0, nob):
   if k%2 == 0:
      f3.write (str(k)+' '+str(difference[k])+' '+str(sigma_difference[k])+' '+str(beam_on[k])+' '+str(sigma_beam_on[k])+' '+str(beam_off[k])+' '+str(sigma_beam_off[k])+'\n')
   if k%2 == 1:
      f4.write (str(k)+' '+str(difference[k])+' '+str(sigma_difference[k])+' '+str(beam_on[k])+' '+str(sigma_beam_on[k])+' '+str(beam_off[k])+' '+str(sigma_beam_off[k])+'\n')
        
f1.close()
f2.close()
f3.close()
f4.close()

spectrum_corr=[]
for j in range(8, nof-8):
        if j not in bad_channels:
            spectrum_corr.append(spectrum[j])

noc = len(spectrum_corr)

frequency_central = (frequency[0]+frequency[nof-1])/2.
if rest_frame == True:
    velocity_central = (velocity[0]+velocity[nof-1])/2.


###print 'beam_1', numpy.average(difference_beam_1), numpy.std(difference_beam_1) / math.sqrt(len(difference_beam_1))
###print 'beam_2', numpy.average(difference_beam_2), numpy.std(difference_beam_2) / math.sqrt(len(difference_beam_2))

k_b = 1.38e-23
area = 7.55
eta = 0.5
area_eff = eta * area
c_eff = 2.
t_sys = 200.
delta_f = 2.0 * k_b / area_eff * c_eff * t_sys / math.sqrt(nof * delta_freq * 1.e6 * nob * 0.52)



###PRINT VALUES FOR CONTROL
print '----------------------------------------------------------------------'
print 'KRT observation from', time_format[0], 'to', time_format[N-1]
if bmsw == False:
   print 'Integration length =', time[N-1], 's'
print 'Bandwidth =', nof * delta_freq, 'MHz'
print 'Number of channels =', nof
print 'Central frequency =', frequency_central, 'MHz'
if bmsw == False:
   print 'T_A  =', numpy.average(spectrum_corr[8:noc-8]), '+/-', numpy.std(spectrum_corr[8:noc-8])/math.sqrt(len(spectrum_corr[8:noc-8])),'K'
if rest_frame == True:
    print 'VLSR =', vlsr_mean, 'km s^-1 (from', vlsr[0], 'to', vlsr[N-1],')'
    print 'Vcenter =', velocity_central, 'km s^-1'

if bmsw == True:
    print 'Beam switch difference = ', numpy.average(difference), '+/-', numpy.std(difference) / math.sqrt(nob), 'K'
    print 'S/N = ', numpy.average(difference) / numpy.std(difference) * math.sqrt(nob),'(Time on source = ', nob * 0.52, 's)'
    print 'For the following it is assumed that eta = 0.5 and T_sys = 200K:'
    print 'Flux density', 730 * numpy.average(difference), '+/-', 730  * numpy.std(difference) / math.sqrt(nob),'Jy (1 K = 730 Jy)'
    print 'Estimated sensitivity', delta_f * 1.e26, 'Jy'
    
    # for i in range(0,N):
#     print i, time[i], intensity[i, 0], average[i]


print '----------------------------------------------------------------------'

