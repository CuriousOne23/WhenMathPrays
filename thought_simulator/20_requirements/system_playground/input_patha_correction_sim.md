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

- Computes $ΔH\%$ (normalized hypothesis‑mass delta)  
- Computes `confidence`  
- Applies `threshold`  
- Does **not** perform semantic inference  

---

## **2.6 TPU — Thought Processing Unit**

- Commits $TP(N+1)$ and $semantic\_core$ **exactly as produced**  
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

# ------------------------------------------------------------
# **Appendix A — Formal Definitions of Path‑A Scoring, Confidence, Thresholding, and TPU Fields**
# ------------------------------------------------------------

This appendix defines the quantitative and bookkeeping fields used throughout the Path‑A Correction Simulation. These definitions apply uniformly across all 14 cases and are consistent with the TS‑20 architectural requirements.

---

# **A.1 Structural and Lexical Scores (CE Stage)**

## **A.1.1 structural_score**

`structural_score ∈ [0,1]`

A normalized measure of **how well the candidate’s internal structure conforms to a valid proto‑proposition** under Path‑A rules.

It is computed from:

- role completeness (agent, object, predicate, etc.)  
- adjacency plausibility  
- clause boundary clarity  
- POS‑pattern conformity  
- penalties for structural anomalies (missing subject, missing connector, etc.)

**Interpretation:**

- `$1.00$` → structurally perfect  
- `$0.70$` → structurally sound with minor issues  
- `$0.40$` → structurally degraded but still parseable  
- `$0.00$` → structurally invalid (would be rejected)

Path A **never repairs** structure; it only scores what is present.

---

## **A.1.2 lexical_score**

`lexical_score ∈ [0,1]`

A normalized measure of **surface lexical plausibility** of the tokens in the candidate.

It is computed from:

- token canonicality  
- dictionary plausibility  
- penalties for lexical anomalies (misspellings, double‑key, transposition, etc.)  
- part‑of‑speech lexical fit  

**Interpretation:**

- `$1.00$` → lexically clean  
- `$0.50$` → lexically degraded but interpretable  
- `$0.30$` → lexically anomalous  
- `$0.00$` → lexically uninterpretable

Path A **never corrects** lexical anomalies; it only flags them.

---

# **A.2 ΔH%, Confidence, and Threshold (ISc Stage)**

## **A.2.1 ΔH% — Hypothesis‑Mass Delta**

`ΔH% ∈ [-1, +1]` (normalized)

A measure of **how much new, structurally supported information** the candidate adds relative to the intake envelope.

- Positive `$ΔH\%$` → new information added  
- Zero `$ΔH\%$` → pure ambiguity (no new mass)  
- Negative `$ΔH\%$` → missing information (fragmentary input)

This is **not** a probability — it is a **mass‑accounting metric**.

---

## **A.2.2 threshold**

`threshold ∈ [0,1]`

The **minimum confidence required for TPU commit**.

Thresholds vary by MI_class:

- `MI_INCOMP` → lower thresholds (e.g., `$0.35$`)  
- `MI_NOISE` → medium thresholds (e.g., `$0.50$`)  
- `MI_VAGUE` → ambiguity‑tolerant thresholds (e.g., `$0.45$`)  

Thresholds prevent Path A from committing structurally invalid or unsupported propositions.

---

## **A.2.3 confidence**

`confidence ∈ [0,1]`

A scalar computed from:

- structural_score  
- lexical_score  
- `$ΔH\%$`  
- anomaly penalties  
- candidate completeness  

**Interpretation:**

- `$confidence ≥ threshold$` → commit allowed  
- `$confidence < threshold$` → commit suppressed (candidate rejected)

Confidence is **not** a probability of truth — it is a **structural‑support measure**.

---

# **A.3 TPU Bookkeeping Fields**

## **A.3.1 commit_id**

A unique identifier for the TPU commit event.

Format:

```
PATHA-SIM-CXX-YYY
```

Where:

- `CXX` = case number  
- `YYY` = commit sequence number  

This ensures reproducibility and traceability.

---

## **A.3.2 commit_status**

Indicates **how** the TPU committed the candidate(s):

- `COMMITTED` — clean commit  
- `COMMITTED_WITH_WARNINGS` — structural or lexical anomalies present  
- `COMMITTED_AMBIGUOUS` — multiple candidates preserved  
- `COMMITTED_MULTI_TRACE` — multiple negation‑scope or structural traces  
- `COMMITTED_MINIMAL` — fragmentary input, minimal viable proposition  
- `REJECTED` — (not seen in your 14 cases) confidence < threshold  

Path A **never repairs**; it only commits or rejects.

---

## **A.3.3 missing_mass**

A structured record of **which semantic or structural slots could not be filled** due to degraded input.

Examples:

```
{ agent_slot: 1 unresolved }
{ connector_slot: 1 unresolved }
{ pronoun_referent: unresolved }
{ tense_normalization_slot: 1 }
```

Missing mass is **not** an error — it is an **accounting mechanism** ensuring Path A never fabricates content.

---

# **A.4 Summary**

This appendix formalizes the quantitative and bookkeeping fields used throughout the Path‑A Correction Simulation. These definitions ensure:

- transparency  
- reproducibility  
- architectural consistency  
- correct interpretation of the 14‑case results  

Absolutely, Jeff — here is **Appendix B**, written in the same polished, architectural, TS‑20‑consistent style as Appendix A. It cleanly explains **what Path A does and does not record in the TP**, why, and how this affects replay, ambiguity, and downstream processing.

You can paste this directly after Appendix A.

---

# ------------------------------------------------------------
# **Appendix B — TP Recording Policy for Path‑A Commits**
# ------------------------------------------------------------

This appendix defines **which fields from the Path‑A pipeline are recorded in the Thought Packet (TP)** and which fields are **not**, along with the architectural rationale. These rules apply uniformly across all 14 simulation cases and across all TS‑20‑compliant Path‑A implementations.

---

# **B.1 Overview**

Path A produces many **diagnostic** fields during execution:

- `structural_score`  
- `lexical_score`  
- `ΔH%`  
- `confidence`  
- `threshold`  
- `MI_class`  
- `candidate_count`  
- `extraction_basis`  
- anomaly penalties  

However:

> **Path A does not record diagnostic fields in the TP.**  
> **Only the semantic and structural results of the commit are stored.**

This ensures that the TP remains a **semantic artifact**, not a scoring log.

---

# **B.2 Fields *Not* Recorded in the TP**

The following fields **evaporate** after TPU commit:

### **B.2.1 structural_score**
Used only to evaluate structural plausibility.  
Not part of the thought.  
Not needed for replay.

### **B.2.2 lexical_score**
Used only to penalize lexical anomalies.  
Not part of the semantic content.

### **B.2.3 ΔH%**
A mass‑accounting metric, not semantic content.  
Not recorded.

### **B.2.4 confidence**
A decision‑support scalar.  
Not part of the thought.

### **B.2.5 threshold**
A control parameter, not semantic content.

### **B.2.6 MI_class**
A classification of input degradation.  
Useful for diagnostics, not for semantic replay.

### **B.2.7 candidate_count**
Internal to CEx; not semantically meaningful.

### **B.2.8 extraction_basis**
Describes how candidates were extracted.  
Not part of the thought.

### **B.2.9 anomaly penalties**
Used to adjust scores; not recorded.

**Architectural reason:**  
These fields are **implementation‑dependent**, **non‑semantic**, and **not required** for Path B or replay.  
The TP must remain a **pure semantic record**.

---

# **B.3 Fields Recorded in the TP**

The TP **does** record the following fields, because they are part of the semantic or structural outcome of the commit.

---

## **B.3.1 commit_id**

A unique identifier for the TPU commit event.

Purpose:

- reproducibility  
- traceability  
- debugging  
- cross‑case comparison  

Format:

```
PATHA-SIM-CXX-YYY
```

This is stored in the TP.

---

## **B.3.2 commit_status**

Indicates **how** the TPU committed the candidate(s):

- `COMMITTED`  
- `COMMITTED_WITH_WARNINGS`  
- `COMMITTED_AMBIGUOUS`  
- `COMMITTED_MULTI_TRACE`  
- `COMMITTED_MINIMAL`  
- `REJECTED` (not seen in the 14 cases)

This is stored because it affects:

- how Path B interprets the TP  
- how replay reconstructs the thought  
- how ambiguity is preserved  

---

## **B.3.3 semantic_core**

The **main payload** of the TP.

Contains:

- propositions  
- roles  
- slots  
- UNKNOWN placeholders  
- ambiguity branches  
- affect layers (when present)  
- warnings (as flags)  

This is the **entire purpose** of the TP.

---

## **B.3.4 flags**

Flags represent **surface anomalies that affect semantics**, such as:

- `MISSING_AGENT_SLOT`  
- `MISSING_CONNECTOR`  
- `PRONOUN_REFERENT_AMBIGUOUS`  
- `LEXICAL_ANOMALY`  
- `NEGATION_SCOPE_AMBIGUOUS`  

Flags are stored because they:

- preserve ambiguity  
- preserve missing information  
- prevent Path B from inferring content that Path A did not extract  

---

## **B.3.5 missing_mass**

A structured record of **which semantic or structural slots could not be filled**.

Examples:

```
{ agent_slot: 1 unresolved }
{ connector_slot: 1 unresolved }
{ pronoun_referent: unresolved }
{ tense_normalization_slot: 1 }
```

This is stored because:

- Path A must never fabricate content  
- Path B must never assume content  
- replay must preserve the exact structural incompleteness  

Missing mass is a **first‑class semantic artifact**, not a diagnostic.

---

# **B.4 Why Path A Does Not Store Scores**

Path A is a **front‑end structural extractor**, not a reasoning engine.

Scores are:

- ephemeral  
- implementation‑dependent  
- not part of the thought  
- not needed for replay  
- not needed for Path B  
- not stable across versions  

The TP must remain:

- semantic  
- structural  
- minimal  
- replayable  
- architecture‑neutral  

Therefore, **scores are never recorded**.

---

# **B.5 Why Path A *Does* Store Missing Mass and Flags**

Missing mass and flags:

- preserve ambiguity  
- preserve incompleteness  
- prevent hallucination  
- prevent inference  
- ensure Path B cannot “fix” or “complete” the thought  
- ensure replay reconstructs the exact degraded structure  

These fields are essential for **semantic integrity**.

---

# **B.6 Summary**

### **Not recorded:**
- structural_score  
- lexical_score  
- ΔH%  
- confidence  
- threshold  
- MI_class  
- extraction_basis  
- candidate_count  
- anomaly penalties  

### **Recorded:**
- commit_id  
- commit_status  
- semantic_core  
- flags  
- missing_mass  

### **Architectural Principle:**
> **The TP stores only semantic and structural outcomes, not diagnostic or scoring metadata.**

---

# ------------------------------------------------------------
# **Appendix C — MI_class Taxonomy and Input‑Degradation Categories**
# ------------------------------------------------------------

The **MI_class** (Messy‑Input Class) taxonomy categorizes the *type* of degradation present in the intake envelope.  
It is assigned during **IIInB** and influences:

- threshold selection  
- anomaly expectations  
- missing‑mass accounting  
- ambiguity handling  
- structural penalties  

MI_class **does not** determine meaning, truth, or correction.  
It is strictly a **local structural classification**.

---

# **C.1 Overview of MI_class**

Path A recognizes five high‑level messy‑input categories:

1. **MI_INCOMP** — Incomplete structure  
2. **MI_VAGUE** — Ambiguous structure  
3. **MI_AFFECT** — Affective noise mixed with factual content  
4. **MI_NOISE** — Surface‑form lexical anomalies  
5. **MI_CONTRA** — Local contradictions (not present in the 14 cases)

Each class corresponds to a **distinct failure mode** in human input.

---

# **C.2 MI_INCOMP — Incomplete Structure**

### **Definition**
Structural incompleteness: one or more required syntactic or semantic slots are missing.

### **Typical causes**
- missing subject  
- missing main clause  
- missing connector  
- fragmentary clause  
- ellipsis without recoverable structure  

### **Detection (IIInB)**
Triggered when:

- required roles are absent  
- clause boundaries are incomplete  
- POS patterns indicate missing anchors  

### **Path‑A behavior**
- lower threshold (e.g., `$0.35$`)  
- missing_mass recorded  
- UNKNOWN placeholders preserved  
- no repair or insertion  

### **Examples from the 14 cases**
- Case 1 — Missing subject  
- Case 7 — Fragment only  
- Case 8 — Missing connector  
- Case 10 — Missing agent  

---

# **C.3 MI_VAGUE — Ambiguous Structure**

### **Definition**
Multiple structurally valid interpretations exist, and Path A cannot choose between them.

### **Typical causes**
- ambiguous pronoun referent  
- ambiguous role assignment  
- ambiguous negation scope  
- NP‑NP‑V patterns  

### **Detection (IIInB)**
Triggered when:

- two or more role assignments are equally plausible  
- pronoun antecedents are locally ambiguous  
- negation can attach to multiple scopes  

### **Path‑A behavior**
- ambiguity preserved  
- `$ΔH\% = 0.00$` (no new mass)  
- threshold moderate (e.g., `$0.45$`)  
- TPU commits **multiple candidates**  

### **Examples from the 14 cases**
- Case 2 — NP‑NP‑V ambiguity  
- Case 4 — Pronoun ambiguity  
- Case 5 — Negation‑scope ambiguity  

---

# **C.4 MI_AFFECT — Affective Noise**

### **Definition**
Affective or emotional tokens co‑occur with factual content.

### **Typical causes**
- interjections (“Ugh”)  
- evaluative adjectives (“stupid”)  
- emotional intensifiers  

### **Detection (IIInB)**
Triggered when:

- INTJ or evaluative ADJ tokens appear  
- affective tone is separable from factual structure  

### **Path‑A behavior**
- affect stripped into `affect_layer`  
- factual core extracted normally  
- no sentiment inference  
- threshold unchanged  

### **Examples from the 14 cases**
- Case 6 — “Ugh this stupid thing never works.”  

---

# **C.5 MI_NOISE — Surface‑Form Lexical Noise**

### **Definition**
Lexical anomalies that do not break structural integrity.

### **Typical causes**
- misspellings  
- dropped letters  
- double‑key errors  
- transposition errors  
- tense drift  
- uninflected verbs  

### **Detection (IIInB)**
Triggered when:

- token surface form is non‑canonical  
- POS tagging still yields a valid structural frame  

### **Path‑A behavior**
- structural_score usually high  
- lexical_score penalized  
- threshold medium (e.g., `$0.50$`)  
- anomalies preserved as flags  
- no correction  

### **Examples from the 14 cases**
- Case 3 — Missing preposition  
- Case 9 — Tense/aspect drift  
- Case 11 — Dropped letter  
- Case 12 — Double‑key  
- Case 13 — Stable misspelling  
- Case 14 — Transposition error  

---

# **C.6 MI_CONTRA — Local Contradiction (Not Present in the 14 Cases)**

### **Definition**
Local structural contradiction within the same clause or event.

### **Typical causes**
- contradictory modifiers  
- incompatible tense/aspect markers  
- mutually exclusive roles  

### **Detection (IIInB)**
Triggered when:

- two tokens impose incompatible structural constraints  
- contradiction is local (not global truth‑value contradiction)  

### **Path‑A behavior**
- both contradictory traces extracted  
- TPU may commit a **multi‑trace** structure  
- no resolution attempted  

### **Example (not in your dataset)**
`He is running but also completely still.`  
→ two incompatible state predicates extracted.

---

# **C.7 Why MI_class Matters**

MI_class influences:

### **1. Threshold selection**
- MI_INCOMP → lower threshold  
- MI_VAGUE → ambiguity‑tolerant threshold  
- MI_NOISE → medium threshold  
- MI_AFFECT → normal threshold  
- MI_CONTRA → multi‑trace threshold  

### **2. Expected anomalies**
Each class predicts a different anomaly pattern.

### **3. Missing‑mass accounting**
MI_INCOMP → missing slots  
MI_VAGUE → unresolved ambiguity  
MI_NOISE → lexical anomalies  
MI_AFFECT → affect layer  
MI_CONTRA → contradictory traces  

### **4. TPU commit_status**
MI_class determines whether the commit is:

- clean  
- with warnings  
- ambiguous  
- multi‑trace  
- minimal  

---

# **C.8 Summary**

The MI_class taxonomy provides a **structural diagnosis** of degraded human input.  
It does **not**:

- infer meaning  
- repair grammar  
- choose a correct interpretation  
- normalize tokens  

Instead, it ensures that Path A:

- preserves ambiguity  
- preserves missing information  
- preserves lexical anomalies  
- commits only what is structurally extractable  
- never hallucinates or repairs  

This taxonomy is essential for understanding the behavior of the 14‑case simulation and for interpreting Path‑A outputs in general.

---

# ------------------------------------------------------------
# **Appendix D — Anomaly Types and Penalties in Path‑A Processing**
# ------------------------------------------------------------

This appendix defines the anomaly types encountered in the 14‑case simulation and describes how Path A detects, scores, and propagates them.  
Anomalies are **never repaired**; they are **diagnosed**, **penalized**, and **preserved** in the TP.

Anomalies fall into four broad categories:

1. **Structural anomalies**  
2. **Lexical anomalies**  
3. **Ambiguity anomalies**  
4. **Affective anomalies**

Each anomaly type influences:

- `structural_score`  
- `lexical_score`  
- `$ΔH\%$`  
- `confidence`  
- `commit_status`  
- `missing_mass`  
- `flags` in the semantic_core  

---

# **D.1 Structural Anomalies**

Structural anomalies arise when the **syntactic frame is incomplete or malformed**.

---

## **D.1.1 Missing Agent Slot**

### **Definition**
A predicate requires an agent role, but no token fills it.

### **Detection**
IIInB detects:

- VERB with no preceding NP  
- gerund phrase with no subject  
- fragmentary clause  

### **Penalty**
- structural_score ↓  
- missing_mass: `{ agent_slot: 1 }`  
- flag: `MISSING_AGENT_SLOT`  

### **Examples**
- Case 1 — “Went store forgot wallet.”  
- Case 10 — “Fixing the car now.”

---

## **D.1.2 Missing Main Clause**

### **Definition**
A subordinating conjunction appears without a main clause.

### **Penalty**
- structural_score ↓  
- missing_mass: `{ main_clause_slot: 1 }`  
- flag: `MISSING_MAIN_CLAUSE`  

### **Example**
- Case 7 — “Because tired.”

---

## **D.1.3 Missing Connector**

### **Definition**
Two events appear without a coordinating or subordinating connector.

### **Penalty**
- structural_score ↓  
- missing_mass: `{ connector_slot: 1 }`  
- flag: `MISSING_CONNECTOR`  

### **Example**
- Case 8 — “I was late the car broke.”

---

## **D.1.4 Fragment‑Only Structure**

### **Definition**
Input contains only a subordinate or dependent fragment.

### **Penalty**
- structural_score ↓  
- `$ΔH\%$` may be negative  
- commit_status: `COMMITTED_MINIMAL`  

### **Example**
- Case 7.

---

# **D.2 Lexical Anomalies**

Lexical anomalies arise when **token surface forms are non‑canonical**, but the structural frame remains intact.

Path A **never corrects** these.

---

## **D.2.1 Dropped‑Letter Misspelling**

### **Definition**
A token is missing one or more expected letters.

### **Penalty**
- lexical_score ↓  
- flag: `LEXICAL_ANOMALY — dropped_letter`  

### **Example**
- Case 11 — “hiting”

---

## **D.2.2 Double‑Key Error**

### **Definition**
A letter is repeated due to keyboard bounce or user error.

### **Penalty**
- lexical_score ↓ (worse than dropped‑letter)  
- flag: `LEXICAL_ANOMALY — double_key`  

### **Example**
- Case 12 — “hhitting”

---

## **D.2.3 Transposition Error**

### **Definition**
Two adjacent letters are swapped.

### **Penalty**
- lexical_score ↓  
- flag: `LEXICAL_ANOMALY — transposition_error`  

### **Example**
- Case 14 — “hte”

---

## **D.2.4 Stable Misspelling**

### **Definition**
A common, phonetically plausible misspelling.

### **Penalty**
- lexical_score ↓  
- flag: `LEXICAL_ANOMALY — stable_misspelling`  

### **Example**
- Case 13 — “definately”

---

## **D.2.5 Tense/Aspect Drift**

### **Definition**
Verb form inconsistent with temporal adverb or aspect marker.

### **Penalty**
- lexical_score ↓  
- flag: `TENSE_MISMATCH` or `ASPECT_DRIFT`  

### **Example**
- Case 9 — “He go yesterday…”

---

# **D.3 Ambiguity Anomalies**

Ambiguity anomalies arise when **multiple structurally valid interpretations exist**.

Path A **preserves all interpretations**.

---

## **D.3.1 Pronoun Referent Ambiguity**

### **Definition**
A pronoun has multiple locally valid antecedents.

### **Penalty**
- structural_score ↓  
- `$ΔH\% = 0.00$`  
- commit_status: `COMMITTED_AMBIGUOUS`  
- flag: `PRONOUN_REFERENT_AMBIGUOUS`  

### **Example**
- Case 4 — “John told Mark he was wrong.”

---

## **D.3.2 Role‑Assignment Ambiguity**

### **Definition**
Two NPs can fill either agent or object roles.

### **Penalty**
- structural_score ↓  
- commit_status: `COMMITTED_AMBIGUOUS`  
- flag: `ROLE_AMBIGUOUS`  

### **Example**
- Case 2 — NP‑NP‑V pattern.

---

## **D.3.3 Negation‑Scope Ambiguity**

### **Definition**
Negation can attach to multiple structural positions.

### **Penalty**
- structural_score ↓  
- commit_status: `COMMITTED_MULTI_TRACE`  
- flag: `NEGATION_SCOPE_AMBIGUOUS`  

### **Example**
- Case 5 — “I didn’t say you stole the money.”

---

# **D.4 Affective Anomalies**

Affective anomalies arise when **emotional tokens** appear alongside factual content.

---

## **D.4.1 Affective Noise**

### **Definition**
Interjections or evaluative adjectives that do not alter factual structure.

### **Penalty**
- no structural penalty  
- affect_layer created  
- flag: `AFFECT_LAYER_PRESENT`  

### **Example**
- Case 6 — “Ugh this stupid thing never works.”

---

# **D.5 How Anomalies Affect Scoring and Commit Behavior**

### **Structural anomalies**
- reduce structural_score  
- may reduce `$ΔH\%$`  
- create missing_mass  
- may trigger `COMMITTED_MINIMAL`

### **Lexical anomalies**
- reduce lexical_score  
- do **not** affect structure  
- produce lexical flags  
- commit_status often `WITH_WARNINGS`

### **Ambiguity anomalies**
- produce multiple candidates  
- `$ΔH\% = 0.00$`  
- commit_status `AMBIGUOUS` or `MULTI_TRACE`

### **Affective anomalies**
- do not reduce structural_score  
- produce affect_layer  
- commit_status usually clean

---

# **D.6 Summary**

Anomalies in Path A are:

- **detected**,  
- **penalized**,  
- **preserved**,  
- **never repaired**,  
- **never inferred**,  
- **never collapsed**.

This ensures that Path A remains:

- structurally honest  
- semantically conservative  
- ambiguity‑preserving  
- non‑hallucinatory  
- fully compliant with TS‑20 invariants  

---

Absolutely, Jeff — here is **Appendix E**, written in the same polished, architectural, TS‑20‑consistent style as Appendices A–D.  
This appendix formalizes **all TPU commit statuses**, explains **when each one is triggered**, **what structural conditions lead to it**, and **how Path A encodes the result in the TP**.

You can paste this directly after Appendix D.

---

# ------------------------------------------------------------
# **Appendix E — TPU Commit Status Reference Table**
# ------------------------------------------------------------

This appendix defines the **commit_status** values used by the TPU when finalizing a Path‑A commit.  
Commit statuses describe **how** the TPU committed the candidate(s), not **what** the candidate means.  
They are essential for:

- replay  
- Path‑B interpretation  
- structural accountability  
- ambiguity preservation  
- missing‑mass propagation  

Commit statuses are **semantic metadata**, not diagnostics — therefore they **are recorded in the TP**.

---

# **E.1 Overview of Commit Statuses**

Path A uses six commit statuses:

1. **COMMITTED**  
2. **COMMITTED_WITH_WARNINGS**  
3. **COMMITTED_AMBIGUOUS**  
4. **COMMITTED_MULTI_TRACE**  
5. **COMMITTED_MINIMAL**  
6. **REJECTED** *(not present in the 14‑case simulation)*

Each status corresponds to a distinct structural condition in the pipeline.

---

# **E.2 COMMITTED**

### **Definition**
A clean commit: the candidate is structurally valid, lexically interpretable, and above threshold.

### **Triggered When**
- `confidence ≥ threshold`  
- no structural incompleteness  
- no ambiguity  
- no multi‑trace structure  
- no lexical anomalies requiring warnings  

### **TP Contents**
- semantic_core (single proposition or event)  
- no warnings  
- missing_mass: none  

### **Examples**
- Case 6 — “Ugh this stupid thing never works.”  
- Case 8 — “I was late the car broke.” (two clean propositions)

---

# **E.3 COMMITTED_WITH_WARNINGS**

### **Definition**
Commit succeeded, but structural or lexical anomalies were detected.

### **Triggered When**
- `confidence ≥ threshold`  
- anomalies present (lexical or structural)  
- but structure is still extractable  

### **Typical Causes**
- misspellings  
- double‑key errors  
- transposition errors  
- tense/aspect drift  
- missing agent slot (but still above threshold)

### **TP Contents**
- semantic_core  
- `flags` describing anomalies  
- missing_mass only if structural slots are absent  

### **Examples**
- Case 3 — Missing preposition  
- Case 9 — Tense/aspect drift  
- Cases 11–14 — Lexical anomalies  

---

# **E.4 COMMITTED_AMBIGUOUS**

### **Definition**
Multiple structurally valid candidates exist, and Path A preserves all of them.

### **Triggered When**
- ambiguity is irreducible  
- `$ΔH\% = 0.00$` (no new mass)  
- `confidence ≥ threshold`  
- no structural basis to collapse candidates  

### **Typical Causes**
- pronoun referent ambiguity  
- NP‑NP‑V role ambiguity  

### **TP Contents**
- multiple candidate propositions  
- ambiguity flags  
- missing_mass: `{ role_assignment: unresolved }` or similar  

### **Examples**
- Case 2 — NP‑NP‑V ambiguity  
- Case 4 — Pronoun ambiguity  

---

# **E.5 COMMITTED_MULTI_TRACE**

### **Definition**
Multiple **structural traces** exist due to incompatible scope attachments or contradictory local structures.

### **Triggered When**
- negation scope ambiguous  
- contradictory modifiers  
- incompatible structural readings  
- Path A cannot collapse traces  

### **Difference from COMMITTED_AMBIGUOUS**
- AMBIGUOUS = multiple **role assignments**  
- MULTI_TRACE = multiple **structural traces** (e.g., negation scope)

### **TP Contents**
- multiple traces  
- flags: `NEGATION_SCOPE_AMBIGUOUS`  
- missing_mass: `{ negation_scope: unresolved }`  

### **Examples**
- Case 5 — Negation‑scope ambiguity  

---

# **E.6 COMMITTED_MINIMAL**

### **Definition**
Input is fragmentary, but a minimal viable proposition can still be extracted.

### **Triggered When**
- `confidence ≥ threshold`  
- threshold lowered due to MI_INCOMP  
- only a partial structure is available  
- missing slots cannot be filled  

### **Typical Causes**
- fragmentary clause  
- missing main clause  
- missing subject  
- incomplete subordinate structure  

### **TP Contents**
- minimal semantic_core  
- flags for missing slots  
- missing_mass entries  

### **Examples**
- Case 7 — “Because tired.”

---

# **E.7 REJECTED** *(Not Present in the 14 Cases)*

### **Definition**
Candidate fails to meet the minimum structural or lexical requirements for commit.

### **Triggered When**
- `confidence < threshold`  
- structure is too degraded  
- lexical anomalies render the token uninterpretable  
- no viable proto‑proposition can be extracted  

### **TP Contents**
- **No TP is created**  
- Path A outputs a rejection event  
- Path B receives no semantic_core  

### **Example (hypothetical)**
`asdf qwerty zxcvbn` → no structural anchors.

---

# **E.8 Summary Table**

| commit_status            | Meaning | Trigger | TP Contents |
|--------------------------|---------|---------|-------------|
| **COMMITTED** | Clean commit | Above threshold, no anomalies | Single semantic_core |
| **COMMITTED_WITH_WARNINGS** | Commit with anomalies | Above threshold + lexical/structural issues | semantic_core + flags |
| **COMMITTED_AMBIGUOUS** | Multiple candidates | Irreducible ambiguity | Multiple propositions + ambiguity flags |
| **COMMITTED_MULTI_TRACE** | Multiple structural traces | Negation/structural ambiguity | Multi‑trace semantic_core |
| **COMMITTED_MINIMAL** | Fragmentary commit | Incomplete structure | Minimal core + missing_mass |
| **REJECTED** | No commit | Below threshold | No TP |

---

# **E.9 Architectural Principle**

> **Commit status encodes the structural integrity of the thought, not its truth or correctness.**  
> Path A commits *structure*, not *meaning*.

Commit statuses ensure that:

- ambiguity is preserved  
- missing information is preserved  
- lexical anomalies are preserved  
- Path B cannot hallucinate or infer missing content  
- replay reconstructs the exact structural state  

---

Absolutely, Jeff — here is **Appendix F**, written in the same polished, architectural, TS‑20‑consistent style as Appendices A–E.  
This appendix defines the **role‑slot taxonomy** used by Path A when extracting proto‑propositions.  
It explains **what each slot means**, **how it is detected**, **when it is required**, and **how missing slots propagate into missing_mass**.

You can paste this directly after Appendix E.

---

# ------------------------------------------------------------
# **Appendix F — Role‑Slot Taxonomy for Path‑A Structural Extraction**
# ------------------------------------------------------------

This appendix defines the **role‑slot taxonomy** used by Path A when constructing proto‑propositions during CEx and CE.  
Role‑slots represent the **minimal semantic structure** that Path A can extract without inference, repair, or hallucination.

Role‑slots are **not** conceptual or world‑model constructs — they are **local structural anchors** derived strictly from adjacency, POS patterns, and clause boundaries.

---

# **F.1 Overview**

Path A recognizes the following role‑slots:

### **Core Event Roles**
- **predicate**  
- **agent**  
- **object**  
- **recipient**  
- **subject** (for state predicates)  

### **Modifier Roles**
- **time**  
- **location**  
- **modifier** (adverbial or adjectival)  
- **aspect**  
- **negation**  

### **Structural Roles**
- **connector**  
- **article**  
- **pronoun_referent**  
- **cause_of** (for state predicates)  

Each role‑slot may be:

- **filled** (with a token)  
- **UNKNOWN** (slot exists but cannot be filled)  
- **absent** (slot does not apply to this predicate)  

Missing slots are recorded in **missing_mass**.

---

# **F.2 Core Event Roles**

These roles define the **minimal event structure** Path A can extract.

---

## **F.2.1 predicate**

### **Definition**
The main event or state expressed by the verb or adjective.

### **Detection**
- VERB tokens  
- ADJ tokens in copular or fragmentary structures  
- AUX+VERB combinations  

### **Examples**
- “went”  
- “forgot”  
- “works”  
- “tired”  

### **Notes**
The predicate is **always required**.  
If no predicate can be found, Path A rejects the input.

---

## **F.2.2 agent**

### **Definition**
The entity performing the action.

### **Detection**
- NP before the verb  
- PRON before the verb  
- PROPN before the verb  

### **Missing Agent Behavior**
If no agent is present:

- agent = UNKNOWN  
- missing_mass: `{ agent_slot: 1 }`  
- flag: `MISSING_AGENT_SLOT`  

### **Examples**
- Case 1 — both events missing agents  
- Case 10 — gerund phrase missing agent  

---

## **F.2.3 object**

### **Definition**
The entity acted upon.

### **Detection**
- NP after the verb  
- NOUN after the verb  
- DET+NOUN sequences  

### **Notes**
Object is optional — some predicates do not require one.

### **Examples**
- “forgot wallet” → object = wallet  
- “typed … word” → object = word  

---

## **F.2.4 recipient**

### **Definition**
The entity receiving something (communication, transfer, etc.).

### **Detection**
- NP following communication verbs  
- NP following “to” (when present)  

### **Examples**
- Case 4 — “told Mark” → recipient = Mark  

---

## **F.2.5 subject (state predicates)**

### **Definition**
The entity experiencing a state.

### **Detection**
- ADJ predicates  
- copular constructions  
- fragmentary state clauses  

### **Examples**
- Case 7 — “tired” → subject = UNKNOWN  

---

# **F.3 Modifier Roles**

Modifiers enrich the event but are not required for structural validity.

---

## **F.3.1 time**

### **Definition**
Temporal anchor for the event.

### **Detection**
- ADV tokens (yesterday, now)  
- temporal NPs  

### **Examples**
- Case 3 — time = yesterday  
- Case 9 — time = now  

---

## **F.3.2 location**

### **Definition**
Spatial anchor for the event.

### **Detection**
- NOUN with locative preposition  
- adjacency when preposition is missing (MI_NOISE)  

### **Notes**
Not present in the 14 cases, but supported.

---

## **F.3.3 modifier**

### **Definition**
Adverbial or adjectival modifier.

### **Detection**
- ADJ modifying NOUN  
- ADV modifying VERB  

### **Examples**
- Case 13 — modifier = “definately”  
- Case 14 — modifier = “wrong”  

---

## **F.3.4 aspect**

### **Definition**
Verb aspect (progressive, perfect, etc.).

### **Detection**
- AUX + VERB patterns  
- verb morphology  

### **Examples**
- Case 9 — “is going” → aspect = present_progressive  

---

## **F.3.5 negation**

### **Definition**
Negation marker attached to predicate or event.

### **Detection**
- AUX+NEG tokens (“didn’t”)  
- “never” as adverbial negation  

### **Examples**
- Case 5 — negation scope ambiguous  
- Case 6 — “never works”  

---

# **F.4 Structural Roles**

These roles describe **how events relate to each other** or how determiners and pronouns function.

---

## **F.4.1 connector**

### **Definition**
Structural link between events.

### **Detection**
- “and”, “but”, “because”, etc.  
- POS transitions (when missing)

### **Missing Connector Behavior**
- missing_mass: `{ connector_slot: 1 }`  
- flag: `MISSING_CONNECTOR`  

### **Example**
- Case 8 — no connector between “late” and “broke”  

---

## **F.4.2 article**

### **Definition**
Determiner for a noun.

### **Detection**
- DET tokens  
- anomalous DET tokens (MI_NOISE)

### **Examples**
- Case 14 — “hte” (transposition error)  

---

## **F.4.3 pronoun_referent**

### **Definition**
The entity a pronoun refers to.

### **Detection**
- local NP candidates  
- adjacency window  

### **Ambiguity Behavior**
- multiple candidates preserved  
- flag: `PRONOUN_REFERENT_AMBIGUOUS`  
- missing_mass: `{ pronoun_referent: unresolved }`  

### **Example**
- Case 4 — “he” could refer to John or Mark  

---

## **F.4.4 cause_of**

### **Definition**
Causal relation for state predicates.

### **Detection**
- explicit causal markers (not present in the 14 cases)  
- adjacency in fragmentary structures  

### **Example**
- Case 7 — “tired” → cause_of = UNKNOWN  

---

# **F.5 How Role‑Slots Interact with Missing Mass**

Whenever a required role‑slot cannot be filled:

- the slot is set to **UNKNOWN**  
- a corresponding entry is added to **missing_mass**  
- a flag is added to the semantic_core  

Examples:

```
{ agent_slot: 1 unresolved }
{ connector_slot: 1 unresolved }
{ pronoun_referent: unresolved }
```

This ensures Path A:

- never fabricates content  
- never infers missing roles  
- preserves structural incompleteness  
- remains compliant with TS‑20 invariants  

---

# **F.6 Summary**

The role‑slot taxonomy defines the **minimal structural vocabulary** of Path A.  
It ensures that:

- propositions are extracted consistently  
- ambiguity is preserved  
- missing information is explicitly recorded  
- lexical anomalies do not corrupt structure  
- Path B receives a clean, honest structural representation  

This taxonomy underlies all 14 cases in the simulation and is essential for interpreting Path‑A behavior.

---


