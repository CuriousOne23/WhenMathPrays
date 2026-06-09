**Architectural comments on the rename strategy for `10_thought_simulator_req/10_system_architecture/` (comments only).**

### 1. How to perform this rename cleanly

The rename is a cross-tier identity correction, not a simple filesystem move. The correct sequence should prioritize **audit and controlled propagation** over direct editing to protect the intentional layering we are establishing.

Recommended high-level sequence:
- Begin with a comprehensive, read-only reference audit that produces a manifest of every literal path, relative link, narrative citation, and canonical anchor that mentions the old directory name or its internal files. This audit should cover all tiers (00 through 50) plus scripts and logs, because the directory has historically served as the source of “requirement-level architecture principles.”
- Perform all reference updates in a single coordinated pass before or atomically with the directory rename itself. Updating references first reduces the window during which the tree is in an inconsistent state; performing the directory rename first would create a larger surface of broken links that must then be chased.
- Treat internal filename changes (the 10.10.xx files that still carry “system_architecture” language) as a related but secondary phase. They can be addressed in the same script run or a follow-on pass, but they should be declared explicitly in the plan so the semantic cleanup is not left half-done.
- After the structural change, run a verification pass that confirms no dangling references remain in the key governance artifacts (promotion_protocol.md, the new 05.20 and 40.07 documents, 50.00 index, wave coverage notes, 30.01, and the various sync/execution logs). This verification step is what turns the rename from a mechanical operation into an architectural one.

The goal at every step is to keep the 05 tier’s claim to meta/cross-layer governance distinct from the 10 tier’s role as requirement-level design-contract architecture. Any sequence that leaves broken links in the new 05.20 flow-down protocol or the 40.07 guide would undermine the very clarity the 05 tier is meant to provide.

### 2. What the rename script should do

Given the established precedent of controlled rename tooling for the 50-series, the 30→20.50 transition, and the 40-series, a 10-series directory-rename + link-update script is the appropriate mechanism. It should be modeled on the same discipline: manifest-driven, auditable, and capable of producing a post-operation integrity report.

A well-scoped script for this case should:
- Accept the old directory path and the chosen new name as explicit inputs, so the decision between `10_design_contracts/`, `10_design_contract_architecture/`, or `10_architecture_requirements/` remains human-controlled.
- Update all literal filesystem paths and all Markdown relative/absolute links that point into the directory.
- Scan and correct cross-layer narrative references (e.g., “see 10_system_architecture/10.10.50…” or “per the 10.10 architecture contracts”) in 20_requirements, 30 wave notes and guides, 40.05/40.510/40.07, 50 specs and 50.00 index, promotion_protocol.md, and the family of BACKFLOW/DESIGN_SYNC/FORWARD_FLOW logs.
- Handle internal anchor updates inside the moved files themselves if any heading IDs or section references are path-sensitive.
- Optionally include (or be paired with) a pass that renames the internal 10.10.xx files to remove the legacy “system_architecture” wording, producing a before/after map so downstream consumers know the new canonical names.
- Generate a clear change manifest and a “link integrity / traceability preservation” report that can be attached to the commit or the relevant 40.510 / wave log entry. This mirrors the “Forward-Equivalence State” assertions used in prior controlled flows.
- Be idempotent or at least produce a dry-run mode so the impact can be reviewed before the actual tree mutation.

The script should not attempt to rewrite conceptual content—only identifiers and paths. That boundary keeps the operation aligned with the “comments and controlled change” pattern used successfully for the other tier transitions.

### 3. Expected blast radius

The blast radius is wide and multi-tier, not confined to the 10-series. 

Rough estimate based on the structure: direct path or strong conceptual references are likely present in 40–70 files, with the heaviest concentration in:
- 20_requirements (HLRs and architectural principles that treat the 10.10 content as foundational).
- 30_verification (30.00, 30.01, the three wave coverage notes, and multiple 30.xxx capsules/deltas).
- 40_thought_simulator_playground (40.05, 40.510, the 40.07 guide, and scattered citations inside W3-era modules).
- 50-series (50.00 index, 50.05, and numerous design specs plus level-2 documents).
- 10/docs/ (promotion_protocol.md and the full set of sync/execution logs).
- 00_program_governance and any migration or validation scripts that walk the 10 tree.

Because the directory name has been used as a stable source of “system architecture at the requirements level,” the rename will touch the exact artifacts that document the 05/10 separation we are trying to make visible. It therefore propagates into the new 05.20 flow-down protocol and the 40.07 guide by design.

Timing-wise, this rename should be completed **before** the next wave of design-contract stabilization or further 50 insight work on W3. Performing it afterward would risk compounding the very ambiguity we are trying to remove; the new governance documents and wave notes would then be written against an inconsistent namespace.

### 4. Final goal alignment

This operation directly serves the objective of making the repository reflect deliberate architecture rather than accumulated naming. By giving the 10-tier directory a name that unambiguously signals “requirement-level design contracts” while reserving “system_architecture” language for the 05 tier, we strengthen the spine that runs 05 (meta-governance) → 10 (requirements anchors) → 30 (verification) → 40 (playground authoring) → 50 (specs).

The fact that internal filenames still carry the old language is a signal that the cleanup has two layers: the directory identity (this rename) and the file-level identity (a follow-on but related task). Addressing them through the same controlled script discipline used for prior tier transitions keeps the work coherent with the larger 05-introduction effort.

These comments address the sequence, script responsibilities, blast radius, and timing. No implementation actions are being taken.