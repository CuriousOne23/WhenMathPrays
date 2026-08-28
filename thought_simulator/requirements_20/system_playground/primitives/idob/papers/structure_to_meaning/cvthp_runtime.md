# CvThP runtime (sibling of IdOB, not the hop)

CvThP is an **execution coordinator** if Path A uses one. It is **not** IdOB and it is **not** how `11_idob_core` births \(M\).

Live hop: one `process` / `run_hop` call. See [idob_runtime_flow_s2m.md](idob_runtime_flow_s2m.md).

---

## What 11 actually does

- One structure-to-meaning pass per call.
- No mandatory 4–6 inner cycles inside `idob.py`.
- No `identity_delta` as a second meaning metric (CIE motion is `meaning_cie_delta`; hop motion is `meaning_delta_h`).
- Rank orders a **legal set**; it does not spawn unsupervised parallel minds.
- Next IdOB is **RB**, not CvThP inventing a six-tuple.
- OuBA is not implied by `ready_for_ouba` as truth. That flag only means a vector was born.

---

## What CvThP *may* do later (optional supervisor)

If you build CvThP, keep it **outside** the hop:

| May | Must not |
|-----|----------|
| Decide *when* to call `idob.py` again | Rewrite `structural_key` |
| Cap wall-clock or hop count for the **conversation** | Force 4–6 cycles inside one hop |
| Read Δh / flags / residue from `tp.idob` | Treat `identity_delta` as IdOB output |
| Ask RB to schedule another IdOB | Write `process.routing_filter` |
| Record provenance for replay | Equate itself with OuBA |

Stabilization of meaning is the stability contract (ε, first-pass zeros). Budget language like `budget_exhausted` is a **future status**, not a current 11 field unless you add it in a named revision.

---

## Start condition (still true)

Do not call IdOB until you have an `utterance` and/or a structure card (or a completed 09 miss, which is a legal hop with no \(M\)). Six IDs come from 01/09, not from CvThP.

---

Historical text that required min 4 / max 6 IdOB cycles and parallel branch-as-IdOB lives in git history of this file. Do not implement that as `idob.py`.
