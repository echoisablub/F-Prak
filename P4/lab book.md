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
$T_{b}\cdot \Omega_{S}=T_{A}\Omega_{A}$
	$\Omega_{A}=\frac{\lambda^2}{A_{e}}$, $\Omega_{S}=\frac{S_{\nu}}{B_{\nu}}$, $B_{\nu}=\frac{2k_{B}T_{b}}{\lambda^2}$
	$S_{\nu}=\frac{T_{A}\cdot 2k_{B}}{A_{e}}=f(T_{A},A_{e})$
$A_{e}=\pi r^{2}\cdot\eta=1,5^2\pi\cdot0,5=1,125\pi m^2$
$T_{A}=\frac{S_{\nu}A_{e}}{2k_{B}}$

==T_sys_left  = 98.76 ± 22.54 K
T_sys_right = 107.80 ± 31.65 K
T_sun_left  = 1237.79 +- 89.62 K
T_sun_right = 1302.59 +- 119.16 K==

With $S_{\nu}$ of the Sun (aus SWC): 
76 sfu(solar flux units): $76\cdot10^{-11}Wm^{-2}Hz^{-1}=76\cdot10000Jy =760000 Jy$
$\Rightarrow T_A = 972,753 K$
- störung wegen rfi
# 5.2 angular resolution
USB 1-5, 9-13
position of the sun calculated by the control software

| Source | RA       | DEC       | AZ         | EL          | HA        | Type | Note |
| ------ | -------- | --------- | ---------- | ----------- | --------- | ---- | ---- |
| Sun    | 110410.1 | +055810.9 | +1684733.7 | +42 00 48.8 | -003253.9 | Star | East |
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

TODO:
## Theoretical Sensitivity
$\Delta S_{\nu}= \frac{2k}{A_{e}} \frac{C_{S}T'_{sys}}{\sqrt{ \Delta \nu \tau}}$
spectral flux density
$C_{S}\approx2$
$T'_{sys, left}  = 98.76 ± 22.54 K$
$T'_{sys,right} = 107.80 ± 31.65 K$
$A_{e}=1.125\pi$
$\tau=1s$
$\Delta \nu= 61kHz$
$\Delta S_{\nu, left}= 6,248 \cdot 10^{-24} \frac{W}{m^2Hz}= 624,92 Jy$
$\Delta S_{\nu, right}= 6,82 \cdot 10^{-24} \frac{W}{m^2Hz}= 682,02 Jy$

Necessary integration time τ to detected the selected source with the KRT 3 with a signal-to-noise ratio S/N = 10 in each channel:
- Virgo A: Flux density $=211 ± 11 Jy$, Radiogalaxy
- for 5 channel each side ($\Delta \nu= 5*61kHz= 305kHz$)
- $\frac{S}{N}=10$
- $\tau= \left( \frac{2k\cdot C_{S}\cdot T'_{sys}}{\Delta S_{\nu}\cdot A_{E}} \right)^{2} \cdot \frac{\Delta\nu}{\frac{S}{N}}$
- $\tau_{l}=4,12s$
- $\tau_{r}=5,22s$
## Determination of the uncertainty of radiant flux measurements

### preliminary work
$S_{\nu}=\frac{P}{4\pi d^2\sqrt{ 2\pi }\sigma}=1263,16Jy$
für mobile radio on the moon (tranmitting with 2W, 900MHz, FWHM:80kHz, $\sigma=34kHz$, recieved on earth

$S_{\nu} \propto \nu^{\alpha}$, $\alpha=-0,7$

bei $\nu=1420.4 MHz$: $S_{\nu,CasA}=1420 ± 70 Jy$
$\frac{1420,4^{-0,7}MHz}{1420 Jy}=c$
$S_{\nu, Cas A}= \frac{900^{-0,7}}{c} Jy = 1954,37 Jy$

$T_{A}= \frac{S_{\nu}A_{e}}{2k_{B}}=1,82K$, für $\nu=1420.4 MHz$ again

TODO: Fehlerfortpflanzung
### evaluation
bbc 3,11
![[Pasted image 20260909124324.png]]
über ds9:
![[Pasted image 20260909134422.png]]

![[Pasted image 20260909134436.png]]

$mean= 1455,83$
$std=212,206$
$std_{scaled}=\sigma[K]=\frac{std}{mean}\cdot T'_{sys}= 15,71K$
$mean_{scaled}[K] = T_{A}(OFF) = 156938,474K$
$T_{A}(ON)=3067\cdot 107,8K=330622,6K$
![[Pasted image 20260909134522.png]]
Antenna Temp of source $T_{s} = \frac{T_{A}(ON)-T_{A}(OFF)+T'_{syy}}{T'_{sys}}=1612,17K$
Rauschen sehr viel größer als erwartet
	vergleich mit theoretischer empflindlichkeit (600Jy, ca. 1K)
	bei uns jtz 128Kanäle, 10s integrierzeit
		also eig sollte es noch besser sein( <<1K)
		aber bei uns viel einfluss von RFI -> ~15K std/rauschen
	empfänger/verstärker sensibilität ist ein problem
		termisches rauschen begrenzt nicht
		aber besser als 1K kanns eig nicht werden

$\frac{S}{N}$ gesucht
- 25 karten für S/N=10
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

# Observation of neutral hydrogen in the Milky Way
## frequency setting of the receiver

### preliminary work

- What is the frequency resolution δ ν, i.e. the bandwidth of a single channel? Then what is the velocity resolution δ υ when observing the H I line?
	- 
- In which channel would you expect the H I line at ν0 = 1420.4 MHz, assuming a radial velocity of 0 kms^−1?
	- 
- You want to measure the radio continuum of a source. What frequencies are allowed within the bandwidth so that the measurement is not be contaminated by the 21cm line. Assume a maximum radial velocity of the H I of ± 200 kms^−1;
	- 
- So which frequency bands should be selected in BBC Tools if you want to observe the H I line once and the continuum once?
	- 

## measurement
$R=R_{0}\cdot \sin(l)$, $R_{0}=8,5kpc$

| $l [deg]$ | $R [kpc]$ | $v_{max} [\frac{km}{s}]$ | $v_{R} \left[ \frac{km}{s} \right]$ |
| --------- | --------- | ------------------------ | ----------------------------------- |
| 10        | 1,48±4,09 | -                        | -                                   |
| 20        | 2,91±4,0  | 70,70±14,50              | ...                                 |
$v_{max}$ grafisch bestimmt (schnittwert mit der organgenen $\sigma$-linie)
$v_{R}=v_{max}+\omega_{0}R_{0}\cdot \sin(l)$
$\omega_{0}R_{0}=220 \frac{km}{s}$
$v_{max,err}$ grafisch über blauen bereich bestimmt (schnittpunkt min-schnittpunkt max/2)
$\Delta l=\pm {2}°$
Fehlerfortpflanzung für R:
	$\Delta R=|\frac{\delta R}{\delta l}|\cdot \Delta l=|R_{0}\cdot \cos(l)|\cdot\Delta l$
	$\sigma_{R}=\sqrt{ |R_{0}\cos(l)|\Delta l }$
$M(R)=0,234\cdot{10}^{10}\left( \frac{v(R)}{\frac{100km}{s}}^2 \right)\left( \frac{R}{kpc} \right)\cdot M_{sun}$
$1M_{sun}=1,98\cdot{10^{30}}kg$
ges: eingeschlossene Masse
## distrib dark matter

$M_{DM}(R_0)=66411575447.22 ± 3593349279.00$













