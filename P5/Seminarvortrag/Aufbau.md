# SALOME - Simple Accelerator for Learning Optics and Manipulation of Electrons 
Fortgeschrittenenpraktikum Versuch EXP9

#### 1. Einleitung & Motivation (Folie 1–2)

- **Was ist SALOME?** Ein Lehrbeschleuniger zur Erzeugung von Elektronenstrahlen bis **20 keV**.
- **Ziel des Versuchs:** Bestimmung der Strahlqualität (Emittanz) und der Strahlparameter (Energie, Twiss-Parameter).
- **Physikalischer Kontext:** Verständnis von Strahlführung und Korrektureffekten (z. B. Erdmagnetfeld) bei niedrigen Energien.

#### 2. Theoretische Grundlagen (Folie 3)

- **Emittanz ($\varepsilon$):** Maß für das Phasenraumvolumen des Strahls; entscheidend für die Fokussierbarkeit.
- **Thermische Emittanz:** Das theoretische Minimum, definiert durch die Kathodentemperatur T und die Strahlgröße $\sigma_x$: $\epsilon_{n,thermisch} = \sigma_x \cdot \sqrt{\frac{k_B T}{mc^2}}$
- **Relativistik:** Bei SALOME ist $\gamma \approx 1,013$ (nahezu klassisches Regime).

#### 3. Experimenteller Aufbau (Folie 4)

- **Quelle:** Thermische Wolfram-Kathode $\Phi_{aus} = 4,5 \text{ eV}$.
- **Beschleunigungsstrecke:** Solenoide zur Fokussierung direkt nach der Anode.
- **Diagnostik:** Matching-Section mit Quadrupolen (z. B. V46Match) und fluoreszierenden Schirmen zur Strahlprofil messung.

#### 4. Methodik I: Energiemessung (Folie 5)

- **Prinzip:** Vertikale Ablenkung in einem Dipolfeld.
- **Messung:** Aufnahme der Strahlposition \(\langle y \rangle\) in Abhängigkeit vom Dipolstrom \(I\).
- **Ergebnis:** Aus der Steigung \(dy/dI \approx 14,44 \text{ mm/A}\) folgt eine kinetische Energie von **\(6,62 \pm 0,27 \text{ keV}\)**.

#### 5. Methodik II: Strahlbasierte Justage (BBA) (Folie 6)

- **Problem:** Systematische Fehler durch Dezentrierung in Quadrupolen.
- **Lösung:** Variation der Quadrupolstärke bei verschiedenen Dipolströmen.
- **Visualisierung:** Der Schnittpunkt im \(x/I\)-Diagramm markiert das magnetische Zentrum (\(I_{D0,x} \approx -1,236 \text{ A}\)).

#### 6. Hauptergebnis: Emittanzmessung (Quadrupol-Scan) (Folie 7–8)

- **Verfahren:** Variation der Stärke \(k\) des Quadrupols V46Match und Messung der RMS-Breite \(\sigma^2\) auf dem Schirm.
- **Auswertung:** Lösung der Normalengleichung für die Beam-Matrix \(\sigma_{beam}\).
- **Messwerte:**
    - \(\epsilon_x \approx 0,729 \text{ mm mrad}\)
    - \(\epsilon_y \approx 1,983 \text{ mm mrad}\)
- Hinweis auf die starke **Asymmetrie** zwischen horizontaler und vertikaler Ebene.

#### 7. Diskussion: Vergleich mit der Theorie (Folie 9–10)

- **Vergleich:** Die gemessenen normierten Emittanzen (\(\epsilon_{n,x} \approx 0,118 \text{ mm mrad}\)) liegen über dem thermischen Limit.
- **Fehlerquellen & Effekte:**
    1. **Raumladung (Space Charge):** Bei 6,6 keV stoßen sich Elektronen stark ab, was die Emittanz vergrößert.
    2. **Erdmagnetfeld:** Signifikanter Einfluss bei niedrigen Energien; führt zu Kopplung der Ebenen.
    3. **Nicht-ideale Fokussierung:** Aberrationen in den Magneten.

#### 8. Zusammenfassung & Fazit (Folie 11)

- Erfolgreiche Charakterisierung des SALOME-Strahls bei **6,62 keV**.
- Bestimmung der Twiss-Parameter zur Vorhersage des Strahlverlaufs (Beta-Funktion).
- Erkenntnis: Reale Strahlqualität wird maßgeblich durch kollektive Effekte (Raumladung) limitiert.
