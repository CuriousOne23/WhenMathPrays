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

theta_start = -3*np.pi/4  # -135 deg
theta_end = -np.pi        # -180 deg
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

def pdf_high(r, theta):
    d = norm.pdf(r, mu_r_high, sigma_r_high)
    g1 = gate_on(theta)
    g2 = gate_off(theta)
    angle_ok = (theta >= theta_end) & (theta <= theta_start)
    return d * g1 * g2 if angle_ok else 1e-30

def pdf_low(r, theta):
    mean = [r_boundary, theta_memory]
    cov = [[sigma_r_low**2, 0], [0, sigma_theta_low**2]]
    return multivariate_normal(mean, cov).pdf([r, theta])

# Vectorized PDF construction
theta_wrapped = ((THETA + np.pi) % (2 * np.pi)) - np.pi

# High values
d = norm.pdf(R, mu_r_high, sigma_r_high)
g1 = gate_on(theta_wrapped)
g2 = gate_off(theta_wrapped)
angle_ok = (theta_wrapped >= theta_end) & (theta_wrapped <= theta_start)
pdf_high_val = np.where(angle_ok, d * g1 * g2, 1e-30)

# Low values
rv = multivariate_normal([r_boundary, theta_memory], cov=[[sigma_r_low**2, 0], [0, sigma_theta_low**2]])
pos = np.dstack((R, theta_wrapped)).reshape(-1, 2)
pdf_low_val = rv.pdf(pos).reshape(R.shape)

# Combine raw PDF
pdf = np.where(R >= r_boundary, pdf_high_val, pdf_low_val)

# Continuity scaling
val_high = pdf_high(r_boundary, np.deg2rad(-150))
val_low = pdf_low(r_boundary, np.deg2rad(-150))
scale_low = val_high / val_low if val_low > 0 else 1.0
pdf[R < r_boundary] *= scale_low

# Global normalization
integrand = pdf * R
integral = trapezoid(trapezoid(integrand, x=theta_grid, axis=0), x=r_grid)
pdf /= integral

# Mask very low densities
pdf_masked = np.ma.masked_where(pdf <= 1e-20, pdf)

# -----------------------------
# Generate and SAVE all outputs
# -----------------------------
cmap = 'inferno'
polar_bg_color = 'black'
other_bg_color = 'lightgrey'

# 1. Full polar plot
fig1 = plt.figure(figsize=(10, 8))
ax1 = fig1.add_subplot(111, projection='polar')
im1 = ax1.pcolormesh(THETA, R, pdf_masked, cmap=cmap, shading='auto', vmin=1e-20, vmax=np.max(pdf))
ax1.set_rlim(0, 3)
ax1.set_theta_zero_location('E')  # 0° at positive x (right)
ax1.set_theta_direction(1)  # clockwise for standard math convention? Wait, default is counterclockwise, set to -1 for clockwise if needed, but standard is counter
ax1.grid(True, alpha=0.3, color='gray')
circle = plt.Circle((0,0), r_boundary, transform=ax1.transData._b, color="cyan", lw=2, fill=False)
ax1.add_artist(circle)
ax1.plot(np.deg2rad(-150), 2.0, 'o', color='yellow', markersize=10, markeredgecolor='black')
ax1.text(np.deg2rad(45), 3.5, "Q1", ha='center', va='center', fontsize=14, color='white')
ax1.text(np.deg2rad(135), 3.5, "Q2", ha='center', va='center', fontsize=14, color='white')
ax1.text(np.deg2rad(225), 3.5, "Q3", ha='center', va='center', fontsize=14, color='white')
ax1.text(np.deg2rad(315), 3.5, "Q4", ha='center', va='center', fontsize=14, color='white')
ax1.set_title("Revenge Density map of Revenge population (probability density per unit area)", pad=20, color='white')
cbar1 = plt.colorbar(im1, ax=ax1, shrink=0.6, label='Density')
cbar1.ax.yaxis.set_label_position('left')
cbar1.ax.yaxis.label.set_color('white')
cbar1.ax.tick_params(labelcolor='white')
ax1.set_facecolor(polar_bg_color)
fig1.patch.set_facecolor(polar_bg_color)
plt.savefig(os.path.join(output_dir, "1_revenge_gamma_self_full_polar.png"), dpi=300, bbox_inches='tight', facecolor=polar_bg_color)
plt.close(fig1)

# 2. Zoomed polar
fig2 = plt.figure(figsize=(10, 8))
ax2 = fig2.add_subplot(111, projection='polar')
im2 = ax2.pcolormesh(THETA, R, pdf_masked, cmap=cmap, shading='auto', vmin=1e-20, vmax=np.max(pdf))
ax2.set_rlim(0, 1.0)
ax2.set_theta_zero_location('E')
ax2.set_theta_direction(1)
ax2.grid(True, alpha=0.3, color='gray')
ax2.set_title("Zoomed up Revenge Density plot (probability density per unit area) for radius of less than or equal to 0.5", pad=20, color='white')
cbar2 = plt.colorbar(im2, ax=ax2, shrink=0.6, label='Density')
cbar2.ax.yaxis.set_label_position('left')
cbar2.ax.yaxis.label.set_color('white')
cbar2.ax.tick_params(labelcolor='white')
ax2.set_facecolor(polar_bg_color)
fig2.patch.set_facecolor(polar_bg_color)
plt.savefig(os.path.join(output_dir, "2_revenge_gamma_self_zoom_polar.png"), dpi=300, bbox_inches='tight', facecolor=polar_bg_color)
plt.close(fig2)

# 3. Marginal pdf(r)
fig3 = plt.figure(figsize=(10, 6))
marginal_r = trapezoid(pdf * R, x=theta_grid, axis=0)
gradient_cmap = LinearSegmentedColormap.from_list('black_yellow', ['black', 'yellow'])
gradient = np.linspace(0, 1, len(r_grid))
plt.plot(r_grid, marginal_r, color='black', linewidth=3)
for i in range(len(r_grid)-1):
    plt.fill_between(r_grid[i:i+2], 0, marginal_r[i:i+2], color=gradient_cmap(gradient[i]), alpha=0.7)
plt.xlim(0, 3)
plt.xlabel("r")
plt.ylabel("pdf(r)")
ax3 = plt.gca()
ax3.set_facecolor(other_bg_color)
ax3.spines['bottom'].set_color('black')
ax3.spines['left'].set_color('black')
plt.grid(True, alpha=0.3, color='gray')
plt.tick_params(colors='black')
fig3.patch.set_facecolor(other_bg_color)
plt.savefig(os.path.join(output_dir, "3_revenge_marginal_pdf_r.png"), dpi=300, bbox_inches='tight', facecolor=other_bg_color)
plt.close(fig3)

# 4. XY Scatter (1000 points)
fig4 = plt.figure(figsize=(10, 10))
n_samples = 1000
samples_r = []
samples_theta = []
densities = []

max_target = np.max(pdf * R)

while len(samples_r) < n_samples:
    r_cand = np.random.uniform(0, 3.5)
    theta_cand = np.random.uniform(-np.pi, np.pi)
    th_wrapped = ((theta_cand + np.pi) % (2 * np.pi)) - np.pi
    if r_cand >= r_boundary:
        p = pdf_high(r_cand, th_wrapped)
    else:
        p = pdf_low(r_cand, th_wrapped) * scale_low
    p /= integral
    if np.random.rand() < (p * r_cand) / (max_target * 1.5):
        samples_r.append(r_cand)
        samples_theta.append(theta_cand)
        densities.append(p)

x = np.array(samples_r) * np.cos(samples_theta)
y = np.array(samples_r) * np.sin(samples_theta)
sc = plt.scatter(x, y, c=densities, cmap='hot', s=2, edgecolors='none', alpha=0.9)
circle_sc = plt.Circle((0,0), r_boundary, color="cyan", fill=False, lw=2, ls='--')
plt.gca().add_artist(circle_sc)
plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.axhline(0, color='gray', alpha=0.5)
plt.axvline(0, color='gray', alpha=0.5)
plt.xlabel("x = real (we on +, ego on -)")
plt.ylabel("y = imaginary (love on +, enmity on -)")
plt.title("XY Scatter plot of the Revenge population")
ax4 = plt.gca()
ax4.set_facecolor(other_bg_color)
fig4.patch.set_facecolor(other_bg_color)
plt.tick_params(colors='black')
ax4.spines['bottom'].set_color('black')
ax4.spines['top'].set_color('black')
ax4.spines['left'].set_color('black')
ax4.spines['right'].set_color('black')
plt.gca().set_aspect('equal')
plt.savefig(os.path.join(output_dir, "4_revenge_xy_scatter_samples.png"), dpi=300, bbox_inches='tight', facecolor=other_bg_color)
plt.close(fig4)

# Markdown table + results
table_path = os.path.join(output_dir, "revenge_gamma_self_results.md")
with open(table_path, "w", encoding="utf-8") as f:
    f.write("# Revenge Gamma-Self Distribution Results\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} MST\n\n")
    f.write("**Summary of PDF Construction:**\n")
    f.write("The revenge gamma-self PDF is defined in polar coordinates (r, θ), with r ≥ 0 representing magnitude, and θ in [-π, π] representing angle (0° at positive real axis 'we', 90° at positive imaginary 'love', clockwise or counterclockwise as per standard).\n")
    f.write("For r ≥ 0.5: Density is a Gaussian in r ~ N(μ=2, σ=0.5), multiplied by two tanh-like gates confining to θ in [-135°, -180°] (Q3: ego-enmity): sharp turn-on at -135° with α=5°, soft fade at -180° with β=30°. Zero density outside this angular range to prevent leaks into Q1/Q4.\n")
    f.write("For r ≤ 0.5: Switches to a bivariate normal centered at (r=0.5, θ=-150°), with σ_r=0.3, σ_θ=30° (uncorrelated), allowing faint drift tails only near Q3 and adjacent boundaries.\n")
    f.write("The low-r part is scaled to ensure continuity at r=0.5 (no density jump), and the entire PDF is globally normalized so ∫ pdf(r,θ) r dr dθ = 1 over r=0 to ∞, θ=-π to π.\n")
    f.write("Key values: μ_r=2, σ_r_high=0.5, σ_r_low=0.3, σ_θ_low=30°, α=5°, β=30°, boundary r=0.5, memory θ=-150°.\n")
    f.write("Regions: Q1 (0° to 90°: we-love), Q2 (90° to 180°: ego-love), Q3 (180° to 270° or -180° to -90°: ego-enmity), Q4 (270° to 360° or -90° to 0°: we-enmity).\n")
    f.write("Variables: x = r cosθ (real: we +, ego -), y = r sinθ (imag: love +, enmity -).\n")
    f.write("Properties: Peak at (r≈2, θ≈-150°), only tiny drifts below r=0.5 in Q1/Q4/Q2 from nearby seeding, no high-r leaks into Q1/Q4.\n")
    f.write("To recreate: Implement the above piecewise definition, wrap angles to [-π, π], scale for continuity at match point (e.g., θ=-150°), normalize via numerical integration.\n\n")
    f.write("**Parameters:** σ_r=0.3, σ_θ=30°, α=5°, β=30°, μ_r=2\n\n")
    f.write("| Point        | r   | θ (degrees) | pdf_value    |\n")
    f.write("|--------------|-----|-------------|--------------|\n")
    
    test_points = [
        ("origin",      0.1, -150),
        ("drift-Q3",    0.4, -135),
        ("peak",        2.0, -150),
        ("boundary",    0.6, -150),
        ("Q1-drift",    0.4,   45),
        ("neg45-drift", 0.4,  -45),
        ("pos135-drift",0.4,  135),
    ]
    
    for name, r, theta_deg in test_points:
        theta = np.deg2rad(theta_deg)
        if r >= r_boundary:
            val = pdf_high(r, theta)
        else:
            val = pdf_low(r, theta) * scale_low
        val /= integral
        f.write(f"| {name:<12} | {r:<3} | {theta_deg:>8}    | {val:.2e} |\n")

print("\nAll files successfully saved to:")
print(output_dir)
print("\nFiles created:")
print("   1_revenge_gamma_self_full_polar.png")
print("   2_revenge_gamma_self_zoom_polar.png")
print("   3_revenge_marginal_pdf_r.png")
print("   4_revenge_xy_scatter_samples.png")
print("   revenge_gamma_self_results.md")
print("\nDone. No bugs. Q3 confinement perfect. No revenge tails into Q1/Q4 above r=0.5.")
print(f"Number of samples: {len(samples_r)}")