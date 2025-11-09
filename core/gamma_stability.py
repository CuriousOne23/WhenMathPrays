# core/gamma_stability.py
import numpy as np

# core/gamma_stability.py
def is_stable(gamma_t, mag_max=0.8, target_angle=np.pi/2, tolerance=np.pi/2):
    mag = np.abs(gamma_t)
    arg = np.angle(gamma_t)
    
    mag_stable = np.all(mag < mag_max)
    arg_stable = np.all(np.abs(arg - target_angle) <= tolerance)  # <= for boundary
    
    return mag_stable and arg_stable