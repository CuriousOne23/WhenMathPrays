# S2M IdOB Traversal Proposal

**Date:** 2026-11-25  
**Status:** Research proposal. Non-normative.  
**Authority:** Research only. Does not override normative requirements in 20.705, 20.45, or 20.40.050.  
**Purpose:** Record the mechanical model for bounded IdOB relational traversal that emerged from the 2026-11-25 review.  

## Bounded responsibility of Path A

Path A need not construct comprehensive meaning. Its bounded responsibility is to mechanically expose the relational information justified by the information and constraints available at the present point in processing. Ultimate or comprehensive meaning, and human-like understanding, are outside the necessary realization claim.

## Provisional mechanical chain

```
S_t → door → C_t → E_t → L_t → (D_t, Q_t) → B_t → P_t → H_t → continue / OuBA
```

Each stage has a narrowly bounded responsibility:

- **Door**: Structural legality. The existing `structural_key → meaning_group_candidates` map returns the finite set of legal group_ids for the current stabilized structure. Candidate absence from the map is the mechanical expression of structural incompatibility.
- **C_t**: Finite legal candidate set (meaning-group identifiers returned by the door). Working hypothesis: A_t = C_t. A post-door hard exclusion operator is a reopen condition only; none is presently justified by demonstrated cases.
- **E_t**: Explicit evidence-to-candidate correspondence results. An explicit declared relation ρ must establish that a property of the evidence bears on a property of the candidate. Corr(e, c, ρ) → {+, -, 0}. Absence of an established relation returns 0 (not opposition). Mismatch is not opposition; an explicit opposing relation is required for -.
- **L_t**: Provenance- and dependency-preserving organization of correspondence observations into evidence families. Distinguishes Independent / Dependent / Unknown. Preserves internal conflict and cross-family disagreement. Unknown dependency does not earn independent reinforcement and remains visible.
- **D_t = (S_t, O_t)**: Established directional support and opposition (counts of nonduplicative supporting and opposing families).
- **Q_t = (U_t, I_t)**: Resolution qualifiers (unknown dependency and internal conflict). These qualify reliability of the directional evidence; they do not automatically alter directional support.
- **B_t = S_t - O_t**: Provisional unit-symmetric directional discrimination policy. Preserves every dominance relation already justified by the partial order on D_t. Introduces unit-family and polarity-symmetry assumptions as the least-assumptive experimental baseline. Equal balances do not imply equivalent evidence states.
- **P_t**: Normalized relative directional support among candidates in C_t. Softmax with fixed T=1 is a tested candidate normalization policy, not accepted architecture. Exponential concentration is an identified provisional policy. P_t represents relative directional support only; it is not probability of meaning, truth, or understanding.
- **H_t**: If derived from P_t, measures unresolved directional discrimination among currently legal candidates. It does not measure total Path A uncertainty, meaning entropy, confidence in truth, or semantic completeness. Low H_t can coexist with unresolved Q_t.
- **Continue / OuBA**: Deliberately unresolved. Directional resolution + qualifier condition + current information sufficiency. Entropy drop alone is insufficient for exit.

## Anti-fabrication principles preserved

- Missing evidence ≠ contradiction.
- Missing correspondence ≠ opposition.
- Repeated observation ≠ independent evidence.
- Unknown dependency ≠ independence.
- Conflict ≠ neutrality.
- Structural legality ≠ contextual support.
- One surviving candidate ≠ complete resolution.
- Equal balance ≠ equivalent evidence state.
- Directional concentration ≠ exit readiness.
- Absence of correspondence is not opposition; absence of evidence is not contradiction.

## Open joints (explicitly unresolved)

- B_t = S - O is a provisional unit-symmetric discrimination policy (unit-family and polarity-symmetry assumptions). Reopen if experiments show equal treatment systematically produces inappropriate decisions.
- Normalization of B_t is open. Softmax T=1 is a tested candidate that introduces exponential concentration not demanded by the preceding evidence structure.
- H_t (if computed over P_t) measures directional uncertainty only.
- Q_t remains separately observable and must not disappear from exit logic.
- The precise continue/OuBA sufficiency rule remains open.
- Evidence-to-candidate correspondence requires declared relations and full provenance. New evidence sources must earn correspondence before earning influence.
- A post-door hard filter remains a reopen condition, not present machinery.
- No CRB primitive is justified by this traversal work.
- Nothing here claims comprehensive human-like meaning.

## Relationship to prior work

This proposal refines the conceptual model in `s2m_relational_proposal.md`. It supplies a mechanical account of how structural legality, evidence correspondence, and bounded discrimination can produce a justified informational state without requiring a complete interpretation. It does not erase the five-stage distinction, default meaning, or the working formulation of meaning as a contextually resolved relational structure. Empirical observations and characterization records remain intact.

Category Selection supplies an optional cue that may participate in correspondence once an explicit relation is declared. Qualification remains a research checkpoint, not an architectural prerequisite for traversal.

## Next steps (not part of this proposal)

- Derive an implementation-facing program reference only after this conceptual proposal is reviewed and frozen.
- Derive an experimental plan from the accepted proposal.
- Realization work follows the program reference.

**This document is research authority only.**