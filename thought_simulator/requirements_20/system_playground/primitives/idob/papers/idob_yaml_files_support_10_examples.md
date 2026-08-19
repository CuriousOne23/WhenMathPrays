# **idob_yaml_files_support_10_examples.md**  
### *How the IdOB Example YAML Files Fit Into the Semantic Universe and Path‑A Software Realization*

---

# **1. Purpose of This Document**

This paper explains:

- **how the 10 IdOB example YAML files are structured**,  
- **why they must conform to the generic IdOB schema**,  
- **how they relate to the Semantic Universe**,  
- **how idob.py consumes them**,  
- **how TS and MCB use them**,  
- **and which supporting YAML/MD files will expand or multiply** as Path‑A gains capability.

This document is the **index** for the IdOB example YAML files.  
It does **not** contain the examples themselves — each example is stored in its own YAML file.

---

# **2. Why the Examples Must Use the Generic YAML Structure**

The IdOB examples are not “free‑form.”  
They are **instantiations** of the Semantic Universe and IdOB schema.

This is required because:

### ✔ idob.py expects a **single, stable object schema**  
### ✔ TS expects a **single, stable TP metadata structure**  
### ✔ MCB expects a **single, stable stability structure**  
### ✔ Path‑A primitives expect **consistent meaning fields**  
### ✔ replay determinism requires **identical structure**  
### ✔ testbenches require **consistent YAML structure**  
### ✔ versioning requires **modular files**  

If the examples used custom formats, the entire system would break.

Therefore:

> **All IdOB example YAML files must conform to the generic structure defined in the Semantic Universe YAML files and idob_schema.yaml.**

---

# **3. The Generic YAML Structure (Semantic Universe Foundation)**

The following YAML files define the **machine‑readable meaning universe** that Path‑A and IdOB operate on.

These files are **global**, **shared**, and **generic**.

---

## **3.1 Dictionaries (Words → Concepts)**

These files define the vocabulary used to extract meaning from the world:

- `semantic_universe_dictionary.yaml`  
- `semantic_roles_dictionary.yaml`  
- `domain_concepts_dictionary.yaml`

These files will **expand** as Path‑A gains capability.

---

## **3.2 Fields (Concepts → Meaning Dimensions)**

Defines the top-level meaning dimensions:

- `semantic_field_definitions.yaml`

This file will **expand** as new meaning dimensions are added.

---

## **3.3 Subfields (Meaning Dimensions → Specific Signals)**

Defines the fine structure:

- `semantic_subfields.yaml`  
- `semantic_gradients.yaml`

These files will **expand** as fields gain finer structure.

---

## **3.4 Objects (Subfields → Structured Meaning Units)**

Defines the semantic objects:

- `semantic_objects.yaml`

Defines the IdOB object schema:

- `idob_schema.yaml`

These files will **expand** as new semantic objects are added.

---

# **4. The IdOB Example YAML Files**

Each example YAML file is:

- a **separate file**,  
- representing a **separate identity behavior class**,  
- but using the **same generic structure**.

The correct filenames are:

```
idob_example_01_identity_formation.yaml
idob_example_02_identity_refinement.yaml
idob_example_03_identity_correction.yaml
idob_example_04_identity_drift.yaml
idob_example_05_identity_conflict.yaml
idob_example_06_identity_bifurcation.yaml
idob_example_07_identity_stabilization.yaml
idob_example_08_identity_convergence.yaml
idob_example_09_identity_alignment.yaml
idob_example_10_identity_closure.yaml
```

Each file contains:

### ✔ TP metadata input  
(using dictionaries, fields, subfields, gradients)

### ✔ IdOB object output  
(using `idob_schema.yaml`)

### ✔ Identity behavior class  
(one of the 10)

### ✔ Stability state  
(using `idob_stability_contract.md`)

### ✔ Continuity state  
(using semantic_subfields.yaml)

### ✔ Pressure state  
(using semantic_gradients.yaml)

### ✔ Residual pattern  
(using semantic_objects.yaml)

### ✔ Freeze state  
(using semantic_objects.yaml)

### ✔ Basin/surface state  
(using semantic_field_definitions.yaml)

This is the **correct software‑realization structure**.

---

# **5. Why Separate Files Are Required**

Separate YAML files are required because:

### ✔ Each example is a separate identity behavior class  
### ✔ Each example is a separate testbench unit  
### ✔ Each example is a separate stability unit  
### ✔ Each example is a separate replay determinism unit  
### ✔ Each example is a separate versioning unit  

But all examples must use the **same structure**.

This is how real semantic engines maintain:

- determinism  
- stability  
- replay safety  
- primitive interoperability  
- testbench consistency  
- metadata consistency  

---

# **6. How idob.py Uses These Files**

idob.py:

1. **Loads the example YAML file**  
2. **Validates it against idob_schema.yaml**  
3. **Reads TP metadata**  
4. **Runs IdOB logic**  
5. **Produces deterministic IdOB output**  
6. **Hands output to MCB**  
7. **MCB evaluates stability**  
8. **TS decides whether IdOB runs again**

This is why the structure must be identical across all examples.

---

# **7. How TS Uses These Files**

TS uses the example YAML files to:

- validate TP metadata structure  
- validate IdOB input/output consistency  
- validate identity behavior correctness  
- validate routing correctness  
- validate continuity correctness  
- validate pressure correctness  
- validate stability correctness  

TS testbenches consume these files **directly**.

---

# **8. How MCB Uses These Files**

MCB uses the example YAML files to:

- evaluate stability  
- detect escalation  
- detect termination  
- detect bifurcation  
- detect merging  
- detect closure  

MCB must see **the same fields** in every example.

---

# **9. Which Files Will Expand as Path‑A Gains Capability**

These files will **grow in size**:

- `semantic_universe_dictionary.yaml`  
- `domain_concepts_dictionary.yaml`  
- `semantic_field_definitions.yaml`  
- `semantic_subfields.yaml`  
- `semantic_gradients.yaml`  
- `semantic_objects.yaml`  
- `semantic_operators.md`  
- `semantic_universe_to_tp_mapping.md`  
- `idob_preconditions_contract.md`  
- `idob_stability_contract.md`  
- `world_to_ts_process.md`  

These files grow **in size**, not in number.

---

# **10. Which Files Will Increase in Number as Path‑A Gains Capability**

These files will **multiply**:

### ✔ Example YAML files  
More identity behavior examples → more YAML files.

### ✔ Testbench YAML files  
More test cases → more YAML files.

### ✔ Category-specific example sets  
More drift/conflict/bifurcation examples → more YAML files.

### ✔ Domain-specific example sets (optional)  
If you add domain-specific identity examples → more YAML files.

These files grow **in number**, not in size.

---

# **11. Estimated Size of an Effective Prework Universe**

To match or exceed **normal human meaning capability**, the prework must be:

### **Estimated total size: 4 MB – 8 MB**

Breakdown:

- dictionaries: 1–3 MB  
- fields/subfields: 0.5–1 MB  
- objects: 0.5–1 MB  
- semantics: 0.5–1 MB  
- preconditions: 0.3–0.6 MB  
- process docs: 0.3–0.6 MB  
- examples/testbench: 0.3–0.6 MB  

This is **tractable**, **finite**, **maintainable**, and **sufficient for human-level meaning interpretation**.

---

# **12. Summary**

This paper explains:

- how the 10 IdOB example YAML files fit into the Semantic Universe  
- why they must use the generic IdOB structure  
- how idob.py consumes them  
- how TS and MCB use them  
- which files expand vs multiply  
- how this architecture scales  
- how this supports software realization  

This document is the **index** for the IdOB example YAML files.

The next step is to create the actual YAML files.

---
