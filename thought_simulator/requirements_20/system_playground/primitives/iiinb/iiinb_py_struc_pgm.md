# 20.101.PY.IIINB – Python structural program for IIInB primitive

> Canonical structural specification for the Python implementation of the **IIInB** primitive, aligned with:
> - 20.101_iiinb_prim.md (conceptual primitive spec)
> - 20.15_ts_architecture_scaffold.md (architecture and replay invariants)
> - 20.105_tp_requirements.md (TP envelope requirements)
> - 20.105.010_tp_meta_fields.md (meta‑field naming)
> - 20.105.020_tp_meta_provenance.md (provenance)
> - 20.105.030_tp_meta_usage.md (usage constraints)
> - system_playground/testbenches/progressive_lineup_testing.md (progressive lineup tests)
> - system_playground/primitives/iiinb/iiinb.py (mechanical implementation)
> - system_playground/testbenches/path_a/intake/iiinb_testbench.yaml / iiinb_testbench.py (testbench contract)

This document is **normative** for the Python structural program of IIInB. Any change to IIInB behavior, TP envelope shape, or replay semantics **MUST** be reflected here and synchronized with the documents listed above.

---

## 1. Canonical synchronization set (required)

**Synchronization set for IIInB:**

- **Conceptual primitive spec:**  
  - `thought_simulator/requirements_20/20.101_iiinb_prim.md`
- **Architecture scaffold:**  
  - `thought_simulator/requirements_20/20.15_ts_architecture_scaffold.md`
- **TP envelope requirements:**  
  - `thought_simulator/requirements_20/20.105_tp_requirements.md`
  - `thought_simulator/requirements_20/20.105.010_tp_meta_fields.md`
  - `thought_simulator/requirements_20/20.105.020_tp_meta_provenance.md`
  - `thought_simulator/requirements_20/20.105.030_tp_meta_usage.md`
- **System playground & testbenches:**  
  - `thought_simulator/requirements_20/system_playground/primitives/iiinb/iiinb.py`
  - `thought_simulator/requirements_20/system_playground/primitives/iiinb/iiinb_py_struc_pgm.md` (this file)
  - `thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/iiinb_testbench.yaml`
  - `thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/iiinb_testbench.py`
  - `thought_simulator/requirements_20/system_playground/testbenches/progressive_lineup_testing.md`

**Normative rule:**

- **MUST:** Any change to IIInB’s:
  - TP envelope shape,
  - rule ordering,
  - token handling,
  - metadata behavior,
  - replay semantics,
  - or testbench expectations  
  **MUST** be synchronized across all items in this set.
- **MUST NOT:** Modify IIInB in isolation. Unsynchronized changes are considered **invalid** and **non‑compliant**.

---

## 2. TP envelope compliance (20.105 / 20.15)

IIInB is a **pre‑semantic primitive** that operates on intake text and produces a **TP envelope**. The TP envelope is the only artifact consumed by downstream pipeline stages.

### 2.1 Dict‑only TP envelope

- **MUST:** IIInB **MUST** output a **Python `dict`** representing the TP envelope.
- **MUST:** The TP envelope **MUST** be:
  - JSON‑serializable,
  - stable under replay,
  - free of non‑deterministic fields (no timestamps, random IDs, etc.).
- **MUST:** Any Python wrapper class or helper object is **pure convenience** and **MUST NOT** be relied upon by downstream primitives. Downstream code consumes only the **dict**.
- **MUST:** The TP envelope shape **MUST** be identical across:
  - Python implementation (`iiinb.py`),
  - C++ implementation (see §9).

### 2.2 Canonical TP output schema

The canonical TP envelope produced by IIInB **MUST** have the following shape:

```python
iiinb_tp_envelope = {
    "iiinb_status": str,        # status string for IIInB processing
    "repair_operations": list,  # list of repair operation descriptors
    "anomaly_flags": list,      # list of anomaly flags
    "normalized": str,          # normalized surface string
    "tokens": list,             # list of token strings (from original surface)
}
```

**Normative constraints:**

- **MUST:** All five fields **MUST** be present in every TP envelope produced by IIInB.
- **MUST:** Field names **MUST** match exactly as above (no renaming, no casing changes).
- **MUST:** Types **MUST** match:
  - `iiinb_status`: `str`
  - `repair_operations`: `list`
  - `anomaly_flags`: `list`
  - `normalized`: `str`
  - `tokens`: `list`
- **MUST NOT:** Add extra top‑level fields to the IIInB TP envelope without updating:
  - 20.105_tp_requirements.md
  - 20.105.010_tp_meta_fields.md
  - 20.105.020_tp_meta_provenance.md
  - 20.105.030_tp_meta_usage.md
  - this structural program
  - and the testbenches.

---

## 3. TP meta‑field, provenance, and usage compliance

IIInB interacts with TP metadata and provenance under strict constraints.

### 3.1 Meta‑fields (20.105.010)

- **MUST:** IIInB may only write to the metadata field:
  - `metadata["iiinb_status"]`
- **MUST NOT:** IIInB **MUST NOT** create, rename, or delete any other metadata fields.
- **MUST:** The meaning of `iiinb_status` **MUST** be consistent with 20.101_iiinb_prim.md:
  - e.g., `"ok"`, `"repaired"`, `"anomaly_detected"`, etc., as defined there.
- **MUST:** Any change to allowed status values **MUST** be documented in:
  - 20.101_iiinb_prim.md
  - 20.105.010_tp_meta_fields.md
  - this structural program
  - and reflected in testbenches.

### 3.2 Provenance (20.105.020)

- **MUST:** `repair_operations` and `anomaly_flags` **MUST** be interpretable as provenance:
  - Each entry describes **what** was detected or repaired,
  - and **where** (position, token index, or other stable reference).
- **MUST:** Provenance entries **MUST** be deterministic and reproducible under replay.
- **MUST NOT:** Use opaque, non‑reproducible identifiers (e.g., random IDs, hash of full text) without explicit specification in 20.105.020.

### 3.3 Usage constraints (20.105.030)

- **MUST:** IIInB’s TP envelope is intended for:
  - deterministic replay,
  - pre‑semantic intake normalization,
  - anomaly and repair tracking.
- **MUST NOT:** IIInB **MUST NOT**:
  - perform semantic inference,
  - interpret user intent,
  - modify meaning of the text.
- **MUST:** Downstream usage of IIInB’s envelope **MUST** respect:
  - no semantic commitments,
  - no probabilistic interpretation of `iiinb_status`,
  - no hidden state.

---

## 4. Behavior and forbidden actions (20.101 alignment)

IIInB is a **pre‑semantic primitive** defined in 20.101_iiinb_prim.md. This structural program enforces that conceptual spec.

### 4.1 Allowed behavior

- **MUST:** Operate only on:
  - intake surface string,
  - tokenization derived from that surface,
  - simple structural repairs (spacing, casing, basic normalization).
- **MUST:** Produce:
  - `normalized` as a structurally repaired surface,
  - `tokens` as a tokenization of the **original** surface (see §5),
  - `repair_operations` and `anomaly_flags` describing structural changes/detections.

### 4.2 Forbidden behavior

- **MUST NOT:** Perform semantic repairs (e.g., rephrasing, summarizing, translating).
- **MUST NOT:** Infer user intent or meaning.
- **MUST NOT:** Introduce new content not present in the original surface.
- **MUST NOT:** Drop tokens or content unless explicitly allowed by 20.101_iiinb_prim.md and documented as a repair operation.
- **MUST:** Any behavior change that touches semantics **MUST** be rejected and treated as non‑compliant.

---

## 5. Token preservation and provenance (20.105 alignment)

Token handling is critical for replay and provenance.

### 5.1 Token source

- **MUST:** `tokens` **MUST** be derived from the **original intake surface**, not from `normalized`.
- **MUST:** Tokenization rules **MUST** be stable and documented in 20.101_iiinb_prim.md.
- **MUST:** Python and C++ implementations **MUST** use equivalent tokenization rules so that:
  - token sequences are identical,
  - indices and provenance references remain valid across languages.

### 5.2 Token preservation

- **MUST:** IIInB **MUST** preserve the full token sequence of the original surface, except where:
  - a repair operation explicitly removes or merges tokens,
  - and that operation is recorded in `repair_operations`.
- **MUST NOT:** Silently drop or reorder tokens.
- **MUST:** Any change to tokenization or preservation rules **MUST** be:
  - documented in 20.101_iiinb_prim.md,
  - reflected in 20.105_tp_requirements.md,
  - synchronized with testbenches and this structural program.

---

## 6. Replay determinism (20.15 / 20.105.030)

IIInB participates in the deterministic replay chain defined in 20.15_ts_architecture_scaffold.md.

### 6.1 Deterministic behavior

- **MUST:** Given the same intake surface and configuration, IIInB **MUST** produce:
  - the same `normalized` string,
  - the same `tokens` list,
  - the same `repair_operations`,
  - the same `anomaly_flags`,
  - the same `iiinb_status`.
- **MUST NOT:** Depend on:
  - wall‑clock time,
  - random number generators,
  - external services,
  - global mutable state.

### 6.2 Replay chain integration

- **MUST:** IIInB’s TP envelope **MUST** be sufficient to:
  - reconstruct its behavior during replay,
  - verify that progressive lineup tests (see §7) remain stable.
- **MUST:** Any change that affects replay determinism **MUST** be:
  - documented in 20.15_ts_architecture_scaffold.md,
  - reflected in 20.105.030_tp_meta_usage.md,
  - synchronized with testbenches and this structural program.

---

## 7. Progressive lineup compliance

`progressive_lineup_testing.md` defines how primitives, including IIInB, are sequenced and tested.

### 7.1 Rule ordering and lineup stability

- **MUST:** IIInB’s internal rule ordering (e.g., normalization steps, anomaly checks) **MUST** be stable.
- **MUST:** Progressive lineup tests rely on:
  - fixed ordering of primitives,
  - fixed ordering of IIInB’s internal rules.
- **MUST:** Any change to rule ordering **MUST**:
  - update `progressive_lineup_testing.md`,
  - update `iiinb_testbench.yaml` and `iiinb_testbench.py`,
  - be documented in this structural program.

### 7.2 Statelessness

- **MUST:** IIInB **MUST** be stateless across calls:
  - no accumulation of state between invocations,
  - no dependence on previous inputs.
- **MUST:** Progressive lineup tests **MUST** be able to:
  - run IIInB multiple times in sequence,
  - obtain identical results for identical inputs.

---

## 8. Python structural program

This section describes the expected Python structure for IIInB, consistent with `iiinb.py`.

### 8.1 High‑level interface

IIInB’s Python implementation **SHOULD** expose a primary function or class method with the following shape:

```python
def run_iiinb(intake_surface: str, metadata: dict | None = None) -> dict:
    """
    Run the IIInB primitive on the given intake surface.

    Parameters
    ----------
    intake_surface : str
        Original intake text (pre-semantic).
    metadata : dict | None
        Optional metadata dict. IIInB may only write to metadata["iiinb_status"].

    Returns
    -------
    iiinb_tp_envelope : dict
        {
            "iiinb_status": str,
            "repair_operations": list,
            "anomaly_flags": list,
            "normalized": str,
            "tokens": list,
        }
    """
    ...
```

### 8.2 Optional wrapper class

A convenience wrapper class is allowed but **MUST** respect the dict‑only envelope requirement:

```python
class IIInB:
    def __init__(self, config: dict | None = None):
        self._config = config or {}

    def process(self, intake_surface: str, metadata: dict | None = None) -> dict:
        # Internal steps:
        # 1. Tokenize original surface -> tokens
        # 2. Detect anomalies -> anomaly_flags
        # 3. Apply structural repairs -> normalized, repair_operations
        # 4. Set iiinb_status in metadata (if provided)
        # 5. Build and return TP envelope dict

        iiinb_tp_envelope = {
            "iiinb_status": "...",
            "repair_operations": [],
            "anomaly_flags": [],
            "normalized": "...",
            "tokens": [],
        }
        return iiinb_tp_envelope
```

**Normative constraints:**

- **MUST:** `process` (or equivalent) **MUST** return the canonical TP envelope dict.
- **MUST NOT:** Expose additional mutable state that affects determinism.
- **MUST:** Any structural change to this interface **MUST** be reflected in:
  - `iiinb.py`,
  - testbenches,
  - and this structural program.

---

## 9. C++ parity requirements

IIInB has or may have a C++ implementation. Cross‑language parity is required.

### 9.1 Envelope parity

- **MUST:** Python and C++ implementations **MUST** produce **bit‑identical** TP envelopes after serialization:
  - same field names,
  - same field ordering (where relevant),
  - same values.
- **MUST:** Tokenization and normalization rules **MUST** be aligned so that:
  - `normalized` strings match,
  - `tokens` lists match.

### 9.2 Replay and testbench parity

- **MUST:** Progressive lineup tests and replay tests **MUST** be able to:
  - swap Python and C++ implementations of IIInB,
  - obtain identical results for identical inputs.
- **MUST:** Any divergence between Python and C++ behavior **MUST** be treated as a bug and resolved by:
  - updating both implementations,
  - updating this structural program,
  - and, if necessary, updating 20.101 and 20.15.

---

## 10. Change‑management rules

### 10.1 Required synchronization

Any change to IIInB **MUST** be accompanied by:

- **Conceptual update:**  
  - 20.101_iiinb_prim.md
- **Architecture update (if replay or pipeline affected):**  
  - 20.15_ts_architecture_scaffold.md
- **TP envelope and meta update (if fields or usage affected):**  
  - 20.105_tp_requirements.md  
  - 20.105.010_tp_meta_fields.md  
  - 20.105.020_tp_meta_provenance.md  
  - 20.105.030_tp_meta_usage.md
- **System playground update:**  
  - `iiinb.py`  
  - `iiinb_py_struc_pgm.md` (this file)
- **Testbench update:**  
  - `iiinb_testbench.yaml`  
  - `iiinb_testbench.py`  
  - `progressive_lineup_testing.md`

### 10.2 Prohibited unsynchronized changes

- **MUST NOT:** Modify IIInB’s behavior, envelope shape, or replay semantics in:
  - `iiinb.py`,
  - C++ implementation,
  - or testbenches  
  without updating this structural program and the synchronization set.
- **MUST:** Treat any unsynchronized change as **non‑compliant** and subject to rollback.

---

## 11. Summary

IIInB’s Python structural program:

- Defines a **dict‑only**, deterministic TP envelope.
- Aligns with 20.101 (concept), 20.15 (architecture), and 20.105 (TP requirements).
- Enforces:
  - strict meta‑field and provenance rules,
  - token preservation from original surface,
  - replay determinism,
  - progressive lineup stability,
  - Python/C++ parity.
- Requires synchronized change‑management across the full canonical set.

This file is the **authoritative structural contract** for IIInB in Python. Any implementation or testbench **MUST** conform to it.
```
