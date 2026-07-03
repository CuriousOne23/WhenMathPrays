**TS Knowledge Table (KnDt) — Schema and Grounding Specification**

### 1. Title and Purpose

**Title:** TS Knowledge Table (KnDt) — Schema and Grounding Specification

**Purpose:**  
KnDt is the grammar‑atomic, deterministic knowledge table used by the grounding path (KnB).  

KnDt provides explicit symbolic entries for identity, relation, domain-anchor, qualifier, and truth-validation grounding.  

KnDt is not inferential, not probabilistic, and not semantic.  

KnDt is the only source of symbolic grounding information for KnC, KnM, and KnF.

### 2. Architectural Context

KnDt belongs to Path‑Kn (KnB), the grounding path between Path-A and Path-B.  

KnDt is consumed by KnC, KnM, and KnF.  

All three grounding primitives receive SSR + KnDt as inputs.  

Grounding is deterministic and pointer-driven.

### 3. Definition of “Ground Information”

“Ground information” consists of:  
- explicit symbolic anchors  
- selected deterministically from KnDt  
- representing identity, relation, domain, qualifier, and truth-validation  
- written into SSR by KnC/KnM/KnF  
- non-inferential, non-semantic, non-probabilistic

### 4. Atomic Entry Structure

Each KnDt entry must contain:  
- **symbol** — the canonical symbolic identifier  
- **tier** — coarse | medium | fine  
- **category** — noun | verb | adjective | adverb | pronoun | preposition | determiner | conjunction | identity_anchor | relation_anchor | domain_anchor | qualifier_anchor | truth_validation_anchor  
- **address** — deterministic pointer  
- **keywords[]** — exact keyword matches  
- **features[]** — optional atomic grammar features (e.g., number, tense, case, aspect), strictly non-semantic and non-inferential  
- **version** — schema version for replay invariants

### 5. KnDt Schema Specification

#### Identity Anchors
- **Symbolic entry format**: Unique symbolic identifier (e.g., ID_xxx) with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

#### Relation Anchors
- **Symbolic entry format**: Unique symbolic identifier (e.g., REL_xxx) with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

#### Domain Anchors
- **Symbolic entry format**: Unique symbolic identifier (e.g., DOM_xxx) with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

#### Qualifier Anchors
- **Symbolic entry format**: Unique symbolic identifier (e.g., QUAL_xxx) with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

#### Truth-Validation Anchors
- **Symbolic entry format**: Unique symbolic identifier (e.g., TRUTH_xxx) with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

#### Grammar-Atomic Categories
**Nouns**  
- **Symbolic entry format**: Unique symbolic identifier with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

**Verbs**  
- **Symbolic entry format**: Unique symbolic identifier with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

**Adjectives**  
- **Symbolic entry format**: Unique symbolic identifier with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

**Adverbs**  
- **Symbolic entry format**: Unique symbolic identifier with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

**Pronouns**  
- **Symbolic entry format**: Unique symbolic identifier with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

**Prepositions**  
- **Symbolic entry format**: Unique symbolic identifier with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

**Determiners**  
- **Symbolic entry format**: Unique symbolic identifier with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

**Conjunctions**  
- **Symbolic entry format**: Unique symbolic identifier with tiered variants.  
- **Tier variants**: coarse, medium, fine.  
- **Pointer addressing rules**: Direct index or address into KnDt table.  
- **Keyword addressing rules**: Exact keyword match to entry key.  
- **Deterministic lookup rules**: Exact pointer or keyword resolution; no partial matches, no ranking.

### 6. SSR Candidate Structure

SSR must provide to KnB:  
- identity_candidate[]  
- relation_candidate[]  
- domain_anchor_candidate[]  
- qualifier_candidate[]  
- truth_validation_candidate[]  
- KnDt_addresses[]  
- KnDt_keywords[]

### 7. Mapping Rules (SSR → KnDt → Grounded Fields)

```
SSR.candidate
    → SSR.KnDt_address or SSR.KnDt_keyword
    → KnDt entry
    → grounded field (coarse, medium, fine)
```

The mapping pipeline is strictly deterministic:  
- no heuristics  
- no inference  
- no embeddings  
- no semantic similarity  
- no probabilistic matching

### 8. Deterministic Resolution Rules

1. If KnDt_address is present → resolve by address.  
2. Else if KnDt_keyword is present → resolve by exact keyword match.  
3. Else → grounding error (SSR must provide one).  
4. No fallback heuristics are permitted.  
5. No semantic similarity or embeddings are permitted.  
6. Resolution must be deterministic and replay-safe.

### 9. Tiering Rules

KnDt supports:  
- KnC (coarse tier)  
- KnM (medium tier)  
- KnF (fine tier)  

**Tier selection**: Determined by the calling primitive (KnC uses coarse entries, KnM medium, KnF fine).  
**Tier invariants**: Each tier maintains its own stable symbolic entries; coarse provides broad anchors, medium contextual refinement, fine precise resolution.  
**Tier entropy fields**: H_Kn_coarse, H_Kn_medium, H_Kn_fine (computed by respective primitives).  
**Deterministic tier boundaries**: Fixed by primitive invocation and entry tier labels; no dynamic crossover.

### 10. Category–Tier Matrix

| Category                  | Coarse | Medium | Fine |
|---------------------------|--------|--------|------|
| identity_anchor           | ✓      | ✓      | ✓    |
| relation_anchor           | ✓      | ✓      | ✓    |
| domain_anchor             | ✓      | ✓      | ✓    |
| qualifier_anchor          | ✓      | ✓      | ✓    |
| truth_validation_anchor   | ✓      | ✓      | ✓    |
| nouns                     | ✓      | ✓      | ✓    |
| verbs                     | ✓      | ✓      | ✓    |
| adjectives                | ✓      | ✓      | ✓    |
| adverbs                   | ✓      | ✓      | ✓    |
| pronouns                  | ✓      | ✓      | ✓    |
| prepositions              | ✓      | ✓      | ✓    |
| determiners               | ✓      | ✓      | ✓    |
| conjunctions              | ✓      | ✓      | ✓    |

### 11. Grounding Error Conditions

Grounding fails if:  
- address does not exist in KnDt  
- keyword does not match any entry  
- tier variant is missing  
- entry is malformed  
- category mismatch occurs  

Grounding failure must be surfaced to DF.

### 12. KnDt Completeness Requirements

KnDt must be:  
- complete (entries for all grounding-relevant concepts)  
- stable  
- versioned  
- immutable during grounding  
- immutable across turns and across sessions  
- deterministic across turns  

This preserves replay invariants.

### 13. Determinism Requirements

KnDt entries must be stable.  
KnDt must be complete.  
KnDt must be symbolic.  
KnDt must be pointer-addressable.  
Grounding must be replay-safe.  
No nondeterministic behavior is allowed.

---
