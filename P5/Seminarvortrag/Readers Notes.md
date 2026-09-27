# Aufbau
steht für simple accelerator for learning optics and Manipulation of electrons - kurzer Linearbeschleuniger mit niedrigen Energien, der dafür gedacht ist die Einstellung und Nutzung eines Beschleunigers zu Lernen  
  
Diese geringe max Energie erlaubt es, den Beschleuniger ohne Abschirmungen für den Strahlenschutz betreiben zu können

Lässt sich in drei Abschnitte aufteilen:
## Injection Section: 
- Fokus: 10keV themionic DC-Kathode
## Justage Section: 
Fokus: 
- erste F0D0- Zelle + Strahlbasierte Justage
  (F0D0-Zelle besteht aus zwei Quadrupolmagneten 
  einem fokussierenden und einem defokussierenden)
	- auf Quadrupolmagnete werden wir später noch kommen
- \+ 2 Dipolmagneten (vertikal und horizontal gerichtet) 
   -> Strahl in beide achsen lenken können
## Diagnostic Section: 
- Fokus: 2 F0D0-Zelle + Emittanzmessung

- Länge 4m gestell 6m

- Kameras: mit Schirmen die durch Motoren reingefahren werden können, kann man dann mit Stationären Kameras den Strahl beobachten und messen
- Mit diesen Kameras haben wir auch erst sichergestellt, dass der Strahl am Ende unseres Beschleunigers ankommt.

Einmal ein Bild vom Aufbau von der Kontrollstation aus:
Ein Einblick in das Kontrollsystem, was wir von dem Computer aus steuern konnten. Hier: Teil mit der Kontrolle über angelegte Ströme bei Magneten + Schirme (ob in Strahl oder zur Seite des Strahls)

# Energiemessung
Um die kinetische Energie und den Impuls eines Teilchenstrahls zu bestimmen, wird die Teilchenablenkung durch das Dipolfeld gemessen.

Dafür betrachten wir die Lorentzkraft und die resultierende vertikale Ablenkung zusammen mit einer Änderung des Vertikalen Impulses $p_y$.

Unsere messbaren Größen sind der Strom I, den wir an den Dipol anlegen, die Distanz bzw. die Driftstrecke L zwischen Quadrupol und Schirm und die vertikale Ablenkung y, den wir als zeitlich gemittelte Position $<y>$ messen.

Messung:
1. Dipolströme bestimmen für die y maximal \& minimal ist, (am Rand vom Schirm)
2. zwischen diesen beiden Strömen in 0,1 A schritten durchfahren und $<y>$ notieren

Auswertung:
lin. reg der Strahlposition über dem Magnetstrom, um die Steigung zu bekommen mit der zusammen mit ein paar konstanten unser beta gamma produkt berechnet werden kann.

Ablenkwickel ist Proportional vom Strom abhängig -> deswegen haben wir einen linearen Zusammenhang zw position und Strom -> Steigung einfach bestimmbar
## Messwerte/Ergebnisse
Steigung: Messgröße
Ekin=6,62 keV, p=82,5 keV/c
Daraus kriegen wir einen lorentzfaktor von ca. 1 à nahezu klassisches Geschwindigkeitsregime.

Störanfälligkeit: 
- Strom von Magnet-netzteile usw. oszillitert um einen soll wert: 1 bit rauschen
- generell anfällig gegenüber externen Magnetfeldern

--> deshalb ist der nächste Part so wichtig

Transition :)