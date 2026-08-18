# **ts_tr_readset_update_proposal.md**  
### *Proposed Update to TR Read‑Set Discipline*  
### *Clarifying Normative vs Diagnostic Inputs for TR*

**Status:** Proposed theory expansion  
**Aligned with:** 20.37 (normative), ts_tr_semantic_routing_theory.md (informative), tp_path_a_map.md, progressive_lineup_testing.md  
**Purpose:** Clarify which signals TR is normatively allowed to read, which signals are diagnostic only, and how future promotion of signals into 20.37 should occur.

---

# **0. What This Paper Does, Doesn’t Do, and Its Purpose**

## **0.1 What This Paper *Does***  
This paper:

- **Defines the authoritative (normative) TR read‑set** exactly as 20.37 currently specifies.  
- **Separates normative inputs from diagnostic / expanded theory inputs.**  
- **Defines deterministic omission rules** for optional signals.  
- **Defines criteria for promoting expanded signals into 20.37.**  
- **Defines required updates to progressive lineup tests** if promotion occurs.  
- **Defines required updates to structural programs** if promotion occurs.  
- **Prevents accidental overreach** in TR implementation.  
- **Ensures TR structural program remains valid even with minimal inputs.**

This paper is about **input discipline**, not computation.

---

## **0.2 What This Paper *Does Not* Do**  
This paper does **not**:

- define stance mapping  
- define intent mapping  
- define affect mapping  
- define shading mapping  
- define tension mapping  
- define politeness mapping  
- define commitment/reservation mapping  
- define logical_structure mapping  
- define epistemic_delta_h mapping  
- define lineage_additions mapping  
- define routing_fields mapping  
- define the estimator for $H_t$  
- define the append predicate for lineage additions  
- define the geometry/topology of semantic routing  
- define the full TR computation theory

Those remain open in **ts_tr_semantic_routing_theory.md** and require separate theory papers.

This paper **cannot** close the fog — it can only **bound** it.

---

## **0.3 Purpose of This Paper**  
The purpose of this paper is to:

- **protect TR implementation from premature theoretical expansion**  
- **ensure TR structural program remains correct under 20.37**  
- **provide a safe path for future expansion of TR’s read‑set**  
- **define deterministic behavior when expanded signals are absent**  
- **prepare the ground for future mapping theory papers**  
- **prevent accidental invention or nondeterminism**  
- **ensure progressive lineup tests remain valid across versions**

This paper is the **input‑side companion** to ts_tr_semantic_routing_theory.md.

It does not define computation.  
It defines **what TR is allowed to see**.

---

# **1. Motivation for Read‑Set Update**

TR’s computation theory (ts_tr_semantic_routing_theory.md) identifies many signals that *could* be useful for semantic routing:

- residue topology  
- invariant drift  
- identity geometry  
- semantic adjacency  
- curvature  
- commitments  
- freeze signatures  
- referent lineage  
- qualifier lineage  
- semantic importance residues  
- continuity signals  

But 20.37 currently authorizes only a **narrow read‑set**.

This mismatch creates:

- fog in theory  
- risk in implementation  
- instability in testbench design  
- ambiguity in future expansion  
- potential nondeterminism if expanded signals are used incorrectly

This paper resolves that mismatch by defining:

- **normative read‑set**  
- **diagnostic read‑set**  
- **promotion criteria**  
- **structural program rules**  
- **testbench rules**

---

# **2. Normative Read‑Set (Authoritative Under 20.37)**

TR is normatively allowed to read only:

1. **TP-local semantic meaning-layer fields**  
2. **TP.semantic idob_semantics[]**  
3. **TP.process.routing_metadata**  
4. **TP.semantic.lineage**  
5. **STPX structural cues**  
6. **Permitted ephemeral DCB events (curvature)**

This is the **only** read‑set that structural programs and progressive lineup tests must assume.

If any of these fields are missing, TR must:

- perform deterministic omission  
- produce default values  
- never invent signals  
- never infer meaning or identity  
- never violate 20.105.* boundaries

---

# **3. Diagnostic Read‑Set (Expanded Theory Inputs)**  
These are signals that **the theory paper uses**, but **20.37 does not yet authorize** for normative TR computation.

They are **diagnostic only**, meaning:

- TR may read them **if present**,  
- TR must produce **deterministic omission** if absent,  
- TR must **never invent** them,  
- TR must **never rely** on them for correctness,  
- TR must **never require** them for determinism.

Diagnostic signals include:

1. semantic adjacency  
2. semantic importance residues  
3. referent lineage  
4. qualifier lineage  
5. identity continuity flags  
6. continuity signals  
7. commitments  
8. freeze signatures  
9. curvature (full DCB envelope)  
10. residue topology  
11. invariant drift ($\Delta H$)  
12. semantic-layer hash  
13. adjacency hash  
14. identity hash  
15. continuity hash  

These signals are **allowed for theory**, but **not yet allowed for implementation**.

---

# **4. Deterministic Omission Rules**  
If a diagnostic signal is **not present**, TR must:

### **Rule 1 — Produce a deterministic default**  
Example:

```
semantic_drift = False
identity_drift = False
curvature_level = low
epistemic_delta_h = 0
lineage_additions = []
```

### **Rule 2 — Never infer or invent missing signals**  
TR must not:

- guess semantic adjacency  
- infer identity continuity  
- fabricate residue topology  
- approximate curvature  
- estimate invariant drift  
- create lineage additions  

### **Rule 3 — Maintain full determinism even with minimal inputs**  
TR must produce:

- deterministic stance  
- deterministic intent  
- deterministic affect  
- deterministic shading  
- deterministic tension  
- deterministic routing_fields  

even if only the **narrow normative read‑set** is present.

### **Rule 4 — SSR projection must remain valid**  
Even with missing diagnostic signals, TR must produce:

- stable  
- bounded  
- SSR‑projectable  
- deterministic  

fields.

### **Rule 5 — No degradation of RB routing**  
RB must still be able to:

- detect drift  
- detect instability  
- detect commitments  
- detect freeze conflicts  
- detect curvature instability  

even if diagnostic signals are absent.

This is achieved through:

- routing_metadata  
- semantic meaning‑semantics  
- idob_semantics  
- semantic lineage  
- STPX cues  
- curvature (minimal envelope)

---

# **5. Promotion Criteria for Updating 20.37**  
This section defines **how** diagnostic signals may eventually become **normative**.

Promotion requires:

## **5.1 Criterion A — Stability Across Cycles**  
A signal must demonstrate:

- stable freeze points  
- stable provenance  
- stable replay behavior  
- stable SSR projection  

If a signal cannot be frozen deterministically, it cannot be promoted.

---

## **5.2 Criterion B — Deterministic Mapping Availability**  
Before promotion, the theory must provide:

- a deterministic mapping family  
- a deterministic formula  
- stability rules  
- ordering rules  
- SSR projection rules  

For example:

- stance mapping must be fully defined  
- epistemic_delta_h must have a real estimator  
- lineage_additions must have a real append predicate  
- routing_fields must have a complete key set

Without mapping theory, promotion is impossible.

---

## **5.3 Criterion C — Progressive Lineup Fixture Updates**  
Promotion requires:

- new fixtures  
- new testbench cases  
- new determinism tests  
- new replay tests  
- new SSR projection tests  

These must be added to:

- progressive_lineup_testing.md  
- tr_py_struc_pgm.md  
- tp_path_a_map.md  
- routing_matrix fixtures

---

## **5.4 Criterion D — Structural Program Compatibility**  
Promotion must not break:

- TR structural program  
- RB structural program  
- DCB structural program  
- IdOB structural program  
- CE structural program  
- MCB structural program  

If promotion requires structural program changes, those must be explicitly documented.

---

## **5.5 Criterion E — 20.37 Update**  
Promotion is **not valid** until:

- 20.37 is updated  
- the read‑set section is expanded  
- the mapping section is expanded  
- the determinism section is expanded  
- the boundary section is expanded  

This paper **cannot** update 20.37.  
It can only propose updates.

---

# **6. Structural Program Rules**

This section defines how TR’s structural program must behave under the updated read‑set discipline.

These rules ensure:

- determinism  
- replay stability  
- SSR compatibility  
- compatibility with 20.37  
- compatibility with progressive lineup tests  
- compatibility with future mapping theory papers  

---

## **6.1 TR Must Be Correct Under Minimal Inputs**

TR must produce a valid `TP.TR` block even when **only the narrow normative read‑set is present**:

- semantic meaning‑semantics  
- idob_semantics  
- routing_metadata  
- semantic lineage  
- STPX cues  
- minimal curvature  

All other signals must be treated as **optional**.

If optional signals are missing:

- TR must not degrade  
- TR must not invent  
- TR must not infer  
- TR must not violate boundaries  
- TR must not produce nondeterministic fields  

This ensures TR is **forward‑compatible** with future expansions.

---

## **6.2 TR Must Not Require Diagnostic Signals**

Diagnostic signals (expanded read‑set) must **never** be required for:

- determinism  
- ordering  
- lineage bounding  
- SSR projection  
- routing_fields construction  
- tension computation  
- epistemic_delta_h computation  

If diagnostic signals are missing, TR must:

- produce deterministic defaults  
- maintain full routing functionality  
- maintain full basin‑selection compatibility  

---

## **6.3 TR Must Not Modify Diagnostic Signals**

TR must **never** write or modify:

- commitments  
- freeze signatures  
- referent lineage  
- qualifier lineage  
- identity continuity flags  
- semantic adjacency  
- residue topology  
- invariant drift  
- curvature  

These are **read‑only**.

---

## **6.4 TR Must Record Provenance of Diagnostic Signals**

If diagnostic signals are present, TR must record:

- which signals were consumed  
- which signals were omitted  
- which signals influenced mapping  
- which signals were ignored  

This provenance is required for:

- debugging  
- replay determinism  
- future mapping theory  
- future 20.37 updates  

---

## **6.5 TR Must Be Deterministic Under Mixed Input Conditions**

TR must produce identical outputs when:

- diagnostic signals are present but unused  
- diagnostic signals are absent  
- diagnostic signals are present but null  
- diagnostic signals are present but irrelevant  

This ensures **input‑agnostic determinism**.

---

# **7. Testbench Rules**

Promotion of diagnostic signals into normative read‑set requires updates to:

- progressive lineup tests  
- determinism tests  
- replay tests  
- SSR projection tests  
- structural program tests  
- routing matrix tests  

This section defines the rules.

---

## **7.1 Minimal Input Tests Must Always Pass**

Even after promotion, TR must pass tests where:

- only normative signals are present  
- diagnostic signals are absent  
- diagnostic signals are null  
- diagnostic signals are inconsistent  

This ensures backward compatibility.

---

## **7.2 Expanded Input Tests Must Be Added**

When a diagnostic signal is promoted:

- new fixtures must be added  
- new determinism tests must be added  
- new SSR tests must be added  
- new routing tests must be added  

These must be added to:

- progressive_lineup_testing.md  
- tr_py_struc_pgm.md  
- tp_path_a_map.md  
- routing_matrix fixtures  

---

## **7.3 No Test May Assume Diagnostic Signals Are Present**

Until 20.37 is updated, tests must **not** assume:

- residue topology  
- invariant drift  
- identity continuity flags  
- commitments  
- freeze signatures  
- semantic adjacency  
- referent lineage  
- qualifier lineage  

are present.

Tests must treat them as **optional**.

---

## **7.4 Promotion Requires Versioned Fixtures**

When a diagnostic signal is promoted:

- fixtures must be versioned  
- old fixtures must remain valid  
- new fixtures must be added  
- routing matrix must be updated  

This ensures:

- backward compatibility  
- forward compatibility  
- deterministic replay across versions  

---

# **8. Versioning Rules**

This section defines how TR read‑set updates must be versioned.

---

## **8.1 Semantic Versioning of TR Read‑Set**

TR read‑set updates must follow:

- **major version**: promotion of new signals  
- **minor version**: refinement of mapping families  
- **patch version**: determinism fixes, SSR fixes  

Example:

```
TR_readset_v1.0.0   (current 20.37)
TR_readset_v1.1.0   (promotion of semantic adjacency)
TR_readset_v2.0.0   (promotion of invariant drift)
```

---

## **8.2 Versioning Must Be Reflected in 20.37**

20.37 must be updated with:

- new read‑set entries  
- new mapping rules  
- new determinism rules  
- new boundary rules  
- new SSR rules  

---

## **8.3 Versioning Must Be Reflected in Structural Programs**

When a signal is promoted:

- TR structural program must be updated  
- RB structural program must be updated  
- DCB structural program must be updated  
- IdOB structural program must be updated  

---

## **8.4 Versioning Must Be Reflected in Testbenches**

Promotion requires:

- new fixtures  
- new determinism tests  
- new SSR tests  
- new routing tests  

---

# **9. Closing Summary**

This paper defines the **input‑side discipline** for TR:

### ✔ What TR is normatively allowed to read  
### ✔ What TR is diagnostically allowed to read  
### ✔ How TR must behave when diagnostic signals are missing  
### ✔ How TR must maintain determinism under minimal inputs  
### ✔ How future promotion of signals into 20.37 must occur  
### ✔ How structural programs must adapt  
### ✔ How testbenches must adapt  
### ✔ How versioning must be handled  

This paper **does not** define:

- mapping families  
- mapping formulas  
- mapping invariants  
- semantic geometry  
- residue topology  
- invariant drift estimator  
- lineage append predicate  
- routing_fields key set  

Those remain open in **ts_tr_semantic_routing_theory.md** and require separate theory papers.

This paper **protects TR implementation** from premature theoretical expansion and ensures **forward‑compatible determinism**.

---



