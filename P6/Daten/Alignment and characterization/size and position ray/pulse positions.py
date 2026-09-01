import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path("Daten/Alignment and characterization/size and position ray/pulse_data_7400eV")

files = sorted(folder.glob("*"))   # all files in folder

x_max = []
y_max = []

for file in files:

    # Load x, y and intensity
    data = np.loadtxt(file, delimiter=",", comments="#")
    # BIU2 image is 420 x 420 pixels
    image = data #.reshape(420, 420)

    # Horizontal profile: sum over rows
    profile_x = np.sum(image, axis=0)
    # Vertical profile: sum over columns
    profile_y = np.sum(image, axis=1)

    x_max.append(np.argmax(profile_x))
    y_max.append(np.argmax(profile_y))

    print(f"File: {file.name}, x_max: {x_max[-1]}, y_max: {y_max[-1]}")

# Pixel -> mm
grid_size_mm = 10.0
n_pixels = 420
mm_per_pixel = grid_size_mm / n_pixels

x_max_mm = np.array(x_max) * mm_per_pixel
y_max_mm = np.array(y_max) * mm_per_pixel

# Mean position and spatial jitter in mm
x_mean_mm = np.mean(x_max_mm)
y_mean_mm = np.mean(y_max_mm)

x_std_mm = np.std(x_max_mm)
y_std_mm = np.std(y_max_mm)

'''print("Beam position from 20 X-ray pulses")
print(f"x = {x_mean_mm:.3f} ± {x_std_mm:.3f} mm")
print(f"y = {y_mean_mm:.3f} ± {y_std_mm:.3f} mm")'''

# PLOT max positions
pulse = np.arange(1, len(files) + 1)
fig, ax = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

# Horizontal position
ax[0].plot(pulse, x_max_mm, "o-", label="Pulse position")
ax[0].axhline(x_mean_mm, linestyle="--", label=f"Mean = {x_mean_mm:.2f} mm")
ax[0].axhspan(x_mean_mm - x_std_mm, x_mean_mm + x_std_mm, alpha=0.2, label=f"±1 SD = {x_std_mm:.2f} mm")
ax[0].set_ylabel("x [mm]")
ax[0].set_title("Horizontal beam position")
ax[0].grid(True)
ax[0].legend()

# Vertical position
ax[1].plot(pulse, y_max_mm, "o-", label="Pulse position")
ax[1].axhline(y_mean_mm, linestyle="--", label=f"Mean = {y_mean_mm:.2f} mm")
ax[1].axhspan(y_mean_mm - y_std_mm, y_mean_mm + y_std_mm, alpha=0.2, label=f"±1 SD = {y_std_mm:.2f} mm")
ax[1].set_xlabel("X-ray pulse")
ax[1].set_ylabel("y [mm]")
ax[1].set_title("Vertical beam position")
ax[1].grid(True)
ax[1].legend()

plt.tight_layout()
plt.savefig("Daten/Alignment and characterization/size and position ray/pulse_positions_max.png", dpi=300)
plt.show()

# PLOT x-y distribution of pulse positions
plt.figure(figsize=(7, 6))

plt.scatter(x_max_mm, y_max_mm, s=50, label="Individual pulses")
# Mean position
plt.scatter(x_mean_mm, y_mean_mm, marker="x", s=120, label=f"Mean position ({x_mean_mm:.1f}, {y_mean_mm:.1f}) mm")
# Horizontal ±1 SD
plt.axvspan(x_mean_mm - x_std_mm, x_mean_mm + x_std_mm, alpha=0.15)
# Vertical ±1 SD
plt.axhspan(y_mean_mm - y_std_mm, y_mean_mm + y_std_mm, alpha=0.15)

plt.xlabel("x [mm]")
plt.ylabel("y [mm]")
plt.title("Spatial jitter of X-ray pulses on BIU2")
plt.axis("equal")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("Daten/Alignment and characterization/size and position ray/pulse_positions_jitter.png", dpi=300)
plt.show()