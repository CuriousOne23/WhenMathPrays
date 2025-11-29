# Singles Dating to Love

This scenario documents the relational arc of **M1** and **M2** across 60 days, moving from initial conditions through wobble, repair, and stable plateau.

---

## Scenario Overview
- **Duration:** 60 days (extended to 65 for plotting clarity)
- **Entities:** M1 (ego-heavy start → moderates), M2 (cautious start → warms)
- **Metrics tracked:**
  - γ_self trajectory (Ego/We vs Hate/Love)
  - Love magnitude ||L(t)|| vs time
  - Event markers

---

## Plots

### Dual Plot
![Singles Dating to Love](/results/Singles_Dating_to_Love.png)

- Left: γ_self trajectories (M1 teal, M2 orange)  
- Right: Love magnitude vs time with vertical event markers  
- Events: Initial → First date → Early wobble → Repair → Shared rhythm → Stable → Outcome

---

## Data Tables

### Input (Ground Truth)
- [M1 γ_self table](/data/Single_Dating_2_Love_M1_gamma_self_table.csv)  
- [M2 γ_self table](/data/Single_Dating_2_Love_M2_gamma_self_table.csv)

### Output (Model Prediction)
See the full computed love magnitude table:  
[`Single_Dating_2_Love_magnitude_table.csv`](/results/Single_Dating_2_Love_magnitude_table.csv)

| Day | M1_Love | M2_Love | Event               |
|-----|---------|---------|---------------------|
| 0   | 0.10    | 0.20    | Initial condition   |
| 7   | 0.20    | 0.18    | First date          |
| 14  | 0.30    | 0.25    | Early wobble        |
| 21  | 0.38    | 0.35    | Repair begins       |
| 28  | 0.40    | 0.50    | Shared rhythm       |
| 35  | 0.42    | 0.52    | Repair complete     |
| 42  | 0.44    | 0.54    | Stable Q2 band      |
| 49  | 0.46    | 0.55    | Steady connection   |
| 56  | 0.48    | 0.56    | Higher plateau      |
| 60  | 0.55    | 0.57    | Outcome             |

---

## Notes
- Both M1 and M2 remain in the negative-x (ego/we) domain, rising steadily in y (love).
- M1 shows ego moderation + repair; M2 shows cautious dip → trust growth.
- Final convergence ~0.55–0.57 reflects relational coherence.

---

## Reproducibility

All outputs are generated automatically from the locked UREP equation.

To reproduce:
```bash
python tests/compute_love_magnitude.py   # → writes results/ + plot