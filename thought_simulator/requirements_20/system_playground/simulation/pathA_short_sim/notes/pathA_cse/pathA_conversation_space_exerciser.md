# Path A Conversation Space Exerciser

Coverage corpus for Path A short-sim. Constitution: [`00_header.md`](00_header.md).

This file owns utterances and the nine fields. It does not modify dictionaries, runner, packets, or the freeze manifest.

Status lives in `notes/pathA_supported_sentences.md`. Status is runner reality, not catalog optimism.

---

## Seed corpus

### PA-CSE-001 / copular

1. **ID:** PA-CSE-001 / copular
2. **Utterance:** The sky is blue.
3. **Coverage hole ID:** HOLE-03
4. **Human-space:** primary mood=declarative; secondaries polarity=positive, person=3rd, nesting=simple, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** SOB (NP vs AP complement shape) + SROB (theme / state)
6. **Semantic-space stressor:** TRU label `descriptive_state`; IdOB op `copular_state`
7. **Structural content:** NP → CP → AP
8. **Important structural values:** roles theme, state; geometry NP → CP → AP; TRU `descriptive_state`; IdOB `copular_state`
9. **Notes:** documented-only. Family claimed pipeline-complete. Committed runner does not invoke this string.

### PA-CSE-002 / copular

1. **ID:** PA-CSE-002 / copular
2. **Utterance:** Paris is a city.
3. **Coverage hole ID:** HOLE-03
4. **Human-space:** primary mood=declarative; secondaries polarity=positive, person=3rd, nesting=simple, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** SOB (NP complement vs AP in 001)
6. **Semantic-space stressor:** TRU `descriptive_state`; IdOB `copular_state`
7. **Structural content:** NP → CP → NP
8. **Important structural values:** roles theme, state; geometry NP → CP → NP; TRU `descriptive_state`; IdOB `copular_state`
9. **Notes:** documented-only. Pair with 001 for NP vs AP.

### PA-CSE-003 / locative

1. **ID:** PA-CSE-003 / locative
2. **Utterance:** The book is on the table.
3. **Coverage hole ID:** HOLE-04
4. **Human-space:** primary mood=declarative; secondaries polarity=positive, person=3rd, nesting=simple, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** SOB (CP + LOC) + SROB (location role)
6. **Semantic-space stressor:** TRU `descriptive_locative`; SmOB locative adjacency cue
7. **Structural content:** NP → CP → LOC
8. **Important structural values:** roles theme, state, location; geometry NP → CP → LOC; TRU `descriptive_locative`; IdOB `locative`
9. **Notes:** documented-only. CP locative half of HOLE-04.

### PA-CSE-004 / locative

1. **ID:** PA-CSE-004 / locative
2. **Utterance:** The rain stays in the plain.
3. **Coverage hole ID:** HOLE-04
4. **Human-space:** primary mood=declarative; secondaries polarity=positive, person=3rd, nesting=simple, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** SOB (ST vs CP) + CnOB (state-verb + LOC completeness)
6. **Semantic-space stressor:** TRU `descriptive_locative`; SmOB locative adjacency cue
7. **Structural content:** NP → ST → LOC
8. **Important structural values:** roles theme, state, location; geometry NP → ST → LOC; TRU `descriptive_locative`; IdOB `locative`
9. **Notes:** documented-only. ST locative half of HOLE-04.

### PA-CSE-005 / mixed_desc

1. **ID:** PA-CSE-005 / mixed_desc
2. **Utterance:** The rain in Spain stays mainly in the plain.
3. **Coverage hole ID:** HOLE-06
4. **Human-space:** primary modifier-chain=short; secondaries mood=declarative, polarity=positive, person=3rd, nesting=nested, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** SOB (PP + PN stack) + SROB (relation / modifier)
6. **Semantic-space stressor:** SmOB locative adjacency + modifier_resolution; TRU `descriptive_locative`
7. **Structural content:** NP → PP → PN → ST → LOC
8. **Important structural values:** roles theme, relation, state, location; geometry NP → PP → PN → ST → LOC; TRU `descriptive_locative`; IdOB `mixed_descriptive` + `modifier_resolution`
9. **Notes:** documented-only. Canonical mixed descriptive.

### PA-CSE-006 / interrogative

1. **ID:** PA-CSE-006 / interrogative
2. **Utterance:** Where is the book?
3. **Coverage hole ID:** HOLE-01
4. **Human-space:** primary mood=interrogative; secondaries polarity=positive, person=3rd, nesting=simple, fragment=full clause, speech-act=query
5. **Structural-space stressor:** SOB (WQ + IQ) + CnOB (interrogative scope)
6. **Semantic-space stressor:** TRU `interrogative_open`; IdOB `interrogative_wh`
7. **Structural content:** WQ → IQ → NP
8. **Important structural values:** roles query_focus, predicate, theme; geometry WQ → IQ → NP; TRU `interrogative_open`; IdOB `interrogative_wh`
9. **Notes:** documented-only. WH-locative open question.

### PA-CSE-007 / interrogative

1. **ID:** PA-CSE-007 / interrogative
2. **Utterance:** Is the book on the table?
3. **Coverage hole ID:** HOLE-02
4. **Human-space:** primary mood=interrogative; secondaries polarity=positive, person=3rd, nesting=simple, fragment=full clause, speech-act=query
5. **Structural-space stressor:** SOB (IQ-fronted polar) + CnOB (polar scope)
6. **Semantic-space stressor:** TRU `interrogative_open`; IdOB `interrogative_polar`
7. **Structural content:** IQ → NP → LOC
8. **Important structural values:** roles query_focus, predicate, theme, location; geometry IQ → NP → LOC; TRU `interrogative_open` *(not a polar TRU label)*; IdOB `interrogative_polar`
9. **Notes:** documented-only. Polar maps to TRU `interrogative_open` per constitution §5.

### PA-CSE-008 / interrogative

1. **ID:** PA-CSE-008 / interrogative
2. **Utterance:** Why is the sky blue?
3. **Coverage hole ID:** HOLE-01
4. **Human-space:** primary mood=interrogative; secondaries polarity=positive, person=3rd, nesting=simple, fragment=full clause, speech-act=query
5. **Structural-space stressor:** SOB (WQ + IQ + AP) + CnOB (WH scope over state)
6. **Semantic-space stressor:** TRU `interrogative_open`; IdOB `interrogative_wh`
7. **Structural content:** WQ → IQ → NP → AP
8. **Important structural values:** roles query_focus, predicate, theme, state; geometry WQ → IQ → NP → AP; TRU `interrogative_open`; IdOB `interrogative_wh`
9. **Notes:** live. Only utterance invoked by committed `run_examples.py` as of 2026-09-23.

### PA-CSE-009 / mixed_inter

1. **ID:** PA-CSE-009 / mixed_inter
2. **Utterance:** Why does the rain in Spain stay mainly in the plain?
3. **Coverage hole ID:** HOLE-06
4. **Human-space:** primary nesting=nested; secondaries mood=interrogative, modifier-chain=short, polarity=positive, person=3rd, fragment=full clause, speech-act=query
5. **Structural-space stressor:** CnOB (WH scope over mixed descriptive) + SOB (PP stack under WQ)
6. **Semantic-space stressor:** TRU `interrogative_nested`; SmOB locative + modifier cues
7. **Structural content:** WQ → IQ → NP → PP → ST → LOC
8. **Important structural values:** roles query_focus, predicate, theme, relation, state, location; geometry WQ → IQ → NP → PP → ST → LOC; TRU `interrogative_nested`; IdOB `interrogative_wh` + `mixed_descriptive`
9. **Notes:** documented-only.

### PA-CSE-010 / mixed_inter

1. **ID:** PA-CSE-010 / mixed_inter
2. **Utterance:** Where is the book that is on the table?
3. **Coverage hole ID:** HOLE-05
4. **Human-space:** primary nesting=nested; secondaries mood=interrogative, polarity=positive, person=3rd, fragment=full clause, speech-act=query
5. **Structural-space stressor:** SOB (RELC) + CnOB (relative + WH scope)
6. **Semantic-space stressor:** TRU `interrogative_nested`; SmOB locative adjacency inside RELC
7. **Structural content:** WQ → IQ → NP → RELC → IQ → LOC
8. **Important structural values:** roles query_focus, predicate, theme, relation, location; geometry WQ → IQ → NP → RELC → IQ → LOC; TRU `interrogative_nested`; IdOB `interrogative_wh` + `modifier_resolution`
9. **Notes:** documented-only. RELC locative nest.

### PA-CSE-011 / mixed_inter

1. **ID:** PA-CSE-011 / mixed_inter
2. **Utterance:** Why is the sky that is blue bright?
3. **Coverage hole ID:** HOLE-05
4. **Human-space:** primary nesting=nested; secondaries mood=interrogative, modifier-chain=short, polarity=positive, person=3rd, fragment=full clause, speech-act=query
5. **Structural-space stressor:** SOB (RELC + stacked AP) + CnOB (WH scope vs inner copular)
6. **Semantic-space stressor:** TRU `interrogative_nested`; IdOB `interrogative_wh` + `copular_state`
7. **Structural content:** WQ → IQ → NP → RELC → IQ → AP → AP
8. **Important structural values:** roles query_focus, predicate, theme, relation, state; geometry WQ → IQ → NP → RELC → IQ → AP → AP; TRU `interrogative_nested`; IdOB `interrogative_wh` + `copular_state`
9. **Notes:** documented-only. RELC state nest.

---

## Stretch corpus (cap 10)

All stretch rows are coverage demand. They are not supported families. Status is `Not yet implemented`.

### PA-CSE-012 / copular

1. **ID:** PA-CSE-012 / copular
2. **Utterance:** Close the door.
3. **Coverage hole ID:** HOLE-09
4. **Human-space:** primary mood=imperative; secondaries speech-act=command, person=2nd, polarity=positive, nesting=simple, fragment=full clause
5. **Structural-space stressor:** SOB (missing theme NP; command shape) + SROB (addressee / action)
6. **Semantic-space stressor:** IdOB `agent_action` (proposed use, not a command TRU)
7. **Structural content:** proposed command shape; no frozen imperative segment. Do not invent VP.
8. **Important structural values:** roles proposed addressee, action; no frozen geometry arrow; no frozen command TRU
9. **Notes:** requires packet or dictionary change. Would require new sentence family or new segment type for imperative. Stretch type: imperative.

### PA-CSE-013 / copular

1. **ID:** PA-CSE-013 / copular
2. **Utterance:** The sky is not blue.
3. **Coverage hole ID:** HOLE-08
4. **Human-space:** primary polarity=negative; secondaries mood=declarative, person=3rd, nesting=simple, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** CnOB (negation / polarity constraint)
6. **Semantic-space stressor:** TRU `descriptive_state` under polarity; basin residue if negation is unseen
7. **Structural content:** NP → CP → AP *(negation token has no frozen segment)*
8. **Important structural values:** roles theme, state; geometry NP → CP → AP; TRU `descriptive_state`; polarity unmarked in current TRU
9. **Notes:** requires packet or dictionary change. Would require new constraint / cue for negation. Stretch type: negation.

### PA-CSE-014 / locative

1. **ID:** PA-CSE-014 / locative
2. **Utterance:** The book is on the table and the lamp is on the desk.
3. **Coverage hole ID:** HOLE-11
4. **Human-space:** primary coordination=coordinated; secondaries mood=declarative, polarity=positive, person=3rd, nesting=nested, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** SOB (clause coordination) + CnOB (two LOC completeness constraints)
6. **Semantic-space stressor:** two locative basins; overlap / residue at IdOB
7. **Structural content:** NP → CP → LOC + NP → CP → LOC *(coordinator has no frozen segment)*
8. **Important structural values:** roles theme, state, location (twice); TRU `descriptive_locative`; no frozen coordination geometry
9. **Notes:** requires packet or dictionary change. Would require new segment type or constraint family for coordination. Stretch type: coordination.

### PA-CSE-015 / locative

1. **ID:** PA-CSE-015 / locative
2. **Utterance:** If the book is on the table, the lamp is in the hall.
3. **Coverage hole ID:** HOLE-10
4. **Human-space:** primary conditionality=conditional; secondaries mood=declarative, polarity=positive, person=3rd, nesting=nested, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** CnOB (conditional relation between two locatives)
6. **Semantic-space stressor:** no frozen conditional TRU; basin residue across clauses
7. **Structural content:** NP → CP → LOC , NP → CP → LOC *(if-marker has no frozen segment)*
8. **Important structural values:** roles theme, state, location (twice); TRU none frozen for conditionals
9. **Notes:** requires packet or dictionary change. Would require new TRU label: conditional. Stretch type: conditional.

### PA-CSE-016 / locative

1. **ID:** PA-CSE-016 / locative
2. **Utterance:** On the table.
3. **Coverage hole ID:** HOLE-12
4. **Human-space:** primary fragment=fragment; secondaries mood=declarative, polarity=positive, person=3rd, nesting=simple, speech-act=neutral
5. **Structural-space stressor:** SOB (incomplete clause) + CnOB (missing theme)
6. **Semantic-space stressor:** IdOB `residual_identity`; basin residue from underspecification
7. **Structural content:** LOC
8. **Important structural values:** role location only; no frozen fragment geometry; TRU none
9. **Notes:** requires packet or dictionary change. Catalog requires interpretive completeness. Stretch type: fragment / ellipsis.

### PA-CSE-017 / copular

1. **ID:** PA-CSE-017 / copular
2. **Utterance:** I am tired.
3. **Coverage hole ID:** HOLE-13
4. **Human-space:** primary person=1st; secondaries mood=declarative, polarity=positive, nesting=simple, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** SROB (speaker as theme)
6. **Semantic-space stressor:** IdOB `copular_state`; speaker port not first-class in short-sim catalogs
7. **Structural content:** NP → CP → AP
8. **Important structural values:** roles theme, state; geometry NP → CP → AP; TRU `descriptive_state`; person unmarked
9. **Notes:** requires packet or dictionary change. Would require person / speaker role if 1st person is to be first-class. Stretch type: 1st / 2nd person.

### PA-CSE-018 / copular

1. **ID:** PA-CSE-018 / copular
2. **Utterance:** The door was closed by the wind.
3. **Coverage hole ID:** HOLE-14
4. **Human-space:** primary mood=declarative; secondaries polarity=positive, person=3rd, nesting=simple, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** SROB (theme vs agent under passive) + CnOB (by-PP)
6. **Semantic-space stressor:** IdOB `agent_action` with inverted ports
7. **Structural content:** NP → ST → PP → NP *(passive auxiliary not a frozen segment; VP proposed only)*
8. **Important structural values:** roles proposed theme, state, agent; no frozen passive geometry; TRU none frozen for events
9. **Notes:** requires packet or dictionary change. Would require new sentence family or new IdOB family use-pattern for passive. Stretch type: passive.

### PA-CSE-019 / copular

1. **ID:** PA-CSE-019 / copular
2. **Utterance:** Every sky is blue.
3. **Coverage hole ID:** HOLE-15
4. **Human-space:** primary mood=declarative; secondaries polarity=positive, person=3rd, nesting=simple, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** SOB (quantified NP) + CnOB (universal completeness)
6. **Semantic-space stressor:** TRU `descriptive_state`; quantifier has no frozen cue
7. **Structural content:** NP → CP → AP
8. **Important structural values:** roles theme, state; geometry NP → CP → AP; TRU `descriptive_state`; quantifier unmarked
9. **Notes:** requires packet or dictionary change. Would require new constraint / cue for quantification. Stretch type: quantified NP.

### PA-CSE-020 / copular

1. **ID:** PA-CSE-020 / copular
2. **Utterance:** How blue the sky is!
3. **Coverage hole ID:** HOLE-16
4. **Human-space:** primary mood=exclamative; secondaries polarity=positive, person=3rd, nesting=simple, fragment=full clause, speech-act=neutral
5. **Structural-space stressor:** SOB (exclamative fronting) + CnOB (degree / exclamative scope)
6. **Semantic-space stressor:** no frozen exclamative TRU
7. **Structural content:** AP → NP → CP *(exclamative order; WQ must not be forced onto this row)*
8. **Important structural values:** roles theme, state; no frozen exclamative geometry; TRU none
9. **Notes:** requires packet or dictionary change. Would require new TRU label: exclamative. Stretch type: exclamative.

### PA-CSE-021 / interrogative

1. **ID:** PA-CSE-021 / interrogative
2. **Utterance:** Please put the book on the table.
3. **Coverage hole ID:** HOLE-09
4. **Human-space:** primary speech-act=request; secondaries mood=imperative, person=2nd, polarity=positive, nesting=simple, fragment=full clause
5. **Structural-space stressor:** SROB (addressee + theme + location) + CnOB (request force vs locative completeness)
6. **Semantic-space stressor:** IdOB `agent_action` + locative; no request TRU
7. **Structural content:** NP → LOC *(please / command verb have no frozen segments; VP proposed only)*
8. **Important structural values:** roles proposed addressee, action, theme, location; TRU none frozen for requests
9. **Notes:** requires packet or dictionary change. Would require new sentence family or speech-act TRU. Stretch type: non-WH speech-act request.

---

## Index

| ID | Utterance | Family tag | Hole |
|---|---|---|---|
| PA-CSE-001 / copular | The sky is blue. | copular | HOLE-03 |
| PA-CSE-002 / copular | Paris is a city. | copular | HOLE-03 |
| PA-CSE-003 / locative | The book is on the table. | locative | HOLE-04 |
| PA-CSE-004 / locative | The rain stays in the plain. | locative | HOLE-04 |
| PA-CSE-005 / mixed_desc | The rain in Spain stays mainly in the plain. | mixed_desc | HOLE-06 |
| PA-CSE-006 / interrogative | Where is the book? | interrogative | HOLE-01 |
| PA-CSE-007 / interrogative | Is the book on the table? | interrogative | HOLE-02 |
| PA-CSE-008 / interrogative | Why is the sky blue? | interrogative | HOLE-01 |
| PA-CSE-009 / mixed_inter | Why does the rain in Spain stay mainly in the plain? | mixed_inter | HOLE-06 |
| PA-CSE-010 / mixed_inter | Where is the book that is on the table? | mixed_inter | HOLE-05 |
| PA-CSE-011 / mixed_inter | Why is the sky that is blue bright? | mixed_inter | HOLE-05 |
| PA-CSE-012 / copular | Close the door. | copular | HOLE-09 |
| PA-CSE-013 / copular | The sky is not blue. | copular | HOLE-08 |
| PA-CSE-014 / locative | The book is on the table and the lamp is on the desk. | locative | HOLE-11 |
| PA-CSE-015 / locative | If the book is on the table, the lamp is in the hall. | locative | HOLE-10 |
| PA-CSE-016 / locative | On the table. | locative | HOLE-12 |
| PA-CSE-017 / copular | I am tired. | copular | HOLE-13 |
| PA-CSE-018 / copular | The door was closed by the wind. | copular | HOLE-14 |
| PA-CSE-019 / copular | Every sky is blue. | copular | HOLE-15 |
| PA-CSE-020 / copular | How blue the sky is! | copular | HOLE-16 |
| PA-CSE-021 / interrogative | Please put the book on the table. | interrogative | HOLE-09 |
