import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path


folder = Path("Daten/Experiment with Data Acquisition/laser/xray profile")

files = sorted(folder.glob("*"))

# ============================================================
# Pixel -> mm conversion
# ============================================================

grid_size_mm = 2.0
n_pixels = 420

mm_per_pixel = grid_size_mm / n_pixels

x = np.arange(n_pixels) * mm_per_pixel
y = np.arange(n_pixels) * mm_per_pixel


# ============================================================
# Load image
# ============================================================

for file in files:
    data = np.loadtxt(file, delimiter=",", comments="#")

    image = data.reshape(420, 420)

    # Horizontal profile
    profile_x = np.sum(image, axis=0)

    # Vertical profile
    profile_y = np.sum(image, axis=1)


# ============================================================
# Gaussian
# ============================================================

def gaussian(x, A, mu, sigma, B):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2)) + B


# ============================================================
# Gaussian fit
# ============================================================

def fit_gaussian(coordinate, profile):

    # Background
    B0 = np.median(
        np.concatenate([
            profile[:30],
            profile[-30:]
        ])
    )

    # Amplitude
    A0 = np.max(profile) - B0

    # Initial center
    mu0 = coordinate[np.argmax(profile)]

    # Estimate sigma from approximate FWHM
    half_max = B0 + A0 / 2

    indices = np.where(profile > half_max)[0]

    if len(indices) >= 2:
        fwhm0 = coordinate[indices[-1]] - coordinate[indices[0]]
        sigma0 = fwhm0 / (2 * np.sqrt(2 * np.log(2)))
    else:
        sigma0 = 0.05

    print(
        f"Initial guess: "
        f"A={A0:.3g}, mu={mu0:.4f} mm, "
        f"sigma={sigma0:.4f} mm, B={B0:.3g}"
    )

    p0 = [A0, mu0, sigma0, B0]

    # Bounds
    lower_bounds = [
        0,
        coordinate.min(),
        mm_per_pixel / 2,
        -np.inf
    ]

    upper_bounds = [
        np.inf,
        coordinate.max(),
        grid_size_mm,
        np.inf
    ]

    # Fit
    popt, pcov = curve_fit(
        gaussian,
        coordinate,
        profile,
        p0=p0,
        bounds=(lower_bounds, upper_bounds),
        maxfev=50000
    )

    A, mu, sigma, B = popt

    # FWHM
    fwhm = 2 * np.sqrt(2 * np.log(2)) * sigma

    # Errors
    perr = np.sqrt(np.diag(pcov))

    sigma_err = perr[2]
    fwhm_err = 2 * np.sqrt(2 * np.log(2)) * sigma_err

    return popt, fwhm, fwhm_err


# ============================================================
# Fit
# ============================================================

popt_x, fwhm_x, fwhm_x_err = fit_gaussian(x, profile_x)
popt_y, fwhm_y, fwhm_y_err = fit_gaussian(y, profile_y)

A_x, center_x, sigma_x, B_x = popt_x
A_y, center_y, sigma_y, B_y = popt_y


# ============================================================
# Results
# ============================================================

print()
print("====================================")
print("Beam profile")
print("====================================")

print(f"Pixel size = {mm_per_pixel:.6f} mm/px")
print(f"Pixel size = {mm_per_pixel * 1000:.2f} µm/px")
print()

print("Horizontal:")
print(f"  Center = {center_x:.4f} mm")
print(f"  Sigma  = {sigma_x:.4f} mm")
print(f"  FWHM   = {fwhm_x:.4f} ± {fwhm_x_err:.4f} mm")
print(f"  FWHM   = {fwhm_x * 1000:.1f} ± {fwhm_x_err * 1000:.1f} µm")

print()

print("Vertical:")
print(f"  Center = {center_y:.4f} mm")
print(f"  Sigma  = {sigma_y:.4f} mm")
print(f"  FWHM   = {fwhm_y:.4f} ± {fwhm_y_err:.4f} mm")
print(f"  FWHM   = {fwhm_y * 1000:.1f} ± {fwhm_y_err * 1000:.1f} µm")


# ============================================================
# Smooth curves
# ============================================================

x_fit = np.linspace(x.min(), x.max(), 1000)
y_fit = np.linspace(y.min(), y.max(), 1000)

gauss_x = gaussian(x_fit, *popt_x)
gauss_y = gaussian(y_fit, *popt_y)


# ============================================================
# Plot
# ============================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))


# ------------------------------------------------------------
# Horizontal
# ------------------------------------------------------------

ax[0].plot(
    x,
    profile_x,
    label="Measured profile"
)

ax[0].plot(
    x_fit,
    gauss_x,
    "--",
    label="Gaussian fit"
)

ax[0].axvline(
    center_x - fwhm_x / 2,
    linestyle=":",
    label="FWHM"
)

ax[0].axvline(
    center_x + fwhm_x / 2,
    linestyle=":"
)

ax[0].axvline(
    center_x,
    linestyle="--",
    label=f"$x_0$ = {center_x:.3f} mm"
)

ax[0].set_xlabel("x [mm]")
ax[0].set_ylabel("Integrated intensity")

ax[0].set_title(
    f"Horizontal profile\n"
    f"FWHM = {fwhm_x * 1000:.1f} µm"
)

ax[0].set_xlim(0.95, 1.05)
#ax[0].set_xlim(x.min(), x.max())

ax[0].legend()
ax[0].grid(True)


# ------------------------------------------------------------
# Vertical
# ------------------------------------------------------------

ax[1].plot(
    y,
    profile_y,
    label="Measured profile"
)

ax[1].plot(
    y_fit,
    gauss_y,
    "--",
    label="Gaussian fit"
)

ax[1].axvline(
    center_y - fwhm_y / 2,
    linestyle=":",
    label="FWHM"
)

ax[1].axvline(
    center_y + fwhm_y / 2,
    linestyle=":"
)

ax[1].axvline(
    center_y,
    linestyle="--",
    label=f"$y_0$ = {center_y:.3f} mm"
)

ax[1].set_xlabel("y [mm]")
ax[1].set_ylabel("Integrated intensity")

ax[1].set_title(
    f"Vertical profile\n"
    f"FWHM = {fwhm_y * 1000:.1f} µm"
)

ax[1].set_xlim(0.95, 1.05)
#ax[1].set_xlim(y.min(), y.max())

ax[1].legend()
ax[1].grid(True)


plt.tight_layout()

plt.savefig(
    "Daten/Experiment with Data Acquisition/laser/xray_beam_profile.png",
    dpi=300
)

plt.show()