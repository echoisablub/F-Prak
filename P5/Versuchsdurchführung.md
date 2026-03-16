
### 1. Strahltransport und Erdmagnetfeldkompensation

Der erste Schritt der experimentellen Durchführung bestand darin, einen stabilen Strahltransport durch die gesamte, \qty{6}{m} lange Anlage zu realisieren. Hierzu wurden die Elektronen sukzessive auf den fünf fluoreszierenden Schirmen zentriert, indem die Ströme der Korrekturdipole (z. B. V14INJ und H25INJ) iterativ angepasst wurden. Ein besonderes Augenmerk galt der Kompensation des Erdmagnetfeldes, welches aufgrund der geringen Elektronenenergie von max. \qty{20}{keV} eine signifikante Ablenkung verursacht; ohne diese Korrektur wäre der Strahl bereits nach ca. \qty{60}{cm} verloren gegangen.

### 2. Strahlbasierte Justage (Beam-based Alignment)

Um systematische Fehler bei der Emittanzmessung zu minimieren, wurde eine strahlbasierte Justage am Quadrupol Q57MATCH durchgeführt. Ziel war es, den Strahl exakt auf der magnetischen Achse des Quadrupols zu zentrieren, damit eine Variation der Quadrupolstärke keine zusätzliche Ablenkung des Strahls verursacht. Methodisch wurde dies durch zwei Stromscans des vorlaufenden Dipols bei unterschiedlichen Quadrupolstärken ($I_{Q1}$ und $I_{Q2}$) realisiert. Der Schnittpunkt der resultierenden Regressionsgeraden im $x/I$-Diagramm definiert den Korrekturstrom $I_{D0}$, bei dem der Strahl das Quadrupolzentrum passiert.

### 3. Energiemessung mittels Dipol-Ablenkung

Die Bestimmung der kinetischen Energie erfolgte über die vertikale Ablenkung des Strahls in einem Dipolmagneten. Hierzu wurde die zeitlich gemittelte Strahlposition $\langle y \rangle$ auf Schirm 3 in Abhängigkeit des Dipolstroms $I$ in Schritten von \qty{0,1}{A} gemessen. Unter Verwendung der dipolspezifischen Konstante $\kappa = 7,64 \cdot 10^{-6},\text{Tm/A}$ und der Driftstrecke $L$ wurde aus der Steigung $dy/dI$ der relativistische Impuls $p$ und daraus die kinetische Energie $E_{kin}$ abgeleitet. Die Bildauswertung erfolgte über den Video Client mit einem Umrechnungsfaktor von ca. \qty{0,25}{mm/px}.

### 4. Emittanzbestimmung (Quadrupol-Scan)

Zur Bestimmung der transversalen Emittanz wurde ein Quadrupol-Scan mit dem Magneten V46Match durchgeführt. Dabei wurde die Quadrupolstärke $k$ systematisch variiert (für $x$: \qty{0,6}{A} bis \qty{1,6}{A}; für $y$: \qty{-0,6}{A} bis \qty{-1,6}{A}) und die quadratische Strahlgröße $\sigma^2$ auf dem nachfolgenden Schirm aufgezeichnet. Die Extraktion der Emittanz am Ort des Quadrupols erfolgte durch Anwendung der Normalengleichung auf das lineare Gleichungssystem, welches die gemessenen Strahlgrößen über die Transfermatrix $A$ mit der Beam-Matrix verknüpft.

### 5. Messung der Beta-Funktion (Multiple-Screen)

Die räumliche Entwicklung der Beta-Funktion $\beta(z)$ wurde durch Messung der RMS-Strahlbreiten an den vier Diagnostikstationen der _Diagnostic Section_ (Schirme 3 bis 6) sowie durch Extrapolation des Wertes am Quadrupol-Eingang bestimmt. Methodisch wurde hierbei die zuvor ermittelte Emittanz $\epsilon$ genutzt, um aus den gemessenen Strahlgrößen $\sigma^2$ an den Positionen $z$ die Amplitudenfunktion gemäß $\beta(z) = \sigma^2(z) / \epsilon$ zu berechnen. Dies erlaubt eine Verifizierung der Fokussierungswirkung innerhalb der F0D0-Struktur.

