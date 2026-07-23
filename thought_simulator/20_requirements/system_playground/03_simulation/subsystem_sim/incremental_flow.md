# Incremental Flow — Path A Subsystem Simulation

This document describes the incremental, multi‑primitive execution flow for Path A.  
It is subsystem‑level: it shows how primitives interact when executed in sequence.  
Primitive‑local behavior remains inside each primitive’s folder under `../path_a/`.

The goal is to provide a clear, stepwise view of how envelopes move through Path A.

---

## 1. Context → CEx → CE Initialization

**Inputs:**
- Context machinery (CIL, COB, CST‑Core, CST‑MS, CST‑Mux)
- Intake Envelope (IE)

**Flow:**
1. IE is produced by upstream intake processing.
2. CEx extracts a bounded, replay‑stable CE from IE.
3. CE becomes the initial subsystem envelope for Path A.

**Outputs:**
- CE (Context Envelope)
- Replay‑stable geometry for downstream primitives

---

## 2. InB → IIInB → IE → CEx → CE → TPU

This stage validates the front of Path A.

**Flow:**
1. InB receives initial envelope.
2. IIInB performs inference/repair operations.
3. IE is re‑validated.
4. CEx re‑extracts CE (replay stability check).
5. CE flows into TPU.
6. TPU performs the first transform operations.

**Outputs:**
- CE after TPU transformation
- Verified replay stability across early primitives

---

## 3. TPU → SOB → SROB → CnOB → SmOB → ISc

This stage builds and refines structural and semantic objects.

**Flow:**
1. TPU output enters SOB.
2. SOB constructs structural objects.
3. SROB performs structural rewrite operations.
4. CnOB applies canonical object rules.
5. SmOB applies semantic object rules.
6. ISc receives the refined envelope.

**Outputs:**
- Envelope with structural and semantic geometry
- ISc‑ready envelope for signature generation

---

## 4. ISc → SSG → STPX → RBU → DCB

This stage generates signatures and applies routing boundaries.

**Flow:**
1. ISc prepares envelope for signature generation.
2. SSG generates structural signatures.
3. STPX applies structural transform processing.
4. RBU applies routing boundary rules.
5. DCB applies deterministic context boundary constraints.

**Outputs:**
- Envelope with signatures and boundary constraints
- Ready for routing and transition resolution

---

## 5. DCB → RB → TR → CTP → ISc

This stage performs routing and transition resolution.

**Flow:**
1. DCB output enters RB.
2. RB applies routing boundary logic.
3. TR resolves transitions.
4. CTP applies canonical transform processing.
5. Envelope returns to ISc.

**Outputs:**
- Envelope after routing and canonical transforms
- ISc receives updated envelope for next cycle

---

## 6. ISc → RTU → RB → IdOB → MCB

This stage handles identity and multi‑cycle boundaries.

**Flow:**
1. ISc prepares envelope for routing transform.
2. RTU applies routing transform operations.
3. RB re‑applies routing boundary logic.
4. IdOB applies identity object rules.
5. MCB applies multi‑cycle boundary constraints.

**Outputs:**
- Envelope prepared for multi‑cycle replay
- Ready for next RBU/DCB cycle

---

## 7. MCB → RBU → DCB → RB → TR → CTP

This stage repeats the boundary and transition cycle.

**Flow:**
1. MCB output enters RBU.
2. RBU applies routing boundary rules.
3. DCB applies deterministic context boundary.
4. RB re‑routes envelope.
5. TR resolves transitions.
6. CTP applies canonical transforms.

**Outputs:**
- Envelope ready for final ISc cycle
- Replay stability validated across cycles

---

## 8. CTP → ISc → RTU → RB → OuBA

This stage terminates Path A.

**Flow:**
1. CTP output enters ISc.
2. ISc prepares final routing transform.
3. RTU applies final routing transform.
4. RB applies final routing boundary logic.
5. OuBA produces the final output boundary artifact.

**Outputs:**
- OuBA (final Path A output)
- Envelope ready for downstream system components

---

## 9. OuBA + Context Processing

Final validation step.

**Flow:**
1. OuBA is checked against context constraints.
2. Context machinery validates final envelope geometry.
3. Replay stability is confirmed across entire subsystem flow.

**Outputs:**
- Final subsystem‑validated envelope
- Ready for system‑level integration

---

## Notes

- All primitive names follow 20.190 exactly.
- No acronym expansions are invented.
- This document describes subsystem‑level flow, not primitive‑local behavior.
- Primitive‑local simulation remains under `../path_a/`.

