# 📘 **ts_meaning_dct_userguide.md**  
### *How to Generate the TS Runtime Dictionary (Path A)*

`ts_meaning_dct_path_a.py` converts a **developer dictionary release** (e.g., `dct_rev00`) into a **runtime‑efficient dictionary** by stripping developer‑only metadata and producing compact TS‑ready chunks.

This tool is part of the **runtime dictionary workflow** and lives in:

```
dictionaries_runtime/tools/
```

It reads configuration from:

```
dictionaries_runtime/tools/ts_meaning_dct_path_a_setup.yaml
```

and writes output into the **same directory where the script is executed**.

Users manually move the generated runtime files into:

```
dictionaries_runtime/
```

to prevent accidental overwrites.

---

# 🔹 1. Purpose of the Runtime Dictionary

The **developer dictionary** contains full semantic entries:

- lemma  
- gloss  
- primitive  
- invariant  
- cue envelope  
- identity anchor  
- routing signature  
- alternates  
- metadata used for debugging and development  

The **runtime dictionary** contains only the fields required by the TS runtime engine:

- `lemma`  
- `alternates`  
- `primitive`  
- `invariants`  
- `cue_envelope`  
- `routing_signature`  
- `identity_anchor`  

All other fields (gloss, developer metadata, debug structures) are removed.

This makes runtime chunks:

- smaller  
- faster to load  
- faster to route  
- deterministic  
- TS‑ready  

---

# 🔹 2. Directory Structure (Runtime Side)

```
dictionaries_runtime/
    tools/
        ts_meaning_dct_path_a.py
        ts_meaning_dct_path_a_setup.yaml
        output/   (optional; user may create)
```

The script **never writes** into `dictionaries_runtime/` directly.

All output is written into:

```
dictionaries_runtime/tools/
```

Users manually move the files afterward.

---

# 🔹 3. Setup File (Required)

The script reads:

```
ts_meaning_dct_path_a_setup.yaml
```

Example:

```yaml
dev_dictionary_dir: "../../dictionaries_dev/dct_rev00/"
dev_chunk_prefix: "meaning_dictionary_dev_"
```

This tells the tool:

- which developer release directory to read  
- how developer chunk filenames are prefixed  

This replaces all command‑line directory arguments.

---

# 🔹 4. Input Requirements

The developer release directory must contain:

```
dct_rev00/
    meaning_dictionary_dev_01.json.gz
    meaning_dictionary_dev_02.json.gz
    ...
    manifest.json
```

The script reads:

- the manifest  
- each chunk listed in the manifest  
- each entry inside each chunk  

---

# 🔹 5. Output Files

The script writes the following files into **its own directory**:

```
ts_meaning_dictionary_01.json.gz
ts_meaning_dictionary_02.json.gz
...
manifest.json
```

These files are **runtime‑ready**.

Users must manually move them into:

```
dictionaries_runtime/
```

This prevents accidental overwrites of existing runtime dictionaries.

---

# 🔹 6. How to Run the Tool

From inside:

```
dictionaries_runtime/tools/
```

run:

```
python ts_meaning_dct_path_a.py
```

The script will:

1. Load `ts_meaning_dct_path_a_setup.yaml`  
2. Resolve the developer dictionary directory  
3. Load the developer manifest  
4. Process each developer chunk  
5. Strip developer‑only fields  
6. Write runtime chunks  
7. Write a runtime manifest  

---

# 🔹 7. What the Script Removes

The following fields are **removed**:

- `gloss`  
- developer metadata  
- debug fields  
- any fields not required by TS runtime  

The following fields are **kept**:

- `lemma`  
- `alternates`  
- `primitive`  
- `invariants`  
- `cue_envelope`  
- `routing_signature`  
- `identity_anchor`  

This ensures runtime entries are compact and deterministic.

---

# 🔹 8. What the Runtime Manifest Contains

The runtime manifest contains:

- `chunk_id`  
- `filename`  
- `first_lemma`  
- `last_lemma`  
- `entry_count`  
- `compressed_size`  

Example:

```json
{
  "chunk_id": 3,
  "filename": "ts_meaning_dictionary_03.json.gz",
  "first_lemma": "fastidious",
  "last_lemma": "labanotation",
  "entry_count": 19551,
  "compressed_size": 1968803
}
```

This manifest is used by the TS runtime engine to load chunks efficiently.

---

# 🔹 9. Typical Workflow

### **Step 1 — Generate developer dictionary**
From the conversion pipeline:

```
python batch_converter.py
```

### **Step 2 — Inspect developer dictionary**
Using:

```
inspect_chunk.py
```

### **Step 3 — Modify developer dictionary (optional)**
Using:

```
modify_dev_dct.py
```

### **Step 4 — Generate runtime dictionary**
From:

```
dictionaries_runtime/tools/
```

run:

```
python ts_meaning_dct_path_a.py
```

### **Step 5 — Move runtime files**
Move:

```
ts_meaning_dictionary_XX.json.gz
manifest.json
```

into:

```
dictionaries_runtime/
```

---

# 🔹 10. Troubleshooting

### **Error: setup file not found**
Ensure:

```
ts_meaning_dct_path_a_setup.yaml
```

exists in the same directory as the script.

### **Error: developer manifest not found**
Ensure the path in the setup file points to a valid release directory.

### **Output not appearing**
All output is written into the **tools directory**, not into the release directory.

---

# 🔹 11. Summary

`ts_meaning_dct_path_a.py` is the official TS Path A runtime dictionary generator.  
It converts developer dictionary releases into compact, deterministic runtime chunks by stripping developer‑only metadata.

It is:

- safe  
- deterministic  
- version‑clean  
- architecture‑aligned  
- manually controlled  

and fits perfectly into the TS Path A dictionary workflow.

---
