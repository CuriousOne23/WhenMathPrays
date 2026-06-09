# Contributor Change Workflow

## Purpose

Use this guide when you need to change Thought Simulator documents or module artifacts while preserving the canonical workflow and CI guarantees.

## Operating Principle: Attached Exploration, Protected Canon

This workflow is designed to preserve a useful tension:

- Exploration remains fast and creative in `20_requirements/` and `40_thought_simulator_playground/`.
- Canonical artifacts remain formal, stable, and reviewable in `10_thought_simulator_req/`, `30_verification/`, and `50_thought_simulator_design/`.
- Promotion is intentional, not accidental: exploratory work informs canonical work through explicit approval, verification, and traceability updates.

Use this principle as the default decision rule whenever you are unsure where a change belongs.

## Scope

This workflow applies to edits under:

- `00_program_governance/`
- `10_thought_simulator_req/`
- `20_requirements/`
- `30_verification/`
- `40_thought_simulator_playground/`
- `50_thought_simulator_design/`

## Required Sequence

1. Identify your tier and intent.
- Exploratory updates belong in `20_requirements/` and `40_thought_simulator_playground/`.
- Canonical updates belong in `10_thought_simulator_req/`, `30_verification/`, and `50_thought_simulator_design/`.

2. If adding or evolving a new `40.*` module, follow Two-Phase execution.
- Phase A: update only `software_description.md` and obtain explicit human approval.
- Phase B: then produce `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

3. Keep canonical trace purity.
- Formal trace links stay canonical-to-canonical.
- Exploratory documents may inform decisions but do not become formal trace edges.

4. Update glossary, README, or tier inventory when terminology or **structure** changes.
- If verification terminology changes, update `30_verification/30.30_verification_glossary.md` and `30_verification/glossary_term_registry.json` in the same change.
- If requirements-tier terminology changes, update `20_requirements/archive/20.150_glossary.md` and `20_requirements/glossary_term_registry.json` in the same change.
- For 50-series design terminology (especially new concepts introduced in design specs), update `50_thought_simulator_design/50.01_50_series_glossary.md` and `50_thought_simulator_design/glossary_term_registry.json`.
- `20.150_glossary.md` is scoped to `20_requirements/` documents.
- If folders/files are added, removed, moved, or renamed, update relevant `README.md` files.
- If a **30 verification module** is added, renamed, or removed, update `30_verification/30.01_verification_inventory_index.md` in the same change set.
- If a **level-1 50 design file** is added, renamed, or removed, update `50_thought_simulator_design/50.00_design_traceability_index.md` in the same change set.
- Outside `40_thought_simulator_playground/`, references must point to the canonical glossary at `30_verification/30.30_verification_glossary.md` (not the exploratory 40 glossary).

**Do not** update tier inventory indexes (`30.01`, `50.00`) for content-only edits to capsules, deltas, or design specs.

### Controlled identity renames (40, 30, 10.50, 50)

Address-only renames (filename, folder, band, slug) are **identity maintenance** — not content review. Use the controlled rename pipeline:

1. Author an approved request JSON from [00_identity/rename_request.template.json](00_program_governance/00_identity/rename_request.template.json)
2. Run `scripts/rename_identity.py --request <file> --plan` and review the plan
3. Run `scripts/rename_identity.py --request <file> --apply --yes` in one atomic PR
4. Update human-readable inventories (`30.01`, `50.00`, `40.510`) in the same change set
5. Run `validate_name_tables.py`, `validate_shorthand_usage.py`, and the full pre-PR validation suite below

Band-only shorthand (e.g. `40.100`, `50.220`) is legal only in locations declared in [shorthand_registry.json](00_program_governance/00_identity/shorthand_registry.json). Never use bare band shorthand in Python files or outside governed contexts.

**30 ↔ 10.50** renames are always **atomic** (both peers in one PR). **40** and **50** renames are tier-standalone but must propagate live cross-tier references.

**Phased bulk migration** (many modules at once): use an approved manifest in `00_identity/` plus the tier pipeline in [00.00.43 §11.2](00_program_governance/00_foundations/00.00.43_controlled_identity_rename_policy.md) — **not** bare band substring replace across the tree.

Recommended order for full-program alignment: **40 → 10.50+30 → 50**.

```powershell
# Example: Phase-2 coupled pass (plan first, then apply)
python thought_simulator/scripts/apply_30_1050_renumber_migration.py --plan
python thought_simulator/scripts/apply_30_1050_renumber_migration.py --apply --yes
python thought_simulator/scripts/fix_30_1050_post_renumber_refs.py
python thought_simulator/scripts/fix_post_renumber_residual_refs.py
# Then run blocking validators (00.00.43 §11.4)
```

Tier equivalents: `apply_40_*` + `fix_40_post_renumber_refs.py`; `apply_50_*` + `fix_50_post_renumber_refs.py`. Manifests are immutable audit records — fix scripts skip `00_identity/`. New substring fallout: append rows to `fix_post_renumber_residual_refs.py`, re-run, log in `archive/refactors/`.

Full policy: [00.00.43_controlled_identity_rename_policy.md](00_program_governance/00_foundations/00.00.43_controlled_identity_rename_policy.md). Identity SSOT: [00_identity/](00_program_governance/00_identity/).

**50-series glossary helper scripts** (in `thought_simulator/scripts/`):
- `validate_50_glossary_alignment.py`: Non-blocking CI check that runs on changes to 50 design `.md` files (and the glossary/registry itself). It warns when the glossary and registry are out of alignment or when new candidate terms are observed in design documents. This provides visibility ("we should know") without blocking merges.
- `update_50_glossary.py`: Local helper tool to analyze current 50 design documents against the glossary and registry. It produces a report of drift and concrete proposals (terms to add, suggested registry entries). By default it only prints; use `--write-proposals` to generate reviewable `PROPOSED_*` files. **It never auto-edits** the real glossary or registry. The goal is to reduce token usage by doing mechanical scanning and proposal generation locally or via terminal, while keeping full human control over what gets updated. Run it when working in 50-series design to stay efficient.

5. Run the doc validation suite before opening a PR.

   The detailed rules for what must be produced in `30_verification/` (verification capsules, requirements deltas, run artifacts, three-flow statements) are in `30_verification/30.00_verification_user_guide.md`.

## Document tier inventories

| Tier | Inventory / traceability doc | Process guide |
|------|------------------------------|---------------|
| 30 verification | [30.01_verification_inventory_index.md](30_verification/30.01_verification_inventory_index.md) | [30.00_verification_user_guide.md](30_verification/30.00_verification_user_guide.md) |
| 50 design | [50.00_design_traceability_index.md](50_thought_simulator_design/50.00_design_traceability_index.md) | [50.05_software_spec_construction_guide.md](50_thought_simulator_design/50.05_software_spec_construction_guide.md) |

Repo tier map: [README.md](README.md).

## CI check matrix

Scripts live under `thought_simulator/scripts/`. **Blocking** checks fail the GitHub Actions job. **Warning** checks print drift and exit 0.

| Script / workflow | Mode | Scope |
|-------------------|------|--------|
| `check_doc_dependencies.py` | Blocking | Doc dependency graph |
| Governance marker validation (workflow inline) | Blocking | Required phrases in USER_GUIDE, promotion_protocol, 30 README, 40.05, 50.05 |
| Rename maintenance guard (workflow inline) | Blocking | Renames in 30/40/50/10.50 require identity tables and tier inventories (`30.01`, `50.00`, `40.510` for 40-only) |
| `validate_doc_frontmatter_and_ids.py` | Blocking | Frontmatter and document IDs |
| `validate_relation_semantics.py` | Blocking | Relation semantics in governed docs |
| `validate_doc_naming_prefixes.py` | Blocking | Document naming prefixes |
| `validate_doc_reference_targets.py` | Blocking | Broken file refs and heading anchors |
| `validate_20_traceability_matrix.py` | Blocking | 20-series traceability matrix |
| `validate_design_traceability.yml` (workflow) | Blocking | Level-1 `50.*.md` ↔ `50.00` table |
| `validate_readme_links.py` | Blocking | README link targets exist |
| `validate_glossary_alignment.py` | Warning | 30.160 glossary ↔ registry |
| `validate_requirements_glossary_alignment.py` | Warning | 20 glossary ↔ registry |
| `validate_requirements_glossary_scope.py` | Warning | 20 glossary scope |
| `validate_50_glossary_alignment.py` | Warning | 50.01 glossary ↔ registry |
| `validate_readme_coverage.py` | Warning | README child links ↔ directory |
| `validate_30_inventory_index.py` | Warning | `30.01` module table ↔ `30.*` dirs |
| `validate_30_10_50_pairing.py` | Warning | `30.01` `promoted`/`approved` rows ↔ `10.50.{band}_*.md` (one-way; no orphan 10.50 check) |
| `validate_50_traceability_index.py` | Warning | `50.00` table ↔ level-1 design files (local mirror of blocking workflow) |
| `validate_name_tables.py` | Warning | Identity name tables ↔ filesystem; 30 ↔ 10.50 band pairing |
| `rename_identity.py` | Tool | Controlled identity rename pipeline (dry-run / apply) |
| `bootstrap_name_tables.py` | Tool | Bootstrap or refresh name tables from disk |
| `validate_shorthand_usage.py` | Warning | Band-prefix shorthand only in governed contexts |

Workflow file: [.github/workflows/thought-simulator-doc-dependency-check.yml](../.github/workflows/thought-simulator-doc-dependency-check.yml), [.github/workflows/validate_design_traceability.yml](../.github/workflows/validate_design_traceability.yml).

## Pre-PR Validation Command

Run from repository root:

```powershell
Set-Location c:/Users/jeffg/Documents/GitHub/WhenMathPrays ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_doc_reference_targets.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_readme_coverage.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_readme_links.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_glossary_alignment.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_requirements_glossary_alignment.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_50_glossary_alignment.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_30_inventory_index.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_30_10_50_pairing.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_50_traceability_index.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_name_tables.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_shorthand_usage.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/update_50_glossary.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/check_doc_dependencies.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_doc_frontmatter_and_ids.py --require-frontmatter --strict-ids ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_relation_semantics.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_doc_naming_prefixes.py
```

## Authoritative Process Sources

- `00_program_governance/00_foundations/00.00.41_documentation_tier_map_and_ci_policy.md` (tier map, inventory vs process, CI policy)
- `00_program_governance/00_foundations/00.00.43_controlled_identity_rename_policy.md` (controlled identity rename process)
- `00_program_governance/00_identity/` (identity name tables)
- `10_thought_simulator_req/docs/promotion_protocol.md`
- `50_thought_simulator_design/50.05_software_spec_construction_guide.md`
- `30_verification/30.00_verification_user_guide.md` (verification process, artifact standards, and three-flow rules)
- `30_verification/30.01_verification_inventory_index.md` (30-tier module inventory)
- `50_thought_simulator_design/50.00_design_traceability_index.md` (cross-layer design traceability)
- `30_verification/30.30_verification_glossary.md`

## Pull Request Checklist

- [ ] Changes are placed in the correct tier.
- [ ] Any moved/renamed/deleted references were corrected.
- [ ] README links and direct-child indexes remain aligned.
- [ ] Glossary and glossary registry were updated together when terminology changed.
- [ ] `30.01` / `50.00` updated when module or level-1 design **structure** changed.
- [ ] `10.50.xx` peer exists for every `30.01` row marked `promoted` or `approved` (or Notes record `30-only pending 10.50` while debt is open).
- [ ] Validation suite passes locally (includes `validate_30_10_50_pairing.py` warning check).
- [ ] Bulk renumber PRs: manifest unchanged (pre-migration IDs), tier fixer + `fix_post_renumber_residual_refs.py` run, refactor log in `archive/refactors/`.