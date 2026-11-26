# **PathA Short Simulation — README**

This directory is the Path A short simulator. A new person, or a new AI session, should use this page as the door. It does not carry the whole account. It points to the pages that do.

## Onboarding

Read these in order. Do not start from the reference lists further down.

1. [notes/program/status.md](notes/program/status.md) — current goal (category selection), historical S2M seed, what is implemented, and what is absent.
2. [notes/program/grammar_and_structure.md](notes/program/grammar_and_structure.md) and [notes/program/four_writers.md](notes/program/four_writers.md) — how to think. The cut is pieces, place, fit, and residue. Ordinary grammar is not the repair.
3. [notes/program/claim_ledger.md](notes/program/claim_ledger.md) — what prints now.
4. [notes/program/s2m_structure/result.md](notes/program/s2m_structure/result.md) and [notes/program/known_words.md](notes/program/known_words.md) — the connection record, the open holes, and words that are not invented.
5. [notes/program/packet_sync/README.md](notes/program/packet_sync/README.md) — teaching names against `tp.idob`. Present fields and absent fields. Not \(M\).
6. [notes/program/coverage_map.md](notes/program/coverage_map.md) — conversational coverage roadmap. History is on the map and out of the sim.
7. [notes/program/s2m_relational_proposal.md](notes/program/s2m_relational_proposal.md) — emerging S2M relational mapping proposal (seed, categories, plasticity, audit). Independent of current requirements definitions. Research proposal (non-normative); not the current goal. Its working formulation of meaning is a research hypothesis, refined by the research-only [notes/program/s2m_idob_traversal_proposal.md](notes/program/s2m_idob_traversal_proposal.md).
8. [notes/program/category_selection_proposal.md](notes/program/category_selection_proposal.md) — next realization proposal (sentence-internal or prior-CEx category choice).

Current face: SOB, SROB, CnOB, and SmOB write the structure floor. IdOB sums that floor and writes the teaching packet into `tp.idob`. `idob_packet` is that same sum (teaching name). Crossing fields (six structure IDs, rank, \(M\), CIE, `meaning_delta_h`) are not present on the packet written by IdOB; they are absent, not zero. A constructable shell view that copies the sum and sets those fields explicitly to null is available via `idob/crossing.py` (`crossing_from_packet`). It is not what the main simulator writes into `tp.idob`. The narrow S2M record is connections and holes, not \(M\). Both are accounted on the status page. A readable claim and a connection record are written from that packet. They do not compute \(M\). RBU, RB, TR, RTU, and CTP are mechanical routing beside the floor, not the parent of SOB.

Force ops such as polar, command, request, and exclamative are open holes. They are not object connections. History, likelihood, and the geometry conjecture are not inputs.

## Document indexes under notes/program

Use these navigation indexes to find the right family. They do not duplicate content; they route questions. The family indexes also register the corresponding characterization and experimentation programs. Operator how-to for `run_examples.py` stays in [user_guide.md](user_guide.md). The indexes do not set the goal. The current goal, per [notes/program/status.md](notes/program/status.md), is "Controlled category selection (sentence-internal cue or prior-CEx cue) so a non-default category can be chosen without mutating the floor." Each family below is labelled current goal family, research, active research, or sibling program; the narrow S2M seed is historical / accomplished.

- [notes/program/category_selection_index.md](notes/program/category_selection_index.md) — Category Selection document family (characterization, qualification, palette, observations, program closeout). Cue-source and empirical records for category evidence. **Current goal family** (category selection; see status.md). The present characterization cycle is closed at its characterized boundary ([program closeout](notes/program/category_selection_characterization_program_closeout.md)).
- [notes/program/s2m_index.md](notes/program/s2m_index.md) — S2M document family (relational proposal and IdOB traversal proposal). Owns the mechanical chain from structure through legal candidates, correspondence, and directional discrimination. **Research (non-normative); not the current goal.** The narrow S2M seed is historical / accomplished; the current IdOB traversal characterization cycle is closed at its present-realization boundary ([closeout](notes/program/s2m_idob_traversal_characterization_closeout.md)).
- [notes/program/idob_relational_space_localization_index.md](notes/program/idob_relational_space_localization_index.md) — IdOB relational-space localization — bounded research into whether a replaceable organizational/index layer over stable IdOB relational identities can help Path A identify a tractable active relational surface without treating organizational selection as meaning. Gate A / Phase 3 has been executed with bounded fixture-relative and oracle-relative classification CONTINUE; Gate B design is frozen; Gate B execution is not performed and not authorized. **Active research (non-normative); not the current goal.** Use the track index for current status before any Gate B work.
- [notes/program/scalability/scalability_index.md](notes/program/scalability/scalability_index.md) — Scalability document family (expansion principles, user guide, decision states). **Sibling program; not the current goal.**

For IdOB traversal (research) questions open the S2M index. For IdOB relational-space localization (research) questions open the localization index. For Category Selection characterization questions open the Category Selection index.

## Expanding Path A

Expanding Path A? Start with the scalability program and user guide before treating new YAML/reference coverage as established behavior.

- [notes/program/scalability/scalability_program.md](notes/program/scalability/scalability_program.md) — governing principles, expansion definition, regression versus progression, decision states.
- [notes/program/scalability/scalability_user_guide.md](notes/program/scalability/scalability_user_guide.md) — practical operator guide for the accepted first bounded implementation, including `run_scalability.py`.
- [notes/program/scalability/scalability_index.md](notes/program/scalability/scalability_index.md) — navigation for the scalability document family, including the `scalability/` package and first-pass replay checks.

## S2M mapping (experimental; on main via PR #194/#197; historical)

S2M runs as two additive outputs attached by **IdOB**. Neither replaces the teaching packet. This is now historical / accomplished; the current goal is category selection (see status and the proposal above).

- **Enabled by default:**
  ```bash
  python run_examples.py
  ```
  IdOB writes the normal `tp.idob` packet, then attaches:
  - `tp.s2m_seed` (Part I accountability trail)
  - `tp.s2m_meaning` (Part II interpretive transfer)

  The runner prints labeled blocks:
  ```
  --- S2M Accountability (IdOB) ---
  s2m_seed: {
    "utterance": "...",
    "written_relations": [...],
    "null_relations": [...],
    "crossing_fields": {...},
    "active_context_stores": [],
    "selection_cues": [],
    "seed_complete": true
  }

  --- S2M Meaning (IdOB) ---
  s2m_meaning: {
    "default_meaning": {...},
    "candidate_interpretations": [...],
    "meaning_relations": [...],
    "active_space": [...],
    "active_context_stores": [],
    "cue_state": {
      "category_cue": [],
      "cue_active": false,
      "provenance": {}
    },
    "category_result": {},
    "story_id": "...",
    "extendable": true
  }
  ```

  With no selection cue (the seed currently writes `selection_cues: []`), `meaning_relations` and `active_space` are empty: the run reports `default_meaning` and lists `candidate_interpretations` without legitimizing them (`s2m/loop.py`, `s2m/legitimate.py`).

  With `--enable-category-selection` (default off), TPU copies the merged ISc category result into `tp.semantic.isc_category_result` (`primitives_pathA_short.py:657-672`). `s2m/loop.py:28-37` reads `category_cue` and `top_category` from it; a non-empty cue resolves `active_space` and lets `s2m/legitimate.py` legitimize only the licensed candidates that match the selected category. The cue is reported in `cue_state` and `category_result` of `s2m_meaning`; the seed's own `selection_cues` stays `[]` (`idob/experimental_seed.py:58-59`). A cue with no licensed candidate leaves `meaning_relations` empty and marks the candidate `refused`. Replay: `PYTHONPATH=. python3 support/tools/s2m_category_selection_replay.py`.

- **Disabled:**
  ```bash
  python run_examples.py --no-s2m-seed
  ```
  Both blocks are disabled and do not appear in the log. Existing floor and claim behavior is unchanged.

- **Other `run_examples.py` flags** (`run_examples.py:214-264`): `--no-category-observations` (skip the canonical S2M cases and the category-selection demos), `--enable-category-selection`, `--execution-case` (only `sky_blue`), and the characterization flags `--characterize`, `--char-type`, `--char-session-id`, `--char-run-index`, `--char-version`, `--char-params-json`, `--char-params-file`. Characterization mode is handled by the `characterization/` package (`dispatcher.py`, `artifacts.py`, `infra_smoke.py`); the only registered type is `infra_smoke`. Artifacts are written under `local_characterization/` (`characterization/artifacts.py:47-50`). Details are in the characterization notes under `notes/program/`, not on this page.

The primitive that performs the mapping is IdOB. Details and acceptance criteria: [notes/program/s2m_program_reference.md](notes/program/s2m_program_reference.md).

## Simulation directories

- `desks/` — SOB, SROB, CnOB, SmOB.
- `characterization/` — characterization run dispatcher, artifact writer, and the `infra_smoke` type (used only with `run_examples.py --characterize`).
- `idob/` — sum, packet, claim, and connection record.
- `characterization/` — Milestone-1 characterization library used by `run_examples.py --characterize`.
- `scalability/` — bounded Path A scalability analysis library used by `run_scalability.py`.
- `support/` — YAML cards, schemas, relation list, replays.
- `notes/program/` — status, onboarding pages, and document-family indexes.
- `architecture/` — names and the packet contract. Reference, not the first reading.

Run checks from [user_guide.md](user_guide.md). The claim check is `PYTHONPATH=. python3 support/tools/claim_ledger_replay.py`.

## References

The lists below are references. They are not a second onboarding.

Official expansions (20.700.010): Structural Observation Block (SOB), Structural Refinement Observation Block (SROB), Constraint Observation Block (CnOB), Semantic Observation Block (SmOB), Identity Observation Block (IdOB). Short-sim field names are teaching aliases. 20.40 remains richer; realized functions are listed in each prim’s Path-A-short section.

---

# **1. What the Simulator Does**

The Path‑A short simulator's original five sentence families are still listed below. The claim ledger and CSE also cover action, command, request, reporting, relative, and exclamative sentences. Implemented utterances run across this pipeline (InB → IIInB → IE → CEx → CE → ISc → TPU → SOB → SROB → CnOB → SmOB → SSG → RBU → RB → TR → TRU → RTU → CTP → IdOB → OuBA; `pathA_short_simulator.py:17-23`):

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

S2M mapping (experimental, now historical): enabled by default; disable with `--no-s2m-seed`. See the S2M mapping section above. The mapping is performed by IdOB.

Category-selection behavior on the selected execution case is opt-in (`--enable-category-selection`). Characterization mode (`--characterize`; Milestone-1 type `infra_smoke`) observes one TS execution and is documented in the User Guide. Bounded scalability analysis is a separate operator entry, `run_scalability.py`; see [notes/program/scalability/scalability_user_guide.md](notes/program/scalability/scalability_user_guide.md).

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

The short simulator implements a **subset** of these with simplified behavior. A copy-only MCB seam exists at `mcb/seam.py` (`copy_from_idob`); it copies the IdOB packet and does not compose new meaning. `run_examples.py` prints that seam after IdOB.

---

# **5. Mapping: Real Path‑A → Toy Simulator**

| Full Path‑A Macro | Real Primitive(s) | Toy Primitive(s) | Status in Toy |
|-------------------|-------------------|------------------|---------------|
| Intake | InB, IIInB, IE | InB, IIInB, IE | Implemented |
| Correction | CEx, CE, ISc, TPU | CEx, CE, ISc, TPU | Implemented (simplified) |
| Structural Interpretation (OB‑Set) | SOB, SROB, CnOB, SmOB, SSG | SOB, SROB, CnOB, SmOB, SSG | Implemented (dictionary‑driven) |
| Routing | RBU, RB, STPX, DCB, TR | RBU, RB, TR, RTU, CTP | Partial: TR placeholder; STPX/DCB omitted |
| Identity & Meaning | IdOB, MCB | IdOB, MCB (copy-only seam) | Partial: copy-only seam in `mcb/seam.py`; no composition |
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
3. Add deeper identity/meaning composition after the existing copy-only MCB seam (`mcb/seam.py`).  
4. Expand correction logic with scored candidates and provenance.  
5. Extend OB‑Set outputs into explicit structural graph objects.  
6. Add richer truth‑relation logic referencing provenance and semantic cues.

IdOB coverage and resolution rungs (stamp card, not S2M): [notes/bench_walk/10_extend.md](notes/bench_walk/10_extend.md).

Emerging relational S2M proposal (seed, categories, plasticity): [notes/program/s2m_relational_proposal.md](notes/program/s2m_relational_proposal.md).

Next realization proposal (category selection): [notes/program/category_selection_proposal.md](notes/program/category_selection_proposal.md).

---

# **8. What This Simulator Does NOT Do**

- No STPX or DCB. MCB is a copy-only seam (`mcb/seam.py`), not full composition.  
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

- IdOB object space (ten catalog cards; `agent_action` family is `agent_action`):  
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

- Emerging S2M relational proposal:  
  [notes/program/s2m_relational_proposal.md](notes/program/s2m_relational_proposal.md)

- S2M program reference (implementation contract):  
  [notes/program/s2m_program_reference.md](notes/program/s2m_program_reference.md)

- Category selection proposal (next realization):  
  [notes/program/category_selection_proposal.md](notes/program/category_selection_proposal.md)

- Category Selection index:  
  [notes/program/category_selection_index.md](notes/program/category_selection_index.md)

- S2M index:  
  [notes/program/s2m_index.md](notes/program/s2m_index.md)

- IdOB relational-space localization index (research):  
  [notes/program/idob_relational_space_localization_index.md](notes/program/idob_relational_space_localization_index.md)

- Scalability index:  
  [notes/program/scalability/scalability_index.md](notes/program/scalability/scalability_index.md)

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
|-- replay_parity_harness.py
|-- generate_cutover_readiness_report.py
|-- ie_compat_intake.py
|-- run_scalability.py
|-- requirements.txt
|
|-- architecture/
|   |-- idob_seam.md
|   |-- idob_meaning_lock.md
|   |-- path_a_realization_charter.md
|   `-- IdOB_unified_plan.md
|
|-- characterization/
|-- desks/
|-- idob/
|   |-- sum.py
|   |-- packets.py
|   |-- registry.py
|   |-- connections.py
|   `-- ...
|-- mcb/
|   `-- seam.py
|-- ouba/
|-- s2m/
|-- mapping/
|-- stores/
|-- characterization/
|-- scalability/
|
|-- support/
|   |-- dictionaries/
|   |-- idob_objects/
|   |-- idob_schemas/
|   |-- docs/
|   |-- s2m/
|   `-- tools/
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
|   |-- program/
|   |-- pathA_coverage.md
|   |-- bench_walk/00_how_to_walk.md
|   |-- idob_object_space/idob_object_space.md
|   |-- pathA_supported_sentences.md
|   |-- pathA_relational_geometry.md
|   `-- pathA_routing_to_meaning.md
|
`-- user_guide.md
```
