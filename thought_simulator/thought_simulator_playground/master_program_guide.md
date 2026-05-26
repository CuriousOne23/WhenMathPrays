# Master Program Guide

## Purpose

This document is the **governing constitution** of the `thought_simulator_playground/`.  

It defines the philosophy, rules, structure, and workflow we follow when exploring and building the Thought Simulator. It ensures every module is developed with scientific rigor, humility, and traceability.

## Core Philosophy

We are **explorers**, not experts pretending to know everything upfront.

The Thought Simulator is a novel, conceptual, emergent system. We cannot design it perfectly on paper. Therefore we:

- Stay humble about what we don’t know
- Break the unknown into small, focused modules
- Prototype quickly and safely
- Observe, test, break, and learn
- Refine requirements and design based on evidence
- Document insights, failures, and changes as we go
- Only promote stable, verified modules to the final `thought_simulator_design/` folder

This is the scientific method applied to software engineering.

## Playground Structure

Every module follows this exact layout:

```
<module_name>/
├── software_description.md          # Tentative design sketch
├── prototype.py                     # Macro-style exploratory implementation
├── harness.py                       # Test / verification runner
├── insights.md                      # Run Record + learnings
├── failures.md                      # What broke and why
├── updated_requirements.md          # Requirement evolution
├── verification_summary.md          # Full Verification Capsule
└── requirements_traceability.md     # HLR → LLR → Test → Evidence
```

## Prototype Rules (Macro-Style Module)

`prototype.py` must be written as a **macro-style module**:

- Self-contained and importable
- Exposes a clean public API
- Contains internal helpers
- Defines its own state variables
- Uses only local variables inside functions
- Has **no top-level execution** (no code outside functions/classes)
- Has **no global mutable state**

This ensures reusability, testability, determinism, and parallel safety.

## Variable Control Rules

**Global Variables**  
**Forbidden** (except constants in `UPPER_CASE`).  
No module-level mutable variables, shared caches, or hidden state.

**State Variables**  
Allowed **only inside classes** (e.g., inside `ThoughtPoint`).  
Must be explicit, observable, and updated only through public methods.

**Local Variables**  
Allowed and encouraged.  
They must remain ephemeral and never escape function scope.

**Rationale**: Global mutable state destroys determinism, reproducibility, parallelism, and verifiability.

## What Each File Must Answer

| File                          | Answers These Questions |
|-------------------------------|-------------------------|
| `software_description.md`     | What is this module for? Why does it exist? What are the requirements? What math/formatting/state does it use? What assumptions? |
| `prototype.py`                | How is the module implemented? What is the public API? What state & local variables does it use? How is determinism preserved? |
| `harness.py`                  | How do we test this module? What evidence do we collect? How do we verify invariants, determinism, and parallel safety? |
| `insights.md`                 | What worked well? What surprised us? What did we learn? (Includes Run Record table) |
| `failures.md`                 | What broke? Why? What did we learn from it? |
| `updated_requirements.md`     | What requirements changed? Why? What new requirements emerged? |
| `verification_summary.md`     | Full Verification Capsule: invariants, evidence, status, assumptions, efficiency, parallel safety |
| `requirements_traceability.md`| Mapping from high-level requirements → low-level → tests → evidence |

## Verification Capsule

Every module must eventually produce a **Verification Capsule** (`verification_summary.md`) that scientifically answers:

- What the module does and why it exists
- Key invariants and responsibilities
- How it was implemented and tested
- Evidence of correctness and determinism
- Performance and parallel-safety notes
- Assumptions and open questions

This capsule is the scientific record of the module.

## Workflow

1. **Design** — Write/update `software_description.md`
2. **Prototype** — Implement in `prototype.py` (macro-style)
3. **Test & Verify** — Run `harness.py` and collect evidence
4. **Record** — Update `insights.md`, `failures.md`, Run Record table
5. **Refine** — Update requirements and traceability if needed
6. **Stabilize** — When coherent and verified, promote to `thought_simulator_design/`

## When a Module Graduates

A module leaves the playground when:
- Requirements feel stable and coherent
- Prototype behaves correctly and deterministically
- Harness + tests exist with clear expected outcomes
- Verification Capsule is substantially complete
- Major insights and failures are documented

Only then is the polished version moved to the final design folder.

---

**Last Updated**: May 26, 2026  
**Version**: 0.1

---