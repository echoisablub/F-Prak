import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = "Daten/Analysis and Interpretation/Ref Spectrum/Reference_Data.csv"

df = pd.read_csv(path, sep=';', decimal=',')

plt.plot(df["emission energy"], df["singlet"], label="Singlet")
plt.plot(df["emission energy"], df["doublet"], label="Doublet")
plt.plot(df["emission energy"], df["triplet"], label="Triplet")
plt.plot(df["emission energy"], df["quartet"], label="Quartet")
plt.plot(df["emission energy"], df["quintet"], label="Quintet")

plt.xlabel("Energy")
plt.ylabel("Intensity")
plt.legend()
plt.title("Reference Spectrum")
plt.savefig("Daten/Analysis and Interpretation/Reference_Spectrum.png")

# Take all possible differences between singlet and higher spin states from the reference spectra and plot these.

plt.figure(figsize=(10, 6))
plt.plot(df["emission energy"], df["singlet"] - df["singlet"], label="Singlet - Singlet")
plt.plot(df["emission energy"], df["doublet"] - df["singlet"], label="Doublet - Singlet")
plt.plot(df["emission energy"], df["triplet"] - df["singlet"], label="Triplet - Singlet")
plt.plot(df["emission energy"], df["quartet"] - df["singlet"], label="Quartet - Singlet")
plt.plot(df["emission energy"], df["quintet"] - df["singlet"], label="Quintet - Singlet")

plt.xlabel("Energy")
plt.ylabel("Intensity")
plt.legend()
plt.title("Differences in Reference Spectrum")
plt.savefig("Daten/Analysis and Interpretation/Differences_Reference_Spectrum.png")
plt.show()