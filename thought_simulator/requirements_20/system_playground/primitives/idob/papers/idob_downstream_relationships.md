# IdOB downstream relationships (S2M)

IdOB writes a packet. It does not route.

| Consumer | Reads | Must not assume |
|----------|-------|-----------------|
| TP / CTP | packet snapshot, utterance, Δh | That Δh is human cognitive change |
| TR | flags, residue as hints only | That IdOB filled `routing_filter` |
| RB | residue_code, expand_target, history | That IdOB computed the next six-tuple |
| Path B / OuBA | `ready_for_ouba` / `path_b_eligible` | That eligible means “cognition done” |

Write-boundary: if `process.routing_filter` existed on the way in, it is identical on the way out (`routing_filter_mutated` is a diagnostic, not a license to keep a bad write).
