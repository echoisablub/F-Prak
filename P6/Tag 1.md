1. **Select a suitable nominal X-ray energy E0 for the XFEL radiation source in VLab by setting it in the undulator (Sec. 6.2.1)** 
	Keep in mind that you will perform an experiment using non-resonant X-ray emission spectroscopy (non-resonant XES) of the Fe Kβ1,3 line. Consider two factors when making your choice: 
		a) The required energy to access the absorption edge of atomic iron, which you can look up, for example, in the Database at the Center for X-Ray Optics (CXRO[23]). 
		b) The EXAFS spectrum of the molecule (Fig. A.1). 
	**Justify your choice with respect to a) and b). Also plot the transmission spectrum through iron from below the edge to above your chosen energy using the CXRO data.**
		==7200 eV chosen bc
		Fig A.1: edge at approx 7120, but for $[Fe(terpy)_2]^{2+}$
		CXRO: not found, aber bei [anderer Website](http://skuld.bmsc.washington.edu/scatter/AS_periodic.html) schon -> 7.1keV==
2. Confirm that you have a X-ray beam at all. 
	The best device for this purpose is the beam imaging unit 2 (BIU2, Sec 6.4.1). To avoid saturation of the BIU camera detector, familiarize yourself with the operation of the beam attenuators (SAA, Sec. 6.4.5). Before doing so, all power slits (PS, Sec. 6.4.4) may be fully opened. Try different attenuator foils until the BIU2 camera is at maximum just below saturation.
		Solid Attentuators:
			rod1: C 0.1
			rod2: Si 0.05
			rod3: C 0.4
			rod4: B4C 0.8
	**Determine the size and position of the X-ray beam on the BIU2**. 
	To do this, plot the horizontal and vertical profile width of the beam as a graph and determine the respective full width at half maximum (FWHM, App. B). 
		==420x420 data array
		Horizontal:
		  Center = 197.09 px
		  FWHM   = 98.67 px
		Vertical:
		  Center = 207.15 px
		  FWHM   = 98.48 px==
	Afterward, download about 20 single images (20 different X-ray pulses) and determine the horizontal and vertical position (x,y) of the maximum for each pulse. Then calculate the overall mean position and the standard deviation (±1SD), where the latter is a measure of the spatial jitter of every X-ray pulse as seen on BIU2. Discuss your results in terms of relevance for the actual experiment (e.g., is the experiment feasible or not under these fluctuating conditions?). 
		File: BeamImagingUnit2 26-08-31 14-07-22, x_max: 188, y_max: 210
		File: BeamImagingUnit2 26-08-31 14-07-24, x_max: 176, y_max: 207
		File: BeamImagingUnit2 26-08-31 14-07-27, x_max: 194, y_max: 207
		File: BeamImagingUnit2 26-08-31 14-07-28, x_max: 193, y_max: 208
		File: BeamImagingUnit2 26-08-31 14-07-30, x_max: 231, y_max: 205
		File: BeamImagingUnit2 26-08-31 14-07-32, x_max: 202, y_max: 210
		File: BeamImagingUnit2 26-08-31 14-07-33, x_max: 191, y_max: 212
		File: BeamImagingUnit2 26-08-31 14-07-35, x_max: 240, y_max: 211
		File: BeamImagingUnit2 26-08-31 14-07-37, x_max: 215, y_max: 214
		File: BeamImagingUnit2 26-08-31 14-07-38, x_max: 215, y_max: 214
		File: BeamImagingUnit2 26-08-31 14-07-39, x_max: 215, y_max: 210
		File: BeamImagingUnit2 26-08-31 14-07-41, x_max: 200, y_max: 212
		File: BeamImagingUnit2 26-08-31 14-07-42, x_max: 200, y_max: 212
		File: BeamImagingUnit2 26-08-31 14-07-44, x_max: 244, y_max: 214
		File: BeamImagingUnit2 26-08-31 14-07-45, x_max: 221, y_max: 213
		File: BeamImagingUnit2 26-08-31 14-07-47, x_max: 253, y_max: 210
		File: BeamImagingUnit2 26-08-31 14-07-48, x_max: 239, y_max: 214
		File: BeamImagingUnit2 26-08-31 14-07-50, x_max: 235, y_max: 209
		File: BeamImagingUnit2 26-08-31 14-07-52, x_max: 201, y_max: 209
		File: BeamImagingUnit2 26-08-31 14-07-53, x_max: 172, y_max: 213
		File: BeamImagingUnit2 26-08-31 14-07-54, x_max: 214, y_max: 208
		File: BeamImagingUnit2 26-08-31 14-07-56, x_max: 227, y_max: 209
		File: BeamImagingUnit2 26-08-31 14-07-58, x_max: 250, y_max: 209
		File: BeamImagingUnit2 26-08-31 14-07-59, x_max: 250, y_max: 209
		File: BeamImagingUnit2 26-08-31 14-08-00, x_max: 206, y_max: 213
		File: BeamImagingUnit2 26-08-31 14-08-02, x_max: 194, y_max: 204
		File: BeamImagingUnit2 26-08-31 14-08-03, x_max: 196, y_max: 210
		File: BeamImagingUnit2 26-08-31 14-08-05, x_max: 196, y_max: 214
		File: BeamImagingUnit2 26-08-31 14-08-06, x_max: 202, y_max: 206
		File: BeamImagingUnit2 26-08-31 14-08-07, x_max: 244, y_max: 206
		File: BeamImagingUnit2 26-08-31 14-08-09, x_max: 169, y_max: 210
		==Beam position from 20 X-ray pulses
		x = 212.03 ± 23.61 px
		y = 210.06 ± 2.80 px==
		optical resolution roughly: 25 μm per pixel
3. The X-ray beam exhibits a broader energy distribution of ∆ESASE around E0, the SASE spectrum. It is also called the “pink” X-ray beam, because it is neither truly monochromatic nor as broadband. By inserting the four-bounce crystalmonochromator (Sec. 6.3.2) into the beam path, the spectral bandwidth can be significantly reduced to ∆EMono. 
	**Go to the monochromator and observe i) the pink and ii) the monochromatic X-ray beam on the BIU2. Document the change in intensity of the beam in your lab book, using screenshots and 3D-plotted image data. **
4. **Record the spectrum of the pink X-ray beam with the dispersive single-shot spectrum analyzer (SpA1, Sec. 6.4.3)**
	Plot a) three single-shot spectra of an X-ray pulse and b) an averaged spectrum over many pulses. Indicate the spectral bandwidth (FWHM in eV) of the pink X-ray beam. Note: Move the SpA1 crystal into the X-ray beam and adjust the detector arm to the appropriate Bragg angle. An adjustment guide is provided in the SpA1 subroutine for this purpose. Compare the VLab spectrum to that of European XFEL (Fig. 6.15). 
5. Repeat the previous task for the monochromatic X-ray beam. Discuss the differences in the spectra itself and the spectral bandwidth. How does this compare to your previous observation of the intensity decrease from the pink to the monochromatic X-ray beam in ex. 2 
6. Discuss whether a pink or monochromatic beam would be better suited for a non-resonant X-ray emission spectroscopy (XES) experiment of the Fe Kβ1,3 line. Note: Keep in mind your results from the previous tasks and review the principle of non-resonant X-ray emission (Fig. 4.2). 
7. The XFEL generates a pulse train of many successive X-ray pulses which fluctuate in their position in the beam tube and in their intensity (Sec. 6.2.2). Characterize the changes in a) spatial position and b) intensity for different X-ray pulses. Use the signals from the four diodes of the intensity and position monitor (IPM, Sec. 6.4.2) for this purpose. Consider how you can obtain information from this signal about the changes in spatial position for the different X-ray pulses. Plot these in the lab book. The distance from the scattering foil to the intersection of the plane formed by the 4 diodes with the X-ray beam axis is 40 mm. The distance from the center point of the diode to its opposite diode is also 40 mm. Note: Consider the horizontal and vertical position changes separately. 
8. Determine the transmission of a diamond attenuator foil in the beam attenuator unit (SAA, Sec. 6.4.5). To do this, measure the change in intensity of the X-ray beam on the BIU2 after inserting an additional 0.8 mm thick diamond foil (C) in the SAA. Repeat this for two additional undulator energies E0. Compare your results with the expected transmission for such a foil according to CXRO. 
9. Focus the X-ray beam with the appropriate set of refractive beryllium X-ray lenses (CRL, Sec. 6.4.7) and determine the X-ray beam size at the sample location using the beam imaging unit “X-ray Eye”. Note: Each of the 10 CRL lens holders is individually equipped with up to several lenses (Tab. 6.1). In general, the lens stacks closer to the sample (the left side) contain more Einzellenses and thus focus more strongly than those located upstream (the right side). The excitation laser should still be switched off at this time. To do this, set the pulse energy of the laser to zero. In VLab, a switched-off optical laser is also displayed by “red spheres”