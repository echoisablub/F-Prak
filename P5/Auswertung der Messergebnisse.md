# 5. Auswertung der Messergebnisse

### 5.1 Strahltransport

Zu Beginn des Experiments wurde der Elektronenstrahl erfolgreich durch die gesamte Beschleunigerstrecke bis zum Beam-Dump transportiert. Hierzu wurden die Ströme der horizontalen und vertikalen Dipolpaare iterativ angepasst, bis der Strahl auf allen fünf fluoreszierenden Schirmen zentriert abgebildet werden konnte. Die Orientierung erfolgte an den Live-Bildern der Kameras, wobei insbesondere das Erdmagnetfeld durch die Korrekturdipole kompensiert werden musste, um einen vorzeitigen Strahlverlust nach ca. 60,cm zu verhindern.


Zu Beginn des Experiments wurde der Elektronenstrahl erfolgreich durch die gesamte, \qty{6}{m} lange Beschleunigerstrecke von der Kathode bis zum Beam-Dump transportiert. Das primäre Ziel dieses Arbeitsschrittes war es, die Dipolströme so zu optimieren, dass der Strahl das Strahlrohr möglichst mittig durchquert, um Strahlverluste an den Rohrwandungen zu vermeiden.

Hierzu wurden die horizontalen und vertikalen Dipolpaare iterativ angepasst, während die Strahlposition sukzessive auf den fünf fluoreszierenden Schirmen (Schirm 2 bis 6) mithilfe der zugehörigen Kameras überwacht wurde. Ein kritischer Aspekt war dabei die Kompensation des Erdmagnetfeldes durch die Korrekturdipole V14INJ und H25INJ zu Beginn der Beschleunigerstrecke. Aufgrund der geringen kinetischen Energie der Elektronen von maximal \qty{20}{keV} hat das Erdmagnetfeld einen so starken Einfluss, dass der Strahl ohne diese Korrektur bereits nach einer Strecke von ca. \qty{50}{cm} bis \qty{60}{cm} verloren gegangen wäre.

Die für den stabilen Transport ermittelten Magneteinstellungen sind in \autoref{fig:einstellungenstrahltransport} dokumentiert. In \autoref{fig:fuenf_bilder_gesamt} sind die resultierenden Strahlprofile dargestellt, wie sie auf den Schirmen entlang der Matching- und Diagnostic-Section aufgenommen wurden. Die Aufnahmen zeigen einen gut fokussierten und zentrierten Strahl auf allen Stationen. Dieser erfolgreiche Strahltransport bildete die notwendige Grundlage für die präzise Durchführung der nachfolgenden strahlbasierten Justage und der Emittanzmessung.

### 5.2 Strahlbasierte Justage

Um sicherzustellen, dass der Strahl den Quadrupol Q57MATCH exakt auf der magnetischen Achse durchquert, wurde ein Beam-based Alignment durchgeführt.

- **x- und y-Werte:** Durch Variation des Dipolstroms bei zwei unterschiedlichen Quadrupolstärken ($I_{Q1}$ und $I_{Q2}$) wurden Regressionsgeraden ermittelt, deren Schnittpunkt den magnetischen Mittelpunkt $I_{D0}$ definiert. Für die horizontale Ausrichtung (Abbildung 2) ergab sich ein Korrekturstrom von $I_{D0,x} = -1,236\text{A}$. Für die vertikale Ausrichtung (Abbildung 3) wurde ein Wert von $I_{D0,y} = -0,686\text{A}$ bestimmt.
- **Fehlerbetrachtung:** Die Unsicherheit der Justage wurde konservativ als die Hälfte der gewählten Scanschrittweite ($\Delta I/2$) angesetzt. Dies resultiert in einem Fehler von $\pm 0,0532\text{A}$ für die x-Achse und $\pm 0,0935\text{A}$ für die y-Achse. Die Kontrollmessungen in Abbildung 4 und 5 bestätigen den Erfolg der Justage, da die Strahlposition innerhalb der Fehlergrenzen stabil bleibt, wenn die Quadrupolstärke variiert wird [159, Gesprächshistorie].

### 5.3 Energiemessung

Die **kinetische Energie** der Elektronen wurde über die vertikale Ablenkung in einem Dipolmagneten bestimmt. Aus der linearen Regression der Strahlposition über dem Magnetstrom ergab sich eine Steigung von **$\frac{dy}{dI} = 14,4384 \pm 0,106 \text{ mm/A}$**. Unter Verwendung der dipolspezifischen Konstante **$\kappa = 7,64 \cdot 10^{-6} \text{ Tm/A}$**, der Driftstrecke **$L = 0,52 \pm 0,01 \text{ m}$** und der Ruheenergie der Elektronen von **$E_0 = 511 \text{ keV}$** wurde zunächst das Produkt **$\beta\gamma = 0,1614 \pm 0,00332$** ermittelt, was aufgrund der geringen Geschwindigkeit näherungsweise $\beta$ entspricht.

Daraus resultiert ein Lorentzfaktor von **$\gamma = 1,013 \pm 0,000529$**, was auf ein nahezu klassisches Geschwindigkeitsregime hindeutet. Die finale kinetische Energie wurde zu $E_{kin} = 6,62 \pm 0,27 \text{ keV}$ berechnet. Der entsprechende Impuls der Teilchen wurde mit $p = 2,752 \cdot 10^{-7} \pm 5,661 \cdot 10^{-9} \text{ keV/c}$ bestimmt. Die angewandte Fehlerfortpflanzung berücksichtigt hierbei konsequent die Unsicherheiten der Geometrie ($L$) sowie der experimentell ermittelten Steigungsmessung ($dy/dI$).
### 5.4 Emittanz

Die Emittanz wurde mittels eines Quadrupol-Scans am Ort des Magneten bestimmt, indem die transversalen Strahlgrößen auf dem Schirm als Funktion der Quadrupolstärke $k$ gemessen wurden. Durch Anwendung der Normalengleichung für die lineare Regression ergaben sich folgende Werte für die Emittanz:

- $\epsilon_x = 0,72867 \pm 0,07115,\text{mm,mrad}$.
- $\epsilon_y = 1,98349 \pm 0,09011,\text{mm,mrad}$.

#### 5.4.1 Optische Funktionen

Basierend auf der Emittanz wurden die Twiss-Parameter am Eingang des Quadrupols berechnet. Diese beschreiben die Form und Ausrichtung der Phasenraumellipse. Die ermittelten Werte lauten:

- $\beta_x = 0,578 \pm 0,057, \alpha_x = -1,19 \pm 0,117, \gamma_x = 4,19 \pm 0,41$.
- $\beta_y = 0,814 \pm 0,037, \alpha_y = -1,401 \pm 0,064, \gamma_y = 3,639 \pm 0,165$. Hierbei wurde vorausgesetzt, dass der relative Fehler der optischen Funktionen direkt proportional zum relativen Fehler der Emittanzmessung ist [7, Gesprächshistorie].

### 5.5 Beta-Funktion

In Abbildung 6 ist der Verlauf der $\beta$-Funktion in Abhängigkeit der z-Position entlang des Beschleunigers dargestellt. Die Messpunkte umfassen die Daten der vier Diagnostikschirme sowie den extrapolierten Wert aus dem Q-Scan.

Die Fehlerbalken reflektieren die kombinierte Unsicherheit aus der Emittanzmessung und der Schirmauflösung. Bei der Fehlerfortpflanzung wurde die Schirmunsicherheit von $\pm 50,\mu\text{m}$ für die lineare Strahlbreite auf den quadratischen Term $x_{rms}^2$ transformiert, um physikalisch plausible Fehlergrenzen im Bereich von ca. $0,1$ bis $0,5,\text{m}$ zu erhalten [Gesprächshistorie]. Die Entwicklung der $\beta$-Funktion zeigt die erwartete Fokussierungswirkung der Quadrupol-Zellen im diagnostischen Bereich.