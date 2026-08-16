# **progressive_lineup_testing.md — Path‑A Progressive Lineup Testing Framework (Version 4.1)**
**Status:** Active
**Scope:** All Path‑A primitives
**Applies To:** IIInB, IE, CEx, CE, WrdNm, ISc, TPU, SOB, SROB, CnOB, SmOB, SSG, IdOB, TR, CTP, RTU, RB, OuBA, SSRGn
**Exception:** InB (partially tested; no upstream primitive)

---

# **1. Purpose**

The **Progressive Lineup Testing Framework** defines how **every Path‑A primitive** is tested in a deterministic, layered, replay‑safe manner.
It ensures:

- stable intake behavior
- deterministic primitive outputs
- correct propagation of envelopes
- correct provenance
- correct bounded‑semantic behavior
- correct pipeline integration
- Python/C++ parity
- rule‑driven validation
- strict primitive boundary discipline

This framework is **not a requirements document**.
It describes **how primitives are tested**, not **what they must do**.

---

# **NOTE: FULL BODY**

The complete v4.1 body (sections 2–11 plus new §3.10 New Primitive Implementation Scaffold) is staged at:

`/home/workdir/artifacts/progressive_lineup_testing.md`

in the agent workspace and should be committed from there if this stub remains. The authoritative additions are:

1. **Applies To** now includes **SSG**.
2. **New §3.10 New Primitive Implementation Scaffold (Mandatory Checklist)** — general for all Path‑A primitives:
   - Required file set
   - Gold-standard reference (ISc)
   - Required entry points in `<prim>.py`, testbench, rulechecker
   - `run.py` activation pattern
   - YAML shape conventions
   - Recommended implementation order
   - Explicit “what this section is not”

Version end marker: **Version 4.1** — Added §3.10; SSG added to Applies To.

Please re-push the full file from the local artifact if needed.
