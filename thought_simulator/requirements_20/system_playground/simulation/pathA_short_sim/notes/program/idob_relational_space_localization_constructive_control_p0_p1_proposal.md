# IdOB Relational-Space Localization Constructive Control P0/P1 Proposal

**Date:** 2026-11-27  
**Status:** Research proposal for controlled discrimination (non-normative).  
**Purpose:** Define a bounded constructive-control phase that can discriminate no-signal behavior from real structure-sensitive behavior without selecting a production source or architecture.

Review state: **BEING REVIEWED**

## 1) Objective

Establish whether a frozen structure-sensitive procedure can:

- fail on no-structure controls (P0) when only informative structure is removed; and
- succeed on structure-present controls (P1) only when the informative structural bit is available.

This proposal does not claim production feasibility and does not define HOW-2.

## 2) Program question addressed

Functional question:

Can contextual differentiation of relational material improve meaning construction under non-oracle conditions?

This phase addresses the question only through synthetic controls under strict information boundaries.

## 3) Phase scope

Authorized in this proposed phase:

- synthetic fixture generation for P0 and P1;
- frozen procedure and audit logic;
- bounded control execution and evidence reporting.

Not authorized:

- architecture proposal/selection;
- production selector;
- HOW-2;
- Gate C;
- Category/YAML integration.

## 4) Constructive controls

### P0 (no-structure control)

- latent tuple `U=(P,Q,R)` with deterministic outcome `O=P xor R`;
- decoy channels `X=(x1,x2)` derived from `U`;
- structural channels `Ea,Eb,Ec` contain recoverable `P,Q,R`.

The procedure uses only `Ea,Eb` to decode `P xor R`.

Expected control behavior:

- S0 (unaltered structure): perfect decoding;
- S1 (no structural channels): no better than frozen blind fallback;
- S2 (structure neutralized): no better than frozen blind fallback.

### P1 (single informative structural bit)

- informative bit `S` is encoded in structure;
- outcome `O=S`;
- decoys are independent of `O`.

Procedure:

- if decoded `S=1`, emit `R_B`;
- else emit `R_A`.

Expected control behavior:

- S0: 100%;
- S2 (neutralized `S` preserving marginals): chance-level 50%;
- S1 (no `S` access): chance-level 50%.

## 5) Why this phase is needed

This phase is a discriminative control step between pure oracle-relative sufficiency findings and any future claim about non-oracle functional leverage. It supplies evidence about whether a fixed structure-sensitive mechanism behaves appropriately when signal is present, absent, or neutralized.

## 6) Decision value

A valid P0/P1 characterization can support bounded conclusions on:

- whether the control stack can detect and use frozen structure-embedded signal;
- whether success collapses when that signal is removed or neutralized.

It cannot by itself identify real TS sources, authorize architecture changes, or justify production deployment.
