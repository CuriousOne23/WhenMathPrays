# Master Program Guide

## Purpose

This document is the **governing constitution** of the `thought_simulator_playground/`.

It defines the philosophy, rules, structure, and workflow we follow when exploring and building the Thought Simulator. It ensures every module is developed with scientific rigor, humility, determinism, and full traceability.

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

---

# Playground Structure

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

---

# Prototype Rules (Macro-Style Module)

`prototype.py` must be written as a **macro-style module**.

### Definition of Macro-Style Module
A **macro-style module** is:

- **Self-contained**  
- **Importable** (no top-level execution)  
- **Reusable** in any environment  
- **Deterministic** when deterministic mode is enabled  
- **Encapsulated** (all state inside classes)  
- **Stateless at module level** (no global mutable state)

### Required Properties

- Exposes a clean **public API**  
- Contains **internal helpers**  
- Defines **state variables** inside classes  
- Uses **local variables** freely inside functions  
- Has **no code at top level**  
- Has **no global mutable state**  
- Must be compatible with `harness.py`  

This ensures reusability, testability, determinism, and parallel safety.

---

# Variable Control Rules

## Global Variables
**Forbidden** (except constants in `UPPER_CASE`).

- No module-level mutable variables  
- No shared caches  
- No static mutable fields  
- No hidden counters  
- No hidden registries  

**Rationale:**  
Global mutable state destroys determinism, reproducibility, parallelism, and verifiability.

---

## State Variables
Allowed **only inside classes** (e.g., inside `ThoughtPoint`).

State variables must be:

- Explicit  
- Observable  
- Deterministic  
- Updated only through public API methods  
- Logged by the harness when changed  

Examples:

- entropy  
- embedding  
- energy  
- basin_id  
- tags  
- provenance  
- history  
- state_counter  

---

## Local Variables
Allowed and encouraged.

Local variables must:

- Remain ephemeral  
- Never escape function scope  
- Never mutate global state  
- Never become persistent state  

Examples:

- entropy deltas  
- temporary embedding arrays  
- merge/split intermediates  
- validation buffers  

---

# What Each File Must Answer

| File | Answers These Questions |
|------|-------------------------|
| `master_program_guide.md` | What are the rules, workflow, philosophy, variable constraints, prototype structure, harness expectations, and AI Agent reporting standards? |
| `software_description.md` | What is this module for? Why does it exist? What are the requirements? What math/formatting/state does it use? What assumptions? |
| `prototype.py` | How is the module implemented? What is the public API? What state & local variables does it use? How is determinism preserved? |
| `harness.py` | How do we test this module? What evidence do we collect? How do we verify invariants, determinism, and parallel safety? |
| `insights.md` | What worked well? What surprised us? What did we learn? (Includes Run Record table) |
| `failures.md` | What broke? Why? What did we learn from it? |
| `updated_requirements.md` | What requirements changed? Why? What new requirements emerged? |
| `verification_summary.md` | Full Verification Capsule: invariants, evidence, status, assumptions, efficiency, parallel safety |
| `requirements_traceability.md` | Mapping from high-level requirements → low-level → tests → evidence |

---

# AI Agent Execution & Reporting Standards

This section defines how the AI Agent (Copilot, Grok, etc.) must behave when executing code inside the playground.

## 1. Before Running

The AI Agent must read:

- `software_description.md`  
- `master_program_guide.md`  
- `insights.md`  
- `updated_requirements.md`  

This ensures context, history, and requirement evolution are understood.

---

## 2. When Running Code

The AI Agent must:

- Run `prototype.py` or `harness.py`  
- Capture **full terminal output**  
- Record the **exact command used**  
- Capture all artifacts (JSON, logs, state dumps, etc.)

---

## 3. Required Output Structure

The AI Agent must reply using this template:

### Execution Report — [Module Name]

**Command:** `python harness.py`

**Result:** PASS / FAIL / PARTIAL  
**Exit Code:** 0 / n  

**Run Record Update:**
| Date | Module | Command | Inputs / Config | Result | Exit Code | Artifacts | HLR Ref | LLR Ref | Req Doc | Req Section | Notes |
|------|--------|---------|------------------|--------|-----------|-----------|---------|---------|---------|-------------|-------|
| YYYY-MM-DD | ... | ... | ... | ... | ... | ... | HLR-2 | LLR-2.3 | software_description.md | §3.4.1 | ... |

**Key Observations**
- ...

**Insights & Learnings**
- ...

**Open Questions / Next Iteration**
- ...

**Suggested Next Steps**
1. ...
2. ...
```

---

# Test → Requirement Attachment Rules

Every test run must explicitly attach itself to the requirement(s) it verifies.

This ensures full traceability:

> **High-Level Requirement (HLR)**  
→ **Low-Level Requirement (LLR)**  
→ **Test Case**  
→ **Evidence / Artifacts**  
→ **Verification Capsule**

### Required Columns in Run Record Table

| Column | Meaning |
|--------|---------|
| **HLR Ref** | High-level requirement ID (e.g., `HLR-2`) |
| **LLR Ref** | Low-level requirement ID (e.g., `LLR-2.3`) |
| **Req Doc** | Markdown file containing the requirement |
| **Req Section** | Section number inside the MD file |

### Rules for the AI Agent

- Every test must attach to at least one HLR and one LLR  
- If multiple requirements apply, list them comma-separated  
- If requirement is missing or unclear:  
  - Use `HLR-?` / `LLR-?`  
  - Document the gap in `insights.md`  
  - Propose requirement in `updated_requirements.md`  
- `harness.py` should emit requirement IDs during execution  
- `verification_summary.md` must reference these IDs in the Verification Ledger  

---

# Verification Capsule

Every module must eventually produce a **Verification Capsule** (`verification_summary.md`) that scientifically answers:

- What the module does and why it exists  
- Key invariants and responsibilities  
- How it was implemented and tested  
- Evidence of correctness and determinism  
- Performance and parallel-safety notes  
- Assumptions and open questions  
- Requirement IDs referenced in the Verification Ledger  

This capsule is the **scientific record** of the module.

---

# Workflow

1. **Design** — Write/update `software_description.md`  
2. **Prototype** — Implement in `prototype.py` (macro-style)  
3. **Test & Verify** — Run `harness.py` and collect evidence  
4. **Attach Requirements** — Update Run Record with HLR/LLR references  
5. **Record** — Update `insights.md`, `failures.md`, Run Record table  
6. **Refine** — Update requirements and traceability if needed  
7. **Stabilize** — When coherent and verified, promote to `thought_simulator_design/`  

---

# When a Module Graduates

A module leaves the playground when:

- Requirements feel stable and coherent  
- Prototype behaves correctly and deterministically  
- Harness + tests exist with clear expected outcomes  
- Verification Capsule is substantially complete  
- Requirements Traceability Matrix is complete  
- Major insights and failures are documented  

Only then is the polished version moved to the final design folder.

---

**Last Updated**: May 26, 2026  
**Version**: 0.2

---