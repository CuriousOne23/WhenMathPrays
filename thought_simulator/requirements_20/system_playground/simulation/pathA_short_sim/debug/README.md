# Debugger Documentation (pathA_short_sim/debug)

The `debug/` directory contains human-readable documentation and reference materials used by the `pathA_dbug.py` debugger. These files support debugging, training, and teaching by explaining the simulator's geometry, fields, primitives, and example outputs.

The theory note governs architecture: why the cut exists. The cards govern writers and fields: what a stage wrote. A log inspection can start at a card. An architectural change should start at the theory note.

---

## 0. Read this first

[pathA_structure_theory.md](pathA_structure_theory.md) is the conceptual foundation for this directory. It states why structure is computed before a packet is legal, and what later stages may not reopen.

Program status for the whole short sim, including what is not done yet: [../notes/program/README.md](../notes/program/README.md). Grammar against structure: [../notes/program/grammar_and_structure.md](../notes/program/grammar_and_structure.md).


It is not a primitive card, not a geometry, and not loaded by the debugger in this pass. The cards remain the reference for a log line. They are not sufficient alone for an architectural change.

Prohibition example: [examples/why_this_cut.md](examples/why_this_cut.md).

---

## 1. Purpose

The debugger and its documentation serve three main purposes:

### Debugging
- Provide clear, structured insight into how primitives (SOB, SROB, CnOB, SmOB, IdOB) fired.
- Show segment, role, constraint, identity, semantic-core, and truth-relation vocabularies.
- Surface interpreted blocks in a readable Markdown format.

### Training
- Help developers understand how the simulator processes structural information and assembles a packet.
- Provide consistent reference definitions for geometry dimensions and fields.
- Enable new contributors to learn the simulator's architecture quickly.

### Teaching
- Offer a prohibition example of what a later stage may not reopen.
- Demonstrate how structural cues propagate into a packet.
- Provide a conceptual map of the simulator's pipeline.

---

## 2. Directory Structure

```
debug/
  pathA_structure_theory.md
  dimensions/
  fields/
  primitives/
  examples/
  setup/
```

### Theory
- `pathA_structure_theory.md` — why the cut exists; prior reading for an architectural change

### dimensions/
Live set only:

- `segment_geometry.md` — structural form and segment class membership
- `role_geometry.md` — positional labels (head, modifier, predicate, argument)
- `constraint_geometry.md` — adjacency, compatibility, structural rules
- `identity_geometry.md` — structural, referential, and semantic identity labels on the packet
- `semantic_core.md` — packet dict vocabulary
- `truth_relation.md` — declarative, interrogative, unknown

Not in the tree: `smoothing_geometry.md`, `meaning_geometry.md`. Smoothing is an operation of Semantic Observation Block Job 1, not a dimension file.

### fields/
- `struct_segments.md` — recognized segment structures
- `segment_tokens.md` — token coverage of those segments
- `struct_roles.md` — positional labels
- `constraints_matched.md` — satisfied constraints
- `constraints_unmatched.md` — unresolved constraints
- `constraint_residue.md` — unresolved rule-level signals
- `smoothing_operations.md` — named Job 1 operations
- `semantic_adjacent_cues.md` — stabilized adjacent cues
- `basin_residue.md` — unresolved basin output
- `idob_packet.md` — the sum
- `residue.md`, `smob_smoothing_residue.md` — compatibility aliases

### primitives/
Official names:

- `SOB.md` — Structural Observation Block
- `SROB.md` — Structural Refinement Observation Block
- `CnOB.md` — Constraint Observation Block
- `SmOB.md` — Semantic Observation Block
- `IdOB.md` — Identity Observation Block
- `IE.md` — intake compatibility card

Each primitive file explains what the primitive does, what it may emit, and a symbolic example. IdOB writes a packet. It is not an object.

### examples/
- `why_this_cut.md` — what becomes illegal if a later stage reopens the cut
- `placeholder.md` — debugger stub

### setup/
- `debug_setup.yaml` — documentation names the debugger may load
- `links.yaml` — maps those names to relative paths

These files allow the debugger to generate clickable links in `debug_out.md`. The theory note is intentionally absent from both, so a log report does not treat it as a geometry.

---

## 3. How to Use the Debugger

### Running the debugger

From the simulator root:

```
python run_examples.py > run.log
```

Then:

```bash
python pathA_dbug.py path/to/run.log --base-dir .
```

This produces `debug_out.md` in the base directory.

### What the debugger does

- Loads `debug_setup.yaml` to determine which documentation files to include.
- Loads `links.yaml` to generate clickable links in the output.
- Parses the run log into primitive blocks.
- Interprets each block using semantic placeholders.
- Generates a structured Markdown report.

### Example output snippet

```
## Interpreted Blocks
- SOB: Primitive SOB fired with 3 lines.
- SROB: Primitive SROB fired with 2 lines.
- CnOB: Primitive CnOB fired with 1 line.
```

### Use cases

#### Debugging
- Inspect why a primitive fired.
- Understand segment, role, and constraint interactions.
- Diagnose residue.

#### Training
- Learn how primitives interact.
- Understand geometry and field definitions.
- Read the prohibition example before changing a stage.

#### Teaching
- Demonstrate the pipeline.
- Show how structural cues propagate into a packet.
- Point architectural questions at the theory note, not at a card.

### 3.1 Links Provided Inside `debug_out.md`

The debugger embeds clickable links from `links.yaml`. It does not link the theory note.

#### Types of Links Included

- Dimension links under `debug/dimensions/`: segment, role, constraint, identity, semantic core, truth-relation.
- Field links under `debug/fields/`: segments, tokens, roles, matched and unmatched constraints, constraint residue, smoothing operations, adjacent cues, basin residue, packet.
- Primitive links under `debug/primitives/`: SOB, SROB, CnOB, SmOB, IdOB.
- Example links under `debug/examples/`. The prohibition file is not in `links.yaml` in this pass. Open it from this README.

#### VS Code Compatibility

This debugger writes Markdown output to `debug_out.md` so links are active as Markdown hyperlinks in VS Code preview and Markdown-aware viewers.

---

## 4. Notes

- Card files describe writers and fields. They do not contain the necessity argument.
- They do not contain runtime values or simulator logic.
- Inventory of the live tree: [canonical_debug_document_map.md](canonical_debug_document_map.md).

---

## 5. Contact

For questions or contributions, see the main project repository.
