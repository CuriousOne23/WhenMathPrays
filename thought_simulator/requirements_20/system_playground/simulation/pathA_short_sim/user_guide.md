# PathA Short Simulation — User Guide  
This guide explains how to run the short Path‑A simulator, how to interpret its output, and how the architecture works — including the roles of all Python, YAML, and JSON files involved in the simulation.

---

## 1. Run the Simulator  
Run the examples script from this directory:  
```
python run_examples.py
```

Or log output:  
```
python run_examples.py > run.log
```  
As noted in the original guide, this script runs a set of supported sentences.
See [pathA_supported_sentences.md](notes/pathA_supported_sentences.md) to see current sentences run_examples.py supports.

---

## 2. Modify the Input Raw Sentence  
Open `run_examples.py` and change the raw input sentence passed into `run_pathA_short(...)`, then rerun the script.

---

## 3. Interpret the Final TP  
The final TP is the end‑state substrate after all primitives run.  
Focus on the following fields (unchanged from your original guide):

- **tokens**, **normalized_text** — intake  
- **struct_segments**, **segment_tokens** — segmentation  
- **struct_roles**, **role_segments** — role assignment  
- **constraints_matched**, **constraints_unmatched**, **constraint_residue** — constraint matching  
- **smoothing_operations**, **semantic_adjacent_cues**, **basin_residue** — smoothing  
- **routing_metadata**, **routing_decision** — routing  
- **semantic_core** — semantic extraction  
- **commit_flags** — macro completion checkpoints  

---

## 4. Interpret the Trace Output  
Each trace item includes:

- **primitive** — name executed  
- **input** — TP snapshot before primitive  
- **output** — TP snapshot after primitive  
- **notes** — human‑readable observation  

Read input/output deltas to see exactly what each primitive changed.

---

## 5. Follow TP Evolution Macro‑by‑Macro  
Macro order:

### Intake  
`InB`, `IIInB`, `IE`

### Correction  
`CEx`, `CE`, `ISc`, `TPU`

### Structural Geometry (OB‑Set)  
`SOB`, `SROB`, `CnOB`, `SmOB`, `SSG`

### Routing  
`RBU`, `RB`, `TR`, `TRU`, `RTU`, `CTP`

### Semantic  
`IdOB`

### Final Commit  
`OuBA`

---

## 6. Debug Odd Outputs  
Your original debugging guidance remains correct:

- Confirm token normalization in **IE**  
- Verify YAML dictionaries contain expected entries  
- Check **SOB** segment alignment  
- Check **SROB** role progression  
- Confirm **CnOB** transition pairs in `constraint_rules.yaml`  
- Confirm **IdOB** semantic rules match segment/role traces  

---

## 7. Modify Dictionaries  
Edit files under `support/dictionaries`:

- `token_classes.yaml`  
- `segment_patterns.yaml`  
- `role_patterns.yaml`  
- `constraint_rules.yaml`  
- `semantic_rules.yaml`  

Then rerun `run_examples.py` and compare trace deltas.

---

## 8. Extend Primitives  
Edit `primitives_pathA_short.py` to add or refine primitive logic.

Keep mutations explicit and trace‑visible.

---

# 9. Architecture Overview — How the Short Path‑A Simulator Works

This section explains **exactly how the simulator loads and uses all Python, YAML, and JSON files**.  
This corrects the common confusion that arises because neither `run_examples.py` nor `pathA_short_simulator.py` ever reference YAML or JSON directly.

---

## 9.1 Top‑Level Python Files and Their Responsibilities

### **`run_examples.py`**  
**Role:** Entry point / driver  
- Defines example sentences  
- Calls `run_pathA_short`  
- Prints or logs the trace  
- Does **not** load YAML or JSON  
- Does **not** mutate TP  
- Purely a convenience wrapper

---

### **`pathA_short_simulator.py`**  
**Role:** Macro sequencer  
- Imports all primitives  
- Imports TP substrate  
- Defines macro order (`PRIMITIVES`)  
- Runs each primitive in sequence  
- Captures input/output snapshots  
- Adds human‑readable notes  
- Does **not** load YAML or JSON  
- Does **not** define primitive logic  

This file is intentionally minimal and declarative.

---

### **`tp_substrate.py`**  
**Role:** Defines the TP object  
- TP fields  
- Initialization (`init_tp`)  
- Cloning (`clone_tp`)  
- Bridge trace structures  
- Default values  
- No YAML/JSON loading  
- No primitive logic  

This file defines the substrate that primitives mutate.

---

### **`primitives_pathA_short.py`**  
**Role:** The engine  
This is where the real work happens.

This file contains:

- All primitive implementations  
- All imports of rule files  
- All imports of dictionary files  
- All imports of JSON schemas  
- All imports of prototypes  

This is the file that indirectly loads:

- YAML dictionaries  
- JSON schemas  
- prototype definitions  

When Python imports this file, all rule files are loaded **before any primitive runs**.

---

## 9.2 Support Files — YAML, JSON, and Prototypes

The following files live under `support/` and are loaded by modules imported inside `primitives_pathA_short.py`.

### **YAML Dictionaries**  
Used by segmentation, role assignment, constraints, and semantics:

- `segment_patterns.yaml`  
- `role_patterns.yaml`  
- `constraint_rules.yaml`  
- `semantic_rules.yaml`  
- `token_classes.yaml`

These define the rule tables used by:

- SOB  
- SROB  
- CnOB  
- SmOB  
- IdOB  

---

### **JSON Schemas**  
Used for validating TP structures:

- `committed_token_stream.v1.schema.json`

This ensures deterministic structure across Python and C++.

---

### **Prototype Modules**  
Define structural and mutation templates used by primitives:

- intake prototypes  
- OB‑Set prototypes  
- routing prototypes  
- semantic prototypes  

These ensure deterministic replay and cross‑language consistency.

---

## 9.3 Execution Flow (Full Pipeline)

```
run_examples.py
    ↓
pathA_short_simulator.py
    ↓
tp_substrate.py
    ↓
primitives_pathA_short.py
    ↓
support/yaml/*.yaml
support/contracts/*.json
support/dictionaries/*.yaml
support/prototypes/*.py
    ↓
Primitive sequence (InB → … → OuBA)
    ↓
Final TP + full trace
```

This is the complete architecture.

---

# 10. Summary — What Each File Does

| File | Purpose |
|------|---------|
| `run_examples.py` | Runs examples; prints trace; no rule loading |
| `pathA_short_simulator.py` | Macro sequencer; runs primitives; records trace |
| `tp_substrate.py` | Defines TP structure; initialization; cloning |
| `primitives_pathA_short.py` | Implements primitives; loads YAML/JSON/prototypes |
| `support/yaml/*.yaml` | Segmentation, roles, constraints, semantics |
| `support/dictionaries/*.yaml` | Token classes and dictionary rules |
| `support/contracts/*.json` | JSON schemas for TP validation |
| `support/prototypes/*.py` | Structural and mutation prototypes |

---
