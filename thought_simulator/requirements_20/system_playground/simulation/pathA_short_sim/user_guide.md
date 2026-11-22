# PathA Short Simulation — User Guide

This guide starts with a sentence you already know, then shows how the Path‑A Thought Simulator (TS) short simulator writes **structure** first, an Identity Observation Block (IdOB) **packet**, and now the Structure-to-Meaning (S2M) crossing and category-selection observation layers.

Program status, current face versus intended mapping, and the ready line: [notes/program/README.md](notes/program/README.md). This guide teaches how to run the simulator and correctly read its output as an inspectable observation surface for structure, default meaning, candidate interpretations, and category-influenced extensions.

Names and hard words (object, adjacency, meaning, packet): [architecture/idob_seam.md](architecture/idob_seam.md).  
Catalog (ten cards; the family enum has ten values, including `agent_action`, `imperative`, and `exclamative`): [notes/idob_object_space/idob_object_space.md](notes/idob_object_space/idob_object_space.md).  
Packet contract: [architecture/IdOB_unified_plan.md](architecture/IdOB_unified_plan.md).  
Charter: [architecture/path_a_realization_charter.md](architecture/path_a_realization_charter.md).  
S2M program contract and Phase III/IV: [notes/program/s2m_program_reference.md](notes/program/s2m_program_reference.md).  
Category selection concept: [notes/program/category_selection_proposal.md](notes/program/category_selection_proposal.md).

**Official expansions:** Structural Observation Block (SOB), Structural Refinement Observation Block (SROB), Constraint Observation Block (CnOB), Semantic Observation Block (SmOB), Identity Observation Block (IdOB). Debug field names (`struct_segments`, `struct_roles`, smoothing) are teaching aliases of those jobs. Full contracts: `20.40.010`–`20.40.050`.

---

## 1. Run the simulator

From this directory:

```
python run_examples.py
```

S2M accountability + meaning blocks and category-selection observation cases are enabled by default. To disable S2M layers:

```
python run_examples.py --no-s2m-seed
```

To disable category observation scenarios:

```
python run_examples.py --no-category-observations
```

When enabled, `run_examples.py` prints labeled blocks including:
- `--- S2M Accountability (IdOB) ---` (`s2m_seed`)
- `--- S2M Meaning (IdOB) ---` (`s2m_meaning`)
- Category Observation sections for no-cue, sentence-internal, and prior-context cases

Or log output:

```
python run_examples.py > run.log
```

Then, to read the log as a teaching document:

```
python pathA_dbug.py run.log --base-dir .
```

That writes `debug_out.md`.

Supported sentences: [notes/pathA_supported_sentences.md](notes/pathA_supported_sentences.md).

---

## 2. How to read a run

Read the normal `run_examples.py` output in this order:

1. Read the structural relation (accountability trail / `s2m_seed` written_relations).
2. Read the structurally derived default meaning.
3. Check whether a category cue exists (`category_cue` empty or present).
4. Determine where the cue came from (sentence-internal marker or prior-context/CEx).
5. Read the ISc category evidence (scoring distribution, top_category, confidence, rationale).
6. Confirm what TPU committed (`TP.semantic.isc_category_result`).
7. Observe what IdOB/S2M consumed (read-only cue_state).
8. Inspect candidate interpretation states (unselected, category-supported, etc.).
9. Inspect legitimation or refusal.
10. Compare the final extensions (`meaning_relations`) with the unchanged default meaning.

You do not need to open Python to follow this sequence. The output is the observation surface.

---

## 3. This world → structure, packet, and S2M layers

Take *The sky is blue.*

This world: you are told the sky’s color.

Path A splits that into structure first, then meaning layers:

| Column A — structure (Observation Block set, OB-set) | Column B — meaning on this path (IdOB packet + S2M) |
|---|---|
| Chunks, structural labels, constraints, adjacent cues | Catalog objects, default meaning, candidates, any legitimized extensions |
| Written by SOB, SROB, CnOB, SmOB | Written by IdOB; S2M layers attached additively |
| `struct_segments`, `struct_roles`, `constraints_matched`, `semantic_adjacent_cues`, residues | `activation_set`, `semantic_core` (**dict**), `truth_relation`, `s2m_seed`, `s2m_meaning` |

IdOB does not invent the chunks. If column A is empty or wrong, later layers cannot invent a structural relation.

### 3.1 *The sky is blue.*

| Structure (who wrote it) | Packet + S2M |
|---|---|
| SOB: noun-phrase + state material | Expect one descriptive contributor (`copular_state` family) |
| SROB: theme / state structural labels | `semantic_core` is a dict (keys such as `theme`, `state`) — **not** a list |
| CnOB: copular constraints can close | Default meaning derived from `sky — is — blue`; candidates available but unselected without cue |
| SmOB: little basin leftover | No-cue result: default only; `meaning_relations` empty |

This is the unified-plan D3 proof utterance and a canonical S2M testbench sentence.

### 3.2 *Where is the book that is on the table?*

This world: you ask where the book is, and you pin which book with a clause.

| Structure | Packet + S2M |
|---|---|
| SOB: question word, entity, locative, relative clause | `activation_set` may list more than one name |
| SROB: query focus + entity + location labels | `semantic_core` dict may hold `query_focus` and `location` |
| CnOB: interrogative scope + locative attachment (`constraint_residue` if scope is messy) | Default query meaning; locative continuation potential/null |
| SmOB: book + table in one picture (adjacent-cue / smoothing *operation*) | Candidates visible; no endpoint association selected as meaning without cue |

Three uses of adjacency (do not collapse them):

1. String: *book* touches the clause (SOB/CnOB).
2. Basin: book + table one picture (SmOB).
3. Object: more than one IdOB family eligible (catalog `overlap.*` → packet `overlap_events`).

This is the unified-plan R2 proof utterance.

### 3.3 *The book is on the table.*

Same habit: SOB/SROB place the locative; IdOB `locative` (and possibly `copular_state`) are the catalog names in play. Default locative meaning is derived from structure. Candidates remain unselected without a cue. Do not call the book an IdOB object.

---

## 4. Read the S2M crossing

S2M realizes five distinct stages (see [s2m_program_reference.md](notes/program/s2m_program_reference.md) and [s2m_relational_proposal.md](notes/program/s2m_relational_proposal.md)):

- **Structural relation** — what the floor established (`s2m_seed` written_relations).
- **Default meaning** — the minimal semantic relation derived from that structure. Always present when the seed is on. Not selected from a candidate inventory.
- **Candidate interpretation space** — available associations for relevant endpoints/relations, tagged by interpretation major. Visible but unselected by default.
- **Selected interpretive extension(s)** — candidates written only after a cue is present and the relation is legitimized within the licensed region.
- **Finite customized composite** — default meaning + any legitimized extensions.

Candidate availability does not mean candidate selection. Selected interpretive extensions do not replace default meaning. The customized result is default meaning + any legitimized extension(s).

No cue means default meaning only. A cue may produce default meaning + legitimately selected extension(s).

---

## 5. Read category-selection observation

Category selection is additive. It lets available information make a non-default interpretive category relevant without overwriting the structural default. The path is:

cue source → CEx / CE → ISc → Merge → TPU → `TP.semantic.isc_category_result` → IdOB read-only consumption → S2M candidate consideration → legitimation/refusal → final composite

- **CEx / CE** supply the optional `category_cue` from sentence-internal evidence or prior context. They do not choose meaning.
- **ISc** scores category evidence and produces the distribution, top_category, confidence, and rationale. It does not choose the sentence's final meaning.
- **Merge / TPU** commit the category result into `TP.semantic.isc_category_result`. TPU is the sole writer of that block.
- **IdOB** reads the committed result as a read-only cue. It does not rewrite the category-result envelope. Absence of a result does not block ordinary S2M / default meaning.
- **S2M** uses the cue for candidate consideration, then performs licensed-region assessment and legitimation or refusal.

Ordinary semantic endpoints are not sentence-internal category cues merely by being endpoints. Cues require independently directing evidence such as modifiers, adverbs, structural markers, or equivalent floor-visible information.

See [category_selection_proposal.md](notes/program/category_selection_proposal.md) for the phenomenon and boundaries. Normative ownership lives in 20.45 (ISc), 20.105 (TP), 20.116.010, and 20.40.050 (IdOB).

---

## 6. Field meanings and interpretation limits

### Category-result fields (`TP.semantic.isc_category_result`)

- **`category_cue`**: Evidence directing category consideration (list of majors or empty). Origin is sentence-internal or prior-context. It is not itself meaning.
- **`category_weighted_distribution`**: Normalized scores over candidates in this realization. Relative scores do not establish semantic truth. A category receiving probability mass does not guarantee an extension.
- **`top_category`**: Primary scoring summary (major of the highest-probability candidate, or null). It is not a final meaning-selection command. Candidate relevance may use other supported evidence in the committed result according to the bounded realization policy. It can legitimately differ from the major of a candidate eventually considered or legitimized; that difference is observable information, not automatically an error. With an empty cue the short realization prefers `null`.
- **`category_confidence`**: A scoring field required by the current realization. It is not a probability that the interpretation is true, that the sentence has been understood, or that the final meaning is correct. For the no-cue case it is `0.0`.
- **`category_rationale`**: Inspectable record of why the scoring/category-result state has the form shown (e.g., `empty_category_cue` vs `category_cue_applied`). Not a proof that the resulting interpretation is semantically true.
- **`provenance`**: Origin of the cue (sentence-internal vs prior-context). Keeps the two paths distinguishable.

Empty-cue representation in the short realization:

```
category_cue: []
top_category: null
category_confidence: 0.0
```

This is no evidence-supported category decision, even if a deterministic scoring distribution is still computed.

### S2M fields

- **`default_meaning`**: Structurally derived minimal relation. Always look here for the baseline. Present even when `meaning_relations` is empty.
- **`meaning_relations`**: Legitimized interpretive extensions only. Empty does **not** mean the simulator produced no meaning. Look at `default_meaning`.
- **Candidate states** (visible names in the current realization): `candidate_unselected`, `category_supported`, `legitimized`, `refused`. Progression: candidate exists ≠ category supports it ≠ it is considered ≠ it is legitimized ≠ extension is written. `category_supported` does not imply `legitimized`. Refusal/non-selection is useful information, not a failure of default meaning.
- **Finite customized composite**: default meaning + any legitimized extensions. It does not by itself establish human-like understanding.

### What the output does NOT establish

- `top_category` does not establish final meaning.
- `category_confidence` is not a probability that the interpretation is true.
- A high category score does not guarantee S2M legitimation.
- Candidate presence does not mean candidate selection.
- Candidate selection/relevance does not necessarily mean an extension is written.
- Refusal does not mean the default meaning failed.
- `meaning_relations: []` does not mean S2M produced no meaning.
- Current short-simulator licensing does not establish generalized semantic licensing.
- A Phase III or Phase IV observation does not automatically become a requirement or theoretical claim.
- The finite customized composite does not by itself establish human-like understanding.

These fields are exposed so you can inspect where information originated, what changed, what did not change, which component acted, where candidate consideration began, where selection stopped, whether legitimation occurred, what remained default, what became an extension, and whether replay is deterministic. The short simulator makes the S→M crossing observable.

---

## 7. Scenario walkthroughs (category observations)

### A. No-cue baseline

Notice: default present, `category_cue` empty, `top_category` null, candidates visible but unselected, `meaning_relations` empty.

Question answered: What does the S→M bridge do without category influence? Answer: default meaning only.

### B. Sentence-internal `where` observation

Notice: independent sentence marker → perspectival category evidence → candidate consideration → refusal → default remains.

Question answered: Can category evidence exist without becoming meaning? Yes.

### C. Prior-context observation

Notice: prior context → CEx/CE cue → ISc scored result → TPU committed result → physical candidate relevance → legitimation → additive extensions.

The scoring `top_category` and the major of the eventual legitimized candidate need not always be identical in this bounded realization. Inspect the difference; do not treat it as automatically significant or erroneous.

Canonical three-sentence cases remain the normative S2M testbench. Category Selection Observation cases expose category behavior and are observation cases, not automatically new semantic requirements. Phase III diagnostic probes (if present) are characterization tools and do not establish required semantic outputs.

---

## 8. Interpret the final Thought Packet (TP)

The final TP is the end-state substrate after all primitives run.

**Intake**

- `tokens`, `normalized_text` — Intake Engine (IE) and intake blocks

**Structure (OB-set)**

- `struct_segments`, `segment_tokens` — SOB
- `struct_roles`, `role_segments` — SROB
- `constraints_matched`, `constraints_unmatched`, `constraint_residue` — CnOB
- `smoothing_operations`, `semantic_adjacent_cues`, `smoothing_residue` — SmOB

**Routing**

- `routing_metadata`, `routing_decision`, `tru_hint` — routing primitives including TRU

**Meaning on this path (IdOB + S2M)**

- `semantic_core` — **dict** payload of the sum
- `idob` — full packet (teaching name `idob_packet`; see unified plan §3.3)
- `activation_set`, `contributors`, `contributions`, `overlap_events`, `meaning_delta`, `psc_violations`, `registry_digest`
- `s2m_seed` — structural relation / accountability
- `s2m_meaning` — default_meaning, candidate interpretations, meaning_relations (extensions), cue_state
- `TP.semantic.isc_category_result` — committed category result (when present)

**Commit**

- `commit_flags` — Output Binding / Assemble (OuBA) checkpoints

`meaning_delta` here is legacy-writer vs split-writer. It is not S2M `meaning_delta_h` and not entropy $\Delta H\%$. See the seam alias table.

---

## 9. Interpret the trace

Each trace item includes:

- **primitive** — name executed
- **input** — TP snapshot before the primitive
- **output** — TP snapshot after the primitive
- **notes** — human-readable observation

Read input/output deltas to see exactly what each primitive changed. IdOB should change packet fields, not rewrite `struct_segments`. Category result reaches TP only via Merge → TPU.

---

## 10. Follow TP evolution macro by macro

### Intake
`InB`, `IIInB`, `IE`

### Correction
`CEx`, `CE`, `ISc`, `TPU`

### Structural geometry (OB-set)
`SOB`, `SROB`, `CnOB`, `SmOB`, `SSG`

### Routing
`RBU`, `RB`, `TR`, `TRU`, `RTU`, `CTP`

### Semantic (meaning-as-packet + S2M)
`IdOB`

### Final commit
`OuBA`

Meaning Composition Block (MCB) is present as a copy-only seam in `mcb/seam.py` (`copy_from_idob`). It does not compose new meaning.

---

## 11. Debug odd outputs

- Confirm token normalization in **IE**
- Verify YAML dictionaries contain expected entries (OB-set rules under `support/dictionaries`; S2M associations under `s2m/data/`)
- Check **SOB** segment alignment
- Check **SROB** structural-label progression
- Confirm **CnOB** transition pairs in `constraint_rules.yaml`
- Confirm **IdOB** against the catalog and the packet, not against a six-type linguistic list
- If `semantic_core` prints as a list after IdOB, treat that as a contract break (Primitive Specification Contract (PSC) I10), not as “the meaning”
- For category cases, confirm cue provenance and that empty cue yields `top_category: null`

Debugger teaching cards live under `debug/`. The IdOB card is `debug/primitives/IdOB.md`.

---

## 12. Modify dictionaries

Edit files under `support/dictionaries` for **structure** rules:

- `token_classes.yaml`
- `segment_patterns.yaml`
- `role_patterns.yaml`
- `constraint_rules.yaml`

IdOB catalog objects live under `support/idob_objects/`. Do not add a ninth family by editing `semantic_rules.yaml` and calling it an object type.

S2M association data lives under `s2m/data/associations/`. New associations are data extensions; they do not change the selection/legitimation loop.

Rerun `run_examples.py` and compare trace deltas.

---

## 13. Extend primitives

Edit `primitives_pathA_short.py` only when the lineup itself must change. IdOB sum logic lives in `idob/sum.py` and `idob/packets.py`. Keep mutations explicit and trace-visible. S2M layers are additive; do not mutate core IdOB assignment.

---

## 14. Architecture overview — how files load

Neither `run_examples.py` nor `pathA_short_simulator.py` open YAML by hand. The engine import chain does.

### 14.1 Top-level Python

**`run_examples.py`**  
Entry point / driver. Defines example sentences and observation cases. Calls `run_pathA_short`. Prints or logs the trace and labeled S2M/category blocks. Does not mutate the TP.

**`pathA_short_simulator.py`**  
Macro sequencer. Runs primitives in order. Captures snapshots. No dictionary loading of its own.

**`tp_substrate.py`**  
Defines the TP object, `init_tp`, `clone_tp`.

**`primitives_pathA_short.py`**  
Lineup implementations and imports. This is where support files get pulled in.

**`idob/`**  
Registry, sum, packets, PSC, legacy apply stubs. S2M attachment point.

### 14.2 Support files

**YAML dictionaries (OB-set)**  
`support/dictionaries/` — token classes, segments, roles, constraints.

**IdOB catalog**  
`support/idob_objects/*.yaml` — the ten catalog cards.  
`support/idob_schemas/idob_object.v1.schema.json` — object bound.  
`support/idob_schemas/idob_psc_defaults.yaml` — shared PSC defaults.

**S2M data**  
`s2m/data/majors.yaml`, `s2m/data/associations/*.yaml`, `s2m/data/spaces/`.

**JSON schemas**  
`support/contracts/` — TP / stream contracts.

**Prototypes**  
`support/prototypes/` when present — structural templates.

### 14.3 Execution flow

```
run_examples.py
    ↓
pathA_short_simulator.py
    ↓
tp_substrate.py
    ↓
primitives_pathA_short.py + idob/*
    ↓
support/dictionaries + support/idob_objects + s2m/data + schemas
    ↓
Primitive sequence (InB → … → IdOB → OuBA)
    ↓
Final TP + full trace + labeled S2M/category blocks
```

---

## 15. File roles (summary)

| File | Purpose |
|------|--------|
| `run_examples.py` | Runs examples and observation cases; prints trace and labeled blocks |
| `pathA_short_simulator.py` | Macro sequencer |
| `tp_substrate.py` | TP structure |
| `primitives_pathA_short.py` | Lineup; loads many support files |
| `idob/sum.py` | Writes the packet (meaning here); S2M attachment |
| `support/idob_objects/*.yaml` | IdOB space $\mathcal{I}$ |
| `support/dictionaries/*.yaml` | OB-set rule tables |
| `s2m/data/` | Interpretation majors and candidate associations |
| `architecture/idob_seam.md` | Names and on-ramp |
| `debug/primitives/IdOB.md` | Observer card for IdOB |
| `notes/program/s2m_program_reference.md` | S2M executable contract, Phase III/IV |
| `notes/program/category_selection_proposal.md` | Category-selection phenomenon and boundaries |

---

## 16. Current licensed-region limitation

The current short realization uses an explicit bounded licensing scaffold (exact endpoint/relation/target tuples for the canonical/observation cases). It demonstrates the separation between category support and S2M legitimation, but it is not yet a generalized mechanism for deriving the licensed region from arbitrary structure/default meaning. This is a Phase III characterization fact, not a defect and not a solved general semantic mechanism.

---

## 17. Acceptance for this guide

This guide fails if a reader could reasonably conclude that:
- candidates automatically constitute meaning;
- `top_category` is the final meaning;
- `category_confidence` is truth confidence;
- empty `meaning_relations` means there is no default meaning;
- IdOB directly writes the category-result envelope;
- an ordinary endpoint automatically creates its own category cue;
- the current licensed-region scaffold is a generalized semantic solution;
- Phase IV observations automatically establish new requirements.

It passes if a reader can follow a normal `run_examples.py` category observation from structure/default → cue/provenance → ISc → TPU commit → IdOB/S2M → candidate state → legitimation/refusal → final composite without opening Python.

It also fails if it teaches six IdOB object types, shows list `semantic_core` as canonical, or calls the book an IdOBObject. The two-column examples in §3 remain walkable without opening the engine.
