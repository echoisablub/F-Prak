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

**Datenformat:** 
Die vom Computer verwendete Software erzeugt pro Messung für jeden Messkanal eine Datei, die entsprechend des Signalursprungs benannt ist. Hier werden, für jeden der drei aufgenommenen Datensätze, drei Dateien erzeugt \footnote{Channel 0: Probe, Channel 1: Referenz, Channel 2: Laser}. 
Dort werden die Messwerte des jeweiligen Kanals für jeden vom Linearantrieb angefahrenen Messpunkt als ASCII-Dateien gespeichert. Diese sind in 10000 Zeilen angeordnet, da von -5000 bis 4999 insgesamt 10000 Positionen ab- gefahren werden. Pro Position wurden 20 Messwerte aufgenommen. Die erste Spalte enthält immer die Motorposition in Schritten, die darauffolgenden dann die eigentlichen Messwerte. 

Zu Beginn der Datenanalyse werden die Dateien des Lasersignals und später auch die des Weißlichtsignals in das Auswertungsprogramm importiert.

**Mittelung:** 
Der erste Schritt im Skript ist die Mittelwertbildung der 20 Messwerte pro Position, um das Signal-zu-Rausch-Verhältnis zu verbessern.

# Bestimmung der Kalibrierfunktion

Da die Motorbewegung nicht exakt linear verläuft, muss man die Daten anhand einer Kalibrierfunktion korrigieren.
Für diese Kalibrierfunktion 
Dafür werden die Laserdaten zuerst interpoliert, um die Abtastrate zu erhöhen (siehe ... cite).
Für die Interpolation wurde eine UnivariateSpline vom Grad 4 aus der Scipy-Bibliothek ausgewählt.
Es wurde um einen Faktor von 10 interpoliert.

Die Kalibrierfunktion ordnet jeder existierenden Motorposition $P_{ist}$ eine "Soll-Position" $P_{soll}$ zu.
Dafür wurden die Maxima der interpolierten Laserdaten durch die argrelextrema Funktion aus der Scipy Bibliothek
bestimmt. Diese Maxima sind die $P_{ist}$, denen mithilfe einer linearen Regression ihre $P_{soll}$-Werte
zugeordnet werden.
Die Kalibrierfunktion $\Delta(i)=P_{soll}(i)-P_{ist}(i)$ wird erst nur durch die Korrektur der Maxima
berechnet und dann interpoliert, sodass sie auch auf die anderen Motorpositionen anwendbar ist.