# Tier Naming Strategy (Target — Non-Normative)

## Status

| Field | Value |
|-------|-------|
| **Kind** | Guidance / target / anti-drift reminder |
| **Authority** | **Does not** override normative policy or CI |
| **When this conflicts with policy** | [00.00.41](../00_foundations/00.00.41_documentation_tier_map_and_ci_policy.md), [00.00.42](../00_foundations/00.00.42_document_addressing_and_insertion_policy.md), and [00.00.43](../00_foundations/00.00.43_controlled_identity_rename_policy.md) win |
| **When this conflicts with disk** | Operational inventories win for *what exists*; this document wins for *what we are trying to do next* |

This document records the **target numbering layout** we are working toward across tiers **40**, **10.50**, **30**, and **50**. It is a **should**, not a governance requirement. Use it in planning and review to reduce drift; do not treat deviation as a CI failure unless a separate normative rule applies.

---

## 1. Purpose

- Remind contributors and agents of the **intended band layout** across design-related tiers.
- Anchor **discussion** when adding modules, planning renumbers, or reviewing alignment.
- Record **what was attempted** in prior cleanup passes and the **planned migration order**.
- Separate **must** (CI / policy) from **prefer** (this document).

**Not in scope:** full old→new mapping tables (those live in migration artifacts, name tables, and tier inventories during execution), or repetition of insertion mechanics (see [00.00.42](../00_foundations/00.00.42_document_addressing_and_insertion_policy.md)).

---

## 2. Normative boundary

| Topic | Enforced? | Where |
|-------|-----------|-------|
| 30 band **must** match 10.50 band (for promoted/approved rows) | **Yes** (CI warning) | `validate_30_10_50_pairing.py`, [00.00.41](../00_foundations/00.00.41_documentation_tier_map_and_ci_policy.md) |
| 40, 20, 50 bands independent of each other and of 30/10.50 | **Yes** (policy) | [00.00.41](../00_foundations/00.00.41_documentation_tier_map_and_ci_policy.md) |
| Subfield insertion when primary bands are crowded | **Yes** (policy) | [00.00.42](../00_foundations/00.00.42_document_addressing_and_insertion_policy.md) |
| Controlled identity renames | **Yes** (process) | [00.00.43](../00_foundations/00.00.43_controlled_identity_rename_policy.md), name tables in this directory |
| Stride-10 module bands from `.50`, zone layout, 50 nesting, 40 cleanup order | **No** — target only | **This document** |
| 50 primary band aligned with 10.50/30 when practical | **No** — target only | **This document** |

---

## 3. Shared target pattern

Across tiers that use numeric bands, we **prefer** the same mental model:

| Zone | Typical range | Intended use |
|------|---------------|--------------|
| **Governance** | `xx.00`–`xx.09` | Indexes, user guides, construction guides, glossaries |
| **Headroom** | `xx.10`–`xx.49` | Support artifacts, cross-cutting docs, one-off inserts, tier-only material |
| **Modules** | `xx.50`+ | Subsystem prototypes (40), requirements anchors (10.50), verification folders (30), Level-1 design specs (50) |

**Stride:** primary module bands **should** increment by **10** (`50`, `60`, `70`, …) to leave room for insertions.

**Growth when a band fills:** use dotted subfields (`.010`, `.020`, …) per [00.00.42](../00_foundations/00.00.42_document_addressing_and_insertion_policy.md). Deeper nesting (4th, 5th, … numeric parts) is allowed repository-wide; 50 uses this most often for design detail.

**Slug rule:** the numeric band is the stable address; the slug (`_regulator_prototypes`, `_design_spec`, etc.) carries human meaning. Slugs need not match across tiers.

---

## 4. Coupling matrix

| Pair | Target relationship |
|------|---------------------|
| **10.50 ↔ 30** | **Must** share the same primary band for coupled modules. 10.50 leads as the requirements anchor; 30 folder `30.{band}_*` matches `10.50.{band}_*.md`. Renames **should** be atomic (`tier: "30-1050"` in rename requests). |
| **50 ↔ 10.50/30** | **Should** use the same primary band for Level-1 design specs that belong to a coupled subsystem. Not CI-enforced. |
| **40 ↔ anything** | **Independent.** Evidence from `40.{any}` may promote to `10.50.{band}` + `30.{band}` where `{band}` is chosen at promotion time, not copied from 40. |
| **20** | Out of scope for this strategy; frozen unless a separate 20 hygiene effort is approved. |

```
40 (independent)  →  establish playground layout
        ↓
10.50 + 30 (coupled)  →  canonical module band table
        ↓
50 (independent, prefer alignment)  →  match Level-1 bands; nest extras
```

---

## 5. Per-tier targets

### 5.1 Tier 40 (playground)

**Shape:** `40_thought_simulator_playground/40.{band}_{slug}/` module folders.

| Item | Target |
|------|--------|
| Process guide | Move toward `40.05_*` (governance zone), not a module band |
| Program inventory | **`40.510_refactor.md` stays fixed** — row IDs like `40.510-409` are ledger keys, not module folder bands |
| Module folders | **Should** start at **`40.50`**, stride **10**, after deduplication |
| Low zone `40.00`–`40.49` | Governance, support, and insertion headroom — not crowded module names |
| Bands ≥ `500` | **Should not** blindly stride into `40.510` (inventory doc collision). Cap or jump (e.g. `40.550+`) with explicit rows in 40.510 |

**Operational SSOT:** [40.510_refactor.md](../../40_thought_simulator_playground/40.510_refactor.md), [40_name_table.json](40_name_table.json). Process: [40.05_master_program_guide.md](../../40_thought_simulator_playground/40.05_master_program_guide.md).

**Independence reminder:** `40.100_*` (core structs) evidence may promote to `30.140` / `10.50.42` without matching 40 band numbers to 30/10.50.

### 5.2 Tier 10.50 (design requirements anchors)

**Shape:** flat files `10_thought_simulator_req/50_design/10.50.{band}_{slug}.md`.

| Item | Target |
|------|--------|
| New subsystem anchors | **Should** take the next free stride-10 band agreed with 30 in the same change set |
| Governance | No separate low band required today; this directory is requirements anchors only |
| Orphan 10.50 without 30 | Allowed (10.50 may precede 30); document in `30.01` Notes until paired |

**Operational SSOT:** [10.50_name_table.json](10.50_name_table.json), pairing via [30.01](../../30_verification/30.01_verification_inventory_index.md).

### 5.3 Tier 30 (verification)

**Shape:** `30_verification/30.{band}_{slug}/` module directories.

| Item | Target |
|------|--------|
| Module folders | **Should** match **10.50 `{band}`** for promoted/approved subsystems |
| Governance | `30.00`, `30.01`, glossaries, exemplars stay in **`30.00`–`30.09`** (and similar meta paths) — not module bands |
| Insertions under a module | `30.{band}.010_*` subfolders or files per 00.00.42 |

**Operational SSOT:** [30.01_verification_inventory_index.md](../../30_verification/30.01_verification_inventory_index.md), [30_name_table.json](30_name_table.json). Process: [30.00_verification_user_guide.md](../../30_verification/30.00_verification_user_guide.md).

### 5.4 Tier 50 (design specifications)

**Shape:** primarily flat `50_thought_simulator_design/50.{band}_{slug}.md`; optional depth for support.

| Level | Form | Target use |
|-------|------|------------|
| **Level 1** | `50.{band}_*` | Main subsystem design spec — **should** use same `{band}` as 10.50/30 when the doc belongs to that subsystem |
| **Level 2** | `50.{band}.{yy}_*` | Supporting design detail (stride **10** at `.yy` per [50.05](../../50_thought_simulator_design/50.05_software_spec_construction_guide.md): `.10`, `.20`, …) |
| **Level 3+** | `50.{band}.{yy}.{zz}_*` or `50.{band}.010_*` | Rare or crowded-band insertions per 00.00.42 |

**50 governance may differ from 30+10.50:** platform and cross-cutting design (`50.07`–`50.270` system/architecture/contract today) **should** live in **`50.00`–`50.49`**, not in a module band that implies a 30 peer.

**Nesting rule (anti-drift):** if 10.50+30 already own band `N` for a subsystem, 50 **should not** open a second Level-1 primary at a different band for the same subsystem. Prefer:

- one `50.{N}_*` Level-1 spec, and
- additional material at `50.{N}.010_*`, `50.{N}.10_*`, or deeper.

**Operational SSOT:** [50.00_design_traceability_index.md](../../50_thought_simulator_design/50.00_design_traceability_index.md), [50_name_table.json](50_name_table.json). Process: [50.05_software_spec_construction_guide.md](../../50_thought_simulator_design/50.05_software_spec_construction_guide.md).

---

## 6. Planned migration order

When executing a coordinated cleanup (controlled renames per 00.00.43):

1. **Phase 1 — 40:** Dedupe survivors → map to `40.50+` stride 10 → relocate process guide toward `40.05` → update `40_name_table` + 40.510 rows together.
2. **Phase 2 — 10.50 + 30:** Produce a **band manifest** (subsystem → `{band}`); rename both sides atomically; update `30.01` and `10.50_name_table` / `30_name_table`.
3. **Phase 3 — 50:** Align Level-1 docs to the phase-2 band table where practical; fold extras into Level-2+; keep documented exceptions in `50.00`.

After each phase, record alignment status in §8 below — do not duplicate full inventories in this file.

---

## 7. Known exceptions (target ledger)

Document intentional deviation here when the target cannot be met yet. Update when resolved.

| Item | Current state | Target disposition |
|------|---------------|-------------------|
| ~~`50.140.010_data_structures`~~ | ~~Misaligned~~ | **Resolved 2026-06-09** — nested `50.140.010_data_structures` |
| ~~`50.09_geometry_engine`~~ | ~~Misaligned~~ | **Resolved 2026-06-09** — `50.270_geometry_engine_design` |
| ~~Dual `50.40_*` (scheduler + interaction)~~ | ~~Two primaries~~ | **Resolved 2026-06-09** — `50.210_scheduler` + `50.210.010_interaction_layer` |
| `50.70`/`50.80`/`50.90` duplicate bands | Headroom docs share bands with component peers | **Expected** — `shorthand_eligible: false` for duplicates; use full canonical paths |
| `50.07`–`50.08` platform docs | No 10.50/30 peers | Keep in 50 governance/headroom zone — **expected** exception |
| `40.510_refactor.md` | Fixed inventory filename | Never assign as a module folder band |
| 40 duplicate bands (`40.110_*`×2, `40.500_*`×2, etc.) | ~~Pre-cleanup drift~~ | **Resolved 2026-06-09** — 17 duplicates removed in Phase-1 renumber |
| Historical 40 compression | See 00.00.42 §10 | Superseded by Phase-1 `40.50+` layout; retained for traceability only |

For a live list of disk-vs-target gaps, see [30.01](../../30_verification/30.01_verification_inventory_index.md), [50.00](../../50_thought_simulator_design/50.00_design_traceability_index.md), and [40.510](../../40_thought_simulator_playground/40.510_refactor.md).

---

## 8. What we attempted (historical)

| When | What | Outcome / notes |
|------|------|-----------------|
| pre-renumber branch | 40 folder compression to stride-10 subdirectories while preserving `40.510` | Recorded in [00.00.42 §10](../00_foundations/00.00.42_document_addressing_and_insertion_policy.md); interim layout (`40.420`–`40.540` range) |
| 2026-06 | Identity rename infrastructure (name tables, `rename_identity.py`, 00.00.43) | Enables phased migration without content re-review |
| 2026-06-09 | Phase-1 40 renumber (`40_renumber_manifest.json`, `apply_40_renumber_migration.py`) | 31 survivors at `40.50`–`40.350` stride 10; 17 duplicates removed; guide at `40.05` |
| 2026-06-09 | Phase-2 10.50+30 renumber (`30_1050_renumber_manifest.json`, `apply_30_1050_renumber_migration.py`) | 23 coupled pairs at stride 10 from `.50`; `fix_30_1050_post_renumber_refs.py` for governance-doc repair |
| 2026-06-09 | Phase-3 50 renumber (`50_renumber_manifest.json`, `apply_50_renumber_migration.py`) | 27 file renames; level-2 nest for interaction/data structs; `fix_50_post_renumber_refs.py` for 50.00 rebuild |
| 2026-06-09 | Post-pass residual cleanup (`fix_post_renumber_residual_refs.py`) | Manifest-driven + `CASCADE_REPAIRS` / `FILE_SPECIFIC_REPAIRS`; strips forbidden 50→40 path refs; repairs substring collisions (e.g. `30.220_inb` → `30.50_inb`); **does not** modify manifest JSON |

**Alignment checkpoint (update after migrations):**

- **As of:** 2026-06-09
- **40 vs target:** **aligned** — modules `40.50`–`40.350` stride 10; governance `40.05` + fixed `40.510`; see [40_renumber_manifest.json](40_renumber_manifest.json)
- **10.50+30 vs target:** **aligned** — coupled pairs at `50`–`270` stride 10; see [30_1050_renumber_manifest.json](30_1050_renumber_manifest.json)
- **50 vs target:** **aligned** — subsystem Level-1 specs at `50`–`270` stride 10; headroom at `50.42`/`50.43`; see [50_renumber_manifest.json](50_renumber_manifest.json)

---

## 9. Drift-check questions (PR / planning)

Use these as soft review prompts — not CI gates:

1. Does a new **30** folder band match its **10.50** peer (if promoted/approved)?
2. Is a new **50 Level-1** file using a band that already has a different subsystem spec (duplicate primary)?
3. Could an extra **50** doc nest under an existing parent band instead of taking a new primary?
4. Does a new **40** module avoid the `40.00`–`40.49` and `40.510` reserved zones?
5. Is the next module band the next stride-10 slot in the tier inventory, not an ad hoc gap-fill?
6. If deviating from this document, is the exception noted in §7 or the relevant tier inventory Notes?
7. For bulk migration PRs: does the change set include the approved manifest, name-table updates, and inventory rows — with **no** bare band substring replace?
8. After a bulk pass: were governance tokens checked (`40.05` guide, `40.160_tp` module vs guide shorthand) and blocking validators (§00.00.43 §11.4) run clean?
9. Was `fix_post_renumber_residual_refs.py` run after tier fixers, with any new collision rows appended to that script rather than hand-edited across canon?
10. Are manifests left immutable (pre-migration `entry_id` values preserved) and refactor logs written under `archive/refactors/`?
11. For 50 design specs: do cross-layer source lists avoid `40_thought_simulator_playground/` prefixes and use aligned `Document ID` / `LLR-50.{band}-` values?

---

## 10. Related documents

| Document | Role |
|----------|------|
| [00.00.41](../00_foundations/00.00.41_documentation_tier_map_and_ci_policy.md) | Normative tier map and CI |
| [00.00.42](../00_foundations/00.00.42_document_addressing_and_insertion_policy.md) | Normative insertion and subfields |
| [00.00.43](../00_foundations/00.00.43_controlled_identity_rename_policy.md) | Normative controlled renames |
| [README.md](README.md) | Identity name tables and rename commands |
| [40.05](../../40_thought_simulator_playground/40.05_master_program_guide.md) | 40 process (how to work) |
| [30.00](../../30_verification/30.00_verification_user_guide.md) | 30 process |
| [50.05](../../50_thought_simulator_design/50.05_software_spec_construction_guide.md) | 50 construction and Level-2 rules |

---

## 11. Revision log

| Version | Date | Summary |
|---------|------|---------|
| 0.1 | 2026-06-09 | Initial target strategy — 40 / 10.50 / 30 / 50 layout, migration order, exceptions |
| 0.2 | 2026-06-09 | Phase-1 40 renumber complete — checkpoint and exception ledger updated |
| 0.3 | 2026-06-09 | Post-renumber canon sweep + bulk-migration drift prompts (§9 items 7–8) |
| 0.4 | 2026-06-09 | Phase-2 10.50+30 renumber complete — §8 checkpoint updated |
| 0.5 | 2026-06-09 | Phase-3 50 renumber complete — §7 exceptions resolved; §8 50 aligned |
| 0.6 | 2026-06-09 | Bulk-migration pipeline canon — §8 residual pass; §9 drift prompts 9–11; aligns with 00.00.43 §11.2 |