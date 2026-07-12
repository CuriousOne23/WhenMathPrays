# 📘 **inspect_chunk_users_guide.md**  
### *Developer Dictionary Inspection Tool — TS Path A*

This guide explains how to use the `inspect_chunk.py` tool to inspect **developer dictionary chunks** (`meaning_dictionary_dev_XX.json.gz`) in TS Path A. It reflects the **new architecture**, where:

- tools live in  
  ```
  dictionaries_dev/tools/
  ```
- release directories live parallel to tools, e.g.  
  ```
  dictionaries_dev/dct_rev00/
  ```
- each tool reads its own setup file  
  ```
  inspect_chunk_setup.yaml
  ```
- logs are written locally inside  
  ```
  dictionaries_dev/tools/insp_chnk_log/
  ```

This document replaces the older version that referenced `dictionary_conversion_pipeline` and `config.py`.

---

# 🔹 1. What `inspect_chunk.py` Does

Developer dictionary chunks contain full TS semantic entries:

- lemma  
- gloss  
- primitive  
- invariant  
- cue envelope  
- routing signature  
- identity anchor  

These files are compressed (`.json.gz`) and not human‑readable by default.

`inspect_chunk.py` provides:

### ✔ Pretty‑printed JSON output  
### ✔ Lemma substring filtering (`--lemma`)  
### ✔ Field filtering (`--fields`)  
### ✔ Entry range slicing (`--limit N` or `--limit MIN MAX`)  
### ✔ Automatic resolution of chunk paths via `inspect_chunk_setup.yaml`  
### ✔ Local log file creation for full‑chunk inspection  
### ✔ Read‑only operation (never modifies dictionary files)

It is the primary tool for inspecting developer dictionary content.

---

# 🔹 2. Where the Tool Lives

The tool is located in:

```
dictionaries_dev/tools/inspect_chunk.py
```

It reads configuration from:

```
dictionaries_dev/tools/inspect_chunk_setup.yaml
```

This setup file tells the tool:

- where the active release directory is  
- where the developer dictionary chunks live  
- where to write logs  

Example:

```yaml
dev_dictionary_dir: "../dct_rev00/"
dev_chunk_prefix: "meaning_dictionary_dev_"
log_dir: "insp_chnk_log/"
```

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
python inspect_chunk.py ../dct_rev00/meaning_dictionary_dev_01.json.gz
```

If only a filename is provided, the tool automatically looks inside:

```
dev_dictionary_dir
```

as defined in `inspect_chunk_setup.yaml`.

This makes the tool **release‑aware** and **version‑clean**.

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
  dictionaries_dev/tools/insp_chnk_log/inspect_log_meaning_dictionary_dev_01.json.gz.log
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
python inspect_chunk.py meaning_dictionary_dev_03.json.gz --fields lemma gloss primitive
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

---

## **Combine filters**
```
python inspect_chunk.py meaning_dictionary_dev_05.json.gz --lemma cedar --fields lemma gloss invariant --limit 50 75
```

---

# 🔹 5. What You Can Inspect

Developer dictionary entries contain:

- **lemma** — normalized WordNet lemma  
- **gloss** — cleaned WordNet gloss  
- **primitive** — TS primitive classification  
- **invariant** — semantic invariants  
- **cue_envelope** — triggers and suppressors  
- **routing_signature** — agent/object roles, temporal structure  
- **identity_anchor** — default meaning and continuity markers  

All fields are visible in developer chunks.

Runtime chunks do **not** contain glosses or metadata.

---

# 🔹 6. What the Tool Does *Not* Do

### ❌ It does not modify dictionary files  
Strictly read‑only.

### ❌ It does not inspect runtime dictionary chunks  
A separate runtime inspection tool may be added later.

### ❌ It does not validate manifest files  
A manifest validator can be added separately.

### ❌ It does not diff dictionary versions  
A diff tool can be added later.

---

# 🔹 7. When You Should Use This Tool

Use `inspect_chunk.py` when you need to:

- inspect semantic entries  
- debug gloss extraction  
- debug primitive classification  
- debug invariants  
- debug cue envelopes  
- debug routing signatures  
- debug identity anchors  
- verify chunk boundaries  
- compare dictionary versions  
- validate developer dictionary correctness  

It is the primary inspection tool for TS Path A dictionary development.

---

# 🔹 8. Example: Inspecting a Chunk in a Release Directory

Suppose your release directory is:

```
dictionaries_dev/dct_rev00/
```

and contains:

```
meaning_dictionary_dev_01.json.gz
meaning_dictionary_dev_02.json.gz
...
manifest.json
```

Your setup file:

```
dictionaries_dev/tools/inspect_chunk_setup.yaml
```

contains:

```yaml
dev_dictionary_dir: "../dct_rev00/"
dev_chunk_prefix: "meaning_dictionary_dev_"
log_dir: "insp_chnk_log/"
```

To inspect chunk 3:

```
python inspect_chunk.py meaning_dictionary_dev_03.json.gz
```

To inspect only glosses:

```
python inspect_chunk.py meaning_dictionary_dev_03.json.gz --fields lemma gloss
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
2. `dev_dictionary_dir / filename`  

If neither exists, it prints both attempted paths.

---

### **Output is too long**
Full‑chunk inspection automatically writes a log file.

Use:

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

### **Wrong release directory**
Update:

```
active release directory in inspect_chunk_setup.yaml
```

---

# 🔹 10. Summary

`inspect_chunk.py` is a safe, read‑only, release‑aware inspection tool that makes developer dictionary chunks human‑readable. It supports full‑chunk logging, range slicing, field filtering, lemma filtering, and release‑aware directory resolution via `inspect_chunk_setup.yaml`.

It is essential for debugging, validation, and semantic inspection during TS Path A dictionary development.

---
