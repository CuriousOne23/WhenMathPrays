# 14 Completion Logic

## 1. Purpose
Define how the simulator determines when thought processing is complete (or as complete as currently possible), including clean completion, stressed/provisional completion, and transitions involving Inquiry Basins or terminal states.

## 2. Core Requirements

**CL-01: Primary Completion Signal**
- The system must use **normalized relative entropy** $H_{\%}$ as the main indicator of processing completion.
- Completion decisions must also incorporate remaining time budget and global stress/urgency level.

**CL-02: Clean Completion**
- Triggered when $H_{\%}$ falls below a configurable threshold (recommended default: 15–25%).
- The ThoughtPoint should be routed to the **Done RB** for final packaging and output.
- Represents high-coherence, well-resolved thought.

**CL-03: Stressed / Provisional Completion**
- Triggered when the time budget is critically low, regardless of current $H_{\%}$ (e.g., allowing completion up to 50–60% entropy).
- Must optionally route the thought through a **Feeling OB** before entering the Done RB to attach emotional valence and uncertainty markers.
- Must clearly tag the output as "provisional" with remaining uncertainty metrics.

**CL-04: Inquiry Basin Activation**
- If $H_{\%}$ remains persistently in the medium range (e.g. 35–70%) for a configurable duration without meaningful reduction, the system must activate or dynamically create an **Inquiry Basin**.
- This state represents active, unresolved exploration rather than completion.

## 3. Decision Logic Flow

At each simulation step, the Completion Logic must evaluate:
1. Current $H_{\%}$ value and recent rate of change
2. Remaining time budget
3. Current basin type and stability
4. Global context (stress, urgency, volitional intent)
5. Fanin/fanout activity

Then decide one of:
- Continue normal processing
- Activate Inquiry Basin
- Perform Clean Completion
- Perform Stressed Completion

## 4. Final Output Requirements
- Every completed thought must produce a structured final state containing:
  - Final fuzzy embedding
  - Attached metadata and tags
  - Final $H_{\%}$ and confidence score
  - Completion type (clean / stressed / inquiry-resolved)
  - Emotional valence (if Feeling OB used)
  - Trajectory summary (key basins visited, energy used, etc.)

## 5. Observability and Logging
- Must log every completion-related decision with clear reasoning.
- Must prominently flag stalled entropy reduction and Inquiry Basin activations.
- All transitions to Done RB or Feeling OB must be fully traceable.

## 6. Testability Requirements
- Must reliably trigger clean completion on well-resolved paths.
- Must trigger stressed completion under tight time constraints.
- Must correctly activate Inquiry Basins on persistent medium-entropy cases.
- All completion types must be reproducible given the same seed and config.

## 7. Traceability
Links to:
- `03_core_conceptual_requirements.md` (Section 2.6)
- `11_entropy_and_information.md`
- `06_basins.md` (Done RB, Feeling OB, Inquiry Basins)

---

**Last Updated**: [Insert Date]  
**Version**: 0.1 (Draft)