# Energiemessung

dy_dI = 14.4384e-3 ± 0.000106 m/A
kappa = 7.64e-6 Tm/A
L = 0.52 ±0.01 m
E_0 = 511 keV
beta_gamma = 0.1614 ± 0.00332 ~= beta
gamma = 1.013 ± 0.000529 --> also fast klassisch
E_kin =6.62 ± 0.27 keV
p = 2.752e-07 ± 5.661e-09 keV/c

# Emittanzbestimmung duch Q-Scan

epsilon_x = 0.72867 ± 0.07115 mm mrad
epsilon_y = 1.98349 ± 0.09011 mm mrad
# Optische Funktionen am eingang vom Quadripol (Twiss Parameter)

beta_x = 0.578 ± 0.0565, alpha_x = -1.19 ± 0.117, gamma_x = 4.19 ± 0.41
beta_y = 0.814 ± 0.037, alpha_y = -1.401 ± 0.0637, gamma_y = 3.639 ± 0.165
# Beta Funktions Messung

Plots
(output/beta func mit fehlerfortpflanzung.png)
# Strahlbasierte Justage

## x_werte

I_Q_1:-0.344
plot
I_Q_2: 0.657
plot
I_D0: -1.236 (x_intersection)
plot
## y_werte

I_Q_1: 1.685
plot
I_Q_2: 2.703
plot
I_D0: -0.777 (y_intersection)
plot
## Fehler

Mittlerer Scanschritt x: 0.1063
sigma_ID0_x: 0.0532
Mittlerer Scanschritt y: 0.1869
sigma_ID0_y: 0.0935
# Strahltransport

strahltransport ordner bilder


---

\begin{table}[H]
    \centering
    \caption{Zusammenfassung der experimentell ermittelten Strahlparameter.}
    \label{tab:ergebnisse_parameter}
    \begin{tabular}{|l|l|l|}
        \toprule
        Parameter & Symbol & Wert \\
        \midrule
        Steigung der Energiemessung & $dy/dI$ & $14,4384 \pm 0,1056$ mm/A \\
        Kinetische Energie & $E_{kin}$ & $6,62 \pm 0,27$ keV \\
        Relativistischer Impuls & $p$ & $2,752*10^{-7} \pm 5,661*10^{-9}$ keV/c \\
        \midrule
        Horizontale Emittanz & $\epsilon_x$ & $0,72867 \pm 0,07115$ mm mrad \\
        Vertikale Emittanz & $\epsilon_y$ & $1,98349 \pm 0,09011$ mm mrad \\
        \midrule
        $\beta$-Funktion am Quadrupol (x/y) & $\beta_{x/y}$ & \qty{0,578}{m} / \qty{0,814}{m} \\
        $\alpha$-Parameter am Quadrupol (x/y) & $\alpha_{x/y}$ & -1,19 / -1,401 \\
        \bottomrule
    \end{tabular}
\end{table}


\begin{table}[H]
    \centering
    \caption{Ergebnisse der strahlbasierten Justage am Quadrupol Q57MATCH.}
    \label{tab:justage_ergebnisse}
    \begin{tabular}{llll}
        \toprule
        Ebene & Dipol-Magnet & Korrekturstrom $I_{D0}$ & Unsicherheit $\sigma_{ID0}$ \\
        \midrule
        Horizontal (x) & V102MATCH & \qty{-1,236}{A} & \qty{0,0532}{A} \\
        Vertikal (y) & Q113MATCH & \qty{-0,777}{A} & \qty{0,0935}{A} \\
        \bottomrule
    \end{tabular}
\end{table}