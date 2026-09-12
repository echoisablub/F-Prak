import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 14,
    "axes.labelsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "legend.title_fontsize": 14,
})

path = "Daten/Analysis and Interpretation/Ref Spectrum/Reference_Data.csv"

df = pd.read_csv(path, sep=';', decimal=',')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6), constrained_layout=True)

ax1.plot(df["emission energy"], df["singlet"], label="Singlet")
ax1.plot(df["emission energy"], df["doublet"], label="Doublet")
ax1.plot(df["emission energy"], df["triplet"], label="Triplet")
ax1.plot(df["emission energy"], df["quartet"], label="Quartet")
ax1.plot(df["emission energy"], df["quintet"], label="Quintet")

ax1.set_xlabel("Energy")
ax1.set_ylabel("Intensity")
ax1.legend()
ax1.set_title("Reference Spectrum")

# Take all possible differences between singlet and higher spin states from the reference spectra and plot these.

ax2.plot(df["emission energy"], df["singlet"] - df["singlet"], label="Singlet - Singlet")
ax2.plot(df["emission energy"], df["doublet"] - df["singlet"], label="Doublet - Singlet")
ax2.plot(df["emission energy"], df["triplet"] - df["singlet"], label="Triplet - Singlet")
ax2.plot(df["emission energy"], df["quartet"] - df["singlet"], label="Quartet - Singlet")
ax2.plot(df["emission energy"], df["quintet"] - df["singlet"], label="Quintet - Singlet")

ax2.set_xlabel("Energy")
ax2.set_ylabel("Intensity")
ax2.legend()
ax2.set_title("Differences in Reference Spectrum")

fig.savefig("Daten/Analysis and Interpretation/Reference_Spectra.png")
plt.show()