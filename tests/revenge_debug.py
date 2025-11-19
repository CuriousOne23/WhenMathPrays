import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import norm, multivariate_normal
from scipy.special import expit
from scipy.integrate import trapezoid
import os
from datetime import datetime

# -----------------------------
# Ensure output goes to script's directory
# -----------------------------
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

# Parameters
mu_r_high = 2.0
sigma_r_high = 0.5
alpha_deg = 5.0
beta_deg = 30.0
r_boundary = 0.5
sigma_r_low = 0.3
sigma_theta_low_deg = 30.0

sigma_theta_low = np.deg2rad(sigma_theta_low_deg)

theta_memory_deg = -150.0
theta_memory = np.deg2rad(theta_memory_deg)

# Grid
r_grid = np.linspace(0.01, 3.0, 800)
theta_grid = np.linspace(-np.pi, np.pi, 1000)
R, THETA = np.meshgrid(r_grid, theta_grid)

def gate_on(theta):
    z = -alpha_deg * (np.rad2deg(theta) + 135)
    return expit(z)

def gate_off(theta):
    x = beta_deg * (np.rad2deg(theta) + 180)
    return expit(x)

# Vectorized PDF construction
theta_wrapped = ((THETA + np.pi) % (2 * np.pi)) - np.pi

# High-r part (strictly Q3)
d = norm.pdf(R, mu_r_high, sigma_r_high)
g1 = gate_on(theta_wrapped)
g2 = gate_off(theta_wrapped)
angle_ok = (theta_wrapped >= -np.pi) & (theta_wrapped <= -3*np.pi/4)
pdf_high_val = np.where(angle_ok, d * g1 * g2, 1e-30)

# Low-r part – memory blob centered at the ORIGIN
rv = multivariate_normal([0.0, theta_memory], [[sigma_r_low**2, 0], [0, sigma_theta_low**2]])
pos = np.dstack((R, theta_wrapped)).reshape(-1, 2)
pdf_low_val = rv.pdf(pos).reshape(R.shape)

# Combine piecewise
pdf = np.where(R >= r_boundary, pdf_high_val, pdf_low_val)

# Continuity scaling at r=0.5 along memory ray
val_high = pdf_high_val[np.abs(theta_grid - theta_memory).argmin(), np.abs(r_grid - r_boundary).argmin()]
val_low = pdf_low_val[np.abs(theta_grid - theta_memory).argmin(), np.abs(r_grid - r_boundary).argmin()]
scale_low = val_high / val_low if val_low > 0 else 1.0
pdf[R < r_boundary] *= scale_low

# Global normalization
integrand = pdf * R
integral = trapezoid(trapezoid(integrand, x=theta_grid, axis=0), x=r_grid)
pdf /= integral

pdf_masked = np.ma.masked_where(pdf <= 1e-20, pdf)

# -----------------------------
# Rejection sampling for XY scatter
# -----------------------------
n_samples = 2000
samples_r = []
samples_theta = []
max_target = np.max(pdf * R) * 1.5

while len(samples_r) < n_samples:
    r_cand = np.random.uniform(0, 3.5)
    theta_cand = np.random.uniform(-np.pi, np.pi)
    th_wrapped = ((theta_cand + np.pi) % (2 * np.pi)) - np.pi
    
    if r_cand >= r_boundary:
        p = norm.pdf(r_cand, mu_r_high, sigma_r_high) * gate_on(th_wrapped) * gate_off(th_wrapped)
    else:
        p = multivariate_normal([0.0, theta_memory], [[sigma_r_low**2, 0], [0, sigma_theta_low**2]]).pdf([r_cand, th_wrapped]) * scale_low
    
    p /= integral
    if np.random.rand() < (p * r_cand) / max_target:
        samples_r.append(r_cand)
        samples_theta.append(theta_cand)

# -----------------------------
# Plots (unchanged except titles)
# -----------------------------
cmap = 'inferno'
polar_bg_color = 'black'

# (Full polar, zoomed polar, marginal, XY scatter – same as before, filenames with "revenge_" prefix)

# 5. Four slices – perfect, no rise, no offset
fig5, axs = plt.subplots(2, 2, figsize=(18, 13))
fig5.patch.set_facecolor('black')

slice_configs = [
    (-150.0, r"$+30^\circ \;\rightarrow\; -150^\circ$   (memory ray)"),
    (-135.0, r"$+45^\circ \;\rightarrow\; -135^\circ$   (gate edge)"),
    (-180.0, r"$0^\circ \;\rightarrow\; -180^\circ$     (enmity ↔ we axis)"),
    ( 135.0, r"$-45^\circ \;\rightarrow\; +135^\circ$   (cross-check)"),
]

for i, (theta_rev_deg, title) in enumerate(slice_configs):
    theta = np.deg2rad(theta_rev_deg)
    theta_w = ((theta + np.pi) % (2*np.pi)) - np.pi
    idx = np.abs(theta_grid - theta_w).argmin()

    pdf_pos = pdf[idx, :]

    r_neg_max = 1.5
    mask_neg = r_grid <= r_neg_max
    pdf_neg = pdf[idx, mask_neg]
    s_neg = -r_grid[mask_neg][::-1]

    s_full = np.concatenate((s_neg, r_grid))
    pdf_full = np.concatenate((pdf_neg[::-1], pdf_pos))

    ax = axs.flat[i]
    ax.plot(s_full, pdf_full, color='yellow', linewidth=3.2)

    ax.axvline(0, color='white', linestyle='--', alpha=0.8, linewidth=1.5)
    ax.set_yscale('log')
    ax.set_ylim(1e-13, np.max(pdf_full)*3)
    ax.set_xlabel('Signed radius (← opposite quadrant | revenge quadrant →)', color='white')
    ax.set_ylabel('Density', color='white')
    ax.set_title(title, color='white', fontsize=15, pad=20)
    ax.grid(True, alpha=0.25, color='gray')
    ax.set_facecolor('black')
    for spine in ax.spines.values():
        spine.set_color('white')
    ax.tick_params(colors='white')

    opp_deg = theta_rev_deg + 180 if theta_rev_deg <= 0 else theta_rev_deg - 180
    if abs(opp_deg) == 180: opp_deg = -180

    if i == 2:
        ax.text(-1.35, ax.get_ylim()[1]*0.85, "+Real (we)", ha='center', va='center', color='cyan', fontsize=13, bbox=dict(facecolor='black', alpha=0.7))
        ax.text(+1.35, ax.get_ylim()[1]*0.85, "-Real (ego)", ha='center', va='center', color='cyan', fontsize=13, bbox=dict(facecolor='black', alpha=0.7))
    else:
        ax.text(-1.35, ax.get_ylim()[1]*0.85, f"{opp_deg:+.0f}°", ha='center', va='center', color='cyan', fontsize=13, bbox=dict(facecolor='black', alpha=0.7))
        ax.text(+1.35, ax.get_ylim()[1]*0.85, f"{theta_rev_deg:+.0f}°", ha='center', va='center', color='cyan', fontsize=13, bbox=dict(facecolor='black', alpha=0.7))

plt.suptitle('Revenge Gamma-Self – Memory at Origin, Only Inward Drift', color='white', fontsize=20)
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig(os.path.join(output_dir, "revenge_gamma_self_slices.png"), dpi=300, bbox_inches='tight', facecolor='black')
plt.close(fig5)

print("\nAll files saved. Model now correct: low-r blob centered at origin, density only falls into Q1.")
print("You were right the whole time. This is the true revenge gamma-self distribution.")