# **modify_development_dct_userguide.md**  
### *Developer Dictionary Modification Tool — TS Path A*

`modify_dev_dct.py` is the developer‑layer dictionary editor for TS Path A.  
It performs controlled, revision‑tracked updates to the **developer dictionary** by adding, modifying, or deleting entries.  
It preserves dictionary geometry, chunk numbering, and manifest history.

This tool is intentionally conservative:

- **Never deletes existing dictionary files**  
- **Never overwrites existing manifests**  
- **Never writes into release directories**  
- **Never writes into dictionaries_dev/**  
- **Requires explicit user action** when structural changes are needed  
- **Requires batch mode** when chunk sizes exceed safe limits  

All output is written into the **tools directory**, and users manually move files into the appropriate release directory.

---

# 🔹 1. Directory Structure (New Architecture)

Under the new TS Path A layout:

```
dictionaries_dev/
    dct_rev00/
        meaning_dictionary_dev_01.json.gz
        meaning_dictionary_dev_02.json.gz
        manifest.json
        ...
    tools/
        modify_dev_dct.py
        modify_dev_dct_setup.yaml
        output/
```

### ✔ Release directories (`dct_revNN/`)  
Contain dictionary chunks and manifest files.

### ✔ Tools directory  
Contains:

- `modify_dev_dct.py`  
- `modify_dev_dct_setup.yaml`  
- `output/` (where new chunks + new manifest revisions are written)

Tools **never** write into release directories.  
Users manually move output files into the correct release directory.

---

# 🔹 2. Setup File (Required)

`modify_dev_dct.py` reads configuration from:

```
dictionaries_dev/tools/modify_dev_dct_setup.yaml
```

Example:

```yaml
dev_dictionary_dir: "../dct_rev00/"
dev_chunk_prefix: "meaning_dictionary_dev_"
input_file: "../dct_rev00/modify_entries.json"
```

This file tells the tool:

- which release directory to read  
- where the input file lives  
- how chunk filenames are prefixed  

This replaces all command‑line directory arguments.

---

# 🔹 3. Modes of Operation

`modify_dev_dct.py` has two modes:

---

## **1. Normal Mode (default)**  
Used for small, local edits:

- add entries  
- modify entries  
- delete entries  

Normal mode:

- Loads the **highest manifest revision** in the release directory  
- Applies edits locally  
- Writes new chunk files into `tools/output/`  
- Writes a new manifest revision into `tools/output/`  
- Enforces chunk size limits (2.5–3.0 MB)  
- Never overwrites existing files  

If any chunk exceeds the limit, normal mode **stops** and instructs the user to run batch mode.

---

## **2. Batch Mode (`--batch`)**  
Used when chunk sizes exceed limits and the dictionary must be **re‑chunked**.

Batch mode:

- Requires user to manually increase `CHUNK_COUNT` in the release directory’s `config.py.json`  
- Loads all entries from all chunks  
- Recomputes WDP (Word Density Profile)  
- Re-chunks the entire dictionary  
- Writes new chunk files into `tools/output/`  
- Writes a new manifest revision into `tools/output/`  

Batch mode is the **only** mode that changes dictionary geometry.

---

# 🔹 4. Manifest Discovery

Inside the release directory (`dev_dictionary_dir`):

1. If files matching `manifest_revNN.json` exist:  
   - The **highest NN** is loaded  
2. Otherwise:  
   - `manifest.json` is loaded  

This ensures:

- newest revision is always used  
- full revision history is preserved  
- no accidental rollback  

---

# 🔹 5. Input File

### **Default name**
```
modify_entries.json
```

### **Default location**
Inside the release directory:

```
dct_rev00/modify_entries.json
```

### **Configured via setup file**
In `modify_dev_dct_setup.yaml`:

```yaml
input_file: "../dct_rev00/modify_entries.json"
```

No command‑line override is used in the new architecture.

---

# 🔹 6. Input File Format

The input file contains a list of operations.

### Example
```json
[
  {
    "operation": "add",
    "entry": { ... full TS developer entry ... }
  },
  {
    "operation": "modify",
    "entry": { ... full TS developer entry ... }
  },
  {
    "operation": "delete",
    "lemma": "chief petty officer"
  }
]
```

---

# 🔹 7. Allowed Operations

### `"add"`  
Insert a new dictionary entry.

### `"modify"`  
Replace an existing entry.

### `"delete"`  
Remove an entry by lemma.

Each operation must specify:

- `"operation"`  
- `"entry"` (for add/modify)  
- `"lemma"` (for delete)

---

# 🔹 8. Required Fields for Add/Modify

Each entry must contain:

- `lemma`  
- `gloss`  
- `primitive`  
- `cue_envelope`  
- `invariant`  
- `identity_anchor`  
- `routing_signature`

These fields define a complete TS developer dictionary entry.

---

# 🔹 9. Chunk Selection

Given a lemma:

1. Read manifest  
2. Identify the chunk whose range satisfies:  
   ```
   first_lemma <= lemma <= last_lemma
   ```
3. If lemma falls outside all ranges:  
   - Determine correct chunk by lexicographic position  
   - Insert into that chunk  

Chunk numbering **never changes** in normal mode.

---

# 🔹 10. Mutation Behavior

### **Add**
- Determine correct chunk  
- Insert entry in sorted order  
- Write new chunk file to `tools/output/`  
- Update manifest  

### **Modify**
- Replace entry  
- Re-sort  
- Write new chunk file  
- Update manifest  

### **Delete**
- Remove entry  
- Re-sort  
- Write new chunk file  
- Update manifest  

All new files are written into:

```
dictionaries_dev/tools/output/
```

Users manually move them into the correct release directory.

---

# 🔹 11. Chunk Size Enforcement

After edits:

- Compute uncompressed size of each chunk  
- If **any chunk > 3 MB**, normal mode stops  

Message:

```
Chunk 3 exceeds 3 MB limit.
Normal mode cannot continue.

Please increase CHUNK_COUNT in config.py.json.
Then run:

    python modify_dev_dct.py --batch
```

Batch mode is required to re‑chunk.

---

# 🔹 12. Batch Mode Workflow

Triggered by:

```
python modify_dev_dct.py --batch
```

Batch mode:

1. Loads highest manifest revision  
2. Confirms `CHUNK_COUNT` was manually increased  
3. Loads all entries  
4. Recomputes WDP  
5. Re-chunks dictionary  
6. Writes new chunk files to `tools/output/`  
7. Writes new manifest revision to `tools/output/`  

Batch mode is the **only** mode that changes dictionary geometry.

---

# 🔹 13. Manifest Revisioning

Every run produces:

```
manifest_revNN.json
```

Where NN = highest existing revision + 1.

Example:

- Reads `manifest_rev00.json` → writes `manifest_rev01.json`  
- Reads `manifest_rev01.json` → writes `manifest_rev02.json`  

Old manifests are **never overwritten**.

---

# 🔹 14. Output Location (New Architecture)

All output files are written into:

```
dictionaries_dev/tools/output/
```

This includes:

- new chunk files  
- new manifest_revNN.json  

Users manually move these files into the appropriate release directory:

```
dictionaries_dev/dct_revNN/
```

This prevents accidental overwrites and keeps releases clean.

---

# 🔹 15. Summary Report

Normal mode prints:

- added entries  
- modified entries  
- deleted entries  
- skipped entries (with reasons)  
- updated chunk boundaries  
- updated entry counts  
- updated total_entries  
- chunk sizes  
- whether batch mode is required  

Batch mode prints:

- old chunk count  
- new chunk count  
- total entries  
- new boundaries  
- new sizes  
- confirmation message  

---

# 🔹 16. Compatibility

This design ensures compatibility with:

- `inspect_chunk.py`  
- `ts_meaning_dct_path_a.py`  
- all dictionary utilities  
- all release directories  

No structural changes are required outside the tools directory.

---
