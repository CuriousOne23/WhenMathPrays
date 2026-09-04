# **runtime_dictionary — TS Runtime Dictionary (Path A)**

The **runtime dictionary** is the compact, TS‑efficient version of the developer dictionary.  
It contains only the fields required by the TS runtime engine and is optimized for:

Full meaning-dictionary `.json.gz` archives are local-only in this repo; any committed examples should use a different sample-oriented filename pattern.

- fast loading  
- deterministic routing  
- minimal memory footprint  
- stable chunk geometry  

Runtime dictionaries are generated from developer dictionary releases using:

```
runtime_dictionary/tools/ts_meaning_dct_path_a.py
```

This directory stores the **final runtime dictionary files** used by TS Path A.

---

# 📁 **Directory Structure**

```
runtime_dictionary/
│
├── README.md
├── dct_rev00/                         # tracked release folder
│   ├── README.md                      # tracked — local-only note for *.json.gz
│   ├── manifest.json                  # tracked
│   └── ts_meaning_dictionary_XX.json.gz   # LOCAL-ONLY (gitignored; not on GitHub)
│
└── tools/
    ├── ts_meaning_dct_path_a.py
    ├── ts_meaning_dct_path_a_setup.yaml
    ├── ts_meaning_dct_userguide.md
    └── (optional) output/
```

**Status (paths only):** Full `*.json.gz` runtime dictionaries under `dct_rev00/` are gitignored by the repo-root `.gitignore`. They stay local and are not on GitHub. Tracked in `dct_rev00/` (when present): `manifest.json`, `README.md`.

### ✔ Runtime gzip chunks live under versioned `dct_revNN/` (local-only on disk)  
### ✔ Tools live in `tools/`  
### ✔ Tools **never** write into release directories directly  
### ✔ Users manually move generated runtime files into `dct_revNN/`  

This prevents accidental overwrites and keeps runtime versions clean.

---

# 🔹 **What Runtime Dictionary Files Contain**

Runtime dictionary chunks contain **only the fields required by TS runtime**:

- `lemma`  
- `alternates`  
- `primitive`  
- `invariants`  
- `cue_envelope`  
- `routing_signature`  
- `identity_anchor`  

All developer‑only fields (gloss, debug metadata, extraction notes, etc.) are removed.

This makes runtime chunks:

- smaller  
- faster  
- deterministic  
- stable across versions  

---

# 🔹 **Manifest Structure**

The runtime manifest (`manifest.json`) contains:

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

The manifest is used by the TS runtime engine to load chunks efficiently.

---

# 🔹 **How Runtime Dictionaries Are Generated**

Runtime dictionaries are produced by running:

```
python ts_meaning_dct_path_a.py
```

from inside:

```
runtime_dictionary/tools/
```

The script:

1. Reads `ts_meaning_dct_path_a_setup.yaml`  
2. Loads the developer dictionary release (e.g., `dct_rev00`)  
3. Loads the developer manifest  
4. Processes each developer chunk  
5. Strips developer‑only fields  
6. Writes runtime chunks into the **tools directory**  
7. Writes a runtime manifest into the **tools directory**  

Users then manually move:

```
ts_meaning_dictionary_XX.json.gz
manifest.json
```

into the active release folder, e.g.:

```
runtime_dictionary/dct_rev00/
```

(`*.json.gz` remain local-only / gitignored; `manifest.json` may be tracked.)

This ensures runtime files are never overwritten accidentally.

---

# 🔹 **Setup File**

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

# 🔹 **Workflow Summary**

### **1. Developer dictionary is generated**  
Using the conversion pipeline.

### **2. Developer dictionary is inspected**  
Using `inspect_chunk.py`.

### **3. Developer dictionary is modified (optional)**  
Using `modify_dev_dct.py`.

### **4. Runtime dictionary is generated**  
Using `ts_meaning_dct_path_a.py`.

### **5. Runtime files are promoted**  
Manually moved into the active release folder, e.g.:

```
runtime_dictionary/dct_rev00/
```

(`*.json.gz` local-only; not on GitHub.)

This keeps runtime dictionaries clean, stable, and version‑safe.

---

# 🔹 **Purpose of This Directory**

`runtime_dictionary` is the **final, TS‑ready dictionary** for Path A.  
It contains only the fields required by the runtime engine and is optimized for performance and stability.

This directory is the authoritative source for:

- TS runtime dictionary chunks  
- TS runtime manifest  
- runtime dictionary versioning  
- runtime dictionary deployment  

---