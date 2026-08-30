# Thought Simulator governance brief for CP
**Date:** 2026-08-30  
**From:** project lead + realization pass (Grok)  
**Repo:** CuriousOne23/WhenMathPrays  
**Scope:** Path A field authority, IdOB isolation hop, OB umbrella, bot bench  
**Not in scope:** 20.50 typed RB destinations, 20.206 Path-B wording, full-lineup wiring

---

## 1. Why this note

`thought_simulator/` is measurably more uniform than the pre-bot tree. Names, IdOB invoke, freeze naming, and who may birth meaning are no longer three competing sentences. Bots were used as a **scoreboard**, not as law writers. This note states what exists, what we do **not** build yet, and what actually landed on `main`.

---

## 2. Bots that exist (do not clone)

All of these are **write=no** reporters unless the human stamps an EVENT. Helm is the only one that writes governance logs.

| Bot | Function | Writes |
|-----|----------|--------|
| **Helm** | Reads `BOT_INBOX.md`. Appends `CHANGE_LOG.md`. Refreshes `BOT_REPORTS/LATEST.md`. | Logs only |
| **Spine** | Path A/B door, OuBA, 20.15 / 20.31 / 20.206 collisions. Scores against 20.705 §2 and §3.6 only. | Report rows `S*`, `E*` |
| **Meaning** | Who may write meaning; OB umbrella vs IdOB vs TP vs COB. | Report rows `M*`, `M-705-*` |
| **Route** | TR / CTP / RB / IdOB hop order. | Report rows `R*` |
| **Matrix** (readme-bot) | `20.200` vs README auth list vs live filenames. | Report rows `MX*` |

**Operating rules already stamped**

- Flow-tracker = **20.705 §2** (Path A hops) and **§3.6** (conversation layer). Other 20.705 sections are historical. Do not clean them.
- Field-name authority = **20.116 series**.
- CTP = **20.145 primitive only**. OuBA freeze is not called CTP.
- `write=no` on requirements unless the human opens a named file.
- Do not create extra bots without a human EVENT.

Inbox and reports live under:

`thought_simulator/program_governance/`  
(`BOT_INBOX.md`, `CHANGE_LOG.md`, `BOT_REPORTS/LATEST.md`)

---

## 3. Bots we may create later (none now)

Do **not** add a bot per primitive.

| Possible later bot | Function | Why wait |
|--------------------|----------|----------|
| **Catalog (Names)** | Score playground + testbenches against 20.116 only (wrong root, second envelope, CIE vs stance). | 20.116 just landed; human can see drift first. |
| **Harness** | Run IdOB (then MCB) rulecheckers; one pass/fail line in reports. | Useful when CI is wanted. Not required for isolation proof. |
| **Terms** | Glossary (`20.190` / `20.700`) vs 20.116 and the CTP decision. Suggest-only. | Better than a 20.705 rewriter. Still `write=no`. |
| **Flow** | 20.705 picture vs live shalls. Suggest-only. | Overlaps Spine + Route. Optional. |

**Do not create:** a 20.705 cleanup bot, a glossary rewriter, or hop-bots (SOB-bot, CIL-bot, …).

---

## 4. Changes that landed on `main` (this pass)

### 4.1 Field catalog (20.116)

New normative series under `thought_simulator/requirements_20/`:

- `20.116_field_catalog.md` — names / paths / owners
- `20.116.010_tp_envelope_index.md` — envelope roots
- `20.116.020_ownership_rw.md` — write walls
- `20.116.030_name_separations.md` — CIE ≠ MSL stance ≠ next_context.stance; meaning Δh ≠ entropy ΔH%; `TP.idob` ≠ COB snapshot

Collision rule: **20.116 wins names/paths/owners; the primitive file wins behavior.**

Sidecars (large files not rewritten):

- `system_playground/design/pipeline/00_field_catalog_authority.md`
- `20.705_field_catalog_authority.md`

`patha_field_names.md` and `20.705` bodies stay derived / visualization. Do not treat the playground dictionary as the winner on a name collision.

Authority notes were added to live IdOB files (README, structural program, packet YAML, testbench YAML/py, rulechecker, `idob.py`). Hop logic was not changed.

### 4.2 IdOB isolation hop (Path A focus)

Live realization remains:

- `system_playground/primitives/idob/idob.py`
- `system_playground/testbenches/path_a/identity/` (`idob_*` only)

Agreed with 20.116 on: writer of `TP.idob`, `TP.semantic.meaning_delta_h`, root flags, routing-filter wall, S2M without lifecycle export. Empty stub YAMLs in that folder (`cil_`, `cob_`, `cst_`, …) were not part of this pass. MCB comment batch was started then dropped as low bang-for-buck.

### 4.3 Human decisions (clusters 1–3)

Stamped in `BOT_INBOX.md` (PRs #37 / #39). Law files were not auto-patched by bots.

**Cluster 1 — IdOB invoke + stretch**  
Winner: `HLR-20.40.050-062` and 20.705 §2.

`WrdNm → ISc → RTU → TR → CTP → RB → IdOB → MCB → RBU`

- Old invoke-only-after `RB → RTU` is not live. Current `20.40.050-011` already states `TR → CTP → RB → IdOB`.
- SOB→…→SmOB is the **structural** chain, not the S2M schedule.
- `RB → OuBA` may skip IdOB. Isolation fixtures stay legal.
- Successor after IdOB is **MCB → RBU**, not `IdOB → TR → OuBA`.
- 20.51 `TR → RB → CTP` yields to 20.145 + §2.
- **20.50 typed destinations deferred** (does not help isolation testbench).

**Cluster 2 — meaning-write**  
Winner: 20.116.020-003, `HLR-20.105-116`, IdOB-prm.

- Only IdOB births stand-in \(M\), `TP.idob`, `meaning_delta_h` (plus listed flags).
- Umbrella “no semantic interpretation” applies to **SOB–SmOB producing \(M\)**, not to IdOB.
- Child MAY-read of CE/CIL is **cues**, not a second writer.

**Cluster 3 — OuBA door / conversation polarity**  
Winner: 20.15 §2.14 and 20.116.

- Sole COB **meaning-ingest** door = OuBA freeze.
- CST-Core/MS → COB = stability commands, not meaning ingest. USP remains CIL-only.
- Path A CEx (after IE) and CIL→CEx are **two jobs**. Do not score them as one reversed hop.
- S1 / S3 on 20.206 left open as Path-B wording, not as a new door.

### 4.4 20.40 umbrella v1.3 (PR #38)

File: `thought_simulator/requirements_20/20.40_ob_requirements.md`

- `HLR-20.40-017R` removed (illegal suffix).
- Freeze SHALL is **`HLR-20.40-019`** (previous max was 018).
- `HLR-20.40-017` stays **NA** (do not restore “OuBA produces a CTP”).
- `HLR-20.40-003` / `007` / `008` bind **SOB–SmOB only**; IdOB may read cues and write the 20.116 / 20.40.050 set.
- Informative §3 / §5 / §6 have no SHALL and no HLR numbers.
- Every remaining SHALL sits under `HLR-20.40-nnn`.

### 4.5 Numbering / drafting rules used

- Do not remove information; correct / reword / add.
- No informative sentence carries a SHALL or an HLR number.
- Every SHALL has an HLR id of the form `HLR-20.xxx.yyy-nnn` with `nnn = max(existing)+1` in that document.
- Large files: sidecar or human commit from VS. Do not rewrite 39 KB dictionaries through the chat GitHub pipe.

---

## 5. How to read `LATEST.md`

The header is current (flow-tracker, 20.116, CTP decision, 20.40 v1.3 once Helm processes #39).

The row list is still a **backlog dump**. Many `M-011` / `M-705-008` / family-wide `003` rows were scored **before** the corrections. After Helm refreshes, those should show **decided** against live files.

**Ignore for Path A testbench this week:** `MX-001–046` (filename hygiene).

**Still actually open (low priority vs isolation hop):**

- 20.50 typed WrdNm / IdOB / OuBA destinations  
- 20.206 S1 / S3  
- 20.32 / 20.105 sentences that still talk as if COB eats live CEx (policy is freeze-only; wording later)

---

## 6. What we are optimizing for

Keep **testbench + TS Path A** sharp:

- Isolation IdOB (then MCB) on a fixture  
- Packet walls and 20.116 names  
- One official stretch sentence  
- One meaning writer  

Do not spend the next cycle on RB table schema. Isolation cases do not read it.

---

## 7. Ask of CP

1. Treat 20.116 as the name/path/owner authority; do not invent a parallel dictionary in architecture notes.  
2. Treat 20.40 v1.3 and 20.40.050-062 as the live OB/IdOB neighborhood.  
3. Do not stand up new bots. If a Catalog bot is wanted later, it is read-only vs 20.116.  
4. When reviewing `LATEST.md`, score **current files**, not the pre-correction pass.

---

*End of brief.*
