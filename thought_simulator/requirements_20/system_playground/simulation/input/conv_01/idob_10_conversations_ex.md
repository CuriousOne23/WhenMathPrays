# idob_10_conversation_cases.md

**Purpose:** Document the coherent conversation topic and the ten IdOB input/output forms that drive `idob_testbench.yaml`.

**Topic chosen:**  
“What is the core identity of the Thought Simulator (TS) — is it primarily a deterministic fixed-time-step state machine for meaning, or does it also claim ontological status for the Relational Manifold?”

This topic is deliberately close to the project’s own epistemic stance (manifold as modeling convenience until evidence proves otherwise) and naturally exercises all ten identity behavior classes.

**Alignment:**  
- Schema enums from `idob_schema.yaml` (local)  
- Transition / freeze / basin_surface behavior from `idob_py_struc_pgm.md` v0.1  
- Progressive dual-mode + structural foundation comparison  
- 20.40.050 HLRs (meaning-only, write boundaries, serial support, path_b_eligible)

---

## Conversation Arc (10 turns)

| # | Behavior Class     | Utterance (summary)                                      | Key geometry / pressure / residuals movement          |
|---|--------------------|----------------------------------------------------------|-------------------------------------------------------|
| 1 | Formation          | “Is TS mainly a deterministic semantic engine?”          | formation → basin, low pressure, small residuals      |
| 2 | Refinement         | “More precisely a fixed-time-step state machine?”        | refinement, residuals collapse                        |
| 3 | Correction         | “Actually it feels bigger — maybe an OS for meaning?”    | correction, medium pressure, unstable                 |
| 4 | Drift              | “Or is the manifold itself the real claim?”              | drift, identity_freeze appears                        |
| 5 | Conflict           | “No — the manifold is only a modeling convenience.”      | conflict, high pressure, explosion, transition_surface|
| 6 | Bifurcation      | “Can both views coexist for a while?”                    | bifurcation, two_clusters, split                      |
| 7 | Stabilization      | “Primary identity is the deterministic state machine.”   | stabilization, residuals collapsing, basin            |
| 8 | Convergence        | “Manifold stays secondary / optional viz layer.”         | convergence, low pressure                             |
| 9 | Alignment          | “That matches the stated epistemic stance.”              | alignment, freeze none                                |
|10 | Closure            | “Identity work on this cluster is complete for now.”     | closure, idob_complete true, path_b_eligible true     |

Each case in `idob_testbench.yaml` supplies a minimal but schema-valid TP snapshot (identity block + stance + direction + routing + importance + optional prior envelope / regime hint) and an `expected` block focused on the identity envelope fields + completion / eligibility flags that structural-foundation comparison will check.

---

## Notes for CP

- Cases are written so a pure transition-table implementation of `idob.py` (per struc_pgm §4) can pass them without additional learned logic.
- Write-boundary negatives are **not** yet in this first YAML; they can be added after the positive arc is approved.
- Serial-pass and regime inherit/reset are only lightly exercised; later increments can expand.
- Dictionary YAMLs under `primitives/idob/` are assumed; any missing supporting enums will be added when the full testbench suite is authorized.
