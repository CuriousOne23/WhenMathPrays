# IdOB output contract (S2M / 11_idob_core)

Live packet. Historical output (geometry, continuity, basin_surface, idob_complete ⇒ geometry=closure) is in git history of this file and `lifecycle/`.

Canonical field list: `11_idob_core/packet.schema.yaml`.

---

## 1. Where output lives

- `tp["idob"]` — full packet  
- `tp["idob_complete"]`, `tp["path_b_eligible"]`, `tp["ready_for_ouba"]` — copies for older runners  
- `tp["semantic"]["meaning_delta_h"]` — copy of Δh  
- `process.routing_filter` — **unchanged** if it existed

## 2. Required keys on every hop

`utterance` (string or null), `resolution_status`, `ready_for_ouba`, `path_b_eligible`, `idob_complete`, `routing_filter_mutated`.

On birth also: `structural_key`, `candidate_group_ids`, `final_rank_order`, `selected_group_id`, `meaning_semantics`, `meaning_semantics_prime`, `meaning_delta_h`.

On miss / empty map: meaning fields null; `expand_target` may be set.

## 3. Flags (split on purpose)

| Flag | Meaning |
|------|---------|
| `ready_for_ouba` | A six-vector was born this hop |
| `path_b_eligible` | Birth and no leftover `residue_code` |
| `idob_complete` | Same as eligible in this revision (Path B door, not “closure geometry”) |

`idob_complete=true` does **not** require `hold_geometry=closure`.

## 4. Residuals

- `residue_code` — structure leftover (string or null)  
- `identity_residual.{magnitude,pattern}` — separate from residue_code  
- `meaning_cie_delta` — CIE motion only  
- `meaning_delta_h` — full hop motion vs prior / zeros

## 5. What output must not contain as IdOB writes

- New `process.routing_filter`  
- New SSG / structural_graph fields  
- Listener-uptake narrative  
- Next six-tuple invented from residue (that is pre-work + RB)

## 6. Downstream readers

TR / CTP / TP history may copy the packet. RB reads residue + flags + history. OuBA is not implied by `ready_for_ouba` as a truth claim — only that a vector exists to hand off.

## 7. Historical lifecycle output (not live)

Previous contract required `metadata.identity` keys geometry, continuity, pressure, residuals, freeze, basin_surface and tied `idob_complete` to `geometry=closure`. See archived Path A expected-blocks.
