# Local Inference (LI) Mapping Examples and Validation

**Paper ID:** Future HLR number  
**Version:** 0.1 (Draft)  
**Date:** 2026-07-08  

### 1. Introduction
This document provides concrete worked examples and formal validation rules for the LI Mapping Library in the Thought Simulator (TS). It serves as an informative companion to the formal specification, illustrating deterministic mapping behavior, continuity ordering, template selection, and fallback mechanics.

### 2. Example Set 1 — Identity Mapping
**Example 1.1 — Full KnC → KnM → KnF Refinement**  
Input: KnC provides coarse identity anchor with low continuity weight; KnM refines with medium coherence; KnF finalizes with high truth_tag support.  

Mapping equations:  
$coarse = KnC[id] \times w_c$  
$medium = KnM[id] \oplus coarse$  
$final = KnF[id] \times (1 + truth_factor)$

Result: `identity_mapping` resolves to the fine-grained anchor with continuity ordering applied.

**Example 1.2 — Safety Flag Adjustment**  
Unsafe TPSF flag reduces weight of primary candidate, triggering fallback to secondary identity anchor consistent with safety_flags.

### 3. Example Set 2 — Relation Mapping
**Example 2.1 — Multi-Object Relation Chain**  
Input contains “gave” (transfer) and “recommended” (causal) relations. Relational template is selected, followed by causal template for the recommendation chain. Continuity_fields enforce chronological ordering.

**Example 2.2 — Unsafe Flag Fallback**  
High-risk TPSF flag on a relation candidate causes fallback to a safer relational template while preserving semantic_core alignment.

### 4. Example Set 3 — Domain & Qualifier Mapping
**Example 3.1 — Domain Refinement**  
KnC coarse domain anchor is overridden by KnF fine anchor when domain_anchor_fine coherence exceeds threshold. Qualifier_fine weighting incorporates TPTB truth_tags for stance alignment.

**Example 3.2 — Continuity Influence**  
Strong continuity_fields from CoHI prioritize domain/qualifier mappings that maintain referential history, even when KnM suggests an alternative.

### 5. Example Set 4 — Template Selection
**Example 4.1 — Declarative Template**  
Simple assertion fields match declarative template with high semantic alignment and no ambiguity.

**Example 4.2 — Causal Template**  
Cause-effect chain in SSR selects causal template; continuity_fields enforce proper ordering of antecedent and consequent.

**Example 4.3 — Multi-Object Chain**  
Complex chain with three linked objects selects multi-object chain template and applies continuity priority sorting.

### 6. Example Set 5 — Fallback Behavior
**Example 5.1 — Entropy Threshold Violation**  
High entropy in KnF fields triggers fallback operator to medium-tier (KnM) mapping while respecting safety_flags.

**Example 5.2 — Ambiguous Mapping**  
Multiple equally admissible candidates resolved by continuity coherence score from CoHI continuity_fields.

### 7. Validation Rules

#### 7.1 Mapping Validation
- Verify identity_mapping, relation_mapping, domain_mapping, and qualifier_mapping preserve semantic_core fidelity.
- Check that all outputs respect truth_tags and safety_flags.

#### 7.2 Continuity Validation
- Confirm ordering respects continuity_fields priority.
- Validate referential and topic-thread coherence.

#### 7.3 Template Validation
- Ensure selected templates satisfy all defined constraints and invariants.
- Verify correct application of selection operator.

#### 7.4 Invariants Validation
- Determinism: identical inputs produce identical outputs.
- Monotonicity: small SSR changes produce correspondingly small mapping changes.
- SSR freeze compatibility and manifold compatibility.

### 8. Normative Requirements (Future HLRs)

**Future-HLR-001**  
All LI mapping examples and validation procedures SHALL be consistent with the deterministic invariants defined in the LI Mapping Library Specification.

**Future-HLR-002**  
Validation rules SHALL confirm that KnF mappings take precedence over KnC and KnM when fine-grained fields are available.

**Future-HLR-003**  
Continuity validation SHALL enforce ordering invariants from CoHI continuity_fields in all mapping outputs.

**Future-HLR-004**  
Fallback behavior SHALL only be used when primary mappings violate safety_flags or entropy thresholds.

---
