**Architectural comments on the rename impact and update scope (comments only).**

### 1. Which files will you search for references to the old directory name?

I would search across these categories of files for any occurrence of the old directory name (`10_system_architecture`), its sub-paths, or direct references to its contents:

- All Markdown files containing relative or absolute path references (e.g., `../10_system_architecture/`, `10_thought_simulator_req/10_system_architecture/`, or `10.10.xx` links that resolve through it).
- Files with cross-layer narrative citations (e.g., “see the 10.10 system architecture”, “per 10_system_architecture principles”, or “as defined in the requirement-level architecture”).
- Anchor and internal link targets within Markdown (headings or section IDs that may be referenced from outside).
- Any “include”, “reference”, or traceability mapping files that list canonical sources.
- Wave-note and promotion-related deliverables that document evidence flows or HLR mappings.
- Promotion-rule and flow-down governance documents (the 05.20 and 40.07 guides once moved, plus promotion_protocol.md).
- Cross-layer mapping indexes and inventories (50.00, 30.01, etc.).
- Execution and sync logs (BACKFLOW_*, DESIGN_SYNC_*, FORWARD_FLOW_*, VERIFICATION_SYNC_LOG) that record prior transactions involving the architecture layer.
- Internal 10-series files (both the directory being renamed and the 10.50 design-contract files that cite 10.10 content).
- 20-series HLR and architectural-principles documents that treat the 10.10 content as a foundational anchor.
- 30-series verification artifacts (guides, wave notes, capsules, deltas) that cite architecture contracts for three-flow or traceability statements.
- 40-series governance and module-level artifacts (40.05, 40.510, the 40.07 guide, and any W3-era capsules/deltas that reference the architecture layer).
- 50-series design specs and supporting documents that cite 10.10 as the requirement source.
- Any scripts or validation tools that walk the 10 tree, perform path-based checks, or maintain name tables.

The search scope must be recursive and case-sensitive on path strings, but also broad enough to catch semantic references that do not use the literal directory name.

### 2. Specific files or file patterns expected to be affected

Based on the current structure, these are the files and patterns I expect to contain references that would require updating:

- The entire contents of the directory being renamed itself (`10_thought_simulator_req/10_system_architecture/*.md` and its README), because files inside it reference one another and the parent path.
- `thought_simulator/10_thought_simulator_req/docs/promotion_protocol.md` (multiple sections discuss 10.10 architecture and backward-flow transactions).
- The two governance documents we have been moving:
  - `05.20_flow_down_protocol_50_to_10.50.md` (once placed in 05_system_architecture/)
  - `40.07_40_to_10.50_design_requirements_guide.md` (once placed in 40_thought_simulator_playground/docs/)
- `thought_simulator/50_thought_simulator_design/50.00_design_traceability_index.md` (maps 10.50 anchors and related architecture sources).
- `thought_simulator/50_thought_simulator_design/50.05_software_spec_construction_guide.md` (pre-construction gates and three-flow sections reference 10.10).
- Wave coverage notes and related 30 artifacts:
  - `thought_simulator/30_verification/W1_track_h_wave_coverage_note.md`
  - `thought_simulator/30_verification/W2_conversation_layer_wave_coverage_note.md`
  - `thought_simulator/30_verification/W3_pipeline_a_wave_coverage_note.md`
  - `thought_simulator/30_verification/30.00_verification_user_guide.md`
  - `thought_simulator/30_verification/30.01_verification_inventory_index.md` (especially the W3 promotion table and seeded/promoted rows).
- Multiple 20_requirements/ files (e.g., 20.10_ts_architectural_principles.md, 20.36, 20.37, and other HLR documents that cite 10.10.* as the requirement-level architecture source).
- 10.50 design-requirement files (the 10.50.*.md files that reference 10.10 architecture for contracts or principles).
- The family of logs in `thought_simulator/10_thought_simulator_req/docs/` (BACKFLOW_EXECUTION_LOG_*, DESIGN_SYNC_LOG_*, FORWARD_FLOW_EXECUTION_LOG_*, VERIFICATION_SYNC_LOG_*, ALIGNMENT_LOG_*, etc.).
- 40-series root governance: `thought_simulator/40_thought_simulator_playground/40.05_master_program_guide.md` and `40.510_refactor.md` (wave protocol and log entries).
- 50-series design specs that cite 10.10 (e.g., 50.180_tr_software_spec.md, 50.150_tp_design.md, and others that list 10.10 as source).
- Any name tables, manifests, or validation scripts under `00_program_governance/` or `thought_simulator/scripts/` that reference 10-series paths.
- README files at the 10/, 30/, 40/, and 50/ roots, plus any subsystem_context or architectural_intent documents.

This list is not exhaustive but represents the primary clusters. A full audit would surface additional incidental citations inside individual module capsules or deltas.

### 3. Should the script search for filename changes as well?

Yes, the script should search for and handle internal filename references in the same pass.

The files inside the directory carry legacy “system_architecture” naming (10.10.10_system_architecture.md, etc.). These names are referenced:
- Internally (cross-links between the 10.10.xx files).
- Externally (in 20 HLRs, 30 wave notes, 50 specs, promotion_protocol, the new 05.20 and 40.07 guides, and the 50.00 index).

Treating filename cleanup as a strict second-pass creates a temporary inconsistent state where the directory has a new name but the files inside still advertise the old identity. This would require a second coordinated update wave and risks leaving stale references in the very governance documents that are supposed to demonstrate clarity.

A single pass that (a) renames the directory, (b) updates all path references to the directory, and (c) optionally renames the internal files (with corresponding link updates) is cleaner and more consistent with how prior tier renames (30-1050, 40-series) were handled. The script can make the internal filename renames optional or gated behind a flag if a phased approach is preferred, but the search must include them.

### 4. Should the script search for references in all tiers (05, 10, 20, 30, 40, 50)?

Yes, the script should scan all relevant tiers.

This rename is not a 10-tier-only event. It is a cross-layer identity correction required by the introduction of the 05 tier:

- **05-series**: The new 05.20 flow-down protocol will contain references to 10.10 architecture as the requirement anchor it governs. Leaving stale references here would undermine the very meta-governance the 05 tier is meant to own.
- **10-series**: Obviously the primary location (the directory itself, 10.50 files, docs/, etc.).
- **20-series**: Heavy conceptual and explicit references in HLRs and architectural principles documents.
- **30-series**: Wave notes, 30.00, 30.01, and capsules/deltas that cite the architecture layer for three-flow and traceability.
- **40-series**: 40.05, 40.510, the 40.07 guide, and W3-era module artifacts.
- **50-series**: 50.00 index, 50.05, and design specs that list 10.10 as the source of requirement-level contracts.

Because the directory has served as the stable source of “requirement-level architecture” that the entire forward/backward flow model depends on, the rename propagates into every tier that participates in that model. Limiting the scan to only 10 or 05 would leave the repository in a state where the new 05/10 separation is declared in the directory structure but not enforced in the actual documentation.

### 5. Final Output Summary (comments only)

- **Files to search**: All Markdown files across the repository plus relevant scripts and name tables. Priority categories are the governance documents (promotion_protocol, 05.20, 40.07), indexes (50.00, 30.01), wave notes, 20 HLRs, 50 design specs, the family of execution/sync logs, and the 10.10 files themselves.
- **Files expected to need updating**: The clusters listed in section 2 above (roughly 40–70 files, with the heaviest concentration in 20/30/40/50 governance and the new 05/40 guides). Both path strings and semantic citations must be addressed.
- **Tiers affected**: All of them that participate in the 05/10/20/30/40/50 layering model (05, 10, 20, 30, 40, 50). The rename is a cross-tier event precisely because it clarifies the boundary between meta-architecture (05) and requirement-level architecture (10).
- **Filename-level cleanup**: Should be included in the same pass (or at minimum planned and executed as part of the same coordinated change set) rather than deferred. The internal 10.10.xx files still carry the legacy naming; leaving them untouched would require a second wave of updates and would leave the new 05.20 and 40.07 documents (and the 50.00 index) referencing a mixed namespace.

This scope ensures the rename supports the larger goal of making the repository reflect deliberate architecture rather than accumulated naming conventions. The blast radius is wide but bounded; a manifest-driven script that produces an auditable before/after report is the approach that matches the precedent of prior tier transitions.

These are the architectural comments on search scope, affected files, tiers, and cleanup phasing. No scripts or changes are being generated.