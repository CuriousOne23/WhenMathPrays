# Path A Conversation Space Exerciser — Constitution

- **File:** `notes/pathA_cse/00_header.md`
- **Directory:** `notes/pathA_cse/`
- **Short name:** CSE
- **Long name:** Path A Conversation Space Exerciser
- **Status of this file:** frozen constitution for CSE documentation
- **Does not modify:** dictionaries, runner, packets, freeze manifest

This document is the closed rule set for the CSE corpus and for the status table in `notes/pathA_supported_sentences.md`. It does not introduce a sixth geometry.

---

## 1. Purpose

The CSE provides a coverage corpus of utterances that probe Path A **pipeline stages**:

- IE (Intake Engine)
- SOB / SROB / CnOB (segmentation, roles, constraints)
- SmOB (smoothing)
- IdOB (identity / meaning bundle)
- MCB / OuBA (post-IdOB packets)
- TR / TRU (truth-relation routing placeholder + truth-relation label)

These are pipeline stages, not geometries. The only geometry defined in the independence note is:

\\[\\mathcal{X}_{\\mathrm{PathA}} = \\mathcal{S} \\times \\mathcal{R} \\times \\mathcal{C} \\times \\mathcal{B} \\times \\mathcal{I}\\]

The CSE does not introduce a human-space geometry. Human-space dimensions are descriptors of utterance types. Structural space is \\(\\mathcal{S}\\times\\mathcal{R}\\times\\mathcal{C}\\). Semantic space is \\(\\mathcal{B}\\times\\mathcal{I}\\) plus the TRU label.

The CSE documents what Path A can address today, what it claims to address, and what it cannot yet address. It does not expand Path A's ontology.

---

## 2. Human-space dimensions (closed list)

Each utterance must tick **one primary** human-space dimension and may tick optional secondaries.

Closed list:

- Mood: declarative / interrogative / imperative / exclamative
- Polarity: positive / negative
- Person: 1st / 2nd / 3rd
- Nesting depth: simple / nested / doubly-nested
- Modifier chain length: none / short / long
- Fragment vs clause: fragment / full clause
- Coordination: none / coordinated
- Conditionality: none / conditional
- Speech-act force: neutral / request / command / query

No new dimensions may be added without architectural change.

---

## 3. Sentence families (frozen list)

Official family labels are the catalog names from `notes/pathA_supported_sentences.md`:

| Official family name | Short tag (IDs only) |
|---|---|
| Copular / State Descriptive | `copular` |
| Locative Descriptive | `locative` |
| Mixed Descriptive | `mixed_desc` |
| Interrogative | `interrogative` |
| Mixed Interrogative | `mixed_inter` |

No new families may be added in CSE documents. Stretch rows that do not fit a family stay `Not yet implemented` and say so in Notes.

---

## 4. IdOB families (frozen list)

Each utterance must map to one or more of:

- `interrogative_wh`
- `interrogative_polar`
- `agent_action`
- `modifier_resolution`
- `residual_identity`
- `mixed_descriptive`
- `copular_state`
- `locative`

If an utterance requires a new IdOB family:

- Status = `Not yet implemented`
- Notes must say: `Would require new IdOB family: X`

---

## 5. Truth-relation labels (frozen list)

Use only the TRU labels from the supported-sentences catalog:

- `descriptive_state`
- `descriptive_locative`
- `interrogative_open`
- `interrogative_nested`

`interrogative_polar` is **not** a TRU label today. It is an IdOB family and a human-space mood / speech-act fact.

Polar questions map as:

- TRU: `interrogative_open`
- IdOB family: `interrogative_polar`

If a new TRU label is required:

- Status = `Not yet implemented`
- Notes must say: `Would require new TRU label: X`

---

## 6. Segment alphabet (frozen list)

Structural content must use only:

- `NP`
- `CP`
- `AP`
- `LOC`
- `ST`
- `WQ`
- `IQ`
- `PP`
- `PN`
- `RELC`

`VP` is not a first-class segment. If written at all, mark it `proposed`.

If an utterance requires a new segment type:

- Status = `Not yet implemented`
- Notes must say: `Would require new segment type: X`

---

## 7. ID scheme and ownership

### ID format

```
PA-CSE-NNN / <family_tag>
```

`<family_tag>` is the short tag from §3, not a TRU label.

Example:

```
PA-CSE-004 / locative
```

TRU lives in field 8. IdOB family lives in field 8 / Notes. Neither belongs in the ID.

### Ownership

- `pathA_conversation_space_exerciser.md` owns utterances and the nine fields.
- `notes/pathA_supported_sentences.md` references CSE IDs and records Status.
- Canonical catalog examples appear first in the CSE.

### Negative ownership

The CSE must not:

- edit dictionaries
- edit the runner
- edit packets
- edit the freeze manifest
- add new families

The supported-sentences file must not add utterances. New utterances originate only in the CSE corpus.

---

## 8. Status definition (strict)

Status reflects runner reality, not markdown optimism.

**Implemented**

- dictionary pattern present
- committed `run_examples.py` processes **this utterance** end-to-end
- `run.log` + `debug_out.md` show full pipeline geometry for this utterance

**In work**

- dictionary pattern present for the family
- committed runner does not currently invoke this utterance

**Not yet implemented**

- dictionary pattern missing, or
- runner cannot process the utterance, or
- utterance requires a new frozen object (segment, TRU, IdOB family, sentence family)

Notes must name the frozen object that would need to change, when that is the reason.

As of 2026-09-23, the only committed live runner sentence is *Why is the sky blue?*

---

## 9. Coverage hole catalog (closed list)

Field 3 must cite exactly one hole ID.

| Hole ID | Coverage hole |
|---|---|
| HOLE-01 | WH interrogative variety |
| HOLE-02 | polar interrogative variety |
| HOLE-03 | copular NP vs AP distinction |
| HOLE-04 | locative CP vs ST distinction |
| HOLE-05 | nested RELC |
| HOLE-06 | PP stacking |
| HOLE-07 | modifier chain length |
| HOLE-08 | polarity / negation |
| HOLE-09 | imperative / command / non-WH request force |
| HOLE-10 | conditionality |
| HOLE-11 | coordination |
| HOLE-12 | fragment / ellipsis |
| HOLE-13 | 1st / 2nd person |
| HOLE-14 | passive |
| HOLE-15 | quantified NP |
| HOLE-16 | exclamative |

No new holes may be added without architectural change.

---

## 10. Nine required fields per utterance

1. **ID** — `PA-CSE-NNN / <family_tag>`
2. **Utterance**
3. **Coverage hole ID** — from §9
4. **Human-space dimension(s)** — one primary + optional secondaries
5. **Structural-space stressor** — which of SOB / SROB / CnOB is under load
6. **Semantic-space stressor** — SmOB cue / basin residue / IdOB op / TRU label
7. **Structural content** — segment alphabet only
8. **Important structural values** — roles + geometry arrow + truth-relation + IdOB family
9. **Notes** — `live` / `documented-only` / `requires packet or dictionary change`

Field 5 names the primitive under load. Field 7 names segment labels only.

---

## 11. Seed corpus (required)

The first rows must be the canonical catalog examples, in this order:

**Copular / State Descriptive**

- The sky is blue.
- Paris is a city.

**Locative Descriptive**

- The book is on the table.
- The rain stays in the plain.

**Mixed Descriptive**

- The rain in Spain stays mainly in the plain.

**Interrogative**

- Where is the book?
- Is the book on the table?
- Why is the sky blue? *(only runnable in committed `run_examples.py` today)*

**Mixed Interrogative**

- Why does the rain in Spain stay mainly in the plain?
- Where is the book that is on the table?
- Why is the sky that is blue bright?

These are the first entries in the CSE and the first entries in the status table.

---

## 12. Stretch rows (capped)

After the seed corpus, add **one utterance per stretch type**, capped at 10 rows:

1. imperative
2. negation
3. coordination
4. conditional
5. fragment / ellipsis
6. 1st / 2nd person
7. passive
8. quantified NP
9. exclamative
10. non-WH speech-act request

All stretch rows are `Not yet implemented` unless the committed runner supports them.

---

## 13. File set for this drop

Only these files:

- `notes/pathA_cse/00_header.md` *(this constitution)*
- `notes/pathA_cse/pathA_conversation_space_exerciser.md` *(corpus)*
- status table appended to existing `notes/pathA_supported_sentences.md`

No other CSE notes in the first drop.
