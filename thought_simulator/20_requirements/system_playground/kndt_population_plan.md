# KnDt Population Plan

### 1. Title and Purpose

**Title:** KnDt Population Plan — Deterministic Construction of Grammar‑Atomic Knowledge

**Purpose:**  
Describe how KnDt is populated with grammar‑atomic entries.  

Define the deterministic rules for constructing identity anchors, relation anchors, domain anchors, qualifier anchors, truth‑validation anchors, and grammar categories.  

Ensure population is non‑semantic, non‑probabilistic, non‑inferential, and replay‑safe.  

Ensure population produces a stable, pointer‑addressable, ~15 GB KnDt.

### 2. Architectural Context

KnDt is consumed by KnB (KnC, KnM, KnF).  

Population affects KnDt content but not grounding behavior.  

Population must preserve:  
- deterministic addresses  
- deterministic keyword mappings  
- deterministic tier boundaries  
- deterministic category segmentation  
- immutability across turns and sessions

### 3. Population Goals

- produce a complete grammar‑atomic knowledge table  
- ensure deterministic, replay‑safe population  
- ensure stable pointer addresses  
- ensure stable keyword ordering  
- ensure stable tier/category segmentation  
- avoid semantic inference  
- avoid probabilistic or embedding‑based population  
- target final size: 10–15 GB

### 4. Allowed Population Sources

#### 4.1 Grammar‑Atomic Lexical Sources
- nouns  
- verbs  
- adjectives  
- adverbs  
- pronouns  
- prepositions  
- determiners  
- conjunctions  

#### 4.2 Deterministic Symbol Tables
- identity anchors  
- relation anchors  
- domain anchors  
- qualifier anchors  
- truth‑validation anchors  

#### 4.3 Deterministic Feature Tables
- number  
- tense  
- case  
- aspect  
- other grammar‑atomic features  

Population sources must be symbolic and grammar‑atomic, not semantic or probabilistic.

### 5. Forbidden Population Sources

- semantic clustering  
- embedding‑based extraction  
- probabilistic extraction  
- contextual inference  
- large‑language‑model hallucinated facts  
- fuzzy associations  
- dynamic or adaptive population  
- population that changes across sessions  
- population that alters meaning or semantics

### 6. Tier‑Aware Population Rules

- coarse, medium, fine tiers must be populated separately  
- tier variants must refer to the same underlying symbolic concept  
- tier deltas must be deterministic  
- tier boundaries must remain fixed  
- population must not infer semantic relationships between tiers  
- population must not merge tiers

### 7. Category‑Aware Population Rules

- categories must remain separate  
- category blocks must remain contiguous  
- category offsets must remain stable  
- population must not merge categories  
- population must not infer semantic relationships between categories

### 8. Deterministic Address Assignment

- addresses must be assigned deterministically  
- address assignment must be stable across versions  
- address assignment must not depend on runtime heuristics  
- address assignment must not depend on OS‑level nondeterministic behavior  
- address assignment must preserve replay invariants

### 9. Deterministic Keyword Assignment

- keywords must be exact‑match strings  
- keyword ordering must be deterministic (e.g., lexicographic)  
- keyword blocks must be stable across versions  
- no fuzzy keywords  
- no semantic keyword expansion

### 10. Record Construction Rules

Each KnDt entry is constructed with:  
- symbol assigned deterministically  
- tier assigned deterministically  
- category assigned deterministically  
- address assigned deterministically  
- keywords[] assigned deterministically  
- features[] assigned deterministically  
- version assigned deterministically  

Record size must be fixed or bounded.

### 11. Population Workflow

1. Load grammar‑atomic lexical sources.  
2. Construct symbol tables.  
3. Construct feature tables.  
4. Populate coarse tier.  
5. Populate medium tier.  
6. Populate fine tier.  
7. Assign deterministic addresses.  
8. Assign deterministic keywords.  
9. Encode records.  
10. Validate invariants.  
11. Freeze KnDt_vN.  

Population must be fully deterministic and replay‑safe.

### 12. Versioning and Immutability

- population produces immutable KnDt_vN  
- changes require a new version  
- no in‑place mutation  
- no online population  
- version stored in each entry

### 13. TS Invariants for Population

- deterministic behavior  
- replay‑safe population  
- immutability across turns and sessions  
- stable pointer offsets  
- stable keyword ordering  
- stable tier/category segmentation  
- no semantic or probabilistic population  
- no heuristic fallback  
- no modification of KnDt during grounding

---
