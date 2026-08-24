# **idob_hash_requirements.md**  
### *Formal Hash Specification for SOB → SROB → CnOB → SmOB → RB → IdOB*

---

## 1. Purpose

This document defines the **hash requirements and contracts** across the TS OB pipeline:

> **SOB → SROB → CnOB → SmOB → RB → IdOB**

It specifies:

- what each OB must contribute to hashing  
- which fields are allowed in the hash  
- which fields are forbidden (meaning, identity)  
- how hashes are composed and propagated  
- how determinism and replay‑safety are guaranteed  
- how collisions are bounded  
- how routing_signature and residue_hash are defined  
- how IdOB consumes these hashes for structure→meaning mapping  

This paper is normative.

---

## 2. Hash objects and their roles

TS uses three primary hash constructs:

- **structural_hash** — canonical fingerprint of structural geometry  
- **residue_hash** — fingerprint of constraint/semantic residue  
- **routing_signature** — composite hash used for routing and meaning ranking  

### 2.1 structural_hash

Canonical hash of **pure structural geometry**:

- semantic_field_id  
- semantic_role_id  
- semantic_object_id  
- gradient_id  
- universe_id  
- subfield_id  

Properties:

- **meaning‑agnostic**  
- **identity‑agnostic**  
- **deterministic**  
- **replay‑safe**  
- **collision‑bounded**  

### 2.2 residue_hash

Hash of **constraint/semantic residue** produced by CnOB/SmOB:

- constraint violations  
- unresolved semantic tensions  
- structural anomalies  

Used by:

- SmOB (pre‑semantic processing)  
- RB (routing decisions)  
- IdOB (meaning group ranking, cue envelopes)

### 2.3 routing_signature

Composite routing structure:

```yaml
routing_signature:
  struct_hash: <hex_or_int>        # derived from structural_hash
  feature_hashes: [<hex_or_int>, ...]
```

feature_hashes encode:

- salient structural features  
- residue features  
- pre‑semantic features  

Used by:

- RB (routing)  
- IdOB (meaning group ranking, identity modulation)

---

## 3. OB‑level hash responsibilities

### 3.1 SOB (Structural Object Builder)

**Responsibility:**

- Build **pure structural geometry**.  
- Must not encode meaning or identity.

**Hash requirements:**

- Provide all fields needed for structural_hash:  
  - semantic_field_id  
  - semantic_role_id  
  - semantic_object_id  
  - gradient_id  
  - universe_id  
  - subfield_id  

- Must not compute structural_hash itself.  
- Must ensure geometry is deterministic and normalized.

---

### 3.2 SROB (Structural Refinement OB)

**Responsibility:**

- Refine structural geometry (normalize, resolve minor conflicts).  

**Hash requirements:**

- May adjust structural fields, but must preserve:  
  - deterministic normalization rules  
  - stable ordering  
  - stable encoding  

- Must not compute structural_hash.  
- Must not introduce meaning or identity into geometry.

---

### 3.3 CnOB (Constraint OB)

**Responsibility:**

- Evaluate structural constraints.  
- Produce **constraint residue**.

**Hash requirements:**

- Must compute **residue_hash** from:  
  - constraint violations  
  - unresolved tensions  
  - structural anomalies  

- Must not modify structural_hash inputs.  
- Must not encode meaning or identity into residue_hash.

---

### 3.4 SmOB (Semantic‑adjacent OB)

**Responsibility:**

- Perform pre‑semantic processing.  
- Prepare features for routing and IdOB.

**Hash requirements:**

- Must compute **feature_hashes** for routing_signature from:  
  - salient structural features  
  - residue features  
  - pre‑semantic features  

- Must not compute structural_hash.  
- Must not encode final meaning or identity into feature_hashes.

---

### 3.5 RB (Routing Bridge)

**Responsibility:**

- Route TP segments to downstream OBs (IdOB, OuBA, TR, etc.).

**Hash requirements:**

- Must assemble **routing_signature**:

```yaml
routing_signature:
  struct_hash: structural_hash
  feature_hashes: [<hex_or_int>, ...]
```

- Must ensure routing_signature is:  
  - deterministic  
  - replay‑safe  
  - collision‑bounded  

- Must not alter structural_hash or residue_hash.

---

### 3.6 IdOB (Identity‑Conditioned Object Bridge)

**Responsibility:**

- Consume structural_hash, residue_hash, routing_signature.  
- Perform structure→meaning mapping.

**Hash requirements:**

- Must treat structural_hash as:  
  - key into `struct_to_meaning_map.yaml`  
  - stable structural fingerprint  

- Must treat residue_hash and feature_hashes as:  
  - ranking signals  
  - cue envelope inputs  
  - identity modulation inputs  

- Must not modify structural_hash.  
- May compute additional internal hashes for diagnostics, but these are not part of the TS hash contract.

---

## 4. structural_hash specification

### 4.1 Inputs

structural_hash is computed from:

- semantic_field_id  
- semantic_role_id  
- semantic_object_id  
- gradient_id  
- universe_id  
- subfield_id  

### 4.2 Normalization

Before hashing:

- all IDs must be normalized to fixed‑width integers  
- ordering must be fixed:  
  - field → role → object → gradient → universe → subfield  
- encoding must be stable (e.g., big‑endian, fixed byte width)

### 4.3 Hash function

Requirements:

- deterministic  
- collision‑bounded (e.g., 64–128 bits)  
- fast enough for TS throughput  
- stable across TS versions  

Examples (implementation choice):

- 64‑bit or 128‑bit non‑cryptographic hash (e.g., xxHash, Murmur)  
- or cryptographic hash truncated to required width  

### 4.4 Replay‑safety

Same structural geometry → same structural_hash, always.

If structural geometry changes, structural_hash must change.

---

## 5. residue_hash specification

### 5.1 Inputs

residue_hash is computed from:

- constraint violations  
- unresolved tensions  
- structural anomalies  

Produced by CnOB (and possibly refined by SmOB).

### 5.2 Properties

- deterministic  
- meaning‑agnostic  
- identity‑agnostic  
- collision‑bounded  

Used as:

- signal for routing  
- signal for meaning ranking  
- signal for identity modulation

---

## 6. routing_signature specification

### 6.1 Composition

```yaml
routing_signature:
  struct_hash: structural_hash
  feature_hashes: [<hex_or_int>, ...]
```

feature_hashes derived from:

- salient structural features  
- residue features  
- pre‑semantic features  

### 6.2 Properties

- deterministic  
- replay‑safe  
- collision‑bounded  
- stable ordering of feature_hashes  

### 6.3 Usage

- RB uses routing_signature to route TP segments.  
- IdOB uses routing_signature to rank meaning_group_candidates and modulate identity.

---

## 7. Determinism, collisions, and versioning

### 7.1 Determinism

All hash computations must be:

- pure functions of their inputs  
- independent of runtime state  
- independent of identity and meaning  

### 7.2 Collision bounds

Hash width must be chosen such that:

- collision probability is negligible for TS universe  
- structural_hash collisions are extremely rare  
- routing_signature collisions are bounded and detectable if needed

### 7.3 Versioning

If:

- meaning dictionaries change  
- struct_to_meaning_map.yaml evolves  
- OB implementations change

Then:

- structural_hash must remain stable for identical geometry  
- routing_signature may evolve, but must be versioned if format changes  
- residue_hash may evolve, but must remain deterministic

---

## 8. IdOB consumption of hashes

IdOB uses:

- **structural_hash** as key into `struct_to_meaning_map.yaml`  
- **routing_signature.struct_hash** as a consistency check  
- **routing_signature.feature_hashes** as ranking and modulation signals  
- **residue_hash** as a cue for meaning group selection and identity modulation  

IdOB never writes or modifies these hashes.

---

## 9. Summary

This document defines:

- structural_hash  
- residue_hash  
- routing_signature  
- feature_hashes  
- their roles across SOB → SROB → CnOB → SmOB → RB → IdOB  
- determinism and replay‑safety requirements  
- collision and versioning constraints  

With this spec, the hash contract for TS is:

- **realizable**  
- **supportable**  
- **deterministic**  
- **replay‑safe**  
- **aligned with IdOB’s structure→meaning architecture**

---
