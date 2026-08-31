import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# ------------------------------------------------------------
# Load BIU2 data
# ------------------------------------------------------------

filename = "Daten/Alignment and characterization/size and position ray/BeamImagingUnit2 26-08-31 13-49-38"

data = np.loadtxt(filename, delimiter=",", comments="#")

# BIU2 image is 420 x 420 pixels
image = data.reshape(420, 420)

# Pixel coordinates
x = np.arange(image.shape[1])
y = np.arange(image.shape[0])


# ------------------------------------------------------------
# Calculate horizontal and vertical profiles
# ------------------------------------------------------------

# Horizontal profile: sum over rows
profile_x = np.sum(image, axis=0)

# Vertical profile: sum over columns
profile_y = np.sum(image, axis=1)


# ------------------------------------------------------------
# FWHM function
# ------------------------------------------------------------

def calculate_fwhm(coordinate, profile):

    # Background estimation from the edges
    background = np.median(
        np.concatenate([profile[:30], profile[-30:]])
    )

    profile = profile - background

    # Maximum and half maximum
    peak = np.max(profile)
    half_max = peak / 2

    # Indices above half maximum
    indices = np.where(profile >= half_max)[0]

    left = indices[0]
    right = indices[-1]

    # Linear interpolation at the half-maximum crossings
    f_left = interp1d(
        profile[left-1:left+1],
        coordinate[left-1:left+1]
    )

    f_right = interp1d(
        profile[right:right+2],
        coordinate[right:right+2]
    )

    x_left = float(f_left(half_max))
    x_right = float(f_right(half_max))

    fwhm = x_right - x_left
    center = (x_left + x_right) / 2

    return fwhm, center, half_max, x_left, x_right


# ------------------------------------------------------------
# Calculate FWHM
# ------------------------------------------------------------

fwhm_x, center_x, half_x, left_x, right_x = \
    calculate_fwhm(x, profile_x)

fwhm_y, center_y, half_y, left_y, right_y = \
    calculate_fwhm(y, profile_y)


print(f"Horizontal:")
print(f"  Center = {center_x:.2f} px")
print(f"  FWHM   = {fwhm_x:.2f} px")

print()

print(f"Vertical:")
print(f"  Center = {center_y:.2f} px")
print(f"  FWHM   = {fwhm_y:.2f} px")


# ------------------------------------------------------------
# Plot profiles
# ------------------------------------------------------------

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Horizontal
ax[0].plot(x, profile_x, label="Horizontal profile")
ax[0].axhline(half_x, linestyle="--", label="Half maximum")
ax[0].axvline(left_x, linestyle=":")
ax[0].axvline(right_x, linestyle=":")
ax[0].axvline(center_x, linestyle="--",
              label=f"Center = {center_x:.1f} px")

ax[0].set_xlabel("x [pixel]")
ax[0].set_ylabel("Integrated intensity")
ax[0].set_title(f"Horizontal profile — FWHM = {fwhm_x:.1f} px")
ax[0].legend()
ax[0].grid(True)


# Vertical
ax[1].plot(y, profile_y, label="Vertical profile")
ax[1].axhline(half_y, linestyle="--", label="Half maximum")
ax[1].axvline(left_y, linestyle=":")
ax[1].axvline(right_y, linestyle=":")
ax[1].axvline(center_y, linestyle="--",
              label=f"Center = {center_y:.1f} px")

ax[1].set_xlabel("y [pixel]")
ax[1].set_ylabel("Integrated intensity")
ax[1].set_title(f"Vertical profile — FWHM = {fwhm_y:.1f} px")
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.savefig("Daten/Alignment and characterization/size and position ray/FWHM_profiles.png", dpi=300)
plt.show()