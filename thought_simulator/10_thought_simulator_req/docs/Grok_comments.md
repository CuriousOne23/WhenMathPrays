**05.500_directory_rename_governance_and_refactor_plan.md**

```markdown
---
status: governance
source_of_truth: this
contains:
  - LLR: [LLR-05.500-001]
  - Governance: [GOV-05.500-001, GOV-05.500-002]
---

# 05.500 Directory Rename Governance and Refactor Plan

**Document ID:** 05.500  
**Version:** 0.1  
**Date:** 2026-06-09  
**Status:** Draft for Three-Party Review  
**Owner:** Thought Simulator Governance  
**Related:** [05_system_architecture/README.md](../05_system_architecture/README.md), [promotion_protocol.md](../10_thought_simulator_req/docs/promotion_protocol.md), [40.05_master_program_guide.md](../../40_thought_simulator_playground/40.05_master_program_guide.md), [40.510_refactor.md](../../40_thought_simulator_playground/40.510_refactor.md), [30.00_verification_user_guide.md](../../30_verification/30.00_verification_user_guide.md), [50.00_design_traceability_index.md](../../50_thought_simulator_design/50.00_design_traceability_index.md)

## 1. Purpose

This document is the authoritative governance record for the rename and internal reorganization of the former `10_system_architecture/` directory and the resulting structure of the 10-tier. It captures the semantic rationale, the chosen directory structure, naming conventions, blast radius, sequencing, and rules for future similar operations.

The goal is to ensure the repository reflects **intentional architecture** rather than accumulated naming. The 05-tier owns system-architecture governance (meta/cross-layer rules). The 10-tier owns requirement-level design contracts and architecture. The 20-tier owns system requirements.

## 2. Problem Statement and Rationale

The directory previously named `10_system_architecture/` created a naming collision with the 05-tier’s claim to “system architecture” governance. 

- “System architecture” as a governance concept belongs in the 05-tier.
- “System requirements” (HLRs) belong in the 20-tier.
- The 10-tier is responsible for **requirement-level design contracts** and **requirement architecture** — the realization-ready anchors that sit between 20 guidance and 50 design specifications.

Retaining “system architecture” in a 10-tier path blurred these boundaries, made cross-layer traceability harder, and contradicted the tier-independence and naming-convention principles established in 40.05 and promotion_protocol.md.

This refactor removes “system architecture” language from the 10-tier, makes the 20 → 10 hand-off explicit, and organizes the 10-tier’s architecture-related content into semantically coherent sub-ranges.

## 3. Correct Internal Structure of the 10-Tier

The 10-tier’s architecture-related content shall be organized as follows:

```
10_thought_simulator_req/
└── 10_architecture/
    ├── 10.00_system_requirements/          → link / pointer to 20_requirements
    ├── 10.10_design_contract_architecture/
    ├── 10.20_design_contracts/
    └── 10.30_architecture_requirements/
```

### 3.1 Role of Each Sub-Range

- **10.00_system_requirements/**  
  A lightweight link/pointer (not a content duplicate) into `20_requirements/`. This is the explicit entry point that shows where the 10-tier consumes system requirements.

- **10.10_design_contract_architecture/**  
  Requirement-level architecture focused on design contracts (precise, contract-oriented view).

- **10.20_design_contracts/**  
  Clean, primary realization-ready design requirements (least collision-prone, most readable).

- **10.30_architecture_requirements/**  
  Explicit requirement-architecture framing (most direct “architecture requirements” language within the 10-tier).

All three semantic flavors (10.10–10.30) remain inside the 10-tier and are therefore unambiguously requirement-level rather than system-level.

## 4. Naming Conventions and Prefix Rules

- The 10-tier uses `10.xx` numeric sub-ranges for internal organization of architecture-related requirements.
- The outer container `10_architecture/` is a 10-tier container. Its sub-directories must carry the `10.xx` prefix so the entire structure is visibly 10-tier material.
- “System architecture” is reserved for 05-tier governance documents.
- “System requirements” remains in 20; 10.00 is only a link.
- Future additions inside `10_architecture/` shall follow the same `10.xx` banding (e.g., 10.40_…, 10.50_…).

These conventions shall be referenced from promotion_protocol.md, 40.05, 50.05, and the 05.500 plan itself.

## 5. Blast Radius and File Types to Be Scanned

**Core Principle (GOV-05.500-001):**  
**“If a file can contain a path, prefix, or reference, it must be scanned.”**

All of the following must be scanned for the old directory name (`10_system_architecture`), its sub-paths, and prefix patterns (e.g., `10.10.10`, `10.10.50`):

- `.md` (all tiers: 05, 10, 20, 30, 40, 50, 00)
- `.py` (scripts, validators, generators, promotion utilities, harnesses, migration tools)
- `.json` (name tables, artifact manifests, glossary registries, requirement/design-contract maps)
- `.yaml` / `.yml` (schemas, config, requirement maps, design-contract metadata)
- `.toml` (tooling or build configuration)
- `.sh`, `.ps1`, `.bat` (environment, sync, and migration scripts)
- README files in any tier or module
- Wave notes (W1, W2, W3, future waves)
- Promotion rules and flow-down documents (promotion_protocol.md, 05.20, 40.07, etc.)
- Architecture or requirement indexes (50.00_design_traceability_index.md, 30.01_verification_inventory_index.md, name tables)
- Any file containing cross-layer references, directory paths, or prefix patterns

The scan must be performed across **all tiers** (05, 10, 20, 30, 40, 50, and 00_program_governance) plus scripts and archive areas.

## 6. Sequencing of Operations

1. **Create and approve this 05.500 document** (three-party review: CuriousOne23, CP, Grok).
2. **Comprehensive audit** — produce a manifest of every reference (literal paths, prefix patterns, narrative citations).
3. **Update all references** in a controlled pass (using a rename/update script that follows this plan).
4. **Rename directory and internal files** (apply the 10.00 / 10.10 / 10.20 / 10.30 structure).
5. **Update indexes and governance artifacts** (50.00, 30.01, wave notes, promotion_protocol.md, 05.20, 40.07, this 05.500 plan).
6. **Verification** — run link-integrity checks, reference scans, and cross-layer consistency validation. Record results.
7. **Close-out** — update this document with final manifest, verification results, and “Forward-Equivalence State” assertion.

No structural changes shall occur until step 1 is complete.

## 7. Governance Rules for Future Renames

**GOV-05.500-002:** Any future directory rename or cross-layer structural change that affects naming, paths, or references across tiers shall follow the same discipline:

- A dedicated governance document (next available 05.5xx number) shall be created in `05_system_architecture/` before any implementation.
- The document shall record rationale, blast radius (using the “If a file can contain…” principle), file types, sequencing, and verification steps.
- Three-party review and explicit agreement are required.
- A manifest-driven rename/update script (modeled on precedents for 30↔10.50, 40-series, and 50-series) shall be used.
- Post-change verification and index updates are mandatory.
- The change shall be recorded in the relevant wave log (40.510) and tier indexes (50.00, 30.01).

## 8. Core Principle (Reaffirmed)

**“If a file can contain a path, prefix, or reference, it must be scanned.”**

This principle applies to every rename, refactor, or cross-layer structural change. It is the minimum standard for preserving link integrity, traceability, and the intentional architecture of the repository.

## 9. Related Documents and Artifacts

- 05.20_flow_down_protocol_50_to_10.50.md
- 40.07_40_to_10.50_design_requirements_guide.md
- promotion_protocol.md
- 40.05_master_program_guide.md
- 40.510_refactor.md
- 30.00_verification_user_guide.md
- 50.00_design_traceability_index.md
- 50.05_software_spec_construction_guide.md

## 10. Review and Approval

This document requires explicit agreement from CuriousOne23, CP, and Grok before any rename or script execution begins.

**Approval Status**  
- CuriousOne23: ☐  
- CP: ☐  
- Grok: ☐  

Once approved, this document becomes the single source of truth for the 10-tier rename and the resulting 10.00–10.30 structure.

---
**End of 05.500_directory_rename_governance_and_refactor_plan.md**
```

The document above is complete, self-contained, and ready for review. It directly encodes the agreed 10-tier structure, the 10.00 link to 20, the removal of “system architecture” language, the blast-radius principle, sequencing, and future governance rules. No further actions are taken until three-party sign-off.