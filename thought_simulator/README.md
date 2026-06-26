# Thought Simulator (TS)

**A deterministic, relational, governance-first cognitive architecture.**

TS is a structural alternative to modern Large Model Systems (LMS). It separates meaning construction (Path A) from realization (Path B), enforces strong invariants, and provides explicit governance, provenance, and relational coherence.

TS is designed as a **cognitive operating system** — a kernel that routes, stabilizes, governs, and integrates with specialized coprocessors rather than attempting to do everything itself.

---

## Current Status (June 26, 2026)

- **Architectural specification complete**
- Full master glossary and invariants defined
- Complete flow catalogs (primitives, processes, reference objects, governance, TS-concepts)
- Simulation-ready state machine
- Dual-pipeline design (Path A / Path B) with strict A/B separation
- Governance layer (IB → GBIB → GB) fully specified
- Co-processor architecture defined for hybrid integration

**Implementation phase** is next.

**Detailed Status Paper:** [TS_and_LMS_AI_status_6-26-2026.md](TS_and_LMS_AI_status_6-26-2026.md)

---

## Repository Structure (thought_simulator/)

### Core Document Tiers
- [00_program_governance/](00_program_governance/) — project intent, architecture framing, and philosophical governance
- [system_playground](20_requirements/system_playground) - exploratory system architecture
- [system_simulation](20_requirements/system_simulation) - system logical simulation done with AI with respect to 20_requirements
- [10_thought_simulator_req/](10_thought_simulator_req/) — formalized requirement anchor layer used for coding and architecture realization
- [20_requirements/](20_requirements/) — primary collaborative requirement layer and traceability source
- [30_verification/](30_verification/) — verification capsules and deterministic evidence artifacts
- [40_thought_simulator_playground/](40_thought_simulator_playground/) — exploratory prototypes and experiments
- [50_thought_simulator_design/](50_thought_simulator_design/) — formal design specifications
- [60_review/](60_review/) — grouped review bundles and decision artifacts
- [70_measurement/](70_measurement/) — metrics, instrumentation, and evaluation methodology
- [80_safety/](80_safety/) — safety constraints and protective controls
- [90_validation_certification/](90_validation_certification/) — validation and conformance

### Key Flow Catalog Files (20-series)
- [20.705_patha_pathb_flow.md](20_requirements/20.705_patha_pathb_flow.md) — Core flow diagrams and conventions
- [20.710_primitive_flows.md](20_requirements/20.710_primitive_flows.md) — Primitive Flows (PF)
- [20.715_process_flows.md](20_requirements/20.715_process_flows.md) — Process Flows (PRF)
- [20.720_reference_flows.md](20_requirements/20.720_reference_flows.md) — Reference-Object Flows (ROF)
- [20.725_governance_flows.md](20_requirements/20.725_governance_flows.md) — Governance Flows (GVF)
- [20.730_ts_concept_flows.md](20_requirements/20.730_ts_concept_flows.md) — TS-Concept Flows (TSCF)

### High-Level Documents
- [thought_sim_arch_overview.md](thought_sim_arch_overview.md) — Conceptual overview and Duck Test comparison

---

## Ownership and Workflow

The repository is human-owned in intent and approval, AI-drafted in breadth, and human-reviewed before authoritative adoption.

In practice:
- Humans, led by the repository owner, control the normative direction and final acceptance of the 20-series.
- AI agents draft most supporting content, expansion, normalization, and scaffolding.
- A small set of core documents remain human-written because they define canonical methodology and release decisions.
- AI-generated material becomes authoritative only after human review and approval.

---

## First-Time Contributor Reading Order

1. [README.md](README.md) (this file)
2. [thought_sim_arch_overview.md](thought_sim_arch_overview.md)
3. [TS_and_LMS_AI_status_6-26-2026.md](TS_and_LMS_AI_status_6-26-2026.md)
4. [20.705_patha_pathb_flow.md](20_requirements/20.705_patha_pathb_flow.md)
5. The 20.710–20.730 flow catalog files
6. [10_thought_simulator_req/](10_thought_simulator_req/) for formal anchors

---

## Process Flow (Current)

The process flow is direction-controlled:
- Requirements collaboration and intent shaping in [20_requirements/](20_requirements/)
- Evidence/prototype development in [40_thought_simulator_playground/](40_thought_simulator_playground/)
- Formal realization anchors in [10_thought_simulator_req/](10_thought_simulator_req/)

Direction examples:
1. Forward (typical): 20 → 40 → 10 → 30/50
2. Backward (when selected): 20 → 10 → 40 → 30/50

---

**Last Updated**: June 26, 2026  
**Version**: 0.7 (Flow Catalog Integration + Status Paper)

---

Let me know if this looks good to commit, or if you'd like any small tweaks.  

We're making great progress! What's the next item on your list?
