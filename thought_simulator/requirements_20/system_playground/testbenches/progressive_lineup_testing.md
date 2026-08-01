# progressive_lineup_testing.md — Path‑A Intake Progressive Lineup (Version 3.2)

This document defines the **progressive lineup testing strategy** for the **Path‑A intake pipeline**, focusing on:

- IIInB (Input Inference/Repair Basin, v3.2)
- IE (Intake Envelope, v3.2)
- TP envelope determinism
- anomaly and repair provenance
- replay stability
- Python/C++ parity

It is synchronized with:

- `20.101_iiinb_prim.md` (IIInB primitive spec, v3.2)
- `20.109_ie_prim.md` (IE primitive spec, v3.2)
- `iiinb_py_struc_pgm.md` (IIInB Python structural program, v3.2)
- `ie_py_struc_pgm.md` (IE Python structural program, v3.2)
- `iiinb_testbench.yaml`, `iiinb_testbench.py`
- `ie_testbench.yaml`, `ie_testbench.py`
- `run.py` (pipeline runner)

---

## 1. Purpose

The progressive lineup is a **deterministic test harness** that exercises Path‑A intake primitives in a controlled, layered fashion.

Goals:

- verify IIInB’s proposal‑only, non‑mutating behavior
- verify IE’s committed intake construction and machine‑efficiency role
- verify anomaly and repair provenance across the pipeline
- verify replay determinism
- verify Python/C++ parity

---

## 2. Scope

This document covers:

- IIInB → IE intake boundary
- TP envelope shape and stability
- anomaly taxonomy and propagation
- repair proposal integration
- composite merge behavior (IE only)
- dictionary validation (IE only)
- structural construction (IE only)
- replay metadata

It does **not** cover downstream semantic primitives (CEx, CE, ISc, TPU).

---

## 3. Lineup Stages

The progressive lineup is organized into stages:

1. **Stage A — IIInB only**  
   - exercise IIInB’s tokenization, anomaly detection, and repair proposal generation

2. **Stage B — IIInB → IE**  
   - feed IIInB output into IE and verify committed intake construction

3. **Stage C — Replay and provenance**  
   - verify that TP envelopes can be reconstructed deterministically

4. **Stage D — Python/C++ parity**  
   - verify that Python and C++ implementations produce identical outputs

Each stage builds on the previous one.

---

## 4. Test Inputs

Test inputs are defined in:

- `iiinb_input.yaml` (developer playground for intake anomalies)
- `iiinb_testbench.yaml` (canonical IIInB test cases)
- `ie_testbench.yaml` (canonical IE test cases)

Inputs include:

- clean text
- text with illegal characters
- malformed tokens
- unicode anomalies
- punctuation anomalies
- repetition patterns
- dictionary‑absence (`no_entry`)
- shorthand and spelling variants

---

## 5. IIInB Behavior (v3.2)

IIInB is:

- proposal‑only
- non‑mutating
- pre‑semantic
- bounded‑semantic
- token‑span indexed
- deterministic
- replay‑stable

IIInB output:

```python
{
    "iiinb_status": "inspected",
    "repair_proposals": [...],
    "anomaly_flags": [...],
    "intake_surface": str,
    "intake_tokens": list[str]
}
```

Key properties:

- `intake_surface` is the original surface (unchanged)
- `intake_tokens` are tokens from the original surface (unchanged)
- `repair_proposals` are deterministic, token‑span indexed
- `anomaly_flags` are deterministic, token‑span indexed

IIInB does **not**:

- apply repairs
- normalize surface
- mutate tokens
- perform composite merges
- infer meaning

---

## 6. IIInB Anomaly Taxonomy (v3.2)

IIInB emits local anomaly types, including:

- `illegal_character.*`
- `malformed_token`
- `unicode_anomaly`
- `punctuation_anomaly`
- `repetition_pattern`
- `no_entry` (token has no dictionary entry as a standalone form)

All anomalies are:

- local
- bounded
- non‑composite
- token‑span indexed

The lineup verifies:

- correct detection of each anomaly type
- correct span and location encoding
- deterministic behavior across runs
- Python/C++ parity

---

## 7. IIInB Repair Proposals (v3.2)

IIInB generates **repair proposals** only:

```python
{
    "rule_id": str,
    "span": [i, j],
    "replacement": str
}
```

Examples:

- repetition collapse proposals
- unicode normalization proposals
- punctuation normalization proposals
- shorthand expansion proposals
- spelling correction proposals

Constraints:

- proposals are deterministic
- proposals are not applied by IIInB
- proposals do not mutate surface or tokens
- proposals do not perform composite merges

The lineup verifies:

- correct proposal generation
- correct span encoding
- correct rule_id usage
- deterministic replay

---

## 8. IE Behavior (v3.2)

IE is:

- the first committed intake constructor
- the machine‑efficiency boundary between IIInB and downstream primitives
- the first mild‑semantic primitive (meaning‑adjacent, not meaning‑inferential)

IE receives:

- `intake_surface`
- `intake_tokens`
- `repair_proposals`
- `anomaly_flags`
- `metadata.iiinb`

IE produces:

```json
{
  "intake": {
    "tokens": ["string"],          // raw IIInB tokens (read‑only)
    "ie_tokens": ["string"],       // committed IE tokens (post‑repair, post‑merge)
    "token_flags": ["TokenFlag"],
    "normalized_text": "string"
  },
  "structure": {
    "tags": ["StructuralTag"],
    "spans": ["Span"],
    "markup": ["MarkupIndicator"]
  },
  "metadata": {
    "repair_annotations": ["RepairAnnotation"],
    "replay": "ReplayMetadata",
    "ruleset_id": "string"
  },
  "error": "TPError | null"
}
```

IE:

- applies IIInB repairs exactly
- performs composite merges when repairs require them
- validates dictionary entries for merged tokens
- constructs committed normalized surface
- constructs committed IE tokens
- classifies tokens via `token_flags`
- constructs structure deterministically
- encodes replay metadata

IE does **not**:

- reinterpret IIInB repairs
- invent repairs
- infer meaning
- modify upstream fields

---

## 9. IE Responsibilities for IIInB‑Driven Intake (HLR‑20.109‑048 → 057)

The lineup specifically verifies IE’s new responsibilities:

- composite merges when IIInB repairs require merging tokens
- dictionary validation of merged tokens
- handling `no_entry` anomalies (marking tokens as anomalous)
- handling repetition anomalies (applying repetition‑collapse only when proposed)
- handling illegal characters (removing only when proposed)
- handling malformed tokens (marking as anomalous)
- handling unicode normalization repairs (applying only when proposed)
- preserving IIInB token order except where repairs modify spans
- constructing normalized_text from committed IE tokens using rule‑driven normalization
- constructing TP.structure from IIInB structural tags and deterministic IE rules

---

## 10. Token‑Level Normative Classification

IE emits `token_flags` with one entry per committed IE token:

- `normative`
- `repaired`
- `anomalous`
- `unrecognized`
- `null`

Classification is rule‑driven and depends on:

- IIInB repair proposals
- IIInB anomaly flags
- dictionary validation
- composite merge results
- unicode normalization repairs
- repetition collapse repairs
- illegal character removal repairs

The lineup verifies:

- correct classification for each anomaly type
- correct classification for repaired tokens
- correct handling of `no_entry` and `malformed_token`
- deterministic behavior across runs

---

## 11. Structural Construction and Integrity

IE constructs:

- `structure.tags`
- `structure.spans`
- `structure.markup`

from:

- IIInB structural tags
- deterministic IE structural rules

The lineup verifies:

- deterministic structural construction
- valid spans and tags
- correct markup indicators
- correct structural provenance in replay metadata
- deterministic error envelopes when malformed

---

## 12. Replay Determinism

Replay determinism requires:

- stable IIInB output for identical input
- stable IE output for identical IIInB output
- stable TP envelopes across runs and environments

Replay metadata encodes:

- repair operations
- anomaly propagation
- composite merge provenance
- dictionary validation provenance
- structural tags and spans
- token boundaries
- token_flags
- normalization metadata
- ruleset identifiers

The lineup verifies:

- exact reconstruction of TP envelopes from replay metadata
- no dependence on external context
- no nondeterministic fields

---

## 13. Python/C++ Parity

Python and C++ implementations must produce identical:

- IIInB tokenization
- IIInB anomaly detection
- IIInB repair proposals
- IE committed tokens (`ie_tokens`)
- IE token_flags
- IE normalized_text
- IE structure
- IE metadata.repair_annotations
- IE metadata.replay
- IE error envelopes

The lineup runs:

- Python testbenches (`iiinb_testbench.py`, `ie_testbench.py`)
- C++ equivalents (where implemented)

and compares outputs.

---

## 14. Pipeline Propagation Rules

Propagation rules:

- IIInB produces proposals and anomalies only; no committed normalization, no merges
- IE applies proposals, performs merges, validates dictionary entries, constructs committed intake
- downstream primitives consume IE’s committed tokens and token_flags as the primary machine substrate
- normalized_text is used for structural geometry, replay, and debugging, not required for semantic primitives

The lineup verifies:

- correct propagation of anomalies and repairs from IIInB to IE
- correct construction of committed intake in IE
- correct downstream consumption assumptions

---

## 15. Change Management

Any change to:

- IIInB behavior
- IE behavior
- anomaly taxonomy
- repair semantics
- TP envelope shape
- replay metadata

must be reflected in:

- `20.101_iiinb_prim.md`
- `20.109_ie_prim.md`
- `iiinb_py_struc_pgm.md`
- `ie_py_struc_pgm.md`
- `iiinb_testbench.yaml`, `iiinb_testbench.py`
- `ie_testbench.yaml`, `ie_testbench.py`
- `run.py`
- this `progressive_lineup_testing.md`

Unsynchronized changes are non‑compliant.

---

## 16. Summary

The progressive lineup is the **authoritative test harness** for Path‑A intake:

- IIInB: proposal‑only, non‑mutating, bounded‑semantic, deterministic
- IE: committed intake constructor, machine‑efficiency boundary, deterministic
- TP envelopes: stable, replay‑equivalent, provenance‑rich
- Python/C++: aligned

This document is now aligned with **Version 3.2** of IIInB and IE.

---

# End of Document — progressive_lineup_testing.md (Version 3.2)
