**mapping_rules_for_knb.md**

### 1. Title and Purpose

**Title:** Mapping Rules for KnB — Deterministic Grounding Pipeline

**Purpose:**  
KnB is the grounding path between Path‑A and Path‑B.  

KnB consists of KnC, KnM, KnF, and KnDt.  

This document defines the deterministic mapping rules used by KnB to convert SSR candidates into grounded symbolic fields.  

Mapping must be non‑inferential, non‑probabilistic, non‑semantic, and pointer‑driven.

### 2. Architectural Context

KnB sits between Path‑A (meaning construction) and Path‑B (meaning realization).  

KnB receives SSR + KnDt.  

KnB produces grounded SSR fields for TPTB/TPSF and Path‑B.  

KnB does not construct meaning and does not realize meaning.

### 3. Inputs to Mapping

**SSR Inputs**  
- identity_candidate[]  
- relation_candidate[]  
- domain_anchor_candidate[]  
- qualifier_candidate[]  
- truth_validation_candidate[]  
- KnDt_addresses[]  
- KnDt_keywords[]  

**KnDt Inputs**  
- atomic entries (symbol, tier, category, address, keywords[], features[], version)  

SSR must provide either a KnDt address or a KnDt keyword for every candidate.

### 4. Deterministic Mapping Pipeline

```
SSR.candidate
    → SSR.KnDt_address or SSR.KnDt_keyword
    → KnDt entry
    → grounded field (coarse, medium, fine)
```

- address resolution takes precedence  
- keyword resolution must be exact  
- no fallback heuristics  
- no semantic similarity  
- no embeddings  
- no inference  
- no probabilistic matching  

SSR candidates are read‑only and must not be altered, rewritten, merged, or normalized by KnC/KnM/KnF.  
Grounded field names must match the SSR schema exactly and must not introduce new fields or rename existing ones.

### 5. Mapping Rules for Each Primitive

**KnC (Coarse Grounding)**  
- uses coarse tier entries  
- writes identity_coarse, relation_coarse, domain_anchor_coarse, qualifier_coarse, truth_validation_coarse  
- computes H_Kn_coarse  
- sets Kn_level = "KnC"  

**KnM (Medium Grounding)**  
- uses medium tier entries  
- refines coarse grounding  
- writes identity_medium, relation_medium, domain_anchor_medium, qualifier_medium, truth_validation_medium  
- computes H_Kn_medium  
- sets Kn_level = "KnM"  

**KnF (Fine Grounding)**  
- uses fine tier entries  
- refines medium grounding  
- writes identity_fine, relation_fine, domain_anchor_fine, qualifier_fine, truth_validation_fine  
- computes H_Kn_fine  
- sets Kn_level = "KnF"  

KnC/KnM/KnF do not perform inference, semantic interpretation, or probabilistic matching.

### 6. Deterministic Resolution Rules

1. If KnDt_address exists → resolve by address.  
2. Else if KnDt_keyword exists → resolve by exact keyword match.  
3. Else → grounding error.  
4. No fuzzy matching.  
5. No ranking.  
6. No semantic similarity.  
7. No embeddings.  
8. No inference.  
9. Resolution must be replay‑safe.

### 7. Grounding Error Conditions

Grounding fails if:  
- address does not exist  
- keyword does not match  
- tier variant is missing  
- entry is malformed  
- category mismatch occurs  

Grounding errors must be surfaced to DF.

### 8. KnDt Tier Consistency

KnDt entries must be tier‑consistent: coarse, medium, and fine variants must refer to the same underlying symbolic concept and must not diverge semantically.

### 9. Mapping Invariants

- mapping must be deterministic  
- mapping must be symbolic  
- mapping must be grammar‑atomic  
- mapping must be replay‑safe  
- mapping must be stable across turns and sessions  
- mapping must not modify SSR candidates  
- mapping must not modify KnDt  
- mapping must not invoke Path‑A or Path‑B primitives

### 10. Mapping Stability Across Routing Epochs

Mapping must remain stable across routing epochs. Routing changes must not affect grounding behavior.

---
