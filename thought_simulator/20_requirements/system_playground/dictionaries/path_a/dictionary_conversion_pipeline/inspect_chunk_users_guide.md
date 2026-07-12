# 📘 **inspect_chunk_users_guide.md**  
### *How to Inspect TS Path A Developer Dictionary Chunks*

This guide explains how to use the `inspect_chunk.py` tool to view the contents of TS Path A **developer dictionary chunks** in a readable, structured way. It is designed for engineers who need to inspect, debug, validate, or understand the semantic entries produced by the dictionary conversion pipeline.

This document complements:

- **README.md** — system architecture  
- **how_to_gen_change_dct.md** — dictionary generation workflow  

and focuses specifically on **developer dictionary inspection**.

---

# 🔹 1. What `inspect_chunk.py` Does

The developer dictionary chunks (`meaning_dictionary_dev_XX.json.gz`) contain full TS semantic entries:

- lemma  
- gloss  
- primitives  
- invariants  
- cue envelope  
- routing signature  
- identity anchor  

These files are compressed and not human‑readable by default.

`inspect_chunk.py` provides:

### ✔ Pretty‑printed JSON output  
### ✔ Optional lemma filtering  
### ✔ Optional field filtering  
### ✔ Entry range slicing (`--limit MIN MAX`)  
### ✔ Automatic detection of the correct dictionary directory  
### ✔ Support for versioned dictionary directories  
### ✔ Zero‑configuration usage for users  
### ✔ Automatic log file creation for full‑chunk inspection  

It is the primary tool for inspecting developer dictionary content.

---

# 🔹 2. Where the Tool Lives

The tool is located in:

```
dictionary_conversion_pipeline/inspect_chunk.py
```

It automatically imports:

```python
BASE_DIR
DEV_OUTPUT_DIR
```

from `config.py`, so it always points to the correct dictionary version.

All inspection logs are written to:

```
BASE_DIR/inspection_logs/
```

This keeps logs version‑aware and prevents clutter.

---

# 🔹 3. How the Tool Resolves Chunk Paths

Users may provide:

### ✔ A full path  
```
python inspect_chunk.py /tmp/test.json.gz
```

### ✔ A filename  
```
python inspect_chunk.py meaning_dictionary_dev_03.json.gz
```

### ✔ A relative path  
```
python inspect_chunk.py dictionaries_dev_v3/meaning_dictionary_dev_01.json.gz
```

If only a filename is provided, the tool automatically looks inside:

```
DEV_OUTPUT_DIR
```

as defined in `config.py`.

This makes the tool version‑aware and repo‑aware.

---

# 🔹 4. Basic Usage

## **Inspect an entire chunk (writes a log file)**
```
python inspect_chunk.py meaning_dictionary_dev_01.json.gz
```

This produces:

- a summary in the terminal  
- a full log file at:  
  ```
  BASE_DIR/inspection_logs/inspect_log_meaning_dictionary_dev_01.json.gz.txt
  ```

Full‑chunk inspection **always** writes a log file to avoid overwhelming the terminal.

---

## **Inspect entries containing a substring**
```
python inspect_chunk.py meaning_dictionary_dev_06.json.gz --lemma oak
```

---

## **Show only specific fields**
```
python inspect_chunk.py meaning_dictionary_dev_03.json.gz --fields lemma gloss primitives
```

---

## **Show only the first N entries**
```
python inspect_chunk.py meaning_dictionary_dev_02.json.gz --limit 10
```

---

## **Show entries in a range (MIN MAX)**
```
python inspect_chunk.py meaning_dictionary_dev_02.json.gz --limit 100 110
```

This displays entries 100 through 110 (inclusive).

Range slicing works with:

- lemma filtering  
- field filtering  
- log file output  

---

## **Combine filters**
```
python inspect_chunk.py meaning_dictionary_dev_05.json.gz --lemma cedar --fields lemma gloss invariants --limit 50 75
```

---

# 🔹 5. What You Can Inspect

Developer dictionary entries contain:

- **lemma** — normalized WordNet lemma  
- **gloss** — cleaned WordNet gloss  
- **primitives** — TS primitive classification  
- **invariants** — semantic invariants  
- **cue_envelope** — triggers and suppressors  
- **routing_signature** — agent/object roles, temporal structure  
- **identity_anchor** — default meaning and continuity markers  

All fields are visible in developer chunks.

Runtime chunks do **not** contain glosses or metadata.

---

# 🔹 6. What the Tool Does *Not* Do

### ❌ It does not modify dictionary files  
It is strictly read‑only.

### ❌ It does not inspect runtime dictionary chunks  
A separate tool (`inspect_runtime_chunk.py`) can be added if needed.

### ❌ It does not validate manifest.json  
A separate validator can be added.

### ❌ It does not diff dictionary versions  
A diff tool can be added later.

---

# 🔹 7. When You Should Use This Tool

Use `inspect_chunk.py` when you need to:

- verify chunk boundaries  
- inspect semantic entries  
- debug gloss extraction  
- debug primitive classification  
- debug invariants  
- debug cue envelopes  
- debug routing signatures  
- debug identity anchors  
- compare dictionary versions  
- confirm WDP bucket distribution  
- validate developer dictionary correctness  

It is the primary inspection tool for TS Path A dictionary development.

---

# 🔹 8. Example: Inspecting a Chunk After Generation

After running:

```
python batch_converter.py
```

your developer dictionary directory will contain:

```
meaning_dictionary_dev_01.json.gz
meaning_dictionary_dev_02.json.gz
...
meaning_dictionary_dev_06.json.gz
manifest.json
```

To inspect chunk 3:

```
python inspect_chunk.py meaning_dictionary_dev_03.json.gz
```

To inspect only glosses:

```
python inspect_chunk.py meaning_dictionary_dev_03.json.gz --fields lemma gloss
```

To inspect only routing signatures:

```
python inspect_chunk.py meaning_dictionary_dev_03.json.gz --fields lemma routing_signature
```

To inspect entries 200–230:

```
python inspect_chunk.py meaning_dictionary_dev_03.json.gz --limit 200 230
```

---

# 🔹 9. Troubleshooting

### **Error: file not found**
The tool checks:

1. The exact path you provided  
2. `DEV_OUTPUT_DIR / filename`  

If neither exists, it prints both attempted paths.

---

### **Output is too long**
Full‑chunk inspection automatically writes a log file.

For smaller terminal output:

```
--limit N
```

or

```
--limit MIN MAX
```

---

### **Too much detail**
Use:

```
--fields lemma gloss
```

---

### **Cannot find config.py**
If the tool is run outside the repo, it falls back to:

```
BASE_DIR = Path(__file__).parent.resolve()
DEV_OUTPUT_DIR = BASE_DIR / "dictionaries_dev"
```

---

# 🔹 10. Summary

`inspect_chunk.py` is a safe, read‑only, version‑aware inspection tool that makes developer dictionary chunks human‑readable. It supports full‑chunk logging, range slicing, field filtering, lemma filtering, and version‑aware directory resolution. It is essential for debugging, validation, and semantic inspection during TS Path A dictionary development.

---
