# Slide 06 / Stop 6 — Cycle, delta, named freeze

**Theory:** [../papers/idob_s2m_theory.md](../papers/idob_s2m_theory.md)
**Previous:** [../05_cie/README.md](../05_cie/README.md)
**Next:** [../07_idob_slide/README.md](../07_idob_slide/README.md)

## Objective

See time as **bounded search**, not as "it settled."

Each cycle:

1. Start from current M (and identity vector).
2. Apply a named refinement: decaying CIE shove `scale = alpha * 0.5^(cycle-1)`.
3. Compute `meaning_delta_h = ||M_i - M_{i-1}||_2` and `identity_delta = ||I_i - I_{i-1}||_2`.
4. Halt if a stop condition fires. Write `resolution_status` from the **same** predicate that halted.

## Formula / table this revision

Program: `run_06_cycle.py`
Table: `stabilization.slide.yaml`
Envelopes: [../05_cie/cie.examples.yaml](../05_cie/cie.examples.yaml)
Names: [stop_reasons.md](stop_reasons.md)

| Knob | Value |
|------|------:|
| `epsilon_meaning` | 0.05 |
| `epsilon_identity` | 0.05 |
| `idob_search_budget_min` | 4 |
| `idob_search_budget_max` | 6 |

Stop order (papers):

1. meaning stable (`meaning_delta_h < epsilon_meaning`) after min cycles
2. identity stable (`identity_delta < epsilon_identity`) after min cycles
3. `budget_exhausted` at max
4. `time_exhausted` (supervisor; not this runner)

Default demo (`group_id=1001`, `cie_id=physical_stance`) decays the physical shove until a named halt. Do not relabel a budget stop as `stable`.

`run()` returns `{M, meaning_delta_h, identity_delta, refinement_cycles, resolution_status}` so Slide 07 can wire it.

## This slide must print

- Cycle number and scale
- M
- both deltas
- halt line
- `resolution_status` and cycles used

## This slide must not do

- Full map + rank pipeline (slide 07)
- Invent candidates
- Label `stable` when the halt was budget
- Clear `residue_code` (Slide 10)

## Note — freeze vs leftover (Slide 10)

A named freeze can still leave `residue_code` on the card. Freeze means **this hop's M search stopped**, not "tension digested." What CTP would copy for the next search, and which file a human expands: [../10_residue_expand/residue_expand.md](../10_residue_expand/residue_expand.md). This slide does not implement CTP.

## Run

    python run_06_cycle.py
    python ../run_ts_struc2mn.py   # with RUN_06_CYCLE = True

Driver vars: `VAR_06_GROUP_ID`, `VAR_06_CIE_ID`, `VAR_06_CLIP_TO_UNIT`.
