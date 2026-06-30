# KnDt Compression Strategy

### 1. Title and Purpose

**Title:** KnDt Compression Strategy — Deterministic, Grammar‑Atomic Compaction

**Purpose:**  
Describe how a ~15 GB grammar‑atomic KnDt is compressed, encoded, and stored.  

Compression must preserve determinism, replay safety, immutability, and pointer stability.  

Compression must be non‑semantic, non‑probabilistic, and non‑inferential.  

The strategy must support fast random access for KnC, KnM, KnF.

### 2. Architectural Context

KnDt is consumed by KnB (KnC, KnM, KnF).  

Compression affects storage layout but not grounding behavior.  

Compression must preserve:  
- deterministic offsets  
- stable addresses  
- stable keyword mappings  
- stable tier boundaries  
- stable category segmentation

### 3. Compression Goals

- reduce KnDt to ~10–15 GB  
- maintain deterministic random‑access lookup  
- preserve fixed or bounded record sizes  
- preserve pointer stability  
- preserve keyword stability  
- preserve tier segmentation  
- preserve category segmentation  
- avoid semantic or probabilistic compression methods  
- ensure replay‑safe decoding

### 4. Allowed Compression Techniques

#### 4.1 Structural Compression
- shared symbol tables  
- shared grammar‑feature tables  
- tier‑variant deltas (coarse → medium → fine)  
- category‑specific block compression  
- pointer‑table compaction

#### 4.2 Binary Encoding
- fixed‑width fields  
- bounded‑width fields  
- deterministic padding  
- deterministic alignment  
- deterministic block headers

#### 4.3 Dictionary Compression (Non‑Semantic)
- exact‑match keyword dictionaries  
- grammar‑atomic feature dictionaries  
- symbol‑table deduplication  
- no semantic clustering  
- no embedding‑based compression

#### 4.4 Page‑Level Compression
- compressed pages (e.g., LZ4, Zstandard)  
- deterministic page boundaries  
- page‑aligned offsets  
- no variable‑length records inside pages  

Compression must never change the meaning, semantics, or interpretation of any KnDt entry.

### 5. Forbidden Compression Techniques

- semantic clustering  
- embedding‑based compression  
- probabilistic compression  
- lossy conceptual compression  
- variable‑length record formats  
- context‑dependent compression  
- adaptive compression that changes across sessions  
- compression that alters pointer offsets  
- compression that alters keyword ordering

### 6. Tier‑Aware Compression Rules

- coarse, medium, fine tiers must remain separate  
- tier deltas must be deterministic  
- tier boundaries must remain fixed  
- tier offsets must remain stable across versions  
- compression must not merge tiers  
- compression must not infer relationships between tiers

### 7. Category‑Aware Compression Rules

- categories must remain separate  
- category blocks must remain contiguous  
- category offsets must remain stable  
- compression must not merge categories  
- compression must not infer semantic relationships between categories

### 8. Deterministic Decoding Rules

- decoding must be deterministic  
- decoding must be replay‑safe  
- decoding must not depend on runtime heuristics  
- decoding must not depend on OS‑level nondeterministic behavior  
- decoding must preserve fixed offsets  
- decoding must preserve keyword order  
- decoding must preserve record boundaries

### 9. Versioning and Immutability

- compressed KnDt files are immutable once deployed  
- changes require a new version (KnDt_vN)  
- compression version must be stored in each entry  
- decoding must be compatible with older versions  
- no in‑place mutation  
- no online recompression

### 10. Performance Targets

- decompression latency per page: ≤ 0.2 ms  
- total grounding pass overhead from compression: ≤ 2 ms  
- random access preserved  
- pointer resolution preserved  
- keyword resolution preserved  

Compression must not degrade KnC/KnM/KnF timing budgets.

### 11. TS Invariants for Compression

- deterministic behavior  
- replay‑safe decoding  
- immutability across turns and sessions  
- stable pointer offsets  
- stable keyword ordering  
- stable tier/category segmentation  
- no semantic or probabilistic compression  
- no heuristic fallback  
- no modification of KnDt during grounding

---
