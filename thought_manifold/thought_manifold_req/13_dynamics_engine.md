# 13 Dynamics Engine

## 1. Purpose
Define how the simulator determines when thought processing is complete (or as complete as possible under current constraints), including clean completion, stressed completion, and transitions to terminal states.

## 2. Core Requirements

**CL-01: Completion Criteria**
- The system must use **normalized entropy** $H_{\%}$ as the primary signal for completion.
- Must also consider time budget remaining and global stress level.

**CL-02: Clean Completion**
- Triggered when $H_{\%}$ falls below a configurable threshold (default: 15–25%).
- ThoughtPoint should be routed to the **Done RB** for final packaging.
- Must represent high-coherence, well-resolved thought.

**CL-03: Stressed / Provisional Completion**
- Triggered when time budget is nearly exhausted, even if $H_{\%}$ is still high (e.g. 40–60%).
- Must optionally route through a **Feeling OB** before entering Done RB.
- Must attach metadata indicating provisional status, remaining uncertainty, and emotional valence.

**CL-04: Inquiry Basin Activation**
- If $H_{\%}$ remains in the medium range (e.g. 35–70%) for an extended period without significant reduction, the system must activate or create an **Inquiry Basin**.
- This represents unresolved but active questioning.

## 3. Key Decision Flow

At each step, the Completion Logic must evaluate:
1. Current $H_{\%}$
2. Remaining time budget
3. Recent entropy reduction rate
4. Current basin type
5. Global stress/urgency level

Then decide:
- Continue processing
- Enter Inquiry Basin
- Perform clean completion
- Perform stressed completion

## 4. Output Requirements
- All completed thoughts must produce a final structured output containing:
  - Final embedding
  - Attached information/tags
  - Final $H_{\%}$
  - Completion type (clean / stressed / inquiry-resolved)
  - Emotional valence (if Feeling OB was used)
  - Trajectory summary

## 5. Observability
- Must log every completion decision with clear rationale.
- Must flag stalled thoughts and Inquiry Basin activations prominently.

## 6. Testability Requirements
- Must reliably trigger clean completion on low-entropy paths.
- Must trigger stressed completion under tight time budgets.
- Must activate Inquiry Basins on persistent medium-entropy cases.
- Must handle all completion types reproducibly.

## 7. Traceability
Links to:
- `03_core_conceptual_requirements.md` (Section 2.6)
- `11_entropy_and_information.md`
- `06_basins.md` (Done RB, Feeling OB, Inquiry Basins)

---

**Last Updated**: [Insert Date]  
**Version**: 0.1 (Draft)