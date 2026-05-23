# 11 Entropy and Information

## 1. Purpose
Define the requirements for normalized entropy tracking as the primary measure of thought completion and processing progress.

## 2. Core Requirements

**ET-01: Normalized Relative Entropy**
- The system must maintain a **normalized percentage entropy** $H_{\%} = \frac{H_{\text{current}}}{H_{\text{initial}}} \times 100\%$.
- $H_{\text{initial}}$ is measured at the moment raw input first enters the Entry RB.
- $H_{\%}$ must be preserved (or only minimally affected) during splitting, merging, energy changes, and most RB operations.

**ET-02: Entropy Reduction Rules**
- Significant entropy reduction must occur **primarily inside Object Basins (OBs)** through feature binding, sharpening, and coherence formation.
- Relational Basins (RBs) should generally preserve $H_{\%}$ (except for minor natural losses).
- Inquiry Basins should maintain or only slowly reduce $H_{\%}$.

**ET-03: Completion Logic**
- **Clean Completion**: When $H_{\%}$ drops below a configurable threshold (default: 15–25%), route to Done RB.
- **Stressed / Provisional Completion**: When time budget is critically low, allow completion at higher $H_{\%}$ (up to 50–60%) and route through Feeling OB if appropriate.
- Must support dynamic adjustment of thresholds based on global stress or urgency.

**ET-04: Multi-Dimensional Entropy**
- Should optionally track separate entropy components (semantic, emotional, contextual) that contribute to the overall $H_{\%}$.

## 3. Interaction with Other Systems

- **Fanout/Splitting**: All child branches inherit the parent's $H_{\%}$ at the moment of split.
- **Fanin/Merging**: Merged $H_{\%}$ is a weighted average of incoming branches.
- **Energy Dynamics**: Energy fluctuations and amplifiers must not directly alter $H_{\%}$ (strict decoupling required).
- **Basins**: Each basin type must declare its expected entropy reduction range.

## 4. Observability and Logging
- Current $H_{\%}$, $H_{\text{initial}}$, and $H_{\text{current}}$ must be logged at every major step and transition.
- Must clearly log when and why entropy was reduced (e.g., "OB binding reduced entropy by 12.4%").
- Must flag stalled entropy reduction (potential trigger for Inquiry Basin activation).

## 5. Testability Requirements
- Must pass tests showing $H_{\%}$ remains stable across multiple split/merge cycles with no OB visits.
- Must demonstrate clear entropy drops in OBs versus minimal change in RBs.
- Must correctly trigger both clean and stressed completion paths under different conditions.

## 6. Traceability
Links to:
- `03_core_conceptual_requirements.md` (Section 2.6)
- `06_basins.md`
- `12_energy_dynamics.md`
- `08_embedding_space.md`

---

**Last Updated**: [Insert Date]  
**Version**: 0.2 (Draft)