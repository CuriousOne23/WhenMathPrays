# **progressive_lineup_testing.md — Path‑A Progressive Lineup Testing Framework (Version 4.1.1)**
**Status:** Active  
**Scope:** All Path‑A primitives

This file was briefly emptied by a bad push and is restored. Testing-mode rules, directory schema, dual-mode contract, packet expected-keys, and IdOB isolation notes are those of **v4.1** (commit `8d200c8`). This revision only replaces the pipeline diagram with the **official Path A flow** from `20.15` v4.1.

If any v4.1 subsection is missing after this restore, recover it from `8d200c8` and keep §6 as written here.

---

# **6. Pipeline Integration Testing — official Path A flow**

```
InB (Beginning of Path A) → IIInB → IE → CEx → CE → TPU → SOB → SROB → CnOB → SmOB
  → WrdNm → ISc → SSG → STPX → RBU → DCB → TR → CTP → RB
  → WrdNm → ISc → RTU → TR → CTP → RB → IdOB → MCB → RBU → DCB
  → TR → CTP → RB → WrdNm → ISc → RTU → TR → CTP → RB → IdOB → MCB → RBU → . . .
OR
DCB → TR → CTP → RB → WrdNm → ISc → RTU → TR → CTP → RB → OuBA (End of Path A)
```

IdOB runs after a committed RB. Isolation fixtures may start at IdOB without the live RB to its left.

---

# **v4.1 body (re-stated pointers)**

- Dual mode: `testbench` / `general` (§3.1–3.5 of v4.1)
- Packet primitives: declared-key `expected:` + walls (§3.1.1)
- IdOB files: `testbenches/path_a/identity/` + `primitives/idob/idob.py`
- Isolation suite: `idob_s2m_01`…`06`; utterance on every enabled case
- CIE defined in `20.40.050` §0.6
- Law: `20.40.050`; TP slots: `20.105` / `20.105.010`

# **End of Document — progressive_lineup_testing.md (Version 4.1.1)**
