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

    x = np.arange(data.shape[1])
    y = np.arange(data.shape[0])

    # Horizontal profile: sum over rows
    profile_x = np.sum(image, axis=0)
    # Vertical profile: sum over columns
    profile_y = np.sum(image, axis=1)

    x_max.append(np.argmax(profile_x))
    y_max.append(np.argmax(profile_y))

    print(f"File: {file.name}, x_max: {x_max[-1]}, y_max: {y_max[-1]}")

# Mean position and spatial jitter

x_mean = np.mean(x_max)
y_mean = np.mean(y_max)

x_std = np.std(x_max)
y_std = np.std(y_max)


print("Beam position from 20 X-ray pulses")
print(f"x = {x_mean:.2f} ± {x_std:.2f} px")
print(f"y = {y_mean:.2f} ± {y_std:.2f} px")

# PLOT max positions
pulse = np.arange(1, len(files) + 1)
fig, ax = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

# Horizontal position
ax[0].plot(pulse, x_max, "o-", label="Pulse position")
ax[0].axhline(x_mean, linestyle="--", label=f"Mean = {x_mean:.2f} px")
ax[0].axhspan(x_mean - x_std, x_mean + x_std, alpha=0.2, label=f"±1 SD = {x_std:.2f} px")
ax[0].set_ylabel("x [pixel]")
ax[0].set_title("Horizontal beam position")
ax[0].grid(True)
ax[0].legend()

# Vertical position
ax[1].plot(pulse, y_max, "o-", label="Pulse position")
ax[1].axhline(y_mean, linestyle="--", label=f"Mean = {y_mean:.2f} px")
ax[1].axhspan(y_mean - y_std, y_mean + y_std, alpha=0.2, label=f"±1 SD = {y_std:.2f} px")
ax[1].set_xlabel("X-ray pulse")
ax[1].set_ylabel("y [pixel]")
ax[1].set_title("Vertical beam position")
ax[1].grid(True)
ax[1].legend()

plt.tight_layout()
plt.savefig("Daten/Alignment and characterization/size and position ray/pulse_positions_max.png", dpi=300)
plt.show()

# PLOT x-y distribution of pulse positions
plt.figure(figsize=(7, 6))

plt.scatter(x_max, y_max, s=50, label="Individual pulses")
# Mean position
plt.scatter(x_mean, y_mean, marker="x",s=120, label=f"Mean position ({x_mean:.1f}, {y_mean:.1f}) px")
# Horizontal ±1 SD
plt.axvspan(x_mean - x_std, x_mean + x_std, alpha=0.15)
# Vertical ±1 SD
plt.axhspan(y_mean - y_std, y_mean + y_std, alpha=0.15)

plt.xlabel("x [pixel]")
plt.ylabel("y [pixel]")
plt.title("Spatial jitter of X-ray pulses on BIU2")
plt.axis("equal")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("Daten/Alignment and characterization/size and position ray/pulse_positions_jitter.png", dpi=300)
plt.show()