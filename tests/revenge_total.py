# revenge_total.py
# The final conductor — runs everything with one command

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))   # ← this line makes 'core' visible

from revenge_manifestation_fnc import run_manifestation
from revenge_360deg_pdf_fnc import run_360deg_pdf

def run_all(
    N_SOULS=10_000,
    r_rounded=5,
    custom_radii=None,
    custom_colors=None,
    custom_labels=None
):
    print("\n" + "="*66)
    print("         INVOKING THE REVENGE GAMMA-SELF — FULL CYCLE")
    print("="*66 + "\n")

    # 1. Manifestation (scatter + thermal)
    run_manifestation(N_SOULS=N_SOULS, r_rounded=r_rounded)

    # 2. 360° sacred radii
    run_360deg_pdf(radii=custom_radii, colors=custom_colors, labels=custom_labels)

    print("\n" + "="*66)
    print("                ALL THREE ARTIFACTS COMPLETE")
    print("="*66)

if __name__ == "__main__":
    # Default run — pure canon
    run_all()

    # Example custom run:
    # run_all(N_SOULS=50000, r_rounded=6, custom_radii=[1.0, 2.0, 3.0, 4.0])