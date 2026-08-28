# Path A review — 28 August 2026

**Status:** Informative. Not HLR law. Does not override 20.15 or primitive documents.

**Participants:** Jeff (project lead), CP (architectural review), Grok (realization / fencing).

**Context:** After the Path A primitive sweep for IdOB and COB support, 20.15 was updated to v4.2 with a continuation guide (§3 official flow, §12 write walls and testbench map). CP reviewed the present stake against four questions. Grok recorded precision notes and the next experiment.

**Law pointers (read these, not this file, for implementation):**

- [20.15 v4.2](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.15_ts_architecture_scaffold.md) — §3 official flow, §12 continuation guide
- [20.40.050 IdOB v3.2](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.40.050_idob_prim.md)
- [20.40.055 MCB v2.1](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.40.055_mcb_prim.md)
- Neighbors if a wall is disputed: [20.30.005 RTU](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.30.005_rtu_prim.md), [20.51 RBU](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.51_rbu_prim.md), [20.40.060 OuBA](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.40.060_ouba_prim.md), [20.32 COB](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.32_cob_requirements.md), [20.50 RB](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.50_rb_requirements.md)

---

## 1. Present stake (agreed)

Path A is a research vehicle. Success is **visibility into structure-to-meaning** that can be named, measured, replayed, and revised — the duck test — not a verdict that “this machine is performing cognition.”

Two descriptive geometries:

| Geometry | Feel | Machine form | Writer |
|----------|------|--------------|--------|
| Structure | Landscape / roads the utterance is typed onto | Six IDs + `structural_key` | Structural OBs / assignment tables |
| Meaning | Speaker’s intended projection stand-in | Six axes in [0,1] after a legal map member is selected | IdOB |

Do not let the names trade places. Structure is not a six-axis score. Meaning is not a hash of the six IDs.

Machine realization of language is geometric **for the instrument**. Axes, epsilon, and CIE formula change only by requirement + code revision, not silent runtime toggle.

---

## 2. CP on the four questions

### 2.1 Speaker-projection + consequence-as-significance + listener as reference

**CP verdict:** Holds, and Path A now fences it more cleanly than earlier drafts.

- IdOB is a stand-in geometry in the meaning / identity layer. It does not own routing or structure.
- `meaning_delta_h`, identity-importance, and semantics arrays are downstream-consumable significance (TR, RB view, Path B eligibility, MCB). Not a new owner of the world.
- Listener is not a second agent. Reference and continuity live in COB / CIL / `next_context` and identity-importance cues.

**Grok precision:** Keep the **packet** first (`TP.idob`, six-axis \(M\) / \(M'\), `meaning_delta_h`). Roles / candidates / lineage envelope is optional export. A hop is legal without the full lifecycle envelope (20.15 already states this). Do not make the first isolation case carry the whole envelope as mandatory.

### 2.2 Write walls (20.15 §12.2)

**CP verdict:** The split is right. Do not move the boundaries.

| Wall | Writer | Job |
|------|--------|-----|
| `TP.idob` + crossing `meaning_delta_h` | IdOB | Who / what is projected and how meaning shifts |
| `TP.next_context{}` + `mcb_*` | MCB | Reconcile with clarifying fields; next turn. Does not overwrite `tp.idob` |
| OuBA freeze → COB ingest | OuBA / COB | Path A exit vs conversation substrate entry |

`TP.next_context.stance` is not CIE. CIE is hop pressure on \(M\) after birth.

`pack_ids[]` are owned by continuity (CEx-Pck / CIL / COB). RTU, IdOB, MCB, and RBU do not invent packs.

### 2.3 Residue is a hint; RB owns the next six-tuple

**CP verdict:** Acceptable present stake, consistent with 20.15 and 20.50.

- Residue codes and identity-residual are markers in the IdOB envelope, not routing decisions.
- RB owns routing, manifold chart, and the next structural six-tuple. IdOB must not write `routing_filter`, DCB geometry, or structural ΔH%.
- `expand_target` / leftover `residue_code` plus TP history are enough to expand dictionaries **manually**. Automatic residue → next six-tuple is RB work, not a hidden IdOB function.

### 2.4 What would convict the six axes from traces?

20.15 §12.6 already names collapse, idle axis, locked pair, CIE / budget leak, empty-key / single-key collapse, CIE swap moving `structural_key`.

CP added a bar for “the axes are doing real work”:

| Bar | What it tests | When |
|-----|---------------|------|
| Replay + regime stability | Axes are a coordinate system, not a moving target | After one deterministic isolation packet exists |
| Non-local pressure on RB | Meaning moves routing without IdOB writing routing | After RBU has committed the packet and RB *reads* it |
| Cross-utterance coherence | Conversation-scale identity, not one-shot décor | After COB ingest exists (later) |
| Downstream uncertainty drop vs crippled IdOB | Axes earn their keep for TR / Path B flags | After a CIE-zero / axis-free control exists |
| Revision rule exercised | Axes are convictable, not dogma | When a definition actually changes |

Do not run all five on the first trace. First trace: replay identity of the packet, plus a glimpse that RB can *see* the packet without IdOB having written routing.

---

## 3. Next experiment (agreed direction)

**Not** another primitive compatibility sweep.

**Now — isolation plus reader:**

1. One utterance + structure card + packs + `cie_id`.
2. **IdOB → MCB → RBU**.
3. **RB as a reader** of the committed view (not RB before IdOB).

Official *live* stretch remains `RTU → TR → CTP → RB → IdOB → MCB → RBU`. That is later.

**Log:**

- utterance (carrier string; not meaning)
- full `TP.idob`
- `meaning_delta_h`, `meaning_cie_delta`, CIE row used
- `TP.next_context` and an explicit note that its stance ≠ `cie_id`
- RBU commit (or first-pass no-op on a no-packet control)
- RB routing choice **and** `routing_filter_mutated == false` from the IdOB side

**Question on that log:** do the six axes move in a way a human can point at, or is the math decorative?

Machine folders:

- Live identity tests: `system_playground/testbenches/path_a/identity/` calling `primitives/idob/`
- Learning bench (do **not** import into Path A tests): `system_playground/testbenches/idob_structure_to_meaning/` including `11_idob_core/`

---

## 4. What this review does *not* reopen

- Whether Path A “is cognition.” That debate does not close. Visibility does.
- Axis count or epsilon as first-order architecture. Those change by named revision when traces convict the current layout.
- Pointing Path A identity tests at `11_idob_core`.
- Teaching RTU or MCB to birth \(M\).
- Writing COB from RBU / IdOB / MCB.
- Treating `next_context.stance` as CIE.

---

## 5. One-line handoff

Path A is synced to speaker-projection + consequence-as-significance, with three write walls (IdOB packet, MCB next-turn, OuBA→COB). Next unit of less fog is one isolation trace, not more requirements.
