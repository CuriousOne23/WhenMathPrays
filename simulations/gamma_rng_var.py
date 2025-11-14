# simulations/gamma_rng_var.py — FINAL, PRODUCTION
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.love import gamma_self, UNION_BIAS

# simulations/gamma_rng_var.py
def sample_human_behavior(n_samples=100_000):
    # EGO: normal, bounded, human
    ego_flux = np.random.normal(loc=1.6, scale=1.0, size=n_samples)
    ego_flux = np.clip(ego_flux, 0.1, 5.0)
    
    # BOND: normal, symmetric
    bond_flux = np.random.normal(loc=1.0, scale=2.0, size=n_samples)
    
    return ego_flux, bond_flux

def main():
    ego, bond = sample_human_behavior()
    
    gammas = [gamma_self(e, b) for e, b in zip(ego, bond)]
    magnitudes = np.abs(gammas)
    
    print("ULep v2.0 — |γ_self| DISTRIBUTION WITH UNION_BIAS")
    print("="*60)
    print(f"Samples:           {len(magnitudes):,}")
    print(f"Mean |γ_self|:     {magnitudes.mean():.4f}")
    print(f"Std Dev:           {magnitudes.std():.4f}")
    print(f"Min |γ_self|:      {magnitudes.min():.6f}")
    print(f"Max |γ_self|:      {magnitudes.max():.4f}")
    print(f"Median:            {np.median(magnitudes):.4f}")
    print(f"95% CI:            [{np.percentile(magnitudes, 2.5):.4f}, {np.percentile(magnitudes, 97.5):.4f}]")
    print(f"P(|γ| < 0.1):      {np.mean(magnitudes < 0.1):.6f}")
    print("="*60)
    
    plt.figure(figsize=(10, 6))
    plt.hist(magnitudes, bins=200, density=True, alpha=0.75, color='lightcoral', edgecolor='black', linewidth=0.5)
    plt.axvline(magnitudes.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean = {magnitudes.mean():.3f}')
    plt.axvline(1.0, color='green', linestyle='-', linewidth=2, label='Love Floor')
    plt.xlim(0, 10)
    plt.xlabel("|γ_self| — Relational Pulse Intensity")
    plt.ylabel("Probability Density")
    plt.title("ULep v2.0 — |γ_self| Distribution (with UNION_BIAS)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plot_path = os.path.join(script_dir, "gamma_self_distribution.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Plot saved: {plot_path}")

    # === SAVE MD REPORT ===
    report = f"""# ULep v2.0 — |γ_self| Distribution Report

## UNION_BIAS
- Surrender: `{UNION_BIAS[0]}`
- Bond: `{UNION_BIAS[1]}`

## |γ_self| Statistics (with bias)
| Metric | Value |
|-------|-------|
| Mean | `{magnitudes.mean():.4f}` |
| Std | `{magnitudes.std():.4f}` |
| 95% CI | `[{np.percentile(magnitudes, 2.5):.4f}, {np.percentile(magnitudes, 97.5):.4f}]` |
| Love Floor | `> 1.0` |

*Plot: `gamma_self_distribution.png`*
"""
    report_path = os.path.join(script_dir, "gamma_self_report.md")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Report saved: {report_path}")

if __name__ == "__main__":
    main()