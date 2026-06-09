**Architectural comments on the rename of `10_thought_simulator_req/10_system_architecture/` (comments only).**

### 1. Difficulty Assessment

**How many files are likely to reference this directory?**

A significant number — probably in the range of 40–70+ files, counting both direct path references and indirect conceptual citations. 

Internally, the directory contains roughly 8 primary documents (the 10.10.10 through 10.10.60 series plus README), which reference one another and the parent directory. 

Externally, references appear across:
- The 10-series itself (docs/, 50_design/ READMEs, individual 10.50 files that cite architectural principles).
- 20_requirements/ (many HLRs and architectural principles documents explicitly anchor to 10.10.* content).
- 30_verification/ (30.00 guide, 30.01 inventory, wave coverage notes W1/W2/W3, and various 30.xxx capsules/deltas that cite architecture contracts).
- 40_thought_simulator_playground/ (40.05 master program guide, 40.510 refactor log, the 40.07 guide once moved, and scattered references inside module capsules and deltas).
- 50-series (50.00_design_traceability_index.md, 50.05, multiple 50.xx design specs, and supporting level-2 documents).
- 00_program_governance/ and cross-layer logs (promotion_protocol.md and the family of BACKFLOW_*, DESIGN_SYNC_*, FORWARD_FLOW_*, and VERIFICATION_SYNC_LOG files).
- Scripts and migration tools that walk or validate paths.

The directory name “10_system_architecture” has been used as a stable conceptual anchor for “requirement-level architecture principles,” so references are both literal paths and semantic.

**Does the rename risk breaking cross‑layer links, traceability chains, or wave‑level notes?**

Yes, it carries meaningful risk.

- **Cross-layer links**: High exposure. Relative and absolute markdown links, as well as narrative citations (“see 10_system_architecture/10.10.50…”), are scattered across the 10/20/30/40/50 boundaries. The new 05.20 flow-down protocol and 40.07 guide will also need to be updated once moved.
- **Traceability chains**: Direct impact on 50.00_design_traceability_index.md (which maps 10.50 anchors and related architecture), promotion_protocol.md, and the various execution logs that record flow transactions. These are the exact artifacts that enforce the “10.50 + 30 before 50” and three-flow rules.
- **Wave-level notes**: The W1/W2/W3 coverage notes and the 30.01 W3 promotion table contain explicit references to architecture principles originating in this directory. Breaking those would affect the documented “30 normalize” evidence for the current wave.

Because the directory name has historically been used to signal “the system architecture that lives at the requirements level,” a rename will touch the conceptual spine that ties 20 HLRs → 10.10 → 10.50 → 30 → 50.

**Would this impact any of the promotion or flow‑down scripts?**

It would affect the *inputs and references* used by promotion and flow logic, even if the core rename scripts themselves do not hard-code the path today.

- promotion_protocol.md (the central governance document) contains sections that discuss 10.10 architecture and backward-flow transactions.
- The 05.20 flow-down protocol and 40.07 guide (the two documents we have been moving) will reference architectural contracts that currently live under this directory.
- Any future or existing migration/renumber scripts that touch 10-series identity (similar to the 30-1050 and 40-series tooling) would need updated manifests or search patterns.
- Validation scripts (e.g., the 30↔10.50 pairing validator and any design-sync checks) that walk the 10/ tree or report on architecture anchors would see stale paths until updated.

The rename does not change the *semantics* of the content, but it changes the stable identifiers that the promotion and flow machinery rely on for traceability.

**Is this a low‑risk rename or a high‑risk one?**

This is a **high-risk rename** relative to a simple file rename inside a single module.

It is not high-risk because the content is complex or voluminous in the usual sense; it is high-risk because the directory name functions as a cross-tier contract boundary. The 05 tier is being introduced precisely to own “system-architecture governance,” while this directory owns “requirement-level architecture.” Any rename that touches a name used pervasively as a source of architectural principles will propagate through the exact artifacts (indexes, wave notes, promotion protocol, logs, and the two new governance documents) that are supposed to make the layering intentional.

Precedent from the 30↔10.50 and 40-series renames shows that the project treats these directory-level identity changes as controlled operations precisely because the blast radius is wide even when the conceptual change is small.

### 2. Script Recommendation

Given the established pattern of creating dedicated rename + link-update tooling for previous tier transitions (50-series, 30→20.50, and 40-series), I recommend generating a 10-series directory-rename + link-update script.

The reasons are consistency and risk reduction:

- The same classes of artifacts that required careful handling in prior renames are present here: markdown link graphs, traceability indexes (50.00), wave-level deliverables (W3 note and 30.01), cross-layer governance documents (promotion_protocol and the two new 05/40 guides), and execution logs.
- Manual search-and-replace at this scale is error-prone and would leave the very documents that are supposed to demonstrate architectural clarity in an inconsistent state.
- A script can produce an auditable manifest, update both literal paths and any canonical reference strings, refresh the relevant sections of 50.00 and the wave notes, and generate a post-rename “link integrity” report — the same discipline applied to the earlier tier cleanups.
- Because the 05 tier is new and the two governance documents we moved are still fresh, running the rename through the same controlled mechanism would keep the overall 05/10 layering effort coherent rather than piecemeal.

A script is advisable if the goal is to make the repository reflect deliberate architecture rather than a series of one-off fixes. The precedent already exists; applying the same approach here would be the lowest-surprise path.

These are the architectural observations on difficulty and the script question. No other actions are being taken.