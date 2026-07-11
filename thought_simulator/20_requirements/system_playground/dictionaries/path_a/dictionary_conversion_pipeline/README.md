# 📘 `dictionary_conversion_pipeline` — README.md

## Overview
The **dictionary_conversion_pipeline** is the offline pre‑work system that converts **raw WordNet data** into the **TS Path A Meaning Dictionary**.  
This pipeline performs deterministic semantic preprocessing to produce:

- primitives  
- invariants  
- cue envelopes  
- routing signatures  
- identity anchors  

These components form the foundation of the **TS Path A Semantic Engine**.

The output of this pipeline is:

```
meaning_dictionary.yaml
```

This file is consumed at runtime by InB → IIInB → CEx  → CE & SOB → SROB → CnOB → SmOB → SSG.

---

## Directory Structure

```
dictionaries/
└── path_a/
    ├── dictionary_conversion_pipeline/
    │   ├── yaml_writer.py
    │   ├── json_gzip_writer.py        ← NEW
    │   ├── ts_meaning_dct_path_a.py   ← NEW (runtime stripper)
    │   ├── batch_converter.py
    │   ├── ts_entry_builder.py
    │   ├── ... (other pipeline modules)
    │   └── wordnet_raw/
    │       ├── index.noun
    │       ├── index.verb
    │       ├── index.adj
    │       ├── index.adv
    │       ├── data.noun
    │       ├── data.verb
    │       ├── data.adj
    │       └── data.adv
    │
    ├── dictionaries_dev/
    │   └── meaning_dictionary_dev.json.gz
    │
    └── dictionaries_runtime/
        └── ts_meaning_dictionary.json.gz
```

---

## File‑by‑File Purpose

### **1. `wordnet_loader.py`**
Directly parses raw WordNet `index.*` and `data.*` files.  
Produces:

- lemma → synset offset index  
- synset objects (lemmas, gloss, pointers, POS)

This is the foundation for all downstream modules.

---

### **2. `lemma_normalizer.py`**
Normalizes WordNet lemmas:

- removes underscores  
- preserves multi‑word expressions  
- lowercases  
- strips punctuation  

Ensures consistent lemma formatting for TS.

---

### **3. `gloss_extractor.py`**
Extracts gloss text from synsets.  
Feeds glosses into:

- primitive classifier  
- invariant generator  
- cue envelope generator  
- routing signature generator

---

### **4. `primitive_classifier.py`**
Assigns TS primitives based on:

- gloss  
- POS  
- semantic relations  

Primitives include: entity, action, relation, event, property, etc.

---

### **5. `invariant_generator.py`**
Builds semantic invariants using:

- gloss  
- hypernyms  
- hyponyms  
- semantic pointers  

Invariants define stable meaning properties.

---

### **6. `cue_envelope_generator.py`**
Creates cue envelopes:

- triggers → contextual activation signals  
- suppressors → contextual suppression signals  

Cue envelopes determine **meaning eligibility** during runtime.

---

### **7. `routing_signature_generator.py`**
Generates routing signatures:

- agent/object roles  
- temporal structure  
- adjacency requirements  
- semantic flow hints  

Used by Path A routing.

---

### **8. `identity_anchor_generator.py`**
Creates identity anchors:

- default meaning  
- continuity markers  
- stability hints  
- multi‑word identity preservation  

Anchors stabilize meaning selection.

---

### **9. `ts_entry_builder.py`**
Combines all components into a single TS dictionary entry:

- primitive  
- invariants  
- cue envelope  
- routing signature  
- identity anchor  

Produces the final in‑memory representation.

---

### **10. `json_gzip_writer.py`**
Writes TS dictionary entries into:

```
meaning_dictionary.json.gz
```

Supports chunking or single‑file output.

yaml_writer.py writes meaning_dictionary.yaml but it will be a lot slower in writing and use a lot more memory, highly reccommend you use json_gzip_writer.py.

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
10. writes YAML output

This is the file you run to produce the dictionary.

---

### **12. `utils.py`**
Shared helpers:

- text cleaning  
- tokenization  
- stopword removal  
- semantic relation helpers  
- logging  
- error handling  

---

### **13. `config.py`**
Configuration for:

- file paths  
- thresholds  
- cue envelope parameters  
- invariant weights  
- routing signature defaults  
- logging verbosity  

---

Here is **section 14** written in the exact style and structure of your existing README, matching tone, formatting, and semantic clarity. It fits directly after section 13.

---

### **14. `ts_meaning_dct_path_a.py`**
Produces the **TS‑efficient runtime dictionary** for Path A by stripping all non‑essential developer metadata from the full dictionary.

This module loads:

```
dictionaries_dev/meaning_dictionary_dev.json.gz
```

and writes the compact, machine‑optimized runtime dictionary:

```
ts_meaning_dictionary.json.gz
After writing the use has to move the file manually to the correct directory, this is done such that the program doesn't automatically overwrite a file. The location will be, dictionaries_runtime is under both path_a, one level above dictionary_conversion_pipeline, indicating release and one under dictionary_conversion_pipeline, indicating still developing.
dictionaries_runtime/ts_meaning_dictionary.json.gz
```

The runtime dictionary contains **only the fields required by TS Path A routing**, including:

- lemma  
- alternate lemmas  
- primitive  
- invariants  
- cue envelope  
- routing signature  
- identity anchor  

All developer‑oriented fields are removed:

- gloss  
- WordNet pointers  
- raw synset metadata  
- diagnostic fields  
- intermediate pipeline artifacts  

The resulting file is **small, fast to load, and fully deterministic**, making it ideal for:

- InB → IIInB → CEx → CE & SOB → SROB → CnOB → SmOB → SSG  
- runtime semantic routing  
- geometric manifold projection  
- stable meaning selection  

This is the dictionary consumed by TS Path A at runtime.

---

## Execution Order

The pipeline must run in this exact order:

1. **wordnet_loader.py**  
2. **lemma_normalizer.py**  
3. **gloss_extractor.py**  
4. **primitive_classifier.py**  
5. **invariant_generator.py**  
6. **cue_envelope_generator.py**  
7. **routing_signature_generator.py**  
8. **identity_anchor_generator.py**  
9. **ts_entry_builder.py**  
10. **json_gzip_writer.py**  
11. **batch_converter.py** (runs everything)

---

## Input Files

Located in:

```
wordnet_raw/
```

Required files:

- `index.noun`
- `index.verb`
- `index.adj`
- `index.adv`
- `data.noun`
- `data.verb`
- `data.adj`
- `data.adv`

These are the official Princeton WordNet 3.0 raw files.

---

## Output Files

Generated in the pipeline directory dictonaries_dev by batch_converter.py:

```
dictionaries_dev/meaning_dictionary.json.gz
```

This file contains all TS semantic identities with:

- primitives  
- invariants  
- cue envelopes  
- routing signatures  
- identity anchors  

This is the dictionary consumed by TS Path A at runtime.

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
