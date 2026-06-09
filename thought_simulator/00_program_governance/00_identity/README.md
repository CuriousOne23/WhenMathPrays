# Identity Name Tables

Machine-readable canonical identity registry for controlled renames across tiers 40, 30, 10.50, and 50.

## Files

| File | Tier |
|------|------|
| `40_name_table.json` | Playground module folders |
| `10.50_name_table.json` | Design-requirements anchors |
| `30_name_table.json` | Verification module folders |
| `50_name_table.json` | Design specification files |
| `rename_request.template.json` | Example rename request for `rename_identity.py` |
| `shorthand_registry.json` | Governed locations where band-only prefix shorthand is legal |

## Policy and targets

- **Controlled renames (normative):** [00.00.43_controlled_identity_rename_policy.md](../00_foundations/00.00.43_controlled_identity_rename_policy.md)
- **Naming layout target (guidance only):** [naming_strategy_target.md](naming_strategy_target.md)
- **40 renumber manifest (executed 2026-06-09):** [40_renumber_manifest.json](40_renumber_manifest.json)

## Commands

```powershell
# Bootstrap / refresh tables from disk
python thought_simulator/scripts/bootstrap_name_tables.py

# Validate tables
python thought_simulator/scripts/validate_name_tables.py

# Plan a rename (dry-run) — copy rename_request.template.json first
python thought_simulator/scripts/rename_identity.py --request thought_simulator/00_program_governance/00_identity/my_rename.json --plan

# Apply after review
python thought_simulator/scripts/rename_identity.py --request thought_simulator/00_program_governance/00_identity/my_rename.json --apply --yes
```

Scripts: [rename_identity.py](../../scripts/rename_identity.py), [bootstrap_name_tables.py](../../scripts/bootstrap_name_tables.py), [validate_name_tables.py](../../scripts/validate_name_tables.py), [validate_shorthand_usage.py](../../scripts/validate_shorthand_usage.py).

Human-readable inventories (`30.01`, `50.00`, `40.510`) must stay aligned with these tables after any rename.