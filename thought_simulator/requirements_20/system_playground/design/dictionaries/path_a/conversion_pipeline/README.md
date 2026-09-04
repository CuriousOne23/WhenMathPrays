# 📘 `dictionary_conversion_pipeline` — README.md (Updated for Chunked Architecture)

## Overview
The **dictionary_conversion_pipeline** is the offline pre‑work system that converts **raw WordNet data** into the **TS Path A Meaning Dictionary**.  
This pipeline performs deterministic semantic preprocessing to produce:

Full meaning-dictionary `.json.gz` archives are local-only in this repo, and any committed examples should use a different sample-oriented filename pattern.

- primitives  
- invariants  
- cue envelopes  
- routing signatures  
- identity anchors  

These components form the foundation of the **TS Path A Semantic Engine**.

The pipeline now produces **six developer dictionary chunks** and **six runtime dictionary chunks**, each approximately **1.7–1.8MB compressed**, with room to grow to **2.5–3MB** in future versions.

This chunked architecture provides:

- stable lemma boundaries  
- predictable chunk sizes  
- fast engineer inspection  
- fast TS runtime loading  
- clean version control  
- self‑contained dictionary directories  

---

## 📘 How to Generate and Modify Dictionaries

This README describes the **architecture** of the dictionary conversion pipeline — how chunking works, how manifest.json is produced, how developer/runtime dictionaries differ, and how the pipeline processes WordNet.

For **step‑by‑step instructions** on:

- generating a new dictionary version  
- changing dictionary output directories  
- changing dictionary naming  
- running `batch_converter.py`  
- running `ts_meaning_dct_path_a.py`  
- understanding input/output file locations  
- knowing what you must modify and must not modify  
- manually moving runtime files into `dictionaries_runtime/`

This companion document provides a **practical workflow guide** for engineers who need to regenerate or version dictionaries. It complements this README by focusing on **user actions**, while this README focuses on **system architecture**.

---

## Directory Structure (Updated)

```
dictionaries/
└── path_a/
    ├── conversion_pipeline/
    │   ├── yaml_writer.py
    │   ├── json_gzip_writer.py
    │   ├── batch_converter.py
    │   ├── ts_entry_builder.py
    │   ├── ... (other pipeline modules)
    │   └── wordnet_raw/
    │       ├── README.md                 # tracked
    │       ├── *.exc, frames.vrb, ...    # tracked helpers
    │       ├── data.noun / data.verb /   # LOCAL-ONLY (gitignored)
    │       │   data.adj / data.adv
    │       └── index.noun / index.verb / # LOCAL-ONLY (gitignored)
    │           index.adj / index.sense
    │
    ├── dictionaries_dev/                 # tracked: README, tools/, modify_entries.json
    │   └── (full *.json.gz release chunks are LOCAL-ONLY — not on GitHub)
    │
    ├── meaning_dictionary/dct_rev00/     # tracked: README, manifest, examples, tools/
    │   └── (full *.json.gz meaning chunks are LOCAL-ONLY — not on GitHub)
    │
    └── runtime_dictionary/dct_rev00/     # tracked: README, manifest.json
        └── (full *.json.gz runtime chunks are LOCAL-ONLY — not on GitHub)
```

**Status (paths only):** Full WordNet `data.*` / `index.*` dumps stay local on the developer machine (see `wordnet_raw/README.md`). Full `*.json.gz` dictionary archives under Path A are gitignored and are not on GitHub. Tracked trees keep READMEs, manifests, tools, and helpers — not a committed gzip dump tree.

Each dictionary version is **self‑contained**.  
No duplicate versions of the same file are allowed.

---

## Chunking Architecture

### 🔹 Word Density Profile (WDP)
During conversion, the pipeline computes a **Word Density Profile**:

```
lemma → size_in_bytes_of_TS_entry
```

This is a deterministic measurement (not statistical) used to create stable chunk boundaries.

### 🔹 Six Chunks
The developer dictionary is split into **six chunks**, each targeting:

```
~1.7–1.8MB compressed
```

This provides headroom for future growth to:

```
2.5MB → 3MB per chunk
```

### 🔹 Paired Dev/Runtime Chunks
For each developer chunk:

```
meaning_dictionary_dev_XX.json.gz
```

there is a matching runtime chunk:

```
ts_meaning_dictionary_XX.json.gz
```

Both chunks contain the same lemma range.

### 🔹 Manifest
Each dictionary directory contains:

```
manifest.json
```

with:

- chunk ID  
- dev filename  
- runtime filename  
- first lemma  
- last lemma
- entry count
- compressed size  

This ensures deterministic loading and easy engineer navigation.

---

## File‑by‑File Purpose (Updated)

### **1. `wordnet_loader.py`**
Parses raw WordNet `index.*` and `data.*` files.  
Produces synsets and lemma → offset mappings.  
Foundation for all downstream modules.

---

### **2. `lemma_normalizer.py`**
Normalizes lemmas:

- removes underscores  
- preserves multi‑word expressions  
- lowercases  
- strips punctuation  

---

### **3. `gloss_extractor.py`**
Extracts gloss text from synsets.  
Feeds glosses into semantic generators.

---

### **4. `primitive_classifier.py`**
Assigns TS primitives based on gloss, POS, and semantic relations.

---

### **5. `invariant_generator.py`**
Builds semantic invariants using gloss and semantic pointers.

---

### **6. `cue_envelope_generator.py`**
Creates cue envelopes (triggers and suppressors).

---

### **7. `routing_signature_generator.py`**
Generates routing signatures (agent/object roles, temporal structure).

---

### **8. `identity_anchor_generator.py`**
Creates identity anchors (default meaning, continuity markers).

---

### **9. `ts_entry_builder.py`**
Combines all components into a single TS dictionary entry.

---

### **10. `json_gzip_writer.py`**
Writes TS entries into **six chunked JSON GZIP files**:

```
meaning_dictionary_dev_01.json.gz
...
meaning_dictionary_dev_06.json.gz
```

Chunking is based on the **Word Density Profile**.

`yaml_writer.py` is still supported but is slower and uses more memory.

---

### **11. `batch_converter.py`**
Top‑level orchestrator:

1. loads WordNet  
2. normalizes lemmas  
3. extracts glosses  
4. generates primitives  
5. generates invariants  
6. generates cue envelopes  
7. generates routing signatures  
8. generates identity anchors  
9. builds TS entries  
10. computes Word Density Profile  
11. writes **six developer chunks**  
12. writes `manifest.json`

This is the file you run to produce the developer dictionary.

---

### **12. `ts_meaning_dct_path_a.py`**
see dictionaries_runtime/tools directory

---

### **13. `utils.py`**
Shared helpers for text cleaning, tokenization, semantic relations, logging.

---

### **14. `config.py`**
Configuration for file paths, thresholds, cue envelope parameters, invariant weights, routing defaults, and logging.

---

## Execution Order

1. `wordnet_loader.py`  
2. `lemma_normalizer.py`  
3. `gloss_extractor.py`  
4. `primitive_classifier.py`  
5. `invariant_generator.py`  
6. `cue_envelope_generator.py`  
7. `routing_signature_generator.py`  
8. `identity_anchor_generator.py`  
9. `ts_entry_builder.py`  
10. `json_gzip_writer.py`  
11. `batch_converter.py`  
12. `ts_meaning_dct_path_a.py` (runtime stripper)

---

## Input Files

Located in:

```
wordnet_raw/
```

Required locally (gitignored — not on GitHub; fetch per `wordnet_raw/README.md`):

- `index.noun`  
- `index.verb`  
- `index.adj`  
- `index.adv` / `index.sense`  
- `data.noun`  
- `data.verb`  
- `data.adj`  
- `data.adv`

Still tracked in `wordnet_raw/`: `README.md`, `*.exc`, `frames.vrb`, `sents.vrb`, `sentidx.vrb`.

---

## Output Files

Developer / meaning dictionary chunks (local-only `*.json.gz`, not on GitHub):

```
meaning_dictionary/dct_rev00/meaning_dictionary_dev_XX.json.gz   # LOCAL-ONLY
dictionaries_dev/…                                               # workspace; no committed gzip tree
```

Runtime dictionary chunks (local-only `*.json.gz`, not on GitHub):

```
runtime_dictionary/dct_rev00/ts_meaning_dictionary_XX.json.gz    # LOCAL-ONLY
```

Tracked alongside those folders (when present): `README.md`, `manifest.json`, tools/helpers — not the full gzip archives.

Manifest:

```
manifest.json
```

---

## How This Pipeline Fits Into TS Path A

TS Path A requires a **deterministic, pre‑computed semantic dictionary**.  
This pipeline provides exactly that.

Runtime layers:

- SOB  
- SROB  
- CnOB  
- SmOB  
- SSG  

consume the dictionary but **never modify it**.

All heavy semantic processing happens **offline**, here, in this pipeline.

This ensures:

- deterministic routing  
- stable meaning selection  
- fast runtime performance  
- geometric manifold consistency  

---