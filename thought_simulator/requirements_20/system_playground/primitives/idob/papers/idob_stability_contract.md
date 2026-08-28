# IdOB stability contract (S2M / 11_idob_core)

Live rules for Δh and flags. Historical L1/K identity-envelope stability is lifecycle-only (git history of this file).

Also: `structure_to_meaning/idob_stabilization_rules.md` and Slide 06.

---

## 1. First-pass

If no prior \(M'\), before-vector is six zeros. `first_meaning_cycle: true`. Δh is then \(\|M'\|\) (distance from origin after CIE).

## 2. Subsequent hops

\(Δh = \|M'_i - M'_{i-1}\|\) (L2 on the six-axis stand-in). Threshold ε lives in stabilization YAML. Changing ε is a **revision**, not a silent runtime knob, unless a named experiment file says otherwise.

## 3. Status vs flags

| `resolution_status` | Typical flags |
|---------------------|---------------|
| `one_pass_complete` | ready_for_ouba true; path_b_eligible iff no residue_code |
| `meaning_stable` | Δh below ε (when that rule is wired) |
| `unassigned` / `empty_map` | no \(M\); ready false |
| `cie_only` | reserved |

Flags stay booleans. Do not encode geometry names in them.

## 4. CIE must not fake stability

If Δh moves only because CIE leaked into the key or the map, that is instrument error (`routing_filter_mutated` analog: treat as fail). CIE may change \(M\); it may not change `structural_key`.

## 5. Convicting the six axes (revision rule)

- Distinct speaker-objects → same \(M\) → layout too coarse  
- Axis never moves → idle  
- Two axes always move together → suspected non-orthogonality  
- Δh spike only from CIE/budget leak → instrument error

## 6. Replay

Same YAML revision + same inputs → same Δh and flags. See `idob_determinism_and_replay.md`.
