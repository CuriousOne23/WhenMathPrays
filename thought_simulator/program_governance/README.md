# 00 Program Governance

This directory contains governance-level documents that establish project intent, architecture framing, and philosophical context.

Governance documents use a three-level numeric prefix:

- `00.00.xx` for foundations
- `00.10.xx` for architecture
- `00.30.xx` for philosophical companions

## Layout

- [00_foundations/](00_foundations/) - vision, principles, and conceptual grounding (`00.00.xx`)
- [10_architecture/](10_architecture/) - architecture framing and system model references (`00.10.xx`)
- [30_philosophical/](30_philosophical/) - companion philosophical texts (`00.30.xx`)
- [00_foundations/00.00.40_normative_evidence_and_conformance_rules.md](00_foundations/00.00.40_normative_evidence_and_conformance_rules.md) - canonical boundary and conformance precedence rules
- [00_foundations/00.00.41_documentation_tier_map_and_ci_policy.md](00_foundations/00.00.41_documentation_tier_map_and_ci_policy.md) - tier map, inventory vs process docs, structural index updates, CI blocking vs warning policy
- [00_foundations/00.00.43_controlled_identity_rename_policy.md](00_foundations/00.00.43_controlled_identity_rename_policy.md) - controlled identity rename process and name-table SSOT
- [00_identity/](00_identity/) - machine-readable identity name tables (`40`, `10.50`, `30`, `50`)
- [ALIGNMENT_LOG_2026-05-31_10-to-20.md](ALIGNMENT_LOG_2026-05-31_10-to-20.md) - governance alignment record for 10-to-20 model transition
- [BOT_INBOX.md](BOT_INBOX.md) - EVENT inbox
- [BOT_REPORTS/](BOT_REPORTS/) - bot reports
- [CHANGE_LOG.md](CHANGE_LOG.md) - change log
- [CP_TS_governance_brief_2026-08-30.md](CP_TS_governance_brief_2026-08-30.md) - CP/TS governance brief (2026-08-30)

## Role in the 10/20/30/40/50 Model

- Governance documents provide program context.
- They are not executable verification evidence.
- They are not implementation design specifications.

## Governance Boundary: Influence Without Trace Edges

Policy statement:

- Exploratory layers may influence canonical artifacts through human judgment, but they are never part of the formal traceability graph.
- Formal traceability is canonical-only and is limited to canonical requirements, canonical design, and canonical verification artifacts.
- Exploratory content may be speculative, contradictory, incomplete, wrong, or abandoned without creating governance debt.
- Promotion rationale must be preserved in human-readable channels (for example: decision notes, promotion summaries, rationale documents, and commit history), not by adding formal dependency edges from exploratory layers.

Boundary intent:

- Preserve the why in exploration without elevating exploratory material into ground truth.
- Preserve the what in canonical layers through strict validation and stable trace semantics.
