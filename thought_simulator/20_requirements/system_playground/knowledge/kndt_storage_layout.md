# KnDT Storage Layout

### 1. Title and Purpose

**Title:** KnDt Storage Layout — Disk, Memory, and Access Strategy

**Purpose:**  
Describe how a ~15 GB grammar‑atomic KnDt is stored on disk and accessed in memory.  

The layout must support deterministic, replay‑safe, low‑latency grounding for KnC, KnM, KnF.  

The design must be non‑probabilistic, non‑semantic, and pointer‑driven.

### 2. Architectural Context

KnDt is the TS Knowledge Table used by KnB (Path‑Kn).  

KnDt is read‑only during grounding.  

KnDt is consumed by KnC, KnM, KnF via SSR + pointer/keyword lookups.  

Storage layout must preserve TS invariants: determinism, replay safety, immutability across turns/sessions.

### 3. High-Level Storage Model

On-disk representation:  
KnDt stored as one or more memory‑mappable files (e.g., flat binary tables, LMDB‑style pages, or custom pointer tables).  
Files are versioned and immutable once deployed.  

In-memory representation:  
Hot indexes (pointer tables, keyword hash maps) kept in RAM.  
OS page cache used for frequently accessed KnDt regions.  

KnDt is primarily read‑only, optimized for random access lookups, not scans.

### 4. File Layout and Segmentation

Tier segmentation:  
Separate files or segments for coarse, medium, and fine tiers.  
Each tier file contains only entries for that tier.  

Category segmentation:  
Within each tier, group entries by category (identity_anchor, relation_anchor, domain_anchor, qualifier_anchor, truth_validation_anchor, nouns, verbs, etc.).  

Index regions:  
Dedicated regions for pointer tables (address → offset).  
Dedicated regions for keyword indexes (keyword → address).  

Layout must favor locality for common categories and tiers (e.g., coarse identity/relations near each other).

### 5. Entry Encoding

A single KnDt entry is encoded on disk using a fixed or bounded record format containing:  
- symbol  
- tier  
- category  
- address  
- keywords[] (or pointer to keyword block)  
- features[] (grammar‑atomic)  
- version  

Record size must be fixed or bounded such that file offsets can be computed deterministically without scanning or variable-length decoding.  
Alignment and padding rules are used to keep access deterministic and efficient.  
No semantic or probabilistic fields.

### 6. Pointer and Keyword Indexes

Pointer index:  
maps address → file offset.  
stored in a compact RAM‑resident table or mmap’d region.  

Keyword index:  
maps keyword → address.  
implemented as a hash map or sorted table with exact match only.  

Keyword blocks must be stored in deterministic order (e.g., lexicographically) to ensure replay‑safe decoding.  

Pointer resolution is O(1) or near‑O(1); keyword resolution is exact match, no fuzzy search.

### 7. Memory Usage and Caching Strategy

Approximate RAM footprint for indexes is in the hundreds of MB.  
OS page cache is used for KnDt files.  
Optional small LRU cache for recently accessed entries (by address).  

Caching must not introduce nondeterminism; it only accelerates reads, not change behavior.

### 8. Access Pattern for KnC/KnM/KnF

1. Primitive receives SSR.candidate + KnDt_address/keyword.  
2. If address present → pointer index → file offset → entry read.  
3. Else keyword present → keyword index → address → pointer index → entry read.  
4. Entry decoded into grounded field (tier‑specific).  

Access is random‑read heavy, small record size, no scans.

### 9. Immutability and Versioning

KnDt files are immutable once deployed.  
Changes require a new version (e.g., KnDt_vN) with full replacement.  
Version field in entries supports replay invariants and auditability.  
No in‑place mutation, no online learning.

### 10. Performance Targets

For a typical laptop with NVMe SSD:  
~60 lookups per grounding pass (KnC+KnM+KnF).  
Total grounding time target: ≤ 15 ms, typical 5–10 ms after warm‑up.  
Random read latency assumptions (20–80 µs per 4K page).  

Layout and indexing are designed to meet these targets.

### 11. TS Invariants for Storage Layout

- deterministic access  
- replay‑safe behavior  
- immutability across turns and sessions  
- no probabilistic caching behavior  
- no semantic indexing  
- no heuristic fallback  
- no modification of KnDt during grounding

### 12. Deterministic Memory-Mapping Rules

- mmap must be read‑only  
- no copy‑on‑write pages  
- no dynamic remapping  
- offsets must remain stable across sessions

---
