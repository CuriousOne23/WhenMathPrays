# IdOB runtime flow (S2M / 11)

Replaces the hop description in `idob_runtime_flow.md` for current `idob.py`. That file is kept for history.

1. Read `utterance` and/or `card_id`, `cie_id`, `packs_loaded`, `prior_M`.  
2. If `card_id` — load structure card (01). Else 09 assign from packs.  
3. Miss → packet `unassigned`, store utterance, stop birth.  
4. Build or copy `structural_key`.  
5. Map lookup → `candidate_group_ids` (set).  
6. Empty → `empty_map`, no \(M\).  
7. Rank ⊆ candidates → `selected_group_id`.  
8. Load group prototype → `meaning_semantics` \(M\).  
9. CIE: \(M' = \mathrm{clip}(M + \alpha I)\).  
10. Δh vs prior or zeros; set flags; write `tp.idob`; restore `routing_filter` if touched.

RB / Slide 10 happen **after** this flow.
