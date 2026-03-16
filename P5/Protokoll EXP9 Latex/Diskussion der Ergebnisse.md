
### 6.1 Energiemessung und Dynamik

Die experimentell ermittelte kinetische Energie von $E_{kin} = 6,62 \pm 0,27 \text{ keV}$ liegt im erwarteten Betriebsbereich von SALOME, der für Energien bis zu \qty{20}{keV} ausgelegt ist. Der berechnete Lorentzfaktor von $\gamma = 1,013 \pm 0,0005$ bestätigt, dass sich die Elektronen in einem nahezu klassischen Geschwindigkeitsregime bewegen ($v \approx 0,16c$).

Die geringe Energie der Teilchen erklärt zudem die hohe Empfindlichkeit des Strahls gegenüber externen Störfeldern. Wie in der Versuchsdurchführung beobachtet, ist eine präzise Kompensation des Erdmagnetfeldes durch Korrekturdipole zwingend erforderlich, da der Strahl andernfalls bereits nach etwa \qty{60}{cm} die Rohrwandungen touchieren würde.

### 6.2 Emittanz und Strahlqualität

Die Bestimmung der Emittanz ergab eine deutliche Asymmetrie zwischen der horizontalen Ebene ($\epsilon_x = 0,72867 \pm 0,07115 \text{ mm,mrad}$) und der vertikalen Ebene ($\epsilon_y = 1,98349 \pm 0,09011 \text{ mm,mrad}$).

- Die höhere vertikale Emittanz könnte auf eine stärkere Kopplung oder verbleibende Dispersionseffekte in der vertikalen Ebene hindeuten.
#### 6.2.1 Vergleich mit der thermischen Emittanz und Strahlqualität

Ein zentraler Aspekt der Strahlcharakterisierung ist der Vergleich der gemessenen Emittanz mit dem theoretisch erreichbaren Minimum, der thermischen Emittanz $\epsilon_{n,thermisch}$. An SALOME wird der Elektronenstrahl durch eine thermische Kathode (Wolfram, $\Phi_{aus} = 4,5 \text{ eV}$) erzeugt, bei der Elektronen durch Erhitzen die nötige Energie erhalten, um die Austrittsarbeit des Metalls zu überwinden. Die theoretische normierte thermische Emittanz ist dabei durch die Strahlgröße an der Kathode $\sigma_x$ und die Temperatur $T$ definiert: $$\epsilon_{n,thermisch} = \sigma_x \cdot \sqrt{\frac{k_B T}{mc^2}}$$Diese stellt das physikalische Limit dar, da die Geschwindigkeitsverteilung der Elektronen direkt nach dem Austritt der Maxwell-Boltzmann-Verteilung folgt.

In den Messungen wurden für die Emittanz folgende Werte am Ort des Quadrupols V46Match ermittelt: $\epsilon_x = 0,72867 \pm 0,07115 \text{ mm mrad}$, $\epsilon_y = 1,98349 \pm 0,09011 \text{ mm mrad}$

Berücksichtigt man das Produkt $\beta\gamma \approx 0,1614$, ergeben sich die normierten Emittanzen zu $\epsilon_{n,x} \approx 0,118 \text{ mm mrad}$ und $\epsilon_{n,y} \approx 0,320 \text{ mm mrad}$. Es zeigt sich, dass die experimentellen Werte deutlich über dem theoretischen Minimum liegen (die meist in einer Größenordnung von **unter** 0,1 mm mrad liegen). Diese Zunahme der Emittanz lässt sich auf verschiedene physikalische Effekte zurückführen:

Raumladungseffekte (Space Charge): Aufgrund der relativ geringen kinetischen Energie der Elektronen von nur $6,62 \pm 0,27 \text{ keV}$ ist die gegenseitige Abstoßung der Elektronen (Coulomb-Kraft) sehr ausgeprägt. Diese Raumladung wirkt als nichtlineare Kraft, die die Teilchenbahnen im Phasenraum verzerrt und somit zu einer effektiven Zunahme der Emittanz führt.

Nicht-ideale Fokussierung und Aberrationen: Die Strahlführung durch die Solenoid- und Quadrupolmagnete (wie Q57MATCH) unterliegt in der Realität Aberrationen. Nichtlineare Feldkomponenten führen dazu, dass die Transformation im Phasenraum keine perfekte Ellipse erhält, was die gemessene Fläche vergrößert.

Einfluss des Erdmagnetfeldes: Da der Strahl bei diesen niedrigen Energien ohne Korrektur bereits nach ca. $50-60 \text{ cm}$ verloren ginge, muss er permanent durch Korrekturdipole (z. B. V14INJ, H25INJ) auf der Sollbahn gehalten werden. Jede kleinste Dezentrierung in den Quadrupolen führt zu einer Kopplung der Bewegungsebenen, was insbesondere die starke Asymmetrie zwischen $\epsilon_x$ und $\epsilon_y$ erklären könnte.

Nicht-ideales Matching: Wenn die Twiss-Parameter in der Matching Section nicht perfekt an die Akzeptanz der Maschine angepasst sind, oszilliert die Beta-Funktion instabil, was die Empfindlichkeit gegenüber den oben genannten Störfaktoren weiter erhöht.

### 6.3 Optische Funktionen und F0D0-Zellen

Der Verlauf der $\beta$-Funktion (Abbildung 10) demonstriert anschaulich die Funktionsweise der F0D0-Struktur. Die Messpunkte folgen der erwarteten periodischen Oszillation der Einhüllenden (Envelope). Die berechneten Twiss-Parameter wie $\alpha_x = -1,19$ und $\alpha_y = -1,401$ beschreiben eine konvergente Phase der Phasenraumellipse am Eingang des Quadrupols, was auf eine korrekte Abstimmung der Matching Section hindeutet.

### 6.4 Fehlerbetrachtung und Messpräzision

Die Genauigkeit der Ergebnisse wird durch zwei Hauptfaktoren limitiert:

1. Schirmauflösung: Die Auflösung der Kameras von \qty{0,250}{px/mm} sowie die Schirmunsicherheit von \qty{50}{\mu m} beeinflussen direkt die Bestimmung der Strahlbreiten. Dies führt insbesondere bei der Fehlerfortpflanzung auf die $\beta$-Funktion zu Unsicherheiten im Bereich von $0,1$ bis $0,5 \text{ m}$.
2. Statistische Unsicherheit: Die Nutzung der halben Scanschrittweite ($\Delta I/2$) als Fehlermaß für die Justage ist ein konservativer Ansatz, der jedoch durch die stabilen Kontrollmessungen gerechtfertigt wird. Die Übereinstimmung der Schnittpunkte beim Beam-based Alignment belegt, dass systematische Fehler durch eine Dezentrierung des Strahls im Quadrupolfeld erfolgreich minimiert wurden.