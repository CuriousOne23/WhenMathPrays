# **PathA Short Simulation — README**

This directory is the Path A short simulator. A new person, or a new AI session, should use this page as the door. It does not carry the whole account. It points to the pages that do.

## Onboarding

Read these in order. Do not start from the reference lists further down.

1. [notes/program/README.md](notes/program/README.md) — present status, what has been done, what is not done.
2. [notes/program/grammar_and_structure.md](notes/program/grammar_and_structure.md) and [notes/program/four_writers.md](notes/program/four_writers.md) — how to think. The cut is pieces, place, fit, and residue. Ordinary grammar is not the repair.
3. [notes/program/claim_ledger.md](notes/program/claim_ledger.md) — what prints now.
4. [notes/program/s2m_structure/result.md](notes/program/s2m_structure/result.md) and [notes/program/known_words.md](notes/program/known_words.md) — the connection record, the open holes, and words that are not invented.
5. [notes/program/packet_sync/README.md](notes/program/packet_sync/README.md) — teaching names against `tp.idob`. Present fields and absent fields. Not \(M\).

Current face: SOB, SROB, CnOB, and SmOB write the structure floor. IdOB sums that floor into `idob_packet`, a teaching view over `tp.idob`. The requirement fields for six IDs, rank, \(M\), CIE, and `meaning_delta_h` are absent, not zero. A readable claim and a connection record are written from that packet. They do not compute \(M\). RBU, RB, TR, RTU, and CTP are mechanical routing beside the floor, not the parent of SOB.

Force ops such as polar, command, request, and exclamative are open holes. They are not object connections. History, likelihood, and the geometry conjecture are not inputs.

## Simulation directories

- `desks/` — SOB, SROB, CnOB, SmOB.
- `idob/` — sum, packet, claim, and connection record.
- `support/` — YAML cards, schemas, relation list, replays.
- `notes/program/` — status and onboarding pages.
- `architecture/` — names and the packet contract. Reference, not the first reading.

Run checks from [user_guide.md](user_guide.md). The claim check is `PYTHONPATH=. python3 support/tools/claim_ledger_replay.py`.

## References

The lists below are references. They are not a second onboarding.

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

The list below is a later machine. It is not the ready line. Structure-to-Meaning waits on [notes/program/ready_line.md](notes/program/ready_line.md). This pass does not implement it.


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

Structure theory (why the cut exists; read before an architectural change): [debug/pathA_structure_theory.md](debug/pathA_structure_theory.md).

IdOB teaching card (packet, dict `semantic_core`): [debug/primitives/IdOB.md](debug/primitives/IdOB.md).

# **10. Related Documents**

- Coverage map (printed, hole, shut):  
  [notes/pathA_coverage.md](notes/pathA_coverage.md)

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
|   |-- pathA_structure_theory.md
|   |-- dimensions/
|   |-- fields/
|   |-- primitives/
|   |   `-- IdOB.md
|   `-- setup/
|
|-- notes/
|   |-- pathA_coverage.md
|   |-- bench_walk/00_how_to_walk.md
|   |-- idob_object_space/idob_object_space.md
|   |-- pathA_supported_sentences.md
|   |-- pathA_relational_geometry.md
|   `-- pathA_routing_to_meaning.md
|
`-- user_guide.md
```
