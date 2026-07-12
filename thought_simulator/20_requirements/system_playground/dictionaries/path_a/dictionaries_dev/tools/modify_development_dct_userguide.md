# **modify_development_dct_userguide.md**

## **Overview**
`modify_dev_dct.py` is the developer‑layer dictionary editor for Path A.  
It allows controlled, revision‑tracked updates to the **developer dictionary** by adding, modifying, or deleting entries.  
It preserves dictionary geometry, chunk numbering, and manifest history.

This tool is intentionally conservative:  
- It **never deletes existing dictionary files**  
- It **never overwrites manifests**  
- It **forces explicit user decisions** when structural changes are required  
- It **requires batch mode** when chunk sizes exceed safe limits

---

## **Modes of Operation**
`modify_dev_dct.py` has two modes:

### **1. Normal Mode (default)**
Used for small, local edits:
- Add entries  
- Modify entries  
- Delete entries  

Normal mode:
- Loads the **highest manifest revision** in the target directory  
- Applies edits locally  
- Writes new chunk files  
- Writes a new manifest revision  
- Enforces chunk size limits (2.5–3.0 MB)

If any chunk exceeds the limit, normal mode **stops** and instructs the user to run batch mode.

---

### **2. Batch Mode (`--batch`)**
Used when chunk sizes exceed the limit and the dictionary must be **re‑chunked**.

Batch mode:
- Requires the user to **manually increase `CHUNK_COUNT`** in `config.py`  
- Loads all entries from all chunks  
- Recomputes WDP (Word Density Profile)  
- Re-chunks the entire dictionary  
- Writes a new full set of chunk files  
- Writes a new manifest revision  

Batch mode is the only mode that changes dictionary geometry.

---

## **Directory Structure**
By default, the tool operates in:

```
dictionaries_dev/
```

Users may override this:

```
python modify_dev_dct.py --dir path/to/other_directory
```

This allows users to:
- Work on older revisions  
- Maintain multiple dictionary branches  
- Avoid accidental edits to the main dictionary  

---

## **Manifest Discovery**
Inside the target directory:

1. If files matching `manifest_revNN.json` exist:
   - The **highest NN** is loaded  
2. Otherwise:
   - `manifest.json` is loaded

This ensures:
- The newest revision is always used  
- No accidental rollback  
- Full revision history is preserved  

---

## **Input File**
### **Default name**
```
modify_entries.json
```

### **Default location**
Same directory being edited:

```
dictionaries_dev/modify_entries.json
```

### **Override**
```
python modify_dev_dct.py --input my_changes.json
```

---

## **Input File Format**
The input file contains a list of operations.

### **Example**
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

## **Allowed Operations (How to Use Them)**

Each entry in `modify_entries.json` must specify an `"operation"` field.  
There are **three** allowed operations:

- `"add"` — insert a new dictionary entry  
- `"modify"` — replace an existing entry with a new version  
- `"delete"` — remove an entry by lemma  

### ✔ How to apply operations (examples)

```json
[
  {
    "operation": "add",
    "entry": {
      "lemma": "new concept",
      "gloss": "a description of the new concept",
      "primitive": "ENTITY",
      "cue_envelope": { ... },
      "invariant": { ... },
      "identity_anchor": { ... },
      "routing_signature": { ... }
    }
  },
  {
    "operation": "modify",
    "entry": {
      "lemma": "chieftaincy",
      "gloss": "updated gloss text",
      "primitive": "ENTITY",
      "cue_envelope": { ... },
      "invariant": { ... },
      "identity_anchor": { ... },
      "routing_signature": { ... }
    }
  },
  {
    "operation": "delete",
    "lemma": "chief petty officer"
  }
]
```

This example shows the **format**, not the content.  
Users can add, modify, or delete entries using this structure.

---

## **Required Fields (What This Refers To)**

This section refers to the **required fields inside each dictionary entry**, *not* the command‑line options or the modify_dev_dct.py program itself.

These fields are required because they define a **complete TS developer dictionary entry**.

### ✔ Required fields for `"add"` and `"modify"` operations

These operations must supply a **full TS entry**, containing:

- `lemma`  
- `gloss`  
- `primitive`  
- `cue_envelope`  
- `invariant`  
- `identity_anchor`  
- `routing_signature`

These are the same fields present in your developer dictionary chunks.

### ✔ Required fields for `"delete"` operations

Only:

- `lemma`

is required.

The tool uses the lemma to locate and remove the entry.

---

## **What manifest_revNN.json Contains**

Every time modify_dev_dct.py runs (normal or batch mode), it produces a new manifest:

```
manifest_revNN.json
```

This file contains **all the same information as the original manifest.json**, plus any updated metadata resulting from edits.

### ✔ Contents of manifest_revNN.json

Each manifest revision includes:

- `total_entries` — total number of entries across all chunks  
- `chunks` — a list of chunk metadata objects  

Each chunk object contains:

- `chunk_id` — integer chunk number  
- `filename` — name of the chunk file  
- `first_lemma` — lexicographically first lemma in the chunk  
- `last_lemma` — lexicographically last lemma in the chunk  
- `entry_count` — number of entries in the chunk  
- `uncompressed_size` — size in bytes before gzip  
- `compressed_size` — size in bytes after gzip  

### ✔ Example chunk entry in manifest_revNN.json

```json
{
  "chunk_id": 3,
  "filename": "meaning_dictionary_dev_rev05_03.json.gz",
  "first_lemma": "fastidious",
  "last_lemma": "labanotation",
  "entry_count": 19551,
  "uncompressed_size": 11796337,
  "compressed_size": 1968803
}
```

### ✔ Why manifest_revNN.json exists

- It preserves revision history  
- It prevents accidental overwrites  
- It allows rollback  
- It allows users to work from older revisions by pointing to a different directory  
- It ensures modify_dev_dct.py always uses the **latest** revision unless told otherwise  

---

## **Validation Rules**
Before applying any mutation, the tool validates:

- Required fields present  
- Correct types  
- No illegal characters  
- Lists contain valid elements  
- Primitive is valid  
- Identity anchor vector is valid  
- Routing signature codes are valid  
- No malformed structures  

Invalid entries are **skipped** with detailed log messages.

---

## **Chunk Selection**
Given a lemma:

1. Read manifest  
2. Identify the chunk whose range satisfies:  
   ```
   first_lemma <= lemma <= last_lemma
   ```
3. If lemma falls outside all ranges:
   - Determine correct chunk by lexicographic position  
   - Insert into that chunk  
   - Update boundaries  

Chunk numbering **never changes** in normal mode.

---

## **Mutation Behavior**

### **Add**
- Determine correct chunk  
- Load chunk  
- Insert entry in sorted order  
- Update metadata  
- Write new chunk file  
- Update manifest  

### **Modify**
- Load chunk  
- Replace entry  
- Re-sort  
- Update metadata  
- Write new chunk file  
- Update manifest  

### **Delete**
- Load chunk  
- Remove entry  
- Re-sort  
- Update metadata  
- Write new chunk file  
- Update manifest  

---

## **Chunk Size Enforcement**
After all edits:

- Compute uncompressed size of each chunk  
- If **any chunk > 2.5–3.0 MB**:

### **Normal mode stops**  
Message:

```
Chunk 3 exceeds 2.5 MB limit (actual: 3.12 MB).
Normal mode cannot continue.

Please increase CHUNK_COUNT in config.py from X to X+1.
Then run:

    python modify_dev_dct.py --batch
```

This forces a conscious user decision.

### **Batch mode proceeds**  
Batch mode is allowed to exceed limits temporarily because it will re-chunk.

---

## **Batch Mode Workflow**
Triggered by:

```
python modify_dev_dct.py --batch
```

Batch mode:

1. Loads highest manifest revision  
2. Reads `config.py`  
3. Confirms `CHUNK_COUNT` was manually increased  
4. Loads all entries from all chunks  
5. Recomputes WDP  
6. Re-chunks dictionary into `CHUNK_COUNT` chunks  
7. Writes new chunk files  
8. Writes new manifest revision  
9. Prints summary  

Batch mode is the **only** mode that changes dictionary geometry.

---

## **Manifest Revisioning**
Every run (normal or batch) produces:

```
manifest_revNN.json
```

Where NN = highest existing revision + 1.

Old manifests are **never overwritten**.

This preserves:
- full revision history  
- rollback capability  
- auditability  

---

## **Summary Log Report**
Normal mode reports:

- Entries added  
- Entries modified  
- Entries deleted  
- Entries skipped (with reasons)  
- Updated chunk boundaries  
- Updated entry counts  
- Updated total_entries  
- Chunk sizes  
- Whether batch mode is required  

Batch mode reports:

- Old chunk count  
- New chunk count  
- Total entries  
- New boundaries  
- New sizes  
- Confirmation message  

---

## **Compatibility**
This design ensures **all existing tools continue to work unchanged**, including:

- `inspect_chunk.py`  
- `ts_meaning_dct_path_a.py`  
- any other dictionary utilities  

No structural changes are required.

---
