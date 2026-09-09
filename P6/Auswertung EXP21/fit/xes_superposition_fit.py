import os
import re
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.interpolate import interp1d
from scipy.integrate import trapezoid

# 1. SETUP UND KONFIGURATION (HIER ANPASSEN!)
DATA_DIR = "Daten\Experiment with Data Acquisition\messreihe"

# Pfad zu deiner Referenz-Datei (Singlet, Triplet, Quintet Spektren)
# Die Datei muss die Spalten "Energy", "Singlet", "Triplet" und "Quintet" enthalten.
REF_FILE = "Daten\Analysis and Interpretation\Ref Spectrum\Reference_Data_Fig_4_4.csv"

# Dateiendung deiner Spektren-Dateien (z.B. ".txt", ".csv", ".dat")
FILE_EXTENSION = ""

# Erwartete maximale Anregungseffizienz (Excitation Yield) in deinem Fokusvolumen.
# Typischerweise liegt dieser Wert im VLab bei ca. 15% bis 20% (0.15 - 0.20).
# Dieser Wert dient zur automatischen Zustandsskalierung deines Rohsignals!
EXPECTED_EXCITATION_YIELD = 0.18

# 2. HILFSFUNKTIONEN ZUM PARSEN UND MITTELN (GOTTHARD-FORMAT)

def parse_delay(folder_name):
    """
    Sucht nach Delay-Werten im Ordnernamen.
    Unterstützt positive Delays (z.B. "50 fs" -> 50.0) und negative Delays 
    mit dem Präfix "min" (z.B. "min50 fs" -> -50.0) gemäß dem FXE-Standard.
    """
    name = folder_name.lower().replace("fs", "").strip()
    try:
        if name.startswith("min"):
            return -float(name.replace("min", "").strip())
        else:
            return float(name)
    except ValueError:
        return None

def read_gotthard_file(filepath):
    """
    Spaltenstruktur des Detektors:
    - Spalte 0: Pixel-Index ("Number")
    - Spalte 1: Energie in eV ("Energy")
    - Spalte 2: Intensität in a.u. ("Intensity")
    """
    df = pd.read_csv(
        filepath, 
        comment='#', 
        sep=r'\s+', 
        header=None,
        names=['Number', 'Energy', 'Intensity']
    )
    return df

def average_runs(file_list):
    """
    Mittelt alle Spektren (die 20 Läufe) für ein Delay.
    Interpoliert die Daten bei minimalen Gitterschwankungen auf ein einheitliches Gitter.
    """
    if not file_list:
        return None, None
        
    # Erste Datei als Standardgitter festlegen
    first_df = read_gotthard_file(file_list[0])
    energy_grid = first_df['Energy'].values
    
    intensities = []
    
    for filepath in file_list:
        df = read_gotthard_file(filepath)
        
        # Falls das Energiegitter minimal abweicht, interpolieren wir es
        if len(df) != len(energy_grid) or not np.allclose(df['Energy'].values, energy_grid, atol=1e-2):
            f_interp = interp1d(df['Energy'].values, df['Intensity'].values, 
                                kind='linear', fill_value="extrapolate")
            intensities.append(f_interp(energy_grid))
        else:
            intensities.append(df['Intensity'].values)
            
    # Arithmetisches Mittel über alle 20 Läufe
    mean_intensity = np.mean(intensities, axis=0)
    return energy_grid, mean_intensity

# 3. PIPELINE FÜR DAS DATENVERARBEITEN
def process_all_delays(data_dir):
    """
    Geht durch alle Delay-Ordner, liest und mittelt die Runs.
    Da die Rohdaten im Ordner 'messreihe' bereits Differenzspektren (Laser On - Laser Off)
    sind, erhalten wir direkt die zeitaufgelöste Differenzintensität Delta_I(E, t).
    """
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Datenverzeichnis '{data_dir}' wurde nicht gefunden.")
        
    delay_folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    
    averaged_series = {}
    standard_energy = None
    
    for folder in sorted(delay_folders):
        delay_val = parse_delay(folder)
        if delay_val is None:
            continue
            
        folder_path = os.path.join(data_dir, folder)
        file_pattern = os.path.join(folder_path, f"*{FILE_EXTENSION}")
        files = glob.glob(file_pattern)
        
        if not files:
            print(f"[Warnung] Keine Dateien in {folder} gefunden.")
            continue
            
        # print(f"Mittelung für Delay {delay_val:6.1f} fs: {len(files)} Runs geladen...")
        energy, mean_diff_spectrum = average_runs(files)
        
        if standard_energy is None:
            standard_energy = energy
            
        # Interpolation auf Standard-Energiegitter sichern
        if not np.allclose(energy, standard_energy):
            f = interp1d(energy, mean_diff_spectrum, fill_value="extrapolate")
            mean_diff_spectrum = f(standard_energy)
            
        averaged_series[delay_val] = mean_diff_spectrum
        
    return standard_energy, averaged_series

# 4. DIREKTER FIT DER TRANSIENTEN DIFFERENZSPEKTREN
def fit_difference_spectrum_raw(energy, y_diff_exp, ref_df):
    """
    Fittet das experimentelle transienten Differenzspektrum Delta_I_exp(E) 
    direkt über eine Linearkombination der Referenz-Differenzspektren:
    
      Delta_I_fit(E) = w_Triplet * (S_Triplet - S_Singlet) + w_Quintet * (S_Quintet - S_Singlet)
      
    Unter den physikalischen Randbedingungen (Constraints):
      1. w_Triplet >= 0, w_Quintet >= 0  (Keine negativen Populationen)
      2. w_Triplet + w_Quintet <= 1.0    (Die Summe der angeregten Zustände kann max. 100% sein)
      
    Die verbleibende Population im Singulett-Grundzustand ergibt sich direkt aus der Erhaltung:
      w_Singlet = 1.0 - w_Triplet - w_Quintet
    """
    # Referenzen auf das experimentelle Energiegitter interpolieren
    def get_ref(name):
        f = interp1d(ref_df['emission energy'].values, ref_df[name].values, kind='cubic', fill_value="extrapolate")
        return f(energy)
        
    S_singlet = get_ref('singlet')
    S_triplet = get_ref('triplet')
    S_quintet = get_ref('quintet')
    
    # Referenzen auf Fläche = 1 normieren, um mathematische Konsistenz zu garantieren
    S_singlet /= trapezoid(S_singlet, energy)
    S_triplet /= trapezoid(S_triplet, energy)
    S_quintet /= trapezoid(S_quintet, energy)
    
    # Berechne die transienten Referenz-Differenzspektren (Delta_S)
    diff_triplet = S_triplet - S_singlet
    diff_quintet = S_quintet - S_singlet
    
    # Zielfunktion: Kleinste Quadrate
    def objective(c):
        c_T, c_Q = c
        fit = c_T * diff_triplet + c_Q * diff_quintet
        return np.sum((y_diff_exp - fit)**2)
        
    # Bounds: Koeffizienten dürfen nicht negativ sein, haben aber KEIN oberes Limit!
    bounds = [(0.0, None), (0.0, None)]
    w0 = [0.0, 0.0]
    
    res = minimize(objective, w0, method='L-BFGS-B', bounds=bounds, tol=1e-15)
    c_T_opt, c_Q_opt = res.x
    
    return c_T_opt, c_Q_opt, diff_triplet, diff_quintet

# 6. PHYSKALISCHES KINETIK-FIT-MODELL (RATE EQUATIONS CONVOLVED WITH IRF)
def fit_physical_kinetics(delays, exp_S, exp_T, exp_Q):
    """
    Fittet die Ratengleichungen convolved mit der Laser-Response (IRF) an die
    experimentell extrahierten Populationen.
    
    Model:
      S_0 -> Laser-Excitation -> Triplet (tau_1 decay) -> Quintet (stable HS)
    """
    t_fine = np.linspace(-300, 1000, 2000)
    dt = t_fine[1] - t_fine[0]
    
    def solve_kinetics(eta, tau_1, t_0, sigma):
        # Initialisiere die zeitabhängigen Populationen
        w_S_sim = np.ones_like(t_fine)
        w_T_sim = np.zeros_like(t_fine)
        w_Q_sim = np.zeros_like(t_fine)
        
        # Laser-Anregungsrate (Gaußscher Puls, Flächenintegral = eta)
        R_exc = (eta / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(t_fine - t_0)**2 / (2 * sigma**2))
        
        # Numerische Integration der gekoppelten DGLs
        for i in range(1, len(t_fine)):
            dw_S = -R_exc[i] * dt
            dw_T = (R_exc[i] - w_T_sim[i-1] / tau_1) * dt
            dw_Q = (w_T_sim[i-1] / tau_1) * dt
            
            w_S_sim[i] = w_S_sim[i-1] + dw_S
            w_T_sim[i] = w_T_sim[i-1] + dw_T
            w_Q_sim[i] = w_Q_sim[i-1] + dw_Q
            
        return w_S_sim, w_T_sim, w_Q_sim

    def objective(p):
        eta, tau_1, t_0, sigma = p
        
        # Physikalisch plausible Grenzen erzwingen (Constraints)
        if eta < 0.01 or eta > 0.40:
            return 1e10
        if tau_1 < 10.0 or tau_1 > 500.0:
            return 1e10
        if t_0 < -100.0 or t_0 > 100.0:
            return 1e10
        if sigma < 5.0 or sigma > 150.0:
            return 1e10
            
        sim_S, sim_T, sim_Q = solve_kinetics(eta, tau_1, t_0, sigma)
        
        f_S = interp1d(t_fine, sim_S, fill_value="extrapolate")
        f_T = interp1d(t_fine, sim_T, fill_value="extrapolate")
        f_Q = interp1d(t_fine, sim_Q, fill_value="extrapolate")
        
        # Summe der quadratischen Abweichungen über alle drei Spinzustände
        res_S = np.sum((exp_S - f_S(delays)*100)**2)
        res_T = np.sum((exp_T - f_T(delays)*100)**2)
        res_Q = np.sum((exp_Q - f_Q(delays)*100)**2)
        
        return res_S + res_T + res_Q

    # Startparameter für den Fit: [eta, tau_1, t_0, sigma]
    p0 = [EXPECTED_EXCITATION_YIELD, 120.0, 10.0, 120 / 2.355]
    
    # Nelder-Mead simplex algorithm für stabilen nicht-linearen Fit
    res = minimize(objective, p0, method='Nelder-Mead', tol=1e-12)
    
    eta_fit, tau_1_fit, t_0_fit, sigma_fit = res.x
    fwhm_fit = sigma_fit * 2.355
    
    # Best-Fit Kinetikkurven auf feinem Gitter erzeugen
    fit_S, fit_T, fit_Q = solve_kinetics(eta_fit, tau_1_fit, t_0_fit, sigma_fit)
    
    fitted_model_curves = {
        't_fine': t_fine,
        'S': fit_S * 100.0,
        'T': fit_T * 100.0,
        'Q': fit_Q * 100.0
    }
    
    fit_parameters = {
        'eta': eta_fit,
        'tau_1': tau_1_fit,
        't_0': t_0_fit,
        'sigma': sigma_fit,
        'fwhm': fwhm_fit
    }
    
    return fit_parameters, fitted_model_curves

# 5. MAIN PIPELINE
if __name__ == "__main__":
    print("   XES PUMP-PROBE DIFFERENZ-FIT PIPELINE (VLAB GOTTHARD PIPELINE)    ")
    
    # 1. Referenzspektren laden
    ref_df = pd.read_csv(REF_FILE)
    # 2. Daten einzulesen
    energy, delay_data = process_all_delays(DATA_DIR)

    # 3. Erste Fitphase: Bestimmung der unbeschränkten Intensitäts-Koeffizienten
    delays = sorted(delay_data.keys())
    raw_coefficients = {'Delay': delays, 'c_T': [], 'c_Q': []}
    
    print("\nFühre unbeschränkten SLSQP-Fit über alle Delays durch...")
    for t in delays:
        y_diff_exp = delay_data[t]
        c_T, c_Q, _, _ = fit_difference_spectrum_raw(energy, y_diff_exp, ref_df)
        raw_coefficients['c_T'].append(c_T)
        raw_coefficients['c_Q'].append(c_Q)
        
    # 4. Selbstkalibrierung: Ermittlung des Intensitäts-Skalierungsfaktors (N_total)
    # Die Summe c_T + c_Q repräsentiert die absolute Anregungsstärke.
    # Ihr Maximum im gesamten Scan entspricht der maximalen Anregungs-Population (EXPECTED_EXCITATION_YIELD)
    total_raw_excitation = np.array(raw_coefficients['c_T']) + np.array(raw_coefficients['c_Q'])
    max_raw_excitation = np.max(total_raw_excitation)
    
    if max_raw_excitation <= 0:
        print("[Warnung] Keine nennenswerte Anregung im gesamten Scan detektiert.")
        N_total = 1.0
    else:
        N_total = max_raw_excitation / EXPECTED_EXCITATION_YIELD
        print(f"\n[Kalibrierung] Automatischer Skalierungsfaktor ermittelt: N_total = {N_total:.3e} Counts")
        print(f"[Kalibrierung] Dies entspricht {EXPECTED_EXCITATION_YIELD*100:.1f}% maximaler Anregung im Jet.")

    # 5. Berechnung der physikalisch normierten Zustandspopulationen (S, T, Q)
    kinetics_data = {
        'Delay': delays,
        'Singlet': [],
        'Triplet': [],
        'Quintet': []
    }
    
    for idx, t in enumerate(delays):
        w_T = raw_coefficients['c_T'][idx] / N_total
        w_Q = raw_coefficients['c_Q'][idx] / N_total
        
        # Physikalische Grenzen absichern (0% bis 100% excitation yield)
        w_T = np.clip(w_T, 0.0, EXPECTED_EXCITATION_YIELD)
        w_Q = np.clip(w_Q, 0.0, EXPECTED_EXCITATION_YIELD)
        
        # Falls durch Rauschen die Summe leicht über EXPECTED_EXCITATION_YIELD liegt, skalieren wir sie herunter
        total_exc = w_T + w_Q
        if total_exc > EXPECTED_EXCITATION_YIELD:
            w_T = (w_T / total_exc) * EXPECTED_EXCITATION_YIELD
            w_Q = (w_Q / total_exc) * EXPECTED_EXCITATION_YIELD
            
        w_S = 1.0 - w_T - w_Q
        
        kinetics_data['Singlet'].append(w_S * 100.0)
        kinetics_data['Triplet'].append(w_T * 100.0)
        kinetics_data['Quintet'].append(w_Q * 100.0)
        
    df_kinetics = pd.DataFrame(kinetics_data)

    # 6 Zweite Fitphase: Globaler Kinetischer Fit (Rate Equations + IRF)
    print("\nStarte nicht-linearen Fit des physikalischen Kaskadenmodells...")
    fit_params, fitted_curves = fit_physical_kinetics(
        np.array(delays), 
        df_kinetics['Singlet'].values, 
        df_kinetics['Triplet'].values, 
        df_kinetics['Quintet'].values
    )


    print("\n" + "="*70)
    print("      GEFITTETE PHYSIKALISCHE KINETIK-PARAMETER (EXP21)     ")
    print("="*70)
    print(f"Anregungsausbeute (Excitation Yield eta) : {fit_params['eta']*100:6.2f} %")
    print(f"Triplet-Lebensdauer (tau_1, ISC)         : {fit_params['tau_1']:6.1f} fs")
    print(f"Zeitnullpunkt-Offset (t_0)               : {fit_params['t_0']:+6.1f} fs")
    print(f"Laser-Pulsbreite (FWHM der IRF)          : {fit_params['fwhm']:6.1f} fs")
    print("="*70 + "\n")
    
    # Kinetik-Tabelle im Terminal ausgeben
    print("="*60)
    print("       REKONSTRUIERTE SPIN-POPULATIONEN (MESSWERTE)        ")
    print("="*60)
    print(df_kinetics.to_string(index=False, formatters={
        'Singlet': '{:6.2f}%'.format,
        'Triplet': '{:6.2f}%'.format,
        'Quintet': '{:6.2f}%'.format,
        'Delay': '{:5.1f} fs'.format
    }))
    print("="*60 + "\n")
    
    # Daten und Parameter exportieren
    df_kinetics.to_csv("Auswertung EXP21\\Ergebnisse\\real_kinetics.csv")
    pd.DataFrame([fit_params]).to_csv("fitted_kinetics_parameters.csv", index=False)
    print("[Erfolg] Kinetik exportiert als 'reconstructed_kinetics_v7.csv'")
    print("[Erfolg] Fit-Parameter exportiert als 'fitted_kinetics_parameters.csv'")
    
    # 7.7 Visualisierung (Wunderschöner publikationsreifer Plot!)
    fig, ax = plt.subplots(figsize=(10.5, 6.5))
    
    colors = {'Singlet': '#1f77b4', 'Triplet': '#ff7f0e', 'Quintet': '#9467bd'}
    markers = {'Singlet': 'o', 'Triplet': 's', 'Quintet': '^'}
    
    # 1. Plotte kontinuierliche, gefittete Modellkurven (Glatte Linien)
    t_fine = fitted_curves['t_fine']
    ax.plot(t_fine, fitted_curves['S'], '-', color=colors['Singlet'], linewidth=2.5, label=r'Modell: Singlet ($^1A_1$ Grundzustand)')
    ax.plot(t_fine, fitted_curves['T'], '-', color=colors['Triplet'], linewidth=2.5, label=r'Modell: Triplet ($^3T_1$ Zwischenzustand)')
    ax.plot(t_fine, fitted_curves['Q'], '-', color=colors['Quintet'], linewidth=2.5, label=r'Modell: Quintet ($^5T_2$ High-Spin)')
    
    # 2. Plotte diskrete Messpunkte aus dem XES-Spektren-Fit (Scatter-Symbole ohne Verbindungslinien!)
    ax.scatter(df_kinetics['Delay'], df_kinetics['Singlet'], color=colors['Singlet'], marker=markers['Singlet'], s=65, zorder=5, edgecolors='black', label='Fit: Singlet-Population')
    ax.scatter(df_kinetics['Delay'], df_kinetics['Triplet'], color=colors['Triplet'], marker=markers['Triplet'], s=65, zorder=5, edgecolors='black', label='Fit: Triplet-Population')
    ax.scatter(df_kinetics['Delay'], df_kinetics['Quintet'], color=colors['Quintet'], marker=markers['Quintet'], s=65, zorder=5, edgecolors='black', label='Fit: Quintet-Population')
    
    # 3. Grafik-Verschönerungen
    ax.set_title('Publikationsreifer Kinetik-Fit der photophysikalischen Kaskade (vLab v7)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Zeitverzögerung $\\Delta t$ (fs)', fontsize=11)
    ax.set_ylabel('Molekülpopulation im Strahlvolumen (%)', fontsize=11)
    ax.set_xlim(-200, 900)
    ax.set_ylim(-5, 105)
    ax.axvline(0, color='black', linestyle='--', alpha=0.5)
    
    # 4. Professionelle Annotationen für dein Protokoll hinzufügen
    ax.annotate(f'Laseranregung ({fit_params["fwhm"]:.0f} fs FWHM)\nYield: {fit_params["eta"]*100:.1f}%', \
                xy=(fit_params['t_0'], 50), xytext=(-185, 52),
                arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6),
                fontsize=9, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.15))
                 
    ax.annotate('Triplet Zerfall\n' + r'$\tau_1 \approx ' + f'{fit_params["tau_1"]:.0f}' + r'\ fs$', \
                xy=(100, 8), xytext=(150, 25),
                arrowprops=dict(arrowstyle="->", color=colors['Triplet'], connectionstyle="arc3,rad=.2"),
                color=colors['Triplet'], fontsize=9, fontweight='bold')
                 
    ax.annotate('High-Spin Quintet\nRise & Plateau', \
                xy=(350, 16), xytext=(400, 45),
                arrowprops=dict(arrowstyle="->", color=colors['Quintet'], connectionstyle="arc3,rad=-.2"),
                color=colors['Quintet'], fontsize=9, fontweight='bold')
    
    ax.legend(loc='center right', frameon=True, fontsize=9.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    output_plot = "Auswertung EXP21\\Ergebnisse\\real_data_kinetics.png"
    plt.savefig(output_plot, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"[Erfolg] Grafik erzeugt und gespeichert unter '{output_plot}'")
    



