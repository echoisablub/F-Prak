22. **Center the liquid jet on the X-ray beam**. 
    To optimize the position of the liquid jet in the X-ray beam, maximize the intensity of elastic X-ray scattering. Use the Large Pixel Detector (LPD, Sec. 6.5.4) for this purpose. 
    ==Note: the beam should be centered through the central hole beforehand==.
		11m/s, 0.1mm width, water, moved few mm bis 10^10 intensity vom lpd signal
		jet speed locked? obwohl größerer Laser durchschnitt
    Document your achieved maximum intensity well. When readjusting, for example after each restart of the software, you only have to return to this maximum intensity. 
	    3.8E15 max intensity now using pink spektrum
	    ![[Pasted image 20260902144604.png]]
23. **Adjust the X-ray emission spectrometer.** 
    Set the correct Bragg angle range for the selected crystal (ex. 21) and orient the detector perpendicular to the incoming dispersive spectrum. 
    Make sure that you are in the line focus of the horizontally focusing emission beam. 
    Check and optimize the cylindrical focusing using the 2D display of the Jungfrau detector, and document your geometric setting by suitable screenshots.
		attenuators raus
    **Download the 1D data and plot the Kβ1,3 spectrum of the ground state sample (laser off).** 
	    pretty :)
	    ![[Pasted image 20260902144642.png]]
24. Use the excitation laser with appropriated pulse energy (ex. 19), to prepare for your first pump-probe measurements: 
		$\lambda=400nm$ 
		$25\mu m$??? 
    a) Adjust the focus of the excitation laser (ex. 18) to obtain your desired beam diameter in the sample plane. 
	    $d=150\mu m$ aber bei $f=250mm$ $\Longrightarrow d_{\text{FWHM, Airy}} \approx \mathbf{13{,}26\ \mu\text{m}}$
	    $d_{\text{Airy}} = 2{,}44 \cdot \frac{\lambda \cdot f}{D} \Longrightarrow f=\frac{d\cdot D}{2,44\cdot \lambda}=  \frac{150\cdot10^{-8}}{2,44\cdot 400\cdot 10^{-9}}= \frac{150}{97,6}$  
	    also for laser at $400nm$, with $50\mu J$ pulse energy and $150\mu m$ of diameter
		    $f=1.537m$
		    aber bei 0,05mm bei 400nm ca 120$\mu m$
	b) Adjust the spatial overlap between laser and X-ray beam. To do this, adjust the excitation laser beam by moving the focusing lens in x and y direction. 
	c) Document the profile of the excitation laser and the X-ray beam on the sample with the X-ray microscope. To do this, alternatingly move in strong X-ray attenuators to turn off the x-ray beam, and set the laser energy to zero to measure only the x-ray beam. Afterward, you can also take an image of both pulses together (with appropriate laser and x-ray intensity levels). 
	![[Pasted image 20260902110635.png]]
25. **Record your first time-resolved spectra:**
    a) Set the time delay to 100 ps. With this time delay, the laser pulse strikes the sample surely before the X-ray pulse arrives, and still not too early with respect to the expected excited state lifetime. Even if we do not yet know the exact time zero between the laser and X-ray pulses, it has already been (pre)determined to within a few ps. 
		changed concentration to 100$\mu$
		pink spectrum
		intensity: E15
		fucussiong of opt laser: 0.02
    b) Record an XES spectrum (1D, not the difference) with the laser on and a spectrum with the laser off. Plot the laser-on and laser-off together. Normalize the spectra to the area beforehand. 
	    
    c) Now also save a difference spectrum. Is a transient signal recognizable? If so, briefly describe the curve and identify any striking features. 
	    
22. Verify the optimum spatial overlap, which preset with the X-Ray Eye, based on the intensity of the pump-probe signal. Define a representative figure of merit (FOM) for the intensity of the timeresolved transient. Plot this figure of merit as a function of laser position, once along the x and once along the y directions. 
23. Plot this FOM also as a function of the excitation laser intensity. 
24. Measure the FOM as a function of the time delay between pump and probe pulses. Plot these and explain the measured curve(s). 
25. Which measurement range and step sizes of the time delay are suitable for detecting the individual steps (or the individual intermediate states) of the photophysical/photochemical reaction of [Fe(bipy)3]2+? 
    **Record difference spectra in a series of meaningful pump-probe delays and with suitable signal quality**.

---

Analysis and Interpretation 
The goal is to determine the excited state pathway(s) of [Fe(bipy)3]2+: Which state is present at long pump-prob time delays? Are there any short-lived intermediate states? What is the time-dependent population of the respective states? 
To do this, compare your measured spectra with reference spectra from a series of iron complexes (fig: 4.4, data file is provided separately). 
This series covers, for each reference sample in its ground state, the different spin multiplicities (2S + 1) between one and five (singlet to quintet). 
30. Plot the reference spectra. Compare your extracted [Fe(bipy)3]2+ spectrum in its ground state (ex. 23) to the reference spectra. 
	![[Pasted image 20260902171259.png]]
31. Take all possible differences between singlet and higher spin states from the reference spectra and plot these. 
	![[Pasted image 20260902184804.png]]
    From exercise 25, compare 
    (i) the measured 100 ps spectrum with the reference spectra and 
    (ii) the measured transient with the differences of the reference spectra. In which spin state is the [Fe(bipy)3]2+ molecule after 100 ps? 
	
33. Plot your time-resolved difference spectra from exercise 29. How does the difference spectrum change qualitatively and quantitatively over time? 
	![[Pasted image 20260902222432.png]]
34. Generate a 3D false-color plot of the time-resolved spectra, i.e., plot the emission intensity color-coded as a function of X-ray energy (yaxis) and time delay between pump and probe pulses (x-axis). Discuss this plot. 
35. ![[Pasted image 20260903015913.png]]
    ![[Pasted image 20260902222619.png]]
36. Plot the so-called kinetic traces, i.e., plot the emission intensity as a function of the time delay. To do this, choose suitable discrete emission energies and represent them by different colors. From this, determine the rise time of the population of the excited state of [Fe(bipy)3]2+. 
    ![[Pasted image 20260903011420.png]]![[Pasted image 20260903015951.png]]![[Pasted image 20260903020002.png]]
37. Can you also identify a possible ultrafast intermediate state in the relaxation cascade?
	$_{}^{3}T$-State?
	 seeeeeeeeehr schwach bei 7053.7 (100fs) zu sehen
