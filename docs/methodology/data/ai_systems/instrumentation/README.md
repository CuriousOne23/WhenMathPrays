# **Instrumentation Layer — Behavioral Metrics Overview**

This folder defines the **behavioral instrumentation** used to compare how different AI systems interpret, map, and reason over the same primitives and tasks.

These metrics support the Paper‑5 music experiment and the broader GRP architecture by providing a reproducible way to measure:

- interpretive divergence  
- mapping divergence  
- trajectory divergence  
- expressive divergence  
- cross‑system construct fidelity (CSCF)

The four files below represent the four experimental conditions.

---

## **E — Entangled Copilot (Copilot‑with‑CuriousOne)**  
**File:** `co_cp_ent_div_metric.md`  
Contains the **definitions** of the entangled behavioral divergence metrics.  
This file currently includes the *metric schema only*.  
Measured entangled data will be added after the baseline, fresh Copilot, and fresh Grok runs.

---

## **B — Baseline Copilot (fresh, no primitives)**  
**File:** `co_cp_baseline_div_metric.md`  
Defines the behavioral metrics for a fresh Copilot instance with no primitives and no entanglement.  
This is the **true baseline** and will be populated after the baseline run.

---

## **F — Fresh Copilot (fresh + primitives)**  
**File:** `co_cp_fresh_div_metric.md`  
Defines the behavioral metrics for a fresh Copilot instance given the primitives explicitly.  
This is the **controlled fresh condition** and will be populated after the fresh‑with‑primitives run.

---

## **G — Fresh Grok (fresh + primitives)**  
**File:** `grok_fresh_div_metric.md`  
Defines the behavioral metrics for a fresh Grok instance given the same primitives.  
This is the **cross‑model fresh condition** and will be populated after the Grok run.

---

## **Purpose of This Folder**

This folder forms the **instrumentation layer** of the repository.  
It provides the measurement framework needed to determine:

- which behaviors arise from entanglement  
- which arise from the primitives themselves  
- which are architecture‑specific  
- and whether the primitives represent **real informational categories** across systems

---
