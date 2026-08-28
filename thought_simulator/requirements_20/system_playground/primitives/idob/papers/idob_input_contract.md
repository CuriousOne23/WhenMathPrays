# IdOB input contract (S2M / 11_idob_core)

Live hop. Historical lifecycle contract (identity vector \(I=\{G,R,C,P,K,E,F\}\)) is in git history of this file before 2026-08-28 and is summarized in §9. That contract is **not** what `idob.py` consumes now.

---

## 1. Purpose

Name what the hop may read so replay is possible and structure stays off the meaning axes.

## 2. Accepted inputs

| Name | Where | Required |
|------|--------|----------|
| `utterance` | TP root or kwargs | For reference always preferred; required if no `card_id` |
| `card_id` | TP root or kwargs | Alternate to 09 |
| `packs_loaded` | kwargs / TP | 09 only |
| `cie_id` | kwargs / TP | Default `neutral` |
| `prior_M` | kwargs or last `meaning_semantics_prime` | Optional; absent → first-pass zeros |
| `process.routing_filter` | TP | Optional; **must be unchanged** after process |
| `metadata.geometric_state` | TP | Optional; DCB-owned; must be unchanged |

Utterance is the **carrier**. The hop does not parse meaning off the string except via 09 id assignment.

## 3. Rejected / ignored as meaning

- Nested listener-uptake claims.
- Six-axis floats presented as structure IDs.
- Rank lists that are not a subset of the map (caller error; hop still clamps to map).
- Mutations of RB/DCB fields as “input hints” for this hop to write.

Malformed assignment → `unassigned` packet, not an exception, unless YAML is unreadable.

## 4. Boundary conditions

1. Deterministic given (utterance or card) + packs + CIE + prior_M + frozen YAML revision.  
2. Miss and empty-map are legal outputs.  
3. CIE does not invent a new `structural_key`.  
4. Replay of the same tuple repeats the packet.

## 5. Normalization

- 09 lowercases and tokenizes for cues only.  
- Six IDs default `0` when a cue is silent.  
- CIE `I` clipped to \([0,1]\).  
- First-pass: before-vector = zeros.

## 6. Worked miss

Utterance: `zzzzq no cue at all` + `packs_loaded: [base_en]`  
→ `assignment_status: miss`, `structural_key: null`, `meaning_semantics: null`, utterance **still on the packet**.

## 7. Worked card

`card_id: S_rock_burst` + utterance `The rock burst open.`  
→ key from card, map candidates, rank, \(M\), CIE, leftover `residue_code` from the card.

## 8. Failure vs expand

YAML missing → load error.  
Unknown card_id → treat as miss/unassigned.  
Leftover code → `expand_target` for Slide 10; IdOB does not pick the next six-tuple.

## 9. Historical lifecycle input (not live)

Previous text accepted geometry/role/continuity/pressure/curvature/entropy/freeze as the identity input vector, with split on two clusters and merge on convergence. That is the **lifecycle instrument**. See `lifecycle/README.md`.
