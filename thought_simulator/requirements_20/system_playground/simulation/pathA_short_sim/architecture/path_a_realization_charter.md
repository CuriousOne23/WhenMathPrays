# Path A realization charter

**Date:** 2026-09-28  
**Status:** Active for this cycle  
**Scope:** Path-A short simulator + first-class requirements (`20.700.010`, `20.40.010`–`20.40.050`)  
**Does not update:** playground primitive testbenches

**Program (2026-10-08):** [../notes/program/pathA_program.md](../notes/program/pathA_program.md). Current face remains IdOB-sum. Intended face, not running, is IdOB mapping the composed floor. The reserved IdOB-S2M row is that unrealized job, not a second block and not a ban. Mechanics (RBU, RB, TR, RTU, CTP) sit beside the structure floor.


## Goal

Path A Thought Simulator (TS) lineup visibility: world → intake → structure (SOB → SROB → CnOB → SmOB) → identity packet.

- **Current lineup realization:** `system_playground/simulation/pathA_short_sim`
- **Depth lab (frozen this cycle):** playground primitives + `testbenches/path_a/*`
- **Requirements of record:** `20.700.010_primitives_glossary.md` and `20.40.010`–`20.40.050`

Neither tree supersedes the other. The goal chooses the realization. This cycle the short sim shows the forest. 20.40 keeps the full job.

## Official expansions (first use)

| Token | Official expansion | Normative home |
|---|---|---|
| SOB | Structural Observation Block | 20.40.010 / 20.700.010 |
| SROB | Structural Refinement Observation Block | 20.40.020 / 20.700.010 |
| CnOB | Constraint Observation Block | 20.40.030 / 20.700.010 |
| SmOB | Semantic Observation Block | 20.40.040 / 20.700.010 |
| IdOB | Identity Observation Block | 20.40.050 / 20.700.010 |

Teaching words (`segment`, `struct_roles`, `smoothing`) may follow the official expansion. They must not replace it.

## Two IdOB faces

| Face | Record | Status |
|---|---|---|
| IdOB-sum | `idob_packet` (dict `semantic_core`, contributors, overlap_events, digest) | **In Path-A-short lineup** |
| IdOB-S2M | six-ID card, CIE, `meaning_delta_h` | **Reserved** in 20.40.050; not claimed as running in the short sim |

Do not import Meaning Signal Layer (MSL), Cognitive Identity Envelope (CIE), or Structure-to-Meaning (S2M) geometry into the short lineup as if they already run there.

## Edit rules

1. Keep existing 20.40 SHALLs. Add a Path-A-short realization block. Do not thin the requirement so the toy passes.
2. If short-sim does not meet a SHALL, mark **not realized**.
3. Capability reserve lives in `20.700.010`.
4. Testbenches stay frozen; they are the evidence locker for reserved rows.

## See

- Reserve + alias table: `thought_simulator/requirements_20/20.700.010_primitives_glossary.md`
- Seam: `architecture/idob_seam.md`
- Meaning lock: `architecture/idob_meaning_lock.md`
