# wetter

Datum: 07/09/26
um 12h35:
![[Pasted image 20260907123451.png]]

teilweise bedeckter himmel
kein niederschlag

# 5.1.1 Calibration (system temp)
USB 1-5, 9-13

data structure in programm (RadioUniversePro)

| rep | dev   | sb  | on_tbi   | off_tbi | cal_tbi | flux  | SEFD  |
| --- | ----- | --- | -------- | ------- | ------- | ----- | ----- |
| 1   | bbc01 | u   | 12195,30 | 1001,40 | 2634,20 | 00,00 | 00,00 |
P_on_left_mean  = 13680.82 ± 3444.69
P_off_left_mean = 1023.63 ± 196.40
P_cal_left_mean = 2785.62 ± 723.30
P_on_right_mean  = 16597.42 ± 4814.85
P_off_right_mean = 1292.15 ± 340.61
P_cal_right_mean = 3329.96 ± 1009.47


==T_sys_left  = 98.76 ± 22.54 K
T_sys_right = 107.80 ± 31.65 K
T_sun_left  = 1237.79 +- 89.62 K
T_sun_right = 1302.59 +- 119.16 K==

With $S_{\nu}$ of the Sun (aus SWC): 
76 sup $76\cdot10^{-11}Wm^{-2}Hz^{-1}=76\cdot10000Jy =760000 Jy$
$S_{\nu}=\frac{T_{A}\cdot 2k_{B}}{A_{e}}$
$\Rightarrow T_A = 972,753 K$

- störung wegen rfi
- 
# 5.2 angular resolution
USB 1-5, 9-13
position of the sun calculated by the control software

| Source | RA       | DEC       | AZ         | EL        | HA        | Type | Note |
| ------ | -------- | --------- | ---------- | --------- | --------- | ---- | ---- |
| Sun    | 110410.1 | +055810.9 | +1684733.7 | +420048.8 | -003253.9 | Star | East |
in ordner cscan ist der screenshot
in ordner FITS sind die daten (lon vs lat)

# 5.3 sensitivity of the instrument

antenna temp of VirA
BBC 3,11
	shows least RFI influence


time needed for mapping: 
28:35.4s (software)
29:27.8s (own timer)

screenshot auf ubuntu und nicht windows!
files bei ordner maps und in FITS als imageproJ01 VirA 01

# 5.1.2 background radiation
## moon
for moon: elevation 30° 52' 32.0''
(in deg, min, sec)

for BCC 1-5,9-13
(as before for the sun)
even if quality is shit 

span = 2(ELV -10°) = 2(30°-10°)=2(20°)=40°
but because azimuth at 268° 03' 32.7'' chose slightly smaller span
-> span = 38°

around 14.56

data in FITS: LON-MOON und LAT-MOON
+screenshot in cscan: CSCAN-MOON
## virgo A
for Virgo A: at 15.28
elevation 47° 56' 18''
azimuth= 196°
span = 74











