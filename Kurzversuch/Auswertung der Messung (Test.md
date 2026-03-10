# aus der mappe schritte

Nachdem die Daten eingelesen sind, müssen für die vollständige Auswertung folgende Schritte  
durchgeführt werden:  
1. Messwerte mitteln, ggf. sortieren oder auf einen Bereich einschränken.  
2. Daten interpolieren, um die Abtastrate zu erhön. 
3. Bestimmung der Position der Maxima (ggf. auch Minima) des Laserinterferogramms.  
4. Bestimmung einer Kalibrierfunktion aus der Lage der Maxima/Minima.  
5. Korrektur der ursprünglichen Ortsachse mit der Kalibrierkurve.  
6. Erneute Interpolation der korrigierten Daten. Damit werden äquidistante Messpunktabstände erzeugt, was für die Fouriertransformation notwendig ist.  
7. Umrechnen der Ortsachse in eine Zeitachse.  
8. Fouriertransformation der Daten zur Berechnung des Spektrums des Lasers.  
9. Ggf. zweiter Iterationsschritt der Kalibrierung, wenn die bestimmte Laserfrequenz bzw. -wellenlänge nicht mit der tatsächlichen übereinstimmt.  
10. Einlesen des Weisslichtinterferogramms, Kalibrierung und Berechnung des Spektrums.  

Um subtile Details in den gemessenen Spektren sichtbar zu machen, ist es sinnvoll, die Daten mit  
einem Referenzspektrum zu korrigieren. Dazu wird typischerweise die optische Dichte OD =  
−log(I/I0) oder aber auch die differentielle optische Transmission (I −I0)/I0 berechnet. I0  
bezieht sich dabei auf das Referenzspektrum. Berechnen Sie wahlweise die OD oder DOT aus  
den Spektren der Jod- und Referenzprobe.

# Datenstruktur und Vorverarbeitung

## Datenformat:
Die vom Computer verwendete Software erzeugt pro Messung für jeden Messkanal eine Datei, die entsprechend des Signalursprungs benannt ist. Hier werden, für jeden der drei aufgenommenen Datensätze, drei Dateien erzeugt \footnote{Channel 0: Probe, Channel 1: Referenz, Channel 2: Laser}. 
Dort werden die Messwerte des jeweiligen Kanals für jeden vom Linearantrieb angefahrenen Messpunkt als ASCII-Dateien gespeichert. Diese sind in 10000 Zeilen angeordnet, da von -5000 bis 4999 insgesamt 10000 Positionen ab- gefahren werden. Pro Position wurden 20 Messwerte aufgenommen. Die erste Spalte enthält immer die Motorposition in Schritten, die darauffolgenden dann die eigentlichen Messwerte. 

Zu Beginn der Datenanalyse werden die Dateien des Lasersignals und später auch die des Weißlichtsignals in das Auswertungsprogramm importiert.

## Mittelung:
Der erste Schritt im Skript ist die Mittelwertbildung der 20 Messwerte pro Position, um das Signal-zu-Rausch-Verhältnis zu verbessern.

# Bestimmung der Kalibrierfunktion

Da die mechanische Bewegung des Linearverschiebetisches nicht exakt linear verläuft und der Antrieb zudem ein gewisses Umkehrspiel aufweist, ist eine numerische Korrektur der Ortsachse nötig. Die Kalibrierung erfolgt anhand des Laser-Interferogramms (Kanal 2), da dessen Wellenlänge ($\lambda_{L}​=532nm$) exakt bekannt ist.

Die Bestimmung der Kalibrierfunktion gliedert sich in folgende Schritte:
- **Interpolation zur Erhöhung der Abtastrate:** Um die Genauigkeit der Peak-Suche zu steigern, werden die gemittelten Laserdaten zunächst um den Faktor 10 interpoliert. Hierbei kommt eine `UnivariateSpline`-Funktion vierten Grades aus der SciPy-Bibliothek zum Einsatz. Die Wahl eines Splines vierten Grades begründet sich dadurch, dass sich die Extrema über die Nullstellen der Ableitung mathematisch besonders präzise bestimmen lassen.
- **Identifikation der Ist-Positionen ($P_{ist​}$​)**: Mithilfe der Funktion `argrelextrema` werden die Maxima des interpolierten Lasersignals identifiziert. Diese Maxima markieren die realen Positionen ($P_{ist​}$​) des Spiegels im Interferogramm.
- **Berechnung der Soll-Positionen ($P_{soll​}$​) via linearer Regression:** Im idealen Fall einer völlig linearen Bewegung müssten diese Maxima in äquidistanten Abständen liegen. Über eine lineare Regression der Form $P_{soll​}​(i)=a⋅i+b$ werden daher die theoretischen Soll-Positionen für jedes Maximum bestimmt.
- **Erzeugung der kontinuierlichen Korrekturfunktion:** Die lokale Abweichung der Motorbewegung berechnet sich an den Stützstellen zu $Δ(i)=P_{soll}​(i)−P_{ist​}(i)$. Um diese Korrektur auf den gesamten Datensatz und beliebige Motorpositionen anwenden zu können, wird der diskrete Verlauf von $\Delta$ erneut interpoliert. Das resultierende Funktions-Objekt stellt somit für jeden Messpunkt einen individuellen Korrekturwert zur Linearisierung der Ortsachse bereit.
# Korrektur der Weißlichtdaten und äquidistantes Gitter

Nachdem die Kalibrierung feststeht, wird sie auf die Proben- und Referenzdaten angewendet.

- **Ortskorrektur:** Die ursprüngliche Ortsachse der Weißlichtdaten wird durch Addition der Korrekturfunktion begradigt.
- **Äquidistanz:** Für die FFT ist ein äquidistantes Gitter zwingend erforderlich. Die korrigierten Daten müssen daher erneut auf ein gemeinsames Gitter für Probe und Referenz interpoliert werden.
# Transformation in den Zeit- und Frequenzraum

- **Ort zu Zeit:** Die Weglängendifferenz Δs wird unter Verwendung der Laserwellenlänge (λL​=532 nm) und der Lichtgeschwindigkeit c in die Zeitverzögerung Δt=Δs/c umgerechnet.
- **Fouriertransformation:** Mithilfe der Funktionen `fft` und `fftshift` wird das Interferogramm (die Autokorrelationsfunktion) in das Spektrum transformiert. Laut Wiener-Khinchin-Theorem ist das Interferogramm die Fourier-Transformierte der spektralen Energiedichte.
# Berechnung von OD und DOT

Um die Absorptionsmerkmale der Proben (Notch-Filter und Iod-Küvette) hervorzuheben, vergleichst du das Probenspektrum (I) mit dem Referenzspektrum (I0​).
- **Optische Dichte (OD):**$$ OD=−log10​(I/I0​)$$
- **Differentielle optische Transmission (DOT):** $$DOT=(I−I0​)/I0$$

