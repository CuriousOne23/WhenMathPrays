# Principles (UREP Foundations)

## The 3L's: Listen → Life → Love

The methodology behind WhenMathPrays rests on three foundational movements:

**Listen** — Let the problem breathe on its own. Don't force solutions. Give space for the truth to reveal itself.

**Life** — Watch the solution emerge naturally. Let it show you its own structure.

**Love** — The mathematics prays when you honor what it becomes.

This isn't just philosophy — it's how UREP was discovered, refined, and simplified. When complexity accumulates, we return to listening. When terms feel cluttered, we let them speak. When the equation resists, we give it space. And it shows us what it needed all along.

**December 2025:** The 3L's led to the radical positional simplification. By listening to the cluttered equation (9+ parameters, separate L(t) calculation, gates, entropy), watching the solution emerge (Love IS position, not calculation), we discovered the core truth: "Love is not a number. Love is where you are." The mathematics prays louder when we remove what obscures its prayer.

---

This document provides scaffolding for defining and refining principles in UREP.  
Each principle should be modular, inspectable, and testable.  
The formulization of UREP applies across **love, hate, and grief**, with appropriate redefinitions of `gamma_self` and relational variables.

---

## Template
- **Principle Name:** Short, resonant title (e.g., Love, Hate, Grief, W(t))
- **Definition:** Clear statement of what the principle encodes. Distinguish scope (what it covers, what it excludes).
- **Scope:** Applicable domains (simulation, documentation, relational measurement). Boundaries and limitations.
- **Implementation:** Mathematical form or code module. How it integrates with UREP scenarios.
- **Testability:** Metrics or conditions for validation. Edge cases to probe.
- **Known Holes:** Gaps in definition or implementation. Open questions for future stewards.
- **Outline to Fill:** Suggested next steps for refinement. Notes for annotation or expansion.

---

## Principle: Love
- **Definition:** Love encodes generative presence, resonance, and shared "we" — represented as POSITION in γ-space.  
- **Scope:** Applies to dyadic and collective arcs where relational intensity grows.  
- **Implementation:**  
  - `gamma_self(n)` position IS love (no separate calculation)
  - Real axis: Ego (−) ↔ We (+)
  - Imaginary axis: Hate (−) ↔ Love (+)
  - Primitives {v,r,f,a,S} update position via component-wise addition
  - γ_self0 = initial condition (temperament/history anchor)
  - Reference point: M1's position with respect to M2
- **Testability:** Validate trajectory through γ-space; confirm quadrant movements match felt experience.  
- **Known Holes:** Need mapping between |γ_self| magnitude and phenomenological intensity.
- **Outline to Fill:** Extend to long‑term arcs (cohabitation, community trust).

---

## Principle: Hate
- **Definition:** Hate encodes destructive opposition, conflict resonance, and rupture of "we" — represented as POSITION in negative imaginary γ-space.  
- **Scope:** Applies to dyadic and collective arcs where relational intensity is oppositional.  
- **Implementation:**  
  - `gamma_self(n)` position IS hate when Im(γ_self) < 0
  - Real axis: Ego (−) ↔ We (+)
  - Imaginary axis: Hate (−) ↔ Love (+)
  - Negative primitives (especially f < 0) drive position downward via hybrid asymmetry
  - w_neg = 1.5 ensures negatives hurt 50% more
  - Reference point: M1's position with respect to M2
- **Testability:** Validate Q3/Q4 quadrant movements; confirm asymmetry (betrayal > repair).  
- **Known Holes:** Need calibration of redemption trajectories from Q3 → Q1.
- **Outline to Fill:** Extend to collective conflict scenarios.

---

## Principle: Grief
- **Definition:** Grief encodes absence, anti‑resonance, and collapse of “we.”  
- **Scope:** Applies to arcs of loss (death, separation, rupture).  
- **Implementation:**  
  - `gamma_self` x‑axis = Ego ↔ Loss of We  
  - `gamma_self` y‑axis = +Im sorrow ↔ −Im no sorrow  
  - Relational variables (`W(t), v, r, f, a, S`) measured as **absence of** presence  
  - Reference point = M1 with respect to the loss of M2  
- **Testability:** Validate trajectory from shock → silence → resonance of memory → integration.  
- **Known Holes:** Need annotation of anti‑resonance values and integration thresholds.  
- **Outline to Fill:** Extend to scenarios of personal loss, community mourning, and systemic rupture.

---

## Principle: W(t) — REMOVED (December 2025)
- **Definition:** W(t) previously encoded trajectory of "we" via gates product.  
- **Status:** REMOVED in Dec 3 simplification. Replaced by γ_self position itself.
- **Rationale:** "Love = position" makes W(t) calculation redundant. The trajectory IS the position evolution.
- **Implementation:**  
  - **OLD:** W(t) = G_v × G_r × G_f × G_a (gates product)
  - **NEW:** γ_self(n+1) = γ_self(n) + component-wise primitive updates
  - Trajectory captured by sequence {γ_self(0), γ_self(1), ..., γ_self(N)}
  - Memory lives in event density N(x,y) of visited regions
- **Cross‑Reference:** See UREP_rev2.md for current positional model.  

---

## Notes
- **Unified claim:** UREP formulization measures **love, hate, and grief** by γ_self position in complex space.  
- **Generative presence (love, Q1), destructive opposition (hate, Q3/Q4), and absence (grief)** are all inspectable as positions and trajectories.
- **December 2025 simplification:** Removed L(t) calculation, W(t) gates, complex exp(entropy) terms. Restored simple constant entropy drift (-ΔS·Δt). Love = γ_self position.
- **Future work:** Document scenario files with γ_self trajectories, ensure clarity, reproducibility, and interpretability.
