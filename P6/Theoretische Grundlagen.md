# 1. Erzeugung von Röntgenstrahlung & Pump-Probe-Prinzip
Lichtquellen und Messmethode
## Synchrotronstrahlung (SR) vs. Freie-Elektronen-Laser (FEL)
- Entstehung von Synchrotronstrahlung durch Ablenkung relativistischer Elektronen im Magnetfeld
- Eigenschaften von SR: kontinuierliches Spektrum, hohe Intensität und Pulsung im Pikosekundenbereich
- Funktionsweise von Linearbeschleunigern und extrem langen **Undulatoren** zur Erzeugung kohärenter, femtosekunden-gepulster Röntgenstrahlung
## Der SASE-Effekt (Self-Amplified Spontaneous Emission)
- Wechselwirkung zwischen Elektronenpaketen und emittierter Strahlung im Undulator, die zu einer Dichtemodulation (**Microbunching**) führt
- Erklärung der extremen Brillanz und lateralen Kohärenz sowie der typischen stochastischen "pinken" SASE-Spektralstruktur (Spikes)
### 4. SASE-Undulatorstrahlung: Erzeugung der Röntgenpulse
Die fundamentale Wellenlänge $\lambda$ der in Vorwärtsrichtung emittierten Undulatorstrahlung unter Berücksichtigung relativistischer Effekte (Lorentzkontraktion im Elektronenruhesystem und relativistischer Dopplereffekt im Laborfernrohr) beträgt:
$$\lambda(\theta) = \frac{L}{2\gamma^2} \left( 1 + \frac{K^2}{2} + \gamma^2\theta^2 \right)$$
- **$L$:** Die Periodenlänge des Magnetfeldes des Undulators (z. B. $4\text{ cm}$ beim European XFEL).
- **$\theta$:** Der Beobachtungswinkel relativ zur Strahlachse.
- **$K$:** Der dimensionslose Undulatorparameter, welcher über die Magnetfeldstärke $B$ variiert wird, um die Wellenlänge kontinuierlich abzustimmen: 
$$
K = \frac{e \cdot B \cdot L}{2\pi \cdot m_e \cdot c}
$$
- **$\gamma$:** Der relativistische Lorentz-Faktor der Elektronen mit der kinetischen Energie $E_{kin}$ und der Ruhemasse $m_e$:
$$\gamma = \frac{E_{kin}}{m_e c^2} \approx 1957 \cdot \frac{E_{acc}}{\text{GeV}}$$

## Das Pump-Probe-Prinzip
Anregung des Systems durch einen optischen Laserpuls ("Pump") und zeitverzögerte Abfrage durch den Röntgenpuls ("Probe").
### Grundproblem: Zeitskala molekularer Bewegung
Chemische Reaktionen – wie das Brechen oder Bilden von Bindungen, Molekülschwingungen sowie Energie- und Ladungstransfers – laufen extrem schnell ab. Sie bewegen sich typischerweise im Bereich von einigen Femtosekunden $10^{-15}\text{ s}$ bis hin zu Pikosekunden $10^{-10}\text{ s}$

Da kein elektronischer Detektor der Welt schnell genug ist, um solche Prozesse direkt "live" zu stoppen, nutzt man zwei ultrakurze Lichtpulse, die zeitlich extrem präzise gesteuert nacheinander auf die Probe treffen.
### Pump-Puls / Probe-Puls
1. **Der Pump-Puls (Anregungspuls):**
    - **Was er tut:** Dieser Puls fungiert als Startschuss. Er regt das Molekülsystem zu einem wohldefinierten Zeitpunkt ($t = 0$) aus seinem thermischen Grundzustand in einen energetisch höheren Zustand an.
    - **Im Experiment:** Ein ultrakurzer **optischer Laserpuls** im sichtbaren oder UV-Bereich (z. B. bei 400 nm) regt den Eisenkomplex $[Fe(bipy)_3]^{2+}$ aus seinem Singulett-Low-Spin-Grundzustand ($^1A_1$) in den angeregten $^1\text{MLCT}$-Zustand (Metal-to-Ligand Charge Transfer) an. Damit ist die photophysikalische Reaktion gestartet.
2. **Der Probe-Puls (Abfragepuls):**
    - **Was er tut:** Ein zweiter, zeitverzögerter Puls trifft auf die Probe und "fotografiert" den augenblicklichen Zustand des angeregten Systems.
    - **Im Experiment:** Dies ist ein **ultrakurzer Röntgenpuls** des European XFEL. Er ionisiert ein 1s-Rumpfelektronen des zentralen Eisenatoms. Die anschließende Röntgenemission ($K\beta$-XES) wird gemessen, welche extrem empfindlich auf den aktuellen Spin- und Strukturzustand des Eisens reagiert.
### Die Zeitverzögerung $\Delta t$ / "Molecular Movie"
Der Schlüssel zur Zeitauflösung liegt in der variablen Verzögerung des Probe-Pulses relativ zum Pump-Puls:
$$\Delta t = t_{\text{Röntgen}} - t_{\text{Laser}}$$
- **Der mechanische Trick:** Da Licht sich mit einer konstanten Geschwindigkeit ausbreitet (ca. $300\, \mu\text{m}$ in $1\text{ ps}$ oder $30\,\mu\text{m}$ in $100\text{ fs}$), steuert man die Verzögerung $\Delta t$ oft über die optische Weglänge des Lasers mittels hochpräziser Verzögerungsstrecken.
- **Der "Molecular Movie":**
    - Das Experiment wird für **verschiedene, diskrete Zeitverzögerungen $\Delta t$** wiederholt.
    - Bei negativen Verzögerungen ($\Delta t < 0$) kommt das Röntgenlicht _vor_ dem Laser an – wir messen den reinen Grundzustand.
    - Bei $\Delta t = 0$ überlappen sich beide Pulse perfekt im Raum und in der Zeit.
    - Bei positiven Verzögerungen ($\Delta t > 0$) misst das Röntgenlicht die sich entwickelnde Dynamik. Setzt man diese "Einzelbilder" (Spektren) bei unterschiedlichen $\Delta t$ wie Daumenkinos aneinander, erhält man einen **molekularen Film** der Reaktion.
### Messsignal: transiente Differenzspektrum
Da sich im Jet-Flüssigkeitsstrahl meist nur ein kleiner Bruchteil aller Moleküle im angeregten Zustand befindet, wäre das reine angeregte Spektrum kaum sichtbar. Daher nutzt man das **transiente Signal (Differenzspektrum)**:
$$\text{Transientes Signal} = I_{\text{Laser an}}(\Delta t) - I_{\text{Laser aus}}$$
Dieses Differenzsignal zeigt direkt die physikalischen Veränderungen:
- **Negative Beiträge (Bleichen/Depopulation):** Orte im Spektrum, an denen die Intensität abnimmt, weil der Grundzustand durch den Laser entleert wurde.
- **Positive Beiträge (Transiente Zustände):** Neue spektrale Merkmale (wie das Aufwachsen des spin-sensitiven $K\beta'$-Satellitenpeaks bei ca. 7046 eV), die beweisen, dass intermediäre Zustände (wie der kurzlebige Triplet-Zustand oder der langlebige Quintett-High-Spin-Zustand $^5T_2$) besetzt wurden.

Trägt man die Intensität an diesen markanten Energiepositionen gegen die Zeitverzögerung $\Delta t$ auf, erhält man die **kinetischen Spuren (kinetic traces)**, aus denen sich die Lebensdauern der Übergangszustände präzise mathematisch fitten lassen.
### Zeitliche Jitter
Da der optische Pump-Laser und der Röntgen-FEL in getrennten Systemen erzeugt werden, driften ihre Ankunftszeiten auf der Femtosekunden-Skala minimal gegeneinander ab (stochastischer **Jitter** von ca. 100 bis 300 fs FWHM).

Um die Zeitauflösung nicht zu verschmieren, misst der **Time Arrival Detector (TAD)** an der FXE-Station für jeden einzelnen Schuss die exakte relative Ankunftszeit (mittels räumlicher oder spektraler Dekodierung an einer dünnen Membran). Diese Information wird im Nachhinein genutzt, um die Daten präzise zeitlich zu sortieren und zu mitteln.
# 2. Das untersuchte Molekülsystem & Photophysik
Eisenkomplexes $[Fe(bipy)_3]^{2+}$
## Ligandenfeldtheorie & d-Orbital-Aufspaltung
- Elektrostatische Wechselwirkung der Liganden im oktaedrischen Feld (D3-Symmetrie).
- Aufspaltung der entarteten d-Orbitale des $Fe^{2+}$($d^6$-Konfiguration) in die energetisch niedrigeren $t_{2g}$-Orbitale und die höheren $e_g$-Orbitale um den Betrag $\Delta_{oct}$ (oder $10Dq$).
## High-Spin- (HS) und Low-Spin-Zustände (LS)
- Konkurrenz zwischen der Spinpaarungsenergie und der Ligandenfeldaufspaltung $\Delta_{oct}$.
- Charakterisierung des LS-Grundzustands $(^1A_1$, S=0, Singulett) und des metastabilen HS-Zustands $(^5T_2$, S=2, Quintett) des Komplexes.
- Einfluss der Besetzung auf die Fe-N-Bindungslänge (Verlängerung im HS-Zustand durch Besetzung antibindender $e_g$-Orbitale).

# 3. Der optische Anregungs- und Relaxationsprozess (Pump-Puls)
Was löst die optische Anregung im Molekül aus?
## Molarer Extinktionskoeffizient & Lambert-Beer-Gesetz
- Mathematische Beschreibung der Lichtschwächung beim Durchgang durch das Probenmedium.
### Lambert-Beer-Gesetz
Die Abschwächung der Intensität $I(\lambda)$ beim Durchgang durch die Probe der Dicke $d$ wird chemisch (dekadisch) beschrieben durch:$$
I(\lambda) = I_0(\lambda) \cdot 10^{-\varepsilon(\lambda) \cdot c \cdot d}
$$
- **$\varepsilon(\lambda)$:** Der molare, dekadische Extinktionskoeffizient (in $\text{L mol}^{-1}\text{cm}^{-1}$).
- **$c$:** Die Stoffmengenkonzentration der Lösung (in $\text{mol L}^{-1}$).
- **$d$:** Die Schichtdicke des Flüssigkeitsstrahls (Liquid Jet, $d \approx 25,\mu\text{m}$ bis $100,\mu\text{m}$).

Daraus resultiert die dimensionslose dekadische Extinktion (Optical Density, $A_{OD}$):
$$A_{OD} = -\lg\left(\frac{I}{I_0}\right) = \varepsilon(\lambda) \cdot c \cdot d$$
## Auswahlregeln (Laporte- und Spin-Auswahlregel)

- Warum direkte d-d-Übergänge dipol-verboten sind und wie Schwingungskopplung (**vibronic coupling**) diese teilweise erlaubt.
## Metal-to-Ligand Charge Transfer (MLCT)

- Anregung eines Elektrons aus einem metallischen d-Orbital $(t_{2g}$) in ein antibindendes $\pi^*$-Orbital des Bipyridin-Liganden.
## Relaxationskaskade (Jablonski-Diagramm)

- Ultraschnelle nicht-radiative Relaxationsprozesse: **Internal Conversion (IC)** unter Erhaltung der Multiplizität.
- **Intersystem Crossing (ISC)** mit Spin-Flip (Übergang vom $^1\text{MLCT}$ über $^3\text{MLCT}$ und eventuell transiente $^3T_1$-Zustände in den metastabilen $^5T_2$-Zustand) auf einer Zeitskala von $<100\text{ fs}$.

# 4. Röntgenwechselwirkung, Emission & Detektion (Probe-Puls)
Wechselwirkung der Röntgenprobe mit der Probe
## Element- und schalen-spezifische Röntgenabsorption
- Dominanz des photoelektrischen Effekts im harten Röntgenbereich.
- Die K-Absorptionskante von Eisen bei ca. $7112\text{ eV}$ (Anregung von 1s-Rumpfelektronen) im Vergleich zu leichteren Elementen der Lösung.
### Photoelektronen-Wellenzahl (EXAFS-Analogie)
Falls du in deinen theoretischen Grundlagen kurz die kinetische Energie des durch den harten Röntgenpuls ausgeschlagenen K-Schalen-Photoelektrons und dessen De-Broglie-Wellenzahl $k$ beschreiben möchtest (wichtig für den physikalischen Hintergrund der Streuung an Nachbaratomen):
$$
k = \frac{\sqrt{2m_e (E_{X-ray} - |E_{1s}|)}}{\hbar} \approx 0{,}512 \cdot \sqrt{E_{X-ray} - |E_{1s}| \text{ [in eV]}} \quad (\text{in } \text{AA}^{-1})
$$

- **$E_{Xray}$:** Die Energie des einfallenden Röntgenquants (oberhalb der K-Kante, $E_{Xray} > 7112\text{ eV}$).
- **$E_{1s}$:** Die Bindungsenergie des Fe-1s-Rumpfelektrons ($7112\text{ eV}$).
## Röntgenemissionsspektroskopie (XES) & Fluoreszenzausbeute
- Zerfall des Lochzustands im 1s-Orbital durch Nachrücken von Elektronen aus höheren Schalen.
- Konkurrenz zwischen strahlungslosem Auger-Effekt (ca. 70 %) und Röntgenfluoreszenz (ca. 30 % bei Eisen).
- Unterscheidung zwischen resonantem und nicht-resonantem XES.
- Nomenklatur der Emissionslinien $(K\alpha$ für $2p \rightarrow 1s$, $K\beta$ für $3p \rightarrow 1s$).
## Spin-Sensitivität der $K\beta$-Emissionslinien
- Physikalische Ursache des Satellitenpeaks $(K\beta'$) durch Austauschwechselwirkung zwischen den ungepaarten Elektronen im $3d$-Zustand und dem Loch im $3p$-Zustand.
- Verwendung des $K\beta$-Spektrums zur eindeutigen Unterscheidung zwischen dem LS-Grundzustand und dem optisch erzeugten HS-Zustand.
# 5. Experimenteller Aufbau, Strahlmanipulation und Diagnosekomponenten
Apparativen Komponenten, die zur Strahlführung, Diagnose und Messung genutzt werden.
### Zeitliche Pulsform und Fluenz (Gauß-Profil)
Röntgen- und Laserpulse lassen sich räumlich und zeitlich hervorragend als Gauß-Profile modellieren. Die Intensität $I(r, t)$ im Abstand $r$ zur Strahlachse zum Zeitpunkt $t$ lautet: $$
I(r, t) = I_0 \cdot \exp\left( -2\frac{r^2}{w_0^2} \right) \cdot \exp\left( -\frac{t^2}{\Delta t^2} \right)$$
- **$w_0$:** Der Strahltaillenradius (Intensitätsabfall auf $1/e^2$).
- **$\Delta t$:** Die charakteristische Pulsdauer (Intensitätsabfall auf $1/e$).
Die experimentell zugänglichen Halbwertsbreiten (**FWHM**) hängen mit diesen Parametern wie folgt zusammen: $$\begin{align}
	d_{FWHM} &= w_0 \cdot \sqrt{2 \ln 2} \approx 1{,}18 \cdot w_0 \\
	t_{FWHM} &= \Delta t \cdot \sqrt{4 \ln 2} \approx 1{,}67 \cdot \Delta t
\end{align}$$Die effektive Bestrahlungsfläche $A_{eff}$ der Probe im Fokus ergibt sich zu:$$
A_{eff} = \frac{\pi \cdot d_{FWHM}^2}{4 \ln 2} \approx 1{,}13 \cdot d_{FWHM}^2
$$
## Strahlablenkung und Transport
- Planarspiegel (M1, M2, M3) zur Elimination hochenergetischer Untergrundstrahlung.
## Monochromatisierung (Bragg-Reflexion)
- Physikalische Grundlage der Bragg-Gleichung
	Die konstruktive Interferenz an den Gitterebenen des Analysatorkristalls folgt der Bragg-Bedingung: $$n \cdot \lambda = 2d_{hkl} \cdot \sin(\theta_B)$$
		- **$\lambda$:** Die Wellenlänge der emittierten Röntgenstrahlung.
		- **$d_{hkl}$:** Der Netzebenennabstand des gewählten Kristallschnitts (z. B. Si(111)).
		- **$\theta_B$:** Der Bragg-Winkel (Glanzwinkel).
		- **$n$:** Die Beugungsordnung.
- **4-Crystal Monochromator (4BCM):** Monochromatisierung des "pinken" [[## Der SASE-Effekt (Self-Amplified Spontaneous Emission):|SASE-Strahls]] zu einem schmalbandigen Strahl ohne Strahlversatz (Darwin-Breite von Si(111)).
## Röntgenfokussierung mittels Beryllium-Linsen (CRLs)
- Physikalische Erklärung von **Compound Refractive Lenses** durch anomale Dispersion, bei der der Realteil des Brechungsindex $n = 1 - \delta + i\beta$ kleiner als 1 ist $\delta > 0$).
- Daraus resultierende Notwendigkeit _konkaver_ Linsengeometrien zur Fokussierung.
### Fokussierung mit Beryllium-Linsen (CRLs)

Im Röntgenbereich verhält sich der komplexe Brechungsindex $n$ anomal, da die Phasegeschwindigkeit der Strahlung in Materie größer als die Vakuumlichtgeschwindigkeit ist. Der Brechungsindex wird beschrieben als:
$$
n(\lambda) = 1 - \delta(\lambda) + i \cdot \beta(\lambda)
$$
- **$\delta$ (Realteil-Dekrement):** Beschreibt die Lichtbrechung. Für Beryllium (Be) nimmt $\delta$ sehr kleine positive Werte an (z. B. $\delta \approx 1{,}6 \times 10^{-8}$ bei $12\text{ keV}$). Da der Realteil $n_R = 1 - \delta < 1$ ist, müssen Röntgenlinsen im Gegensatz zu optischen Linsen **konkav** geformt sein, um eine fokussierende Wirkung zu erzielen.
- **$\beta$ (Imaginärteil):** Beschreibt die Photoabsorption des Linsenmaterials. Da Beryllium eine sehr niedrige Ordnungszahl ($Z = 4$) besitzt, bleibt die unerwünschte Absorption minimal.

Da die Brechkraft einer einzelnen Linse extrem gering ist ($F \approx 10\text{ m}$ bis $100\text{ m}$), werden $N$ Einzellinsen zu einer fokussierenden **Compound Refractive Lens (CRL)** hintereinandergeschaltet. Die effektive Brennweite $F$ dieses Linsenpakets berechnet sich nach:
$$F = \frac{R}{2 N \delta}$$

- **$R$:** Der Scheitelkrümmungsradius der parabolischen Linsenflächen (typischerweise $0{,}5\text{ mm}$ bis $1{,}5\text{ mm}$ im Experiment).
- **$N$:** Die Anzahl der aktiven Linsenelemente im Strahlweg.
## Diagnose- und Überwachungsgeräte
- **Beam Imaging Units (BIU):** Szintillationsfolien (YAG-Kristall / pCVD-Diamant) zur 2D-Strahlprofilüberwachung.
- **Intensity and Position Monitor (IPM):** Orts- und intensitätsaufgelöste Messung einzelner Pulse mittels Compton-Rückstreuung an einer Diamantfolie auf vier Quadranten-Avalanche-Photodioden (APDs).
- **Spectrum Analyzer (SpA):** Messung der stochastischen Einzelpuls-[[## Der SASE-Effekt (Self-Amplified Spontaneous Emission):|SASE]]-Fluktuationen über gebogene Kristalldiffraktion auf Gotthard-Streifendetektoren.
- **Time Arrival Detector (TAD):** Räumliche oder spektrale Dekodierung des zeitlichen Jitters (fs-Skala) zwischen optischem Laser und Röntgenpuls zur exakten Bestimmung des Zeitpunkts Null.
## Probenumgebung & Sekundärspektrometer
- **Liquid Jet:** Erzeugung eines laminaren Flüssigkeitsstrahls (Sapphirdüsen) zur kontinuierlichen Erneuerung des angeregten Probenvolumens.
- **Large Pixel Detector (LPD):** Detektion elastischer Vorwärtsstreuung (XSS/XRD) zur Strukturaufklärung.
- **von Hamos-Spektrometer:** Energiedispersive Anordnung mit zylindrisch gekrümmten Kristallen zur simultanen Abbildung des gesamten emittierten Energiespektrums auf einen Jungfrau-2D-Detektor.
### Von Hamos-Spektrometer
Das von Hamos-Spektrometer nutzt [[## **Monochromatisierung (Bragg-Reflexion):**|Bragg-Reflexion]] an zylindrisch gekrümmten Einkristallen zur wellenlängendispersiven Messung.
#### Geometrie und Dispersion
In der von Hamos-Geometrie befinden sich die Probe (Emissionsquelle) und der Detektor auf der Symmetrieachse des zylindrisch gekrümmten Kristalls mit dem Radius $R$. Der Abstand zwischen Probe und Detektor beträgt $2a$.

Aus der Geometrie ergibt sich die räumliche Position $z$ des reflektierten Signals auf dem Detektor entlang der Dispersionsachse relativ zum Kristallmittelpunkt:$$
z(\lambda) = \frac{R}{\tan(\theta_B)} = R \cdot \sqrt{\left(\frac{2d_{hkl}}{n\lambda}\right)^2 - 1}
$$Der messbare spektrale Energiebereich $\Delta E$ des Detektors relativ zur zentralen Energie $E$ ist durch die Strahlbreite $H$ und den Krümmungsradius $R$ des Kristalls beschränkt:
$$\frac{\Delta E}{E} \approx \cot(\theta_B) \frac{H}{R \sin(\theta_B)}$$