'''
Record the spectrum of the pink X-ray beam with the dispersive single-shot spectrum analyzer (SpA1, Sec. 6.4.3)
Plot:
    a) three single-shot spectra of an X-ray pulse 
    b) an averaged spectrum over many pulses. 
Indicate the spectral bandwidth (FWHM in eV) of the pink X-ray beam. 
Note: Move the SpA1 crystal into the X-ray beam and adjust the detector arm to the appropriate Bragg angle. 
An adjustment guide is provided in the SpA1 subroutine for this purpose. 
Compare the VLab spectrum to that of European XFEL (Fig. 6.15)
Repeat the previous task for the monochromatic X-ray beam. 
Discuss the differences in the spectra itself and the spectral bandwidth. 
How does this compare to your previous observation of the intensity decrease from the pink to the monochrom. X-ray beam in ex.2
'''


import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from pathlib import Path
import pandas as pd

folder = Path("Daten/Alignment and characterization/mono pink/spectrum/spektrum_data/spektrum_data_mono")

files = sorted(folder.glob("*"))   # all files in folder

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

spectra = []

plt.figure(figsize=(8, 5))

for file in files[:3]:

    df = pd.read_table(
        file,
        sep=r'\s+',
        comment='#',
        header=None,
        names=['Number', 'Energy', 'Intensity']
    )
    E_0=7400
    E = df['Energy'].to_numpy()
    y = df['Intensity'].to_numpy()

    plt.plot(E-E_0, y, '--', alpha=0.7, label=file.name)

    ''' plt.xlabel("Energy [eV]")
    plt.ylabel("Intensity [arb. units]")
    plt.title("Single-shot X-ray spectra")
    plt.grid(True)
    plt.xlim(-50, 50)
    plt.legend()
    plt.savefig(f"Daten/Alignment and characterization/mono pink/spectrum/3 single-shot spectra.png", dpi=300)
'''

for file in files:

    # Load data
    df = pd.read_table(
        file,
        sep=r'\s+',
        comment='#',
        header=None,
        names=['Number', 'Energy', 'Intensity']
    )
    E_0=7400  
    E = df['Energy'].to_numpy()
    y = df['Intensity'].to_numpy()

    # Interpolate to common energy grid
    dE = E-E_0
    energy_grid = np.linspace(dE.min(), dE.max(), 1000)

    interp_func = interp1d(
        dE,
        y,
        kind='cubic'
    )

    y_interp = interp_func(energy_grid)
    spectra.append(y_interp)

spectra = np.array(spectra)
y_average = np.mean(spectra, axis=0)

# Plot averaged spectrum
# plt.figure(figsize=(8, 5))
plt.plot(
    energy_grid,
    y_average,
    label="Average"
)

plt.xlabel("Energy [eV]")
plt.ylabel("Intensity [arb. units]")
plt.title("Averaged X-ray spectrum")
plt.grid(True)
plt.xlim(-50, 50)
plt.legend()
plt.savefig("Daten/Alignment and characterization/mono pink/spectrum/spectrum_average_mono.png", dpi=300)

plt.show()