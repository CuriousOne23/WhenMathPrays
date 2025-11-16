#!/usr/bin/env python
"""
distributions_gamma_self.py
γ_self Character Region Map — 9 statistical archetypes.
- User-defined N via --N
- Revenge: single continuous field with echo-waver at r ≤ 0.5
- Core: r > 0.5, θ ≈ -135°
- Waver: r ≤ 0.5, θ = reflected from core at r=0.5
- Hard cutoff: no θ > -135°
- Natural decay: p(r) ∝ r^2 * exp(-1.5 r)
- All 9: natural bounds, no clips
- Project: #WhenMathPrays
- Author: @PursueTruth123
- Country: US
- Generated: November 15, 2025 04:07 PM MST
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from typing import Dict, List
from dataclasses import dataclass
import textwrap

# =============================================================================
# γ_self Character Region Map — INTENT & ASSUMPTIONS
# Project: #WhenMathPrays
# Author: @PursueTruth123
# Country: US
# Generated: November 15, 2025 04:07 PM MST
# =============================================================================

"""
CORE PRINCIPLE
> "At large magnitude, the soul is committed.
> At small magnitude, the soul wavers — in the echo of the core."

This is not noise. This is the geometry of free will.

---

REVENGE FIELD — ECHO WAVER
- Single continuous distribution
- p(r) ∝ r^2 * exp(-1.5 r) → peak at r=2.67
- Core: r > 0.5, θ ≈ -135°
- Waver: r ≤ 0.5, θ = reflected from core at r=0.5
- Hard cutoff: no θ > -135°
- Natural max ≈ 4.0

---

OTHER ARCHETYPES
- In-Field: ±45° around major ray
- Outliers: beyond ±45°, or small |γ| in wrong quadrant

---

USER CONTROL
- --N <value> → generate exactly N points per archetype
- Default: N = 1000

---

QUADRANT CONVENTION (angle from +Re axis)
- 0°   ≥ pQ1 < 90°
- 90°  ≥ pQ2 < 180°
- -180° ≥ pQ3 > -90°
- -90° ≥ pQ4 < 0°
"""

# ---------- OUTPUT BASE ----------
PLOT_BASE = "core/gamma_self_character_map"
TABLE_BASE = "core/gamma_self_quadrants"

# ---------- CONSTANTS ----------
OVERSAMPLE_FACTOR = 12
DEFAULT_N = 1000
WAVER_MAX = 0.5
REVENGE_LAMBDA = 1.5
REVENGE_ANGLE_CUTOFF = -135

# ---------- ARCHETYPE DATACLASS ----------
@dataclass
class Archetype:
    name: str
    angle_deg: float
    mean_mag: float
    cov: np.ndarray
    color: str
    quadrant: str
    description: str = ""
    statistical_basis: str = ""
    post_filter: callable = None

# ---------- HELPER: ROTATE COVARIANCE ----------
def rotate_covariance(cov, angle_deg):
    theta = np.deg2rad(angle_deg)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    return R @ cov @ R.T

# ---------- 9 ARCHETYPES ----------
DISTRIBUTIONS: Dict[str, Archetype] = {
    "buddhist": Archetype(
        name="Buddhist",
        angle_deg=0,
        mean_mag=0.0,
        cov=np.array([[0.15, 0.0], [0.0, 0.15]]),
        color="#2ca02c",
        quadrant="Origin",
        description="Tiny symmetric circle at (0,0).",
        statistical_basis="Isotropic Gaussian, σ_re = σ_im = 0.15"
    ),
    "narcissist": Archetype(
        name="Narcissist",
        angle_deg=180,
        mean_mag=3.0,
        cov=np.array([[0.7, 0.0], [0.0, 0.15]]),
        color="#d62728",
        quadrant="Q2/Q3",
        description="Horizontal oval on -Re axis, max Re ≈ -5.1.",
        statistical_basis="Anisotropic Gaussian, σ_re=0.7, σ_im=0.15"
    ),
    "soulmate": Archetype(
        name="Soul Mate",
        angle_deg=90,
        mean_mag=3.0,
        cov=np.array([[0.3, 0.0], [0.0, 1.5]]),
        color="#ff7f0e",
        quadrant="Q1",
        description="Vertical oval along +Im, max Im ≈ +7.5.",
        statistical_basis="Anisotropic Gaussian, σ_re=0.3, σ_im=1.5"
    ),
    "mature_marriage": Archetype(
        name="Mature Marriage",
        angle_deg=45,
        mean_mag=2.5,
        cov=np.array([[0.8, 0.5], [0.5, 0.8]]),
        color="#1f77b4",
        quadrant="Q1",
        description="Circular cloud in Q1, centered on 45°.",
        statistical_basis="Correlated Gaussian, ρ≈0.6"
    ),
    "parent": Archetype(
        name="Parenting",
        angle_deg=45,
        mean_mag=2.8,
        cov=np.array([[0.5, 0.15], [0.15, 0.4]]),
        color="#9467bd",
        quadrant="Q1",
        description="Teardrop fan-out along 45°, max |γ| ≈ 6.8.",
        statistical_basis="Radial Gaussian, p(r)∝1/r"
    ),
    "ego_dating": Archetype(
        name="Ego Dating",
        angle_deg=135,
        mean_mag=2.5,
        cov=rotate_covariance(np.array([[1.0, 0.0], [0.0, 0.5]]), 135),
        color="#8c564b",
        quadrant="Q2",
        description="Asymmetrical oval centered on 135° in Q2.",
        statistical_basis="Rotated Gaussian, σ_long=1.0, σ_short=0.5"
    ),
    "battlefield": Archetype(
        name="Battlefield Hate",
        angle_deg=-90,
        mean_mag=3.5,
        cov=np.array([[0.3, 0.0], [0.0, 1.8]]),
        color="#e377c2",
        quadrant="Q4",
        description="Vertical oval on -Im axis, max Im ≈ -7.0.",
        statistical_basis="Anisotropic Gaussian, σ_re=0.3, σ_im=1.8"
    ),
    "quiet_resentment": Archetype(
        name="Quiet Resentment",
        angle_deg=-45,
        mean_mag=2.0,
        cov=np.array([[0.5, 0.0], [0.0, 0.5]]),
        color="#7f7f7f",
        quadrant="Q3",
        description="Tight circle in Q3.",
        statistical_basis="Isotropic Gaussian, σ_re=σ_im=0.5"
    ),
    "revenge": Archetype(
        name="Revenge",
        angle_deg=-135,
        mean_mag=2.5,
        cov=np.array([[0.25, 0.15], [0.15, 0.20]]),
        color="#bcbd22",
        quadrant="Q3",
        description="Single continuous field. Core: r > 0.5, θ ≈ -135°. Waver: r ≤ 0.5, θ = reflected from core.",
        statistical_basis="Radial Gaussian, p(r)∝r^2*exp(-1.5r), echo-waver"
    ),
}

# ---------- REVENGE: ECHO WAVER ----------
def generate_revenge_samples(N: int) -> np.ndarray:
    """
    Revenge: One continuous soul.
    - p(r) ∝ r^2 * exp(-1.5 r)
    - Core: r > 0.5, θ ≈ -135°
    - Waver: r ≤ 0.5, θ = reflected from core at r=0.5
    - Hard cutoff: no θ > -135°
    - Natural max ≈ 4.0
    """
    # Target mean
    target_x = 2.5 * np.cos(np.deg2rad(-135))
    target_y = 2.5 * np.sin(np.deg2rad(-135))

    # Generate r with p(r) ∝ r^2 * exp(-λr)
    lambda_r = REVENGE_LAMBDA
    r = np.random.exponential(scale=1/lambda_r, size=N*10)
    pdf = r**2 * np.exp(-lambda_r * r)
    accept = np.random.uniform(0, 1, size=len(r)) < (pdf / pdf.max())
    r = r[accept]
    if len(r) < N:
        r = np.concatenate([r, np.random.exponential(scale=1/lambda_r, size=N - len(r))])
    r = r[:N]

    # Core and Waver
    core = r > WAVER_MAX
    waver = ~core

    theta = np.zeros(N)

    # Core: θ ≈ -135°
    theta[core] = np.random.normal(-135, 18, size=core.sum())

    # Waver: reflect core at r=0.5
    if waver.sum() > 0:
        # Use core PDF at r=0.5
        r_core = np.full(waver.sum(), 0.5)
        theta_core = np.random.normal(-135, 18, size=waver.sum())
        # Reflect around -135°
        theta[waver] = 2 * -135 - theta_core

    # Convert
    x = r * np.cos(np.deg2rad(theta))
    y = r * np.sin(np.deg2rad(theta))

    # Lock mean
    x += (target_x - np.mean(x))
    y += (target_y - np.mean(y))

    return x + 1j * y

# ---------- PARENTING FILTER ----------
def filter_parenting(samples, N):
    target_mean = 2.8 * np.exp(1j * np.deg2rad(45))
    current_mean = np.mean(samples)
    samples += (target_mean - current_mean)

    re, im = samples.real, samples.imag
    mag = np.abs(samples)
    angle = np.arctan2(im, re) * 180 / np.pi

    core = (angle >= 0) & (angle <= 90) & (mag > 0.6)
    outliers = (mag <= 0.6)

    max_outliers = int(0.01 * N)
    n_out = min(len(samples[outliers]), max_outliers)
    n_core = N - n_out

    core_sample = np.random.choice(samples[core], size=n_core, replace=False) if np.any(core) else samples[:n_core]
    out_sample = np.random.choice(samples[outliers], size=n_out, replace=False) if np.any(outliers) else np.array([])

    final = np.concatenate([core_sample, out_sample])
    return final[:N]

DISTRIBUTIONS["parent"].post_filter = filter_parenting

# ---------- SAMPLING ----------
def generate_radial_gaussian(angle_deg, mean_mag, base_cov, n_samples, falloff="1/r"):
    angle = np.deg2rad(angle_deg)
    direction = np.array([np.cos(angle), np.sin(angle)])
    target_mean = mean_mag * direction

    if falloff == "1/r":
        r_max = mean_mag * 3.0
        u = np.random.uniform(0, 1, n_samples)
        r = r_max * u
    elif falloff == "exp":
        scale = mean_mag * 0.8
        r = np.random.exponential(scale=scale, size=n_samples)
    else:
        r = np.random.rayleigh(scale=mean_mag * 0.8, size=n_samples)

    theta = angle + np.random.normal(0, np.deg2rad(18), n_samples)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    points = np.column_stack((x, y))

    scale = 0.3 + 0.7 * (r / (np.max(r) + 1e-8))
    samples = []
    for i, pt in enumerate(points):
        cov_i = base_cov * scale[i]
        noise = np.random.multivariate_normal([0, 0], cov_i, 1)[0]
        samples.append(pt + noise)

    samples = np.array(samples)
    samples += (target_mean - np.mean(samples, axis=0))
    return samples[:, 0] + 1j * samples[:, 1]

def generate_standard_gaussian(arch: Archetype, n_samples):
    mean = arch.mean_mag * np.exp(1j * np.deg2rad(arch.angle_deg))
    mean2 = np.array([mean.real, mean.imag])
    samples = np.random.multivariate_normal(mean2, arch.cov, n_samples)
    return samples[:, 0] + 1j * samples[:, 1]

def generate_samples(arch: Archetype, N: int) -> np.ndarray:
    if arch.name == "Revenge":
        return generate_revenge_samples(N)
    if arch.name == "Parenting":
        n_raw = N * OVERSAMPLE_FACTOR
        samples = generate_radial_gaussian(
            arch.angle_deg, arch.mean_mag, arch.cov,
            n_raw, falloff="1/r"
        )
    else:
        n_raw = N * OVERSAMPLE_FACTOR
        samples = generate_standard_gaussian(arch, n_raw)

    if arch.post_filter:
        samples = arch.post_filter(samples, N)
        if len(samples) == 0:
            samples = generate_standard_gaussian(arch, N)

    if len(samples) >= N:
        indices = np.random.choice(len(samples), N, replace=False)
    else:
        indices = np.random.choice(len(samples), N, replace=True)
    return samples[indices]

# ---------- PLOT ----------
def plot_map(selected: List[Archetype], input_str: str, N: int):
    plt.figure(figsize=(14, 10))
    ax = plt.gca()

    all_re = []
    all_im = []
    all_stats = {}

    for arch in selected:
        gamma = generate_samples(arch, N)
        re, im = gamma.real, gamma.imag
        all_re.extend(re)
        all_im.extend(im)

        mag = np.abs(gamma)
        angle = np.arctan2(im, re) * 180 / np.pi

        pQ1 = np.mean((angle >= 0) & (angle < 90)) * 100
        pQ2 = np.mean((angle >= 90) & (angle < 180)) * 100
        pQ3 = np.mean((angle <= -90) | (angle > -180)) * 100
        pQ4 = np.mean((angle >= -90) & (angle < 0)) * 100

        stats = {
            "N": N,
            "pQ1": pQ1, "pQ2": pQ2, "pQ3": pQ3, "pQ4": pQ4,
            "min_re": float(np.min(re)), "max_re": float(np.max(re)),
            "min_im": float(np.min(im)), "max_im": float(np.max(im)),
            "basis": arch.statistical_basis,
            "desc": arch.description
        }
        all_stats[arch.name] = stats

        ax.scatter(re, im, c=arch.color, s=2, alpha=0.75,
                   label=f"{arch.name}", edgecolors='none')

    # DYNAMIC RANGE
    if all_re:
        padding = 1.0
        x_min, x_max = np.min(all_re), np.max(all_re)
        y_min, y_max = np.min(all_im), np.max(all_im)
        ax.set_xlim(x_min - padding, x_max + padding)
        ax.set_ylim(y_min - padding, y_max + padding)

    ax.set_xlabel("Real Axis: Ego ← → We", fontsize=13, labelpad=10)
    ax.set_ylabel("Imaginary Axis: Enmity/Hate ↓    Love ↑", fontsize=13, labelpad=12)
    title = f"γ_self Character Region Map ({input_str}) | N={N}"
    ax.set_title(title, fontsize=16, pad=20)

    leg = ax.legend(loc='upper left', fontsize=11, markerscale=5,
                    title="Selected Archetypes", title_fontsize=12, framealpha=0.95)
    leg.get_frame().set_facecolor('white')

    suffix = input_str if input_str != "all" else "all"
    plot_path = f"{PLOT_BASE}_{suffix}_N{N}.png"
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Plot saved → {plot_path}")

    return all_stats

# ---------- MARKDOWN TABLE ----------
def create_table(selected: List[Archetype], stats: dict, input_str: str, N: int):
    suffix = input_str if input_str != "all" else "all"
    table_path = f"{TABLE_BASE}_{suffix}_N{N}.md"

    lines = [f"# γ_self Character Region Map — {input_str} | N={N}\n"]
    lines += ["## Quadrant Convention (angle from +Re axis)\n"]
    lines += ["- 0°   ≥ pQ1 < 90°\n"]
    lines += ["- 90°  ≥ pQ2 < 180°\n"]
    lines += ["- -180° ≥ pQ3 > -90°\n"]
    lines += ["- -90° ≥ pQ4 < 0°\n"]
    lines += ["\n---\n"]
    lines += ["## Statistical Summary\n"]
    lines += ["| Archetype | N | pQ1% | pQ2% | pQ3% | pQ4% | Min Re | Max Re | Min Im | Max Im |\n"]
    lines += ["|-----------|----|------|------|------|------|--------|--------|--------|--------|\n"]
    for arch in selected:
        s = stats[arch.name]
        lines += [f"| {arch.name} | {s['N']} | {s['pQ1']:.1f} | {s['pQ2']:.1f} | {s['pQ3']:.1f} | {s['pQ4']:.1f} | {s['min_re']:.2f} | {s['max_re']:.2f} | {s['min_im']:.2f} | {s['max_im']:.2f} |\n"]

    with open(table_path, 'w') as f:
        f.write("\n".join(lines))
    print(f"Table saved → {table_path}")

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="γ_self Character Map — N-controlled")
    parser.add_argument("classifications", nargs="*", default=["all"])
    parser.add_argument("--N", type=int, default=DEFAULT_N, help="Population size per archetype")
    args = parser.parse_args()

    input_list = args.classifications or ["all"]
    N = max(1, args.N)
    input_str = "_and_".join([x.lower() for x in input_list]) if len(input_list) > 1 else input_list[0].lower()

    selected = []
    seen = set()
    for name in input_list:
        name = name.lower()
        if name == "all":
            selected = list(DISTRIBUTIONS.values())
            input_str = "all"
            break
        for k, v in DISTRIBUTIONS.items():
            if name in k.lower() and v.name not in seen:
                selected.append(v)
                seen.add(v.name)

    if not selected:
        print("No valid archetypes.")
        return

    stats = plot_map(selected, input_str, N)
    create_table(selected, stats, input_str, N)

if __name__ == "__main__":
    main()