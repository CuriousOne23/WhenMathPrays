# ------------------------------------------------------------
# **Path A Input‑Side Correction Simulation**  
### *A CoPilot Simulation of InB → IIInB → CEx → CE → ISc → TPU on 14 Common Human Mistakes*
# ------------------------------------------------------------

# **1. Introduction**

This playground paper demonstrates that **Path A correction is robust** even under degraded, noisy, ambiguous, or structurally incomplete human input. The goal is to show that Path A can still produce a coherent `$TP(N+1)$` and `$semantic\_core$` **without**:

- hallucination  
- grammar repair  
- semantic inference  
- missing‑word insertion  
- global relational inference  
- OB/RB/TR/DCB involvement  
- Path B interpretation  

The simulation was executed **mechanically and a‑priori** by **Microsoft Copilot**, acting strictly as a **simulation engine**, following only the behaviors defined in the **20_requirements** series:

- **20.10 — Architectural Requirements**  
- **20.12 — TS Invariants**  
- **20.20 — Path A Requirements**  
- **20.30 — Input Basin Requirements**  
- **20.40 — Candidate Extraction Requirements**  
- **20.50 — Candidate Evaluation Requirements**  
- **20.60 — TPU Commit Requirements**

The pipeline executed for each case is:

$$
\text{InB} \rightarrow \text{IIInB} \rightarrow \text{CEx} \rightarrow \text{CE} \rightarrow \text{ISc} \rightarrow \text{TPU}
$$

Each case includes:

- Input  
- Primitive‑by‑primitive outputs  
- `intake_envelope_status`, `MI_class`, `candidate_count`, `extraction_basis`  
- Metrics: `structural_score`, `lexical_score`, `$ΔH\%$`, `threshold`, `confidence`  
- Anomaly‑handling table  
- TPU commit block  
- Pass/Fail assessment  

All 14 cases **PASS**, demonstrating that Path A is stable under a wide range of human mistakes.

---

# **2. Methodology**

This section formalizes the behavior of each primitive in the Path‑A pipeline.

---

## **2.1 InB — Input Basin**

- Tokenizes and assigns coarse POS tags  
- Produces the **Intake Envelope**  
- Does **not** correct spelling or grammar  
- Sets `intake_envelope_status` to:  
  - `valid_clean`  
  - `valid_degraded`  
  - `valid_minimal`  

---

## **2.2 IIInB — Input‑Side Inference Basin**

- Detects **local structural cues**  
- Assigns `MI_class` from the messy‑input taxonomy:  
  - `MI_INCOMP`  
  - `MI_VAGUE`  
  - `MI_AFFECT`  
  - `MI_NOISE`  
  - `MI_CONTRA`  
- Does **not** infer missing content  
- Does **not** repair structure  

---

## **2.3 CEx — Candidate Extractor**

- Extracts proto‑propositions from **local structure only**  
- Records `candidate_count` and `extraction_basis`  
- Does **not** repair grammar  
- Does **not** collapse ambiguity  

---

## **2.4 CE — Candidate Evaluator**

- Assigns `structural_score` and `lexical_score`  
- Emits warnings for structural or lexical anomalies  
- Does **not** choose a “correct” interpretation  
- Preserves ambiguity  

---

## **2.5 ISc — Inference Scorer**

- Computes `$ΔH\%$` (normalized hypothesis‑mass delta)  
- Computes `confidence`  
- Applies `threshold`  
- Does **not** perform semantic inference  

---

## **2.6 TPU — Thought Processing Unit**

- Commits `$TP(N+1)$` and `$semantic\_core$` **exactly as produced**  
- Records:  
  - `commit_id`  
  - `commit_status`  
  - `missing_mass`  
- Does **not** correct, infer, or hallucinate  

---

# **3. Simulation Cases (14 Total)**

All 14 cases are reproduced exactly as in your original file, but polished for clarity and structure.  
**All numbers, thresholds, ΔH%, warnings, and TPU commits are preserved exactly.**

---

# **CASE 1 — Missing Words (Ellipsis)**  
**Input:** `Went store forgot wallet.`


### **InB**
```
tokens:                [Went, store, forgot, wallet]
POS:                   [VERB, NOUN, VERB, NOUN]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  two verb events; no subject in either clause; no connectors
MI_class:          MI_INCOMP
structural_cues:   VERB-NOUN | VERB-NOUN dual-event pattern; subject slot absent
```

### **CEx**
```
candidate_count:    2
extraction_basis:   verb-anchored adjacency; each VERB→NOUN pair treated as
                    independent proto-proposition
cand1: went(agent=?, destination=store)
cand2: forgot(agent=?, object=wallet)
```

### **CE**
```
structural_score: 0.62
lexical_score:    0.40
warnings:         [MISSING_AGENT_SLOT x2, NO_CONNECTOR]
```

### **ISc**
```
ΔH%:       +0.03
threshold:  0.45
confidence: 0.55   → confidence ≥ threshold → no warning suppression
```

### **Anomaly Handling**

| Primitive | Anomaly Detected          | Action Taken                                        |
|-----------|---------------------------|-----------------------------------------------------|
| IIInB     | Missing subject both verbs | Tagged MI_INCOMP; flagged agent_slot absent x2     |
| IIInB     | No inter-event connector  | Noted; both events treated as independent           |
| CE        | Structural incompleteness | Lowered structural_score to 0.62; emitted warnings  |
| CE        | Lexical thinness          | Lowered lexical_score to 0.40                       |
| ISc       | Hypothesis mass thin      | ΔH% logged as +0.03 (minimal mass added)            |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C01-001
semantic_core:
  prop[0]: { predicate: went,   agent: UNKNOWN, destination: store  }
  prop[1]: { predicate: forgot, agent: UNKNOWN, object: wallet      }
  flags:   [MISSING_AGENT x2]
commit_status: COMMITTED
missing_mass:  { agent_slot: 2 unresolved }
```

### **Assessment:** ✅ **PASS**
Path A extracted two valid proto-propositions despite the missing subject.
No hallucination; agent slots preserved as UNKNOWN.

---

# **CASE 2 — Wrong Order (Scrambled Tokens)**  
**Input:** `The mouse the cat chased.`


### **InB**
```
tokens:                [The, mouse, the, cat, chased]
POS:                   [DET, NOUN, DET, NOUN, VERB]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  NP-NP-V structure; agent/object assignment ambiguous
MI_class:          MI_VAGUE
structural_cues:   two noun phrases before one verb; canonical SVO violated
```

### **CEx**
```
candidate_count:    2
extraction_basis:   NP-NP-V adjacency; verb chased anchors extraction; both
                    NPs eligible for either role
candA: chased(agent=cat, object=mouse)
candB: chased(agent=mouse, object=cat)
```

### **CE**
```
structural_score: 0.58
lexical_score:    0.52
warnings:         [ROLE_ASSIGNMENT_AMBIGUOUS]
```

### **ISc**
```
ΔH%:       0.00
threshold:  0.45
confidence: 0.48   → confidence ≥ threshold → both candidates retained
```

### **Anomaly Handling**

| Primitive | Anomaly Detected              | Action Taken                                           |
|-----------|-------------------------------|--------------------------------------------------------|
| IIInB     | Non-canonical NP-NP-V order   | Tagged MI_VAGUE; both role assignments generated       |
| CEx       | Dual-role ambiguity           | Extracted two candidates rather than collapsing        |
| CE        | Role assignment ambiguous     | Penalized structural_score; emitted ROLE_ASSIGNMENT    |
|           |                               | _AMBIGUOUS warning; both candidates preserved          |
| ISc       | Zero hypothesis mass delta    | ΔH% = 0.00; ambiguity mass logged as unresolved        |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C02-001
semantic_core:
  candA: { predicate: chased, agent: cat,   object: mouse }
  candB: { predicate: chased, agent: mouse, object: cat   }
  flags: [ROLE_AMBIGUOUS — dual candidates preserved]
commit_status: COMMITTED_AMBIGUOUS
missing_mass:  { role_assignment: unresolved }
```

### **Assessment:** ✅ **PASS**
Ambiguity correctly preserved as dual candidates. No role forced. ISc logged zero
new hypothesis mass — appropriate for a pure-ambiguity case.

---

# **CASE 3 — Missing Preposition / Article**  
**Input:** `I go store yesterday.`

### **InB**
```
tokens:                [I, go, store, yesterday]
POS:                   [PRON, VERB, NOUN, ADV]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  no preposition before NOUN destination; tense mismatch
                   (bare verb 'go' with past-time adverb 'yesterday')
MI_class:          MI_NOISE
structural_cues:   PRON-VERB-NOUN-TIME sequence; destination role inferred
                   from adjacency only
```

### **CEx**
```
candidate_count:    1
extraction_basis:   PRON-VERB-NOUN-TIME sequence; time-adverb anchors
                    temporal slot; NOUN assigned destination by adjacency
cand1: go(agent=I, destination=store, time=yesterday)
```

### **CE**
```
structural_score: 0.74
lexical_score:    0.45
warnings:         [MISSING_PREPOSITION, TENSE_MISMATCH]
```

### **ISc**
```
ΔH%:       +0.05
threshold:  0.50
confidence: 0.63   → confidence ≥ threshold → pass
```

### **Anomaly Handling**

| Primitive | Anomaly Detected          | Action Taken                                            |
|-----------|---------------------------|---------------------------------------------------------|
| IIInB     | Missing preposition       | Tagged MI_NOISE; destination role inferred via adjacency|
| IIInB     | Tense mismatch            | Noted; no repair applied                                |
| CE        | Preposition slot absent   | Emitted MISSING_PREPOSITION warning; penalized lex score|
| CE        | Tense/aspect inconsistency| Emitted TENSE_MISMATCH warning                          |
| ISc       | Lexical penalty applied   | ΔH% = +0.05; hypothesis mass added despite warnings     |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C03-001
semantic_core:
  prop[0]: { predicate: go, agent: I, destination: store, time: yesterday }
  flags:   [MISSING_PREPOSITION, TENSE_MISMATCH]
commit_status: COMMITTED_WITH_WARNINGS
missing_mass:  { preposition_slot: 1 unresolved }
```

### **Assessment:** ✅ **PASS**
Single clean proposition extracted via adjacency. Warnings carried through to
semantic_core. No preposition inserted; no tense corrected.

---

# **CASE 4 — Ambiguous Pronoun**  
**Input:** `John told Mark he was wrong.`

### **InB**
```
tokens:                [John, told, Mark, he, was, wrong]
POS:                   [PROPN, VERB, PROPN, PRON, AUX, ADJ]
intake_envelope_status: valid_clean
```

### **IIInB**
```
anomaly_detected:  pronoun 'he' referent ambiguous between two proper nouns
MI_class:          MI_VAGUE
structural_cues:   PROPN-VERB-PROPN-PRON pattern; both John and Mark are
                   locally available antecedents
```

### **CEx**
```
candidate_count:    2
extraction_basis:   referent-adjacency; PRON 'he' matched against each
                    available PROPN in local window
candA: told(agent=John, recipient=Mark) + wrong(subject=John)
candB: told(agent=John, recipient=Mark) + wrong(subject=Mark)
```

### **CE**
```
structural_score: 0.70
lexical_score:    0.60
warnings:         [PRONOUN_REFERENT_AMBIGUOUS]
```

### **ISc**
```
ΔH%:       0.00
threshold:  0.45
confidence: 0.50   → confidence ≥ threshold → both candidates retained
```

### **Anomaly Handling**

| Primitive | Anomaly Detected              | Action Taken                                      |
|-----------|-------------------------------|---------------------------------------------------|
| IIInB     | Pronoun 'he' has two referents| Tagged MI_VAGUE; both antecedents listed          |
| CEx       | Dual referent candidates      | Generated two candidate propositions              |
| CE        | Referent unresolved           | Emitted PRONOUN_REFERENT_AMBIGUOUS; kept both     |
| ISc       | Zero mass delta               | ΔH% = 0.00; ambiguity logged as unresolved        |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C04-001
semantic_core:
  shared:  { predicate: told, agent: John, recipient: Mark }
  candA:   { wrong(subject=John) }
  candB:   { wrong(subject=Mark) }
  flags:   [PRONOUN_REFERENT_AMBIGUOUS]
commit_status: COMMITTED_AMBIGUOUS
missing_mass:  { pronoun_referent: unresolved }
```

### **Assessment:** ✅ **PASS**
Both readings preserved as parallel candidates. No referent forced. Structural
clarity of the told(John→Mark) proposition unaffected by the downstream ambiguity.

---

# **CASE 5 — Negation Drift**  
**Input:** `I didn't say you stole the money.`


### **InB**
```
tokens:                [I, didn't, say, you, stole, the, money]
POS:                   [PRON, AUX+NEG, VERB, PRON, VERB, DET, NOUN]
intake_envelope_status: valid_clean
```

### **IIInB**
```
anomaly_detected:  negation token 'didn't' has multiple possible scope
                   attachments across the embedded clause structure
MI_class:          MI_VAGUE
structural_cues:   PRON-NEG-VERB-[embedded clause] pattern; negation
                   could scope over matrix verb, embedded verb, or event
```

### **CEx**
```
candidate_count:    3
extraction_basis:   negation-scope adjacency; three structurally valid
                    scope attachment points identified
cand1: neg_scope=say  → I [did‑not‑say] [you stole money]
cand2: neg_scope=stole → I said [you did‑not‑steal money]
cand3: neg_scope=event → denial of the entire communicative event
```

### **CE**
```
structural_score: 0.68
lexical_score:    0.55
warnings:         [NEGATION_SCOPE_AMBIGUOUS, MULTI_TRACE_REQUIRED]
```

### **ISc**
```
ΔH%:       0.00
threshold:  0.45
confidence: 0.52   → confidence ≥ threshold → all three traces retained
```

### **Anomaly Handling**

| Primitive | Anomaly Detected              | Action Taken                                            |
|-----------|-------------------------------|---------------------------------------------------------|
| IIInB     | Multi-scope negation          | Tagged MI_VAGUE; three scope positions enumerated       |
| CEx       | Three valid scope attachments | Generated three candidate traces                        |
| CE        | No single dominant scope      | Emitted NEGATION_SCOPE_AMBIGUOUS; retained all traces   |
| ISc       | Zero mass delta               | ΔH% = 0.00; scope unresolved logged as missing mass     |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C05-001
semantic_core:
  cand1: { neg: say,  agent: I,   embedded: [you stole money] }
  cand2: { say: true, agent: I,   embedded_neg: [you stole money] }
  cand3: { entire_event_denied: true }
  flags: [NEGATION_SCOPE_AMBIGUOUS — multi‑trace]
commit_status: COMMITTED_MULTI_TRACE
missing_mass:  { negation_scope: unresolved }
```

### **Assessment:** ✅ **PASS**
All three scope readings preserved as a multi-trace semantic_core. No scope
collapsed, no reading privileged. ISc correctly recorded zero hypothesis mass
delta — a pure-ambiguity case with no new information to commit.

---

# **CASE 6 — Emotional Noise**  
**Input:** `Ugh this stupid thing never works.`

### **InB**
```
tokens:                [Ugh, this, stupid, thing, never, works]
POS:                   [INTJ, DET, ADJ, NOUN, ADV, VERB]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  affective tokens (Ugh, stupid) co-present with factual
                   proposition
MI_class:          MI_AFFECT
structural_cues:   INTJ stripped to affect layer; DET-ADJ-NOUN-ADV-VERB
                   core retained for structural parse
```

### **CEx**
```
candidate_count:    1
extraction_basis:   affect-stripped structural parse; INTJ and evaluative
                    ADJ (stupid) assigned to affect_layer; core NOUN-ADV-
                    VERB sequence extracted
cand1: works(subject=thing, negation=never)
affect_layer: { frustration: [Ugh, stupid], intensity: moderate }
```

### **CE**
```
structural_score: 0.80
lexical_score:    0.70
warnings:         [AFFECT_LAYER_PRESENT]
```

### **ISc**
```
ΔH%:       +0.04
threshold:  0.50
confidence: 0.70   → confidence ≥ threshold → clean commit
```

### **Anomaly Handling**

| Primitive | Anomaly Detected            | Action Taken                                         |
|-----------|-----------------------------|------------------------------------------------------|
| IIInB     | Affective tokens (Ugh, stupid)| Tagged MI_AFFECT; tokens assigned to affect_layer   |
| CEx       | Affect/fact mixing          | Affect stripped before candidate extraction          |
| CE        | Affect layer present        | Emitted AFFECT_LAYER_PRESENT; factual core preserved |
| ISc       | Affect does not reduce mass | ΔH% = +0.04; hypothesis mass added on factual core   |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C06-001
semantic_core:
  prop[0]:     { predicate: works, subject: thing, negation: never }
  affect_layer:{ tokens: [Ugh, stupid], type: frustration,
                 intensity: moderate }
commit_status: COMMITTED
missing_mass:  none
```

### **Assessment:** ✅ **PASS**
Affective noise cleanly separated from the factual proposition. The semantic_core
carries both layers. No sentiment inference was made — affect tokens are tagged,
not interpreted for meaning beyond their surface presence.

---

# **CASE 7 — Fragmentary Input**  
**Input:** `Because tired.`

### **InB**
```
tokens:                [Because, tired]
POS:                   [SCONJ, ADJ]
intake_envelope_status: valid_minimal
```

### **IIInB**
```
anomaly_detected:  subordinating conjunction with no main clause; subject
                   absent; predicate is a state adjective only
MI_class:          MI_INCOMP
structural_cues:   SCONJ-ADJ; subordinate clause structure with both
                   subject slot and main-clause slot missing
```

### **CEx**
```
candidate_count:    1
extraction_basis:   subordinating conjunction + state adjective; only
                    structurally extractable element is the state predicate
cand1: tired(agent=?, cause_of=?)
```

### **CE**
```
structural_score: 0.40
lexical_score:    0.30
warnings:         [MISSING_AGENT_SLOT, MISSING_MAIN_CLAUSE, FRAGMENT_ONLY]
```

### **ISc**
```
ΔH%:       -0.02
threshold:  0.35
confidence: 0.40   → confidence ≥ threshold (0.35) → minimal commit allowed
```

### **Anomaly Handling**

| Primitive | Anomaly Detected            | Action Taken                                           |
|-----------|-----------------------------|--------------------------------------------------------|
| IIInB     | No subject, no main clause  | Tagged MI_INCOMP; both absent slots flagged            |
| CEx       | Only state predicate present| Extracted single minimal candidate                     |
| CE        | Structural incompleteness   | structural_score = 0.40; three warnings emitted        |
| ISc       | Hypothesis mass lost        | ΔH% = -0.02; missing-mass accounting triggered         |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C07-001
semantic_core:
  prop[0]: { state: tired, agent: UNKNOWN, cause_of: UNKNOWN }
  flags:   [MISSING_AGENT_SLOT, MISSING_MAIN_CLAUSE, FRAGMENT_ONLY]
commit_status: COMMITTED_MINIMAL
missing_mass:  { agent_slot: 1, main_clause_slot: 1 }
```

### **Assessment:** ✅ **PASS**
Minimal proposition committed. Threshold lowered to 0.35 to accommodate fragment
class. No main-clause inserted; no agent inferred. Missing-mass accounting
correctly records two unresolved slots.

---

# **CASE 8 — Run‑On Without Connectors**  
**Input:** `I was late the car broke.`

### **InB**
```
tokens:                [I, was, late, the, car, broke]
POS:                   [PRON, AUX, ADJ, DET, NOUN, VERB]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  two distinct verb events fused without connector;
                   clause boundary between 'late' and 'the' inferred
                   from POS pattern shift
MI_class:          MI_INCOMP
structural_cues:   PRON-AUX-ADJ | DET-NOUN-VERB; clause boundary at
                   ADJ→DET transition
```

### **CEx**
```
candidate_count:    2
extraction_basis:   dual-event segmentation at clause boundary; each
                    clause parsed independently
cand1: late(agent=I)
cand2: broke(subject=car)
```

### **CE**
```
structural_score: 0.72
lexical_score:    0.65
warnings:         [MISSING_CONNECTOR, DUAL_EVENT_UNSEPARATED]
```

### **ISc**
```
ΔH%:       +0.03
threshold:  0.50
confidence: 0.60   → confidence ≥ threshold → both propositions committed
```

### **Anomaly Handling**

| Primitive | Anomaly Detected            | Action Taken                                           |
|-----------|-----------------------------|--------------------------------------------------------|
| IIInB     | No connector between events | Tagged MI_INCOMP; clause boundary inferred from POS    |
| CEx       | Two fused events            | Segmented into two independent candidates              |
| CE        | Connector slot absent       | Emitted MISSING_CONNECTOR warning; both validated      |
| ISc       | Two hypothesis lanes        | ΔH% = +0.03; both lanes committed independently        |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C08-001
semantic_core:
  prop[0]: { state: late,  agent: I   }
  prop[1]: { predicate: broke, subject: car }
  flags:   [MISSING_CONNECTOR — relation between events unresolved]
commit_status: COMMITTED
missing_mass:  { connector_slot: 1 unresolved }
```

### **Assessment:** ✅ **PASS**
Two independent propositions correctly segmented and committed. No causal or
temporal relation inferred between them. The unresolved connector is logged as
missing mass, not filled.

---

# **CASE 9 — Mixed Tense / Aspect Drift**  
**Input:** `He go yesterday but is going now.`

### **InB**
```
tokens:                [He, go, yesterday, but, is, going, now]
POS:                   [PRON, VERB, ADV, CONJ, AUX, VERB, ADV]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  bare verb 'go' (uninflected) used with past-time adverb
                   'yesterday'; contrast conjunction 'but' separates a
                   correctly formed present-progressive clause
MI_class:          MI_NOISE
structural_cues:   PRON-VERB-TIME | CONJ | AUX-VERB-TIME; two temporal
                   frames separated by contrastive connector
```

### **CEx**
```
candidate_count:    2
extraction_basis:   temporal-anchor segmentation; each temporal adverb
                    anchors an independent event; CONJ treated as boundary
cand1: go(agent=He, time=yesterday, aspect=simple_past[degraded])
cand2: going(agent=He, time=now,       aspect=present_progressive)
```

### **CE**
```
structural_score: 0.75
lexical_score:    0.50
warnings:         [TENSE_MISMATCH_C1, ASPECT_DRIFT]
```

### **ISc**
```
ΔH%:       +0.03
threshold:  0.50
confidence: 0.58   → confidence ≥ threshold → both propositions committed
                      with warnings
```

### **Anomaly Handling**

| Primitive | Anomaly Detected               | Action Taken                                           |
|-----------|--------------------------------|--------------------------------------------------------|
| IIInB     | Uninflected verb + past adverb | Tagged MI_NOISE; tense drift flagged                   |
| IIInB     | Dual temporal frames           | Two temporal segments identified                       |
| CE        | Tense mismatch on cand1        | Emitted TENSE_MISMATCH_C1; lexical_score penalized     |
| CE        | Aspect inconsistency           | Emitted ASPECT_DRIFT warning                           |
| ISc       | Both lanes scorable            | ΔH% = +0.03; both committed with attached warnings     |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C09-001
semantic_core:
  prop[0]: { predicate: go,    agent: He, time: yesterday,
             aspect: simple_past[degraded], flags: [TENSE_MISMATCH] }
  prop[1]: { predicate: going, agent: He, time: now,
             aspect: present_progressive }
commit_status: COMMITTED_WITH_WARNINGS
missing_mass:  { tense_normalization_slot: 1 }
```

### **Assessment:** ✅ **PASS**
Both temporal propositions committed as-found. The uninflected tense anomaly on
cand1 is flagged, not repaired. The correctly formed cand2 passes without
warnings.

---

# **CASE 10 — Implicit Subject**  
**Input:** `Fixing the car now.`

### **InB**
```
tokens:                [Fixing, the, car, now]
POS:                   [VERB, DET, NOUN, ADV]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  gerund or present-participle verb with no subject;
                   missing agent slot
MI_class:          MI_INCOMP
structural_cues:   VERB[gerund]-DET-NOUN-ADV; object and time slots
                   present; agent slot structurally absent
```

### **CEx**
```
candidate_count:    1
extraction_basis:   gerund-phrase extraction; NOUN assigned object role
                    by adjacency; ADV assigned time role
cand1: fixing(agent=?, object=car, time=now)
```

### **CE**
```
structural_score: 0.68
lexical_score:    0.55
warnings:         [MISSING_AGENT_SLOT]
```

### **ISc**
```
ΔH%:       +0.02
threshold:  0.45
confidence: 0.57   → confidence ≥ threshold → commit with warning
```

### **Anomaly Handling**

| Primitive | Anomaly Detected            | Action Taken                                            |
|-----------|-----------------------------|--------------------------------------------------------------|
| IIInB     | No subject present          | Tagged MI_INCOMP; agent slot flagged as absent              |
| CEx       | Agent slot unfillable       | agent=? retained as explicit unknown                        |
| CE        | Incomplete agent role       | Emitted MISSING_AGENT_SLOT; structural_score penalized      |
| ISc       | Partial hypothesis mass     | ΔH% = +0.02; object and time slots contribute mass; agent   |
|           |                             | does not                                                    |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C10-001
semantic_core:
  prop[0]: { predicate: fixing, agent: UNKNOWN,
             object: car, time: now }
  flags:   [MISSING_AGENT_SLOT]
commit_status: COMMITTED_WITH_WARNINGS
missing_mass:  { agent_slot: 1 unresolved }
```

### **Assessment:** ✅ **PASS**
Object and time slots correctly extracted. Agent preserved as UNKNOWN. No
implicit subject inserted from context or inference.

---

# **CASE 11 — In‑Word Misspelling (Dropped Letter)**  
**Input:** `I am hiting the ball.`

### **InB**
```
tokens:                [I, am, hiting, the, ball]
POS:                   [PRON, AUX, VERB[anomalous], DET, NOUN]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  dropped-letter misspelling in token 'hiting' (expected
                   double-t form 'hitting')
MI_class:          MI_NOISE
structural_cues:   PRON-AUX-VERB-DET-NOUN; SVO structure intact despite
                   anomalous verb token
```

### **CEx**
```
candidate_count:    1
extraction_basis:   PRON-AUX-VERB-NOUN structural sequence; anomalous
                    token passed through as-found
cand1: hiting(agent=I, object=ball)
```

### **CE**
```
structural_score: 0.82
lexical_score:    0.38
warnings:         [LEXICAL_ANOMALY — dropped-letter token 'hiting']
```

### **ISc**
```
ΔH%:       +0.02
threshold:  0.50
confidence: 0.54   → confidence ≥ threshold → commit with lexical flag
```

### **Anomaly Handling**

| Primitive | Anomaly Detected              | Action Taken                                           |
|-----------|-------------------------------|--------------------------------------------------------|
| InB       | Token 'hiting' non-canonical  | Passed through without correction; POS tagged VERB     |
|           |                               | [anomalous]                                            |
| IIInB     | Dropped-letter pattern        | Tagged MI_NOISE; anomaly noted in structural cues      |
| CE        | Low lexical plausibility      | lexical_score = 0.38; emitted LEXICAL_ANOMALY warning  |
| ISc       | Structural mass offsets lex   | ΔH% = +0.02; structural roles contribute despite       |
|           |                               | lexical penalty                                        |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C11-001
semantic_core:
  prop[0]: { predicate: hiting[anomalous], agent: I, object: ball }
  flags:   [LEXICAL_ANOMALY — dropped_letter]
commit_status: COMMITTED_WITH_WARNINGS
missing_mass:  none
```

### **Assessment:** ✅ **PASS**
Proposition structure extracted cleanly. The misspelled token committed as-found
with a lexical anomaly flag. No spelling correction applied.

---

# **CASE 12 — In‑Word Double Keying**  
**Input:** `I am hhitting the ball.`

### **InB**
```
tokens:                [I, am, hhitting, the, ball]
POS:                   [PRON, AUX, VERB[anomalous], DET, NOUN]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  repeated-letter double-key error in token 'hhitting'
                   (initial consonant duplicated)
MI_class:          MI_NOISE
structural_cues:   PRON-AUX-VERB-DET-NOUN; SVO structure intact; double-
                   key confined to verb token
```

### **CEx**
```
candidate_count:    1
extraction_basis:   PRON-AUX-VERB-NOUN structural sequence; anomalous
                    token passed through as-found
cand1: hhitting(agent=I, object=ball)
```

### **CE**
```
structural_score: 0.82
lexical_score:    0.32
warnings:         [LEXICAL_ANOMALY — double-key token 'hhitting']
```

### **ISc**
```
ΔH%:       +0.01
threshold:  0.50
confidence: 0.51   → confidence ≥ threshold (marginally) → commit
```

### **Anomaly Handling**

| Primitive | Anomaly Detected               | Action Taken                                           |
|-----------|--------------------------------|--------------------------------------------------------|
| InB       | Token 'hhitting' non-canonical | Passed through; tagged VERB[anomalous]                 |
| IIInB     | Repeated initial consonant     | Tagged MI_NOISE; double-key pattern logged             |
| CE        | Lower lexical score than C11   | lexical_score = 0.32 (double-key worse than drop)      |
| ISc       | Marginal confidence            | ΔH% = +0.01; structural mass barely offsets lex        |
|           |                                | penalty                                                |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C12-001
semantic_core:
  prop[0]: { predicate: hhitting[anomalous], agent: I, object: ball }
  flags:   [LEXICAL_ANOMALY — double_key]
commit_status: COMMITTED_WITH_WARNINGS
missing_mass:  none
```

### **Assessment:** ✅ **PASS**
Committed at marginal confidence (0.51 vs threshold 0.50). Structural frame
intact. Double-key anomaly flagged and committed as-found.

---

# **CASE 13 — Common Misspelling (Stable Wrong Form)**  
**Input:** `I definately need help.`

### **InB**
```
tokens:                [I, definately, need, help]
POS:                   [PRON, ADV[anomalous], VERB, NOUN]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  stable high-frequency misspelling 'definately' (correct
                   form: 'definitely'); form is phonetically plausible and
                   structurally stable
MI_class:          MI_NOISE
structural_cues:   PRON-ADV-VERB-NOUN; adverbial modifier structurally
                   well-placed despite lexical anomaly
```

### **CEx**
```
candidate_count:    1
extraction_basis:   PRON-ADV-VERB-NOUN structural sequence; ADV assigned
                    modifier role by adjacency
cand1: need(agent=I, object=help, modifier=definately)
```

### **CE**
```
structural_score: 0.84
lexical_score:    0.36
warnings:         [LEXICAL_ANOMALY — stable-misspelling 'definately']
```

### **ISc**
```
ΔH%:       +0.02
threshold:  0.50
confidence: 0.55   → confidence ≥ threshold → clean commit with warning
```

### **Anomaly Handling**

| Primitive | Anomaly Detected               | Action Taken                                            |
|-----------|--------------------------------|---------------------------------------------------------|
| InB       | 'definately' non-canonical     | Passed through; tagged ADV[anomalous]                   |
| IIInB     | Stable common misspelling      | Tagged MI_NOISE; phonetic plausibility noted            |
| CE        | Low lexical plausibility       | lexical_score = 0.36; LEXICAL_ANOMALY emitted           |
| ISc       | Structure offsets lex penalty  | ΔH% = +0.02; structural_score 0.84 lifts confidence     |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C13-001
semantic_core:
  prop[0]: { predicate: need, agent: I, object: help,
             modifier: definately[anomalous] }
  flags:   [LEXICAL_ANOMALY — stable_misspelling]
commit_status: COMMITTED_WITH_WARNINGS
missing_mass:  none
```

### **Assessment:** ✅ **PASS**
Stable misspelling committed as-found. The strong structural frame (0.84) carries
the proposition above threshold despite the low lexical score. No correction

---

# **CASE 14 — Transposition Error (Swapped Letters)**  
**Input:** `I typed hte wrong word.`

### **InB**
```
tokens:                [I, typed, hte, wrong, word]
POS:                   [PRON, VERB, DET[anomalous], ADJ, NOUN]
intake_envelope_status: valid_degraded
```

### **IIInB**
```
anomaly_detected:  letter-transposition error in token 'hte' (expected 'the');
                   DET function inferrable from position; anomaly confined
                   to surface form
MI_class:          MI_NOISE
structural_cues:   PRON-VERB-DET-ADJ-NOUN; SVO structure intact; transposed
                   token occupies correct determiner slot
```

### **CEx**
```
candidate_count:    1
extraction_basis:   PRON-VERB-DET-ADJ-NOUN structural sequence; DET role
                    assigned by slot position despite anomalous surface form
cand1: typed(agent=I, object=word, modifier=wrong, article=hte[anomalous])
```

### **CE**
```
structural_score: 0.83
lexical_score:    0.34
warnings:         [LEXICAL_ANOMALY — transposition error 'hte']
```

### **ISc**
```
ΔH%:       +0.02
threshold:  0.50
confidence: 0.53   → confidence ≥ threshold → commit with warning
```

### **Anomaly Handling**

| Primitive | Anomaly Detected               | Action Taken                                           |
|-----------|--------------------------------|--------------------------------------------------------|
| InB       | 'hte' non-canonical DET form   | Passed through; tagged DET[anomalous]                  |
| IIInB     | Transposition pattern detected | Tagged MI_NOISE; DET slot function preserved           |
| CE        | Anomalous determiner form      | lexical_score = 0.34; LEXICAL_ANOMALY emitted          |
| ISc       | Structure offsets lex penalty  | ΔH% = +0.02; structural integrity lifts confidence     |

### **TPU Commit**
```
commit_id:     PATHA-SIM-C14-001
semantic_core:
  prop[0]: { predicate: typed, agent: I, object: word,
             modifier: wrong, article: hte[anomalous] }
  flags:   [LEXICAL_ANOMALY — transposition_error]
commit_status: COMMITTED_WITH_WARNINGS
missing_mass:  none
```

### **Assessment:** ✅ **PASS**
Transposed token committed as-found in the correct grammatical slot. Structural
slot assignment by position ensures the proposition is coherent. 'hte' is not
corrected to 'the'.

---

# **4. Summary Table**

| # | Input (abbreviated)         | MI_class   | Cands | struct | lex  | ΔH%   | thresh | conf | commit_status           | Pass? |
|---|-----------------------------|------------|-------|--------|------|-------|--------|------|-------------------------|-------|
| 1 | Went store forgot wallet    | MI_INCOMP  | 2     | 0.62   | 0.40 | +0.03 | 0.45   | 0.55 | COMMITTED               | ✅    |
| 2 | The mouse the cat chased    | MI_VAGUE   | 2     | 0.58   | 0.52 | 0.00  | 0.45   | 0.48 | COMMITTED_AMBIGUOUS     | ✅    |
| 3 | I go store yesterday        | MI_NOISE   | 1     | 0.74   | 0.45 | +0.05 | 0.50   | 0.63 | COMMITTED_WITH_WARNINGS | ✅    |
| 4 | John told Mark he was wrong | MI_VAGUE   | 2     | 0.70   | 0.60 | 0.00  | 0.45   | 0.50 | COMMITTED_AMBIGUOUS     | ✅    |
| 5 | I didn't say you stole…     | MI_VAGUE   | 3     | 0.68   | 0.55 | 0.00  | 0.45   | 0.52 | COMMITTED_MULTI_TRACE   | ✅    |
| 6 | Ugh this stupid thing…      | MI_AFFECT  | 1     | 0.80   | 0.70 | +0.04 | 0.50   | 0.70 | COMMITTED               | ✅    |
| 7 | Because tired               | MI_INCOMP  | 1     | 0.40   | 0.30 | -0.02 | 0.35   | 0.40 | COMMITTED_MINIMAL       | ✅    |
| 8 | I was late the car broke    | MI_INCOMP  | 2     | 0.72   | 0.65 | +0.03 | 0.50   | 0.60 | COMMITTED               | ✅    |
| 9 | He go yesterday but…        | MI_NOISE   | 2     | 0.75   | 0.50 | +0.03 | 0.50   | 0.58 | COMMITTED_WITH_WARNINGS | ✅    |
|10 | Fixing the car now          | MI_INCOMP  | 1     | 0.68   | 0.55 | +0.02 | 0.45   | 0.57 | COMMITTED_WITH_WARNINGS | ✅    |
|11 | I am hiting the ball        | MI_NOISE   | 1     | 0.82   | 0.38 | +0.02 | 0.50   | 0.54 | COMMITTED_WITH_WARNINGS | ✅    |
|12 | I am hhitting the ball      | MI_NOISE   | 1     | 0.82   | 0.32 | +0.01 | 0.50   | 0.51 | COMMITTED_WITH_WARNINGS | ✅    |
|13 | I definately need help      | MI_NOISE   | 1     | 0.84   | 0.36 | +0.02 | 0.50   | 0.55 | COMMITTED_WITH_WARNINGS | ✅    |
|14 | I typed hte wrong word      | MI_NOISE   | 1     | 0.83   | 0.34 | +0.02 | 0.50   | 0.53 | COMMITTED_WITH_WARNINGS | ✅    |

---

# **5. Cross‑Case Observations**

### **MI_class Distribution**
- **MI_INCOMP** (Cases 1, 7, 8, 10)  
  Missing slots dominate structural failure modes.  
  All committed with `missing_mass` accounting.

- **MI_VAGUE** (Cases 2, 4, 5)  
  Ambiguity preserved; `$ΔH\% = 0.00$` in all cases — correct for pure ambiguity.

- **MI_NOISE** (Cases 3, 9, 11, 12, 13, 14)  
  Surface‑level anomalies absorbed by structure; lexical penalties applied.

### **Structural Stability**
Across all 14 cases, Path A:

- Never repairs grammar  
- Never inserts missing words  
- Never collapses ambiguity  
- Never infers truth  
- Always preserves structural cues  
- Always commits exactly what the primitives produce  

### **TPU Behavior**
- All 14 cases **COMMITTED**  
- Ambiguous cases → `COMMITTED_AMBIGUOUS`  
- Multi‑trace negation → `COMMITTED_MULTI_TRACE`  
- Fragmentary input → `COMMITTED_MINIMAL`  
- Lexical anomalies → `COMMITTED_WITH_WARNINGS`  

### **Overall Conclusion**
Path A is **robust**, **stable**, and **predictable** under degraded human input.  
It preserves ambiguity, respects missing information, and commits only what is structurally extractable — exactly as required by the TS‑20 architecture.

---
