#!/usr/bin/env python
"""
distributions_gamma_self.py
γ_self Character Region Map — 9 statistical archetypes.
- Runs only selected archetypes
- Output filenames include input
- .md file: stats + statistical basis
- FIXED: SyntaxError in battlefield cov
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from typing import Dict, List
from dataclasses import dataclass

# ---------- OUTPUT BASE ----------
PLOT_BASE = "core/gamma_self_character_map"
TABLE_BASE = "core/gamma_self_quadrants"

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
        mean_mag=5.0,
        cov=np.array([[2.5, 0.0], [0.0, 0.15]]),
        color="#d62728",
        quadrant="Q2/Q3",
        description="Horizontal oval on -Re axis.",
        statistical_basis="Anisotropic Gaussian, σ_re=2.5, σ_im=0.15"
    ),
    "soulmate": Archetype(
        name="Soul Mate",
        angle_deg=90,
        mean_mag=3.0,
        cov=np.array([[0.3, 0.0], [0.0, 1.5]]),
        color="#ff7f0e",
        quadrant="Q1",
        description="Vertical oval along +Im.",
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
        cov=np.array([[0.4, 0.1], [0.1, 0.3]]),
        color="#9467bd",
        quadrant="Q1",
        description="Teardrop fan-out along 45° — wider at high magnitude.",
        statistical_basis="Radial Gaussian, p(r)∝1/r, variance ∝ r"
    ),
    "ego_dating": Archetype(
        name="Ego Dating",
        angle_deg=135,
        mean_mag=2.5,
        cov=np.array([[0.6, 0.4], [0.4, 1.0]]),
        color="#8c564b",
        quadrant="Q2",
        description="Tilted oval along 135° in Q2.",
        statistical_basis="Correlated Gaussian, ρ≈0.6"
    ),
    "battlefield": Archetype(
        name="Battlefield Hate",
        angle_deg=-90,
        mean_mag=3.5,
        cov=np.array([[0.3, 0.0], [0.0, 2.0]]),  # ← FIXED: 0 posts → 0.0
        color="#e377c2",
        quadrant="Q4",
        description="Vertical oval along -Im.",
        statistical_basis="Anisotropic Gaussian, σ_re=0.3, σ_im=2.0"
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
        mean_mag=3.0,
        cov=np.array([[0.5, 0.3], [0.3, 0.4]]),
        color="#bcbd22",
        quadrant="Q3",
        description="Fan-out in Q3 with sudden hate cliff.",
        statistical_basis="Radial Gaussian, p(r)∝exp(-r), clipped where |Im| > |Re|"
    ),
}

# ---------- RADIAL GAUSSIAN ----------
def generate_radial_gaussian(angle_deg, mean_mag, base_cov, n_samples=6000, falloff="1/r"):
    angle = np.deg2rad(angle_deg)
    direction = np.array([np.cos(angle), np.sin(angle)])
    target_mean = mean_mag * direction

    if falloff == "1/r":
        r_max = mean_mag * 3.0
        u = np.random.uniform(0, 1, n_samples)
        r = r_max * u
    elif falloff == "exp":
        r = np.random.exponential(scale=mean_mag * 1.2, size=n_samples)
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

# ---------- STANDARD GAUSSIAN ----------
def generate_standard_gaussian(arch: Archetype, n_samples=6000):
    mean = arch.mean_mag * np.exp(1j * np.deg2rad(arch.angle_deg))
    mean2 = np.array([mean.real, mean.imag])
    samples = np.random.multivariate_normal(mean2, arch.cov, n_samples)
    return samples[:, 0] + 1j * samples[:, 1]

# ---------- SAMPLE DISPATCHER ----------
def generate_samples(arch: Archetype) -> np.ndarray:
    if arch.name in ["Parenting", "Revenge"]:
        samples = generate_radial_gaussian(
            arch.angle_deg, arch.mean_mag, arch.cov,
            falloff="1/r" if arch.name == "Parenting" else "exp"
        )
        if arch.name == "Revenge":
            re, im = samples.real, samples.imag
            mask = (re < 0) & (im < 0) & (np.abs(im) > np.abs(re))
            if np.any(mask):
                samples = samples[mask]
            else:
                samples = generate_radial_gaussian(arch.angle_deg, arch.mean_mag, arch.cov, falloff="exp")
    else:
        samples = generate_standard_gaussian(arch)
    return samples

# ---------- PLOT ----------
def plot_map(selected: List[Archetype], input_str: str):
    plt.figure(figsize=(14, 10))
    ax = plt.gca()

    stats = {}

    for arch in selected:
        gamma = generate_samples(arch)
        re, im = gamma.real, gamma.imag

        stats[arch.name] = {
            "min_re": float(np.min(re)),
            "max_re": float(np.max(re)),
            "min_im": float(np.min(im)),
            "max_im": float(np.max(im)),
            "basis": arch.statistical_basis
        }

        ax.scatter(re, im, c=arch.color, s=2, alpha=0.75,
                   label=f"{arch.name}", edgecolors='none')

    # Axes
    ax.set_xlim(-7, 5)
    ax.set_ylim(-6, 6)
    ax.axhline(0, color='k', lw=1.2, alpha=0.7)
    ax.axvline(0, color='k', lw=1.2, alpha=0.7)
    ax.grid(True, alpha=0.3, ls='-', lw=0.5)

    # Quadrant labels
    ax.text( 2.5,  4.0, "Q1", fontsize=16, ha='center', fontweight='bold', bbox=dict(facecolor='white', alpha=0.7))
    ax.text(-2.5,  4.0, "Q2", fontsize=16, ha='center', fontweight='bold', bbox=dict(facecolor='white', alpha=0.7))
    ax.text(-2.5, -4.0, "Q3", fontsize=16, ha='center', fontweight='bold', bbox=dict(facecolor='white', alpha=0.7))
    ax.text( 2.5, -4.0, "Q4", fontsize=16, ha='center', fontweight='bold', bbox=dict(facecolor='white', alpha=0.7))

    # Labels
    ax.set_xlabel("Real Axis: Ego ← → We", fontsize=13, labelpad=10)
    ax.set_ylabel("Imaginary Axis: Enmity/Hate ↓    Love ↑", fontsize=13, labelpad=12)
    title = f"γ_self Character Region Map ({input_str.replace('_', ' ')})"
    ax.set_title(title, fontsize=16, pad=20)

    # Legend
    leg = ax.legend(loc='upper left', fontsize=11, markerscale=5,
                    title="Selected Archetypes", title_fontsize=12, framealpha=0.95)
    leg.get_frame().set_facecolor('white')

    # Save
    suffix = input_str if input_str != "all" else "all"
    plot_path = f"{PLOT_BASE}_{suffix}.png"
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Plot saved → {plot_path}")

    return stats

# ---------- MARKDOWN TABLE ----------
def create_table(selected: List[Archetype], stats: dict, input_str: str):
    suffix = input_str if input_str != "all" else "all"
    table_path = f"{TABLE_BASE}_{suffix}.md"

    lines = [f"# γ_self Quadrants — {input_str.replace('_', ' ')}\n"]

    # Quadrant layout
    lines += [
        "|        | **+Im = Union, Love** |        |",
        "|--------|-----------------------|--------|",
        "| **-Re** | **Q2**                | **Q1** |",
        "| **+Re = We** |                       |        |",
        "| **-Im = Enmity, Hate** | **Q3**        | **Q4** |",
        "\n---\n"
    ]

    # Stats table
    lines += ["## Statistical Summary\n"]
    lines += ["| Archetype | Min Re | Max Re | Min Im | Max Im | Statistical Basis |\n"]
    lines += ["|---------|--------|--------|--------|--------|-------------------|\n"]
    for arch in selected:
        s = stats[arch.name]
        lines += [f"| {arch.name} | {s['min_re']:.3f} | {s['max_re']:.3f} | {s['min_im']:.3f} | {s['max_im']:.3f} | {s['basis']} |\n"]

    with open(table_path, 'w') as f:
        f.write("\n".join(lines))
    print(f"Table saved → {table_path}")

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="γ_self Character Map — selective")
    parser.add_argument("classifications", nargs="*", default=["all"],
                        help="e.g., parent, parent marriage, all")
    args = parser.parse_args()

    input_list = args.classifications
    if not input_list:
        input_list = ["all"]

    # Build input string for filename
    input_str = "_and_".join([x.lower() for x in input_list]) if len(input_list) > 1 else input_list[0].lower()

    # Resolve selections
    selected = []
    seen_names = set()
    for name in input_list:
        name = name.lower()
        if name == "all":
            selected = list(DISTRIBUTIONS.values())
            input_str = "all"
            break
        for key, arch in DISTRIBUTIONS.items():
            if name in key.lower() and arch.name not in seen_names:
                selected.append(arch)
                seen_names.add(arch.name)

    if not selected:
        print("No valid archetypes selected.")
        return

    stats = plot_map(selected, input_str)
    create_table(selected, stats, input_str)

if __name__ == "__main__":
    main()