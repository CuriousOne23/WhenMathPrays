# Stabilization rules (S2M / 11)

Live contract: `../idob_stability_contract.md` and Slide 06.  
This file restates the hop rules only.

1. First hop: before-vector = zeros; `first_meaning_cycle: true`.  
2. Δh = L2 distance between successive \(M'\) (after CIE).  
3. ε lives in YAML. Changing ε is a revision unless an experiment file says otherwise.  
4. `meaning_stable` when Δh < ε (when that status is wired).  
5. `one_pass_complete` when a vector was born this hop — not the same as stable.  
6. Flags: `ready_for_ouba` / `path_b_eligible` / `idob_complete` are booleans; they do not encode formation…closure.  
7. CIE must not change `structural_key`.  
8. Leftover `residue_code` does not by itself mean unstable meaning; it means Path B door stays shut and Slide 10 may expand.
