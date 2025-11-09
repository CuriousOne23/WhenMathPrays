# debug_stability.py
import numpy as np
from core.gamma_self import gamma_self
from core.gamma_stability import is_stable

# === INPUTS ===
dt = 0.1
t = np.arange(0, 10.0, dt)

gamma_t = gamma_self(t, b=0.5, A=0.25)

# === DEBUG ===
mag = np.abs(gamma_t)
arg = np.angle(gamma_t)

print(f"Max |γ_self|: {mag.max():.4f}")
print(f"Arg range: {arg.min():.2f} to {arg.max():.2f} rad")
print(f"Arg in degrees: {np.degrees(arg.min()):.1f}° to {np.degrees(arg.max()):.1f}°")
print(f"is_stable(): {is_stable(gamma_t)}")