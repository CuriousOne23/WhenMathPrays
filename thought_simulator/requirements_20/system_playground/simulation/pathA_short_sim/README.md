# **PathA Short Simulation — README**

This directory contains the **Path‑A Short Simulator**, a lightweight, dictionary‑driven Thought Simulator (TS).  
Its purpose is **educational**: provide an architectural feel for major Path‑A blocks, show Thought Packet (TP) evolution across primitives, and demonstrate how segmentation, structural labels, constraints, adjacent-cue handling, packet assembly, and truth‑relations interact.

The simulator is intentionally small, inspectable, and modifiable.

Start here for Identity Observation Block (IdOB) names and the walk from ordinary talk into Path‑A language:

- [notes/bench_walk/00_how_to_walk.md](notes/bench_walk/00_how_to_walk.md) — new-reader track: false image, stamp card, empty hook, shut S2M door  
- [architecture/idob_seam.md](architecture/idob_seam.md) — names, adjacency, do-not-mix table  
- [user_guide.md](user_guide.md) — run two utterances; structure vs packet  
- [notes/idob_object_space/idob_object_space.md](notes/idob_object_space/idob_object_space.md) — eight catalog families  
- [architecture/IdOB_unified_plan.md](architecture/IdOB_unified_plan.md) — meaning on this path is the `idob_packet`
- [architecture/path_a_realization_charter.md](architecture/path_a_realization_charter.md) — lineup vs reserved 20.40 capability
- [architecture/idob_meaning_lock.md](architecture/idob_meaning_lock.md) — packet contract

Official expansions (20.700.010): Structural Observation Block (SOB), Structural Refinement Observation Block (SROB), Constraint Observation Block (CnOB), Semantic Observation Block (SmOB), Identity Observation Block (IdOB). Short-sim field names are teaching aliases. 20.40 remains richer; realized functions are listed in each prim’s Path-A-short section.

---

# **1. What the Simulator Does**

The Path‑A short simulator supports **five full sentence families**, each implemented across the entire pipeline (SOB → SROB → CnOB → SmOB → IdOB → TRU):

### **Supported Families**
1. **Copular / State Descriptive**  
2. **Locative Descriptive**  
3. **Mixed Descriptive**  
4. **Interrogative (WH + yes/no)**  
5. **Mixed Interrogative (nested descriptive + interrogative scope)**

These families are defined in detail in  
**`notes/pathA_supported_sentences.md`**  
and are exercised in  
**`run_examples.py`**.

The simulator produces:

- segmentation (`struct_segments`)  
- structural labels (`struct_roles`)  
- constraint matching (`constraints_matched`)  
- adjacent cues (`semantic_adjacent_cues`)  
- IdOB packet (`idob_packet`, dict `semantic_core`)  
- truth‑relation (`truth_relation`)  

This gives users a complete view of Path‑A’s factored structure plus the IdOB sum.

---

# **2. How to Run the Simulator**

See the **User Guide**:

[user_guide.md](user_guide.md)

It explains:

- how to run `run_examples.py`  
- how to add your own sentences  
- how to inspect TP evolution as two columns (OB-set vs packet)

---

# **3. Short Simulator Macro Categories**

These are the primitives implemented in the toy simulator:

- **Intake Macro:** InB, IIInB, IE  
- **Correction Macro:** CEx, CE, ISc, TPU  
- **Structural Geometry Macro (OB‑Set):** SOB, SROB, CnOB, SmOB, SSG  
- **Routing Macro:** RBU, RB, TRU (truth‑relation stub), RTU, CTP  
- **Semantic Macro:** IdOB  
- **Final Commit Macro:** OuBA  

These correspond to the real Path‑A architecture but simplified for clarity.

---

# **4. Full Path‑A Macro Categories (20.705 §2)**

For reference, the full Path‑A system contains:

- Intake Macro  
- Correction Macro  
- Structural Interpretation Macro (OB‑Set)  
- Routing Macro (STPX, DCB, TR)  
- Identity & Meaning Macro (IdOB → MCB)  
- Truth‑Relation Macro (TRU)  
- Final Commit Macro (OuBA)

The short simulator implements a **subset** of these with simplified behavior. Meaning Composition Block (MCB) is omitted.

---

# **5. Mapping: Real Path‑A → Toy Simulator**

| Full Path‑A Macro | Real Primitive(s) | Toy Primitive(s) | Status in Toy |
|-------------------|-------------------|------------------|---------------|
| Intake | InB, IIInB, IE | InB, IIInB, IE | Implemented |
| Correction | CEx, CE, ISc, TPU | CEx, CE, ISc, TPU | Implemented (simplified) |
| Structural Interpretation (OB‑Set) | SOB, SROB, CnOB, SmOB, SSG | SOB, SROB, CnOB, SmOB, SSG | Implemented (dictionary‑driven) |
| Routing | RBU, RB, STPX, DCB, TR | RBU, RB, TR, RTU, CTP | Partial: TR placeholder; STPX/DCB omitted |
| Identity & Meaning | IdOB, MCB | IdOB | Partial: MCB omitted |
| Truth‑Relation | TRU | TRU | Implemented (stub → extended for supported families) |
| Final Commit | OuBA | OuBA | Implemented |

---

# **6. What Path‑A Short Simulator Supports (Summary)**

This section gives a new user a quick overview of the simulator’s capabilities.

### **Copular / State Descriptive**
- *The sky is blue.*  
- *Paris is a city.*

### **Locative Descriptive**
- *The book is on the table.*  
- *The rain stays in the plain.*

### **Mixed Descriptive**
- *The rain in Spain stays mainly in the plain.*

### **Interrogative (WH + yes/no)**
- *Where is the book?*  
- *Is the book on the table?*  
- *Why is the sky blue?*

### **Mixed Interrogative**
- *Why does the rain in Spain stay mainly in the plain?*  
- *Where is the book that is on the table?*  
- *Why is the sky that is blue bright?*

Full details and canonical TP traces are in:  
[pathA_supported_sentences.md](notes/pathA_supported_sentences.md)

---

# **7. Future Extension Plan**

1. Implement STPX and DCB for richer routing behavior.  
2. Replace TR placeholder with full Thought Router logic.  
3. Add MCB after IdOB for deeper identity/meaning composition (copy-only seam first).  
4. Expand correction logic with scored candidates and provenance.  
5. Extend OB‑Set outputs into explicit structural graph objects.  
6. Add richer truth‑relation logic referencing provenance and semantic cues.

IdOB coverage and resolution rungs (stamp card, not S2M): [notes/bench_walk/10_extend.md](notes/bench_walk/10_extend.md).

---

# **8. What This Simulator Does NOT Do**

- No STPX, DCB, or MCB.  
- TR is simplified (not full Thought Router).  
- No full provenance chains.  
- No structural graph objects (list‑based only).  
- No routing entropy or confidence metrics.  
- No cross‑sentence memory or latent priors.  
- Not all production Path‑A constraints are implemented.  
- No Structure-to-Meaning (S2M) $M$-vector, no Cognitive Identity Envelope (CIE), no Meaning Signal Layer (MSL) inside IdOB.

---

# **9. Debugger, Training and Teaching Tool**

A debugger, training and teaching tool executable pathA_dbug.py has been provided, which will operate on the output of run_examples.py, in the example below this will be run.log file:

```
python run_examples.py > run.log
```

For more information see debug directory [README.md](debug/README.md).

IdOB teaching card (packet, dict `semantic_core`): [debug/primitives/IdOB.md](debug/primitives/IdOB.md).

# **10. Related Documents**

- Bench walk (new reader, false image to shut door):  
  [notes/bench_walk/00_how_to_walk.md](notes/bench_walk/00_how_to_walk.md)

- IdOB seam (start here for names):  
  [architecture/idob_seam.md](architecture/idob_seam.md)

- Realization charter (lineup vs reserved 20.40):  
  [architecture/path_a_realization_charter.md](architecture/path_a_realization_charter.md)

- Meaning-as-packet lock:  
  [architecture/idob_meaning_lock.md](architecture/idob_meaning_lock.md)

- IdOB object space (eight families):  
  [notes/idob_object_space/idob_object_space.md](notes/idob_object_space/idob_object_space.md)

- IdOB meaning contract / gates:  
  [architecture/IdOB_unified_plan.md](architecture/IdOB_unified_plan.md)

- Architectural simulation details:  
  [support/docs/architectural_simulation.md](support/docs/architectural_simulation.md)

- Dictionary reference and schema:  
  [support/docs/dictionaries_reference.md](support/docs/dictionaries_reference.md)

- Core theory of Path‑A relational geometry:  
  [notes/pathA_relational_geometry.md](notes/pathA_relational_geometry.md)

- Routing ladder snapshot:  
  [notes/pathA_routing_to_meaning.md](notes/pathA_routing_to_meaning.md)

- Supported sentence families and examples:  
  [notes/pathA_supported_sentences.md](notes/pathA_supported_sentences.md)

- Conceptual notes on AI and humanity:  
  [notes/The_Human_Self_in_the_AI_Age.md](notes/The_Human_Self_in_the_AI_Age.md)

---

# **11. Directory Structure (for new users)**

Desk modules live in `desks/`: `segments.py` for Structural Observation Block, `roles.py` for Structural Refinement, `constraints.py` for Constraint Observation Block, and `smoothing.py` for Semantic-adjacent Smoothing. `primitives_pathA_short.py` remains the caller that the runner imports. Intake and the IdOB call stay in that caller.

```
pathA_short_sim/
|
|-- run_examples.py
|-- pathA_short_simulator.py
|-- primitives_pathA_short.py
|-- tp_substrate.py
|-- pathA_dbug.py
|
|-- architecture/
|   |-- idob_seam.md
|   |-- idob_meaning_lock.md
|   |-- path_a_realization_charter.md
|   `-- IdOB_unified_plan.md
|
|-- support/
|   |-- dictionaries/
|   |-- idob_objects/
|   |-- idob_schemas/
|   `-- docs/
|
|-- idob/
|   |-- sum.py
|   |-- packets.py
|   |-- registry.py
|   `-- ...
|
|-- debug/
|   |-- README.md
|   |-- dimensions/
|   |-- fields/
|   |-- primitives/
|   |   `-- IdOB.md
|   `-- setup/
|
|-- notes/
|   |-- bench_walk/00_how_to_walk.md
|   |-- idob_object_space/idob_object_space.md
|   |-- pathA_supported_sentences.md
|   |-- pathA_relational_geometry.md
|   `-- pathA_routing_to_meaning.md
|
`-- user_guide.md
```
