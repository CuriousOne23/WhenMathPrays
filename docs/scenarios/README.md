# GRP Scenarios

This directory contains documented scenarios used to validate and explore the **Gamma Relational Persona framework (GRP)**.  
Each scenario includes plots, tables, and narrative notes to ensure clarity, reproducibility, and interpretability.

---

## 📂 Current Scenarios

- **[Singles Dating to Love](Singles_Dating_to_Love/README.md)**  
  *Why chosen:* Romantic arcs are a natural testbed for GRP because they highlight attraction, wobble, repair, and plateau dynamics. This scenario provides a clear, bounded relational arc with strong narrative markers, making it ideal for validating gamma_self trajectories and love magnitude plots.

---

## 📌 Candidate Scenarios (to be developed)

- **Couples Cohabiting to Long‑Term Partnership**  
  *Why chosen:* Extends the relational arc into stability and plateau dynamics under shared living conditions, testing long‑term fidelity and repair cycles.

- **Friendship Through Conflict and Repair**  
  *Why chosen:* Demonstrates that GRP applies beyond romance, capturing wobble and repair cycles in peer relationships.

- **Parent–Child Development Arc**  
  *Why chosen:* Models asymmetry in agency, altruism, and resonance across growth stages, stressing GRP's ability to handle unequal dynamics.

- **Team Collaboration in Work Projects**  
  *Why chosen:* Tests shared breath, resonance, and fidelity under collective goals, validating GRP in professional contexts.

- **Community Trust Building After Crisis**  
  *Why chosen:* Expands GRP to collective scales, modeling repair arcs and trust dynamics across groups.

# AI–Human Co‑Stewardship (Robotics Collaboration)

This scenario explores the relational arc between a **human operator (H1)** and an **AI‑enabled robotic system (R1)** across 90 days.  
It focuses on collaboration, calibration, and repair cycles in shared tasks, rather than companionship.  
The goal is to validate GRP's ability to measure relational intensity in hybrid agency contexts where humans and machines co‑steward outcomes.

---

## 📊 Scenario Overview
- **Duration:** 90 days (extended view to 100 for plotting clarity)
- **Entities:**
  - **H1 (Human Operator):** cautious start, moderates ego as trust builds.
  - **R1 (Robotic System):** high visibility, low fidelity at start; improves through calibration and shared rhythm.
- **Metrics tracked:**
  - Gamma_self (agency balance: ego/we vs trust/distrust)
  - Relational Intensity (GRP dimensions: resonance, fidelity, altruism, shared breath)
  - Event markers (Deployment → Calibration → Early failure → Repair → Shared rhythm → Plateau → Outcome)

---

## 📈 Plots

### Dual Plot
- **Left:** Gamma_self trajectories for H1 and R1 (agency balance over time).  
- **Right:** Relational Intensity vs Time with vertical event markers.  
- **Events:** Deployment, Calibration, Early failure, Repair, Shared rhythm, Plateau, Outcome.

---

## 📑 Data Tables
- **Gamma_self Table:** Coordinates for H1 and R1 across days, with event markers.  
- **Relational Intensity Table:** Values for resonance, fidelity, altruism, and shared breath.  

---

## 📝 Notes
- **Stress test:** Highlights asymmetry (human agency vs robotic execution) and repair cycles (system failure → human intervention → recalibration).  
- **GRP validation:** Tests visibility (robot performance), fidelity (trust in system), altruism (human oversight vs robotic optimization), and resonance (shared rhythm in workflow).  

---

## 📌 Why chosen
- **Hybrid agency:** Demonstrates GRP's ability to handle relationships where one agent is synthetic but not emotional.
- **Trust dynamics:** Robotics require calibration, repair, and oversight — perfect for testing wobble/repair arcs.  
- **Scalability:** Extends GRP beyond interpersonal into human–system collaboration, without anthropomorphizing.  

---

## 📂 Provenance
- **Plot file:** `AI_Human_CoStewardship.png`  
- **Tables:** `gamma_self_table.csv`, `relational_intensity_table.csv`  
- **Narrative notes:** `notes.md`  

This documentation ensures clarity, reproducibility, and interpretability for future stewards.
---

## 📝 Notes

- Each scenario has its own folder (`/scenarios/<Scenario_Name>/`) with:
  - `README.md` (scenario description, plots, tables, notes)
  - `.png` plot files
  - `.csv` data tables
  - `notes.md` for narrative annotations
- This index file (`/scenarios/README.md`) provides the **overview, rationale, and roadmap** for all scenarios.

---

## 📂 Provenance

- **Current canonical scenario:** `Singles_Dating_to_Love`  
- **Next candidates:** Cohabiting, Friendship, Parent–Child, Team Collaboration, Community Trust, AI–Human.  
- **Documentation ethos:** clarity, reproducibility, interpretability, and stewardship for future collaborators.
