# phi-G Relationship Foundation

## Purpose
Define the core phi-G relationship as a relational primitive that bridges SSG (single-responsibility transformation layer) to RB (Relational Basin) dynamics. This foundation enables subsequent simulation requirements and validation while preserving the overall manifold architecture (object-basin stability through relational transformation).

## Scope
- Technical focus only.
- Links from upstream object-basin variants (SOB, SROB, CnOB, SmOB) through SSG into phi-G and onward to RB.
- RBU (subculture block) is explicitly out of scope.
- Emphasis on simulatable properties suitable for deterministic fixed-time-step execution on standard laptop hardware.

## Definitions and Primitives

**Phi (φ)**  
A generative or phase-like operator that acts on input state from SSG. It introduces dynamic variation or resonance modulation while operating on well-constrained G representations (see below). Phi is deterministic given G, maintains relational openness in fuzzy regimes, and supports approach to singularity-like behavior without full objectification.

**G**  
A grounding or global relational operator that anchors or modulates phi outputs.  

**Form of G (Permissible Representations)**  
G must be representable as a fixed-dimensional relational field vector derived from the four OBs (SOB, SROB, CnOB, SmOB).  
Two permissible construction paths exist:  
1. **Token-based G** — derived from structural features of the input tokens (token classes, punctuation motifs, structural arcs, refinement depth, identity/negation markers).  
2. **Semantic-based G** — derived from meaning-bearing structures (relational motifs, basin-compatible features, resonance patterns, conceptual arcs).  

In both cases, G must be:  
- Deterministic  
- Bounded  
- Refinement-compatible  
- Stable under SSG transformation  
- Consumable by φ without semantic inference  
- Suitable for fixed-time-step simulation  
- Fits in laptop-scale memory  

Regardless of whether G is constructed from token-level structure or semantic-level motifs, it must be representable as a fixed-dimensional relational field vector derived from the four OBs, suitable for deterministic transformation by φ. The overall manifold dimension remains unspecified at this level to avoid premature commitments.

## High-Level Contribution of Each Primitive to G
The G field is constructed through a layered refinement pipeline. Each OB contributes a distinct class of structural information. These contributions are not semantic interpretations but relational and structural signals that φ can operate on deterministically.

- **SOB — Coarse Structural Skeleton**  
  Role: Establish the broad, non-semantic shape of the input.  
  Examples: utterance boundaries, clause segmentation, punctuation class patterns, coarse token-type distribution, structural arcs (e.g., question-shape, list-shape, command-shape).  
  Intuition: SOB gives G its frame — the scaffolding on which all finer structure sits.

- **SROB — Shallow Relational Patterns**  
  Role: Add low-resolution relational hints without committing to meaning.  
  Examples: speech-act class (request, assertion, uncertainty), intent-shape flags (seeking, offering, negating), content-mode flags (procedural, descriptive, evaluative), domain-hint masks (technical, emotional, factual).  
  Intuition: SROB gives G its first layer of relational texture — still fuzzy, still non-semantic, but directional.

- **CnOB — Constraint-Level Structure**  
  Role: Introduce mid-level constraints that shape how the relational field can evolve.  
  Examples: dependency-like constraints (X depends on Y), relational tension (agreement vs contradiction), structural commitments (this must resolve; this must remain open), boundary conditions (identity wobble, negation pressure).  
  Intuition: CnOB gives G its rules of motion — what can change, what must stay stable, and what tensions exist.

- **SmOB — Fine-Scale Relational Microstructure**  
  Role: Add the smallest-grain relational signals that influence curvature and basin approach.  
  Examples: micro-motifs (contrast, elaboration, hesitation), resonance cues (strength, weakness, drift), local coherence signals, fine-scale structural corrections.  
  Intuition: SmOB gives G its micro-geometry — the fine details that influence how φ will deform or stabilize the field.

- **SSG — Single-Responsibility Signature Generator**  
  Role: Produce the final, deterministic, fixed-dimensional signature that phi-G consumes. SSG does not modify TP.  
  Examples: normalized structural vector, aggregated relational features, refinement-compatible signature.  
  Intuition: SSG gives G its final shape — the stable, bounded, replayable vector that φ can operate on.

## phi-G Relationship
The composite mapping φ → G (or bidirectional under certain flows) that transforms SSG outputs into RB-compatible inputs.

## Integration with Lineup
- Upstream (SOB/SROB/CnOB/SmOB → SSG): phi-G consumes stabilized or partially deformed states via SSG’s single job.  
- SSG Role: Single responsibility — prepare and route state for phi-G application.  
- Downstream (phi-G → RB): Outputs feed relational basin dynamics (trajectory curvature, resonance, entropy terms).

## Key Relational Properties
- Approach to Singularity/Mystery: Observable as increased curvature or resonance amplification without collapse into objects.  
- Fuzzy Space Handling: Supports experiential transitions.  
- Stability Invariants: Preserves manifold coherence while allowing transformation.

## Open Questions / Observations for Refinement
- Preferred balance between token-based and semantic-based paths for initial implementation.  
- Exact vector dimensions and feature lists (deferred to simulation requirements).  
- Edge behaviors near identity wobble or basin boundaries.

## Next Documents in Series
- phi_G_simulation_requirements.md  
- phi_G_validation_scenarios.md  

---
