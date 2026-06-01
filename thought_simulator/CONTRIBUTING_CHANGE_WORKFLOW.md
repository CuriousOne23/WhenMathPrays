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

4. Update glossary or README surfaces when terminology or structure changes.
- If verification terminology changes, update `30_verification/30.30_verification_glossary.md` and `30_verification/glossary_term_registry.json` in the same change.
- If requirements-tier terminology changes, update `20_requirements/archive/20.150_glossary.md` and `20_requirements/glossary_term_registry.json` in the same change.
- `20.150_glossary.md` is scoped to `20_requirements/` documents.
- If folders/files are added, removed, moved, or renamed, update relevant `README.md` files.
- Outside `40_thought_simulator_playground/`, references must point to the canonical glossary at `30_verification/30.30_verification_glossary.md` (not the exploratory 40 glossary).

5. Run the doc validation suite before opening a PR.

## Pre-PR Validation Command

Run from repository root:

```powershell
Set-Location c:/Users/jeffg/Documents/GitHub/WhenMathPrays ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_doc_reference_targets.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_readme_coverage.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_readme_links.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_glossary_alignment.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/check_doc_dependencies.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_doc_frontmatter_and_ids.py --require-frontmatter --strict-ids ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_relation_semantics.py ; \
  c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe thought_simulator/scripts/validate_doc_naming_prefixes.py
```

## Authoritative Process Sources

- `10_thought_simulator_req/docs/promotion_protocol.md`
- `50_thought_simulator_design/50.05_software_spec_construction_guide.md`
- `30_verification/30.30_verification_glossary.md`

## Pull Request Checklist

- [ ] Changes are placed in the correct tier.
- [ ] Any moved/renamed/deleted references were corrected.
- [ ] README links and direct-child indexes remain aligned.
- [ ] Glossary and glossary registry were updated together when terminology changed.
- [ ] Validation suite passes locally.
