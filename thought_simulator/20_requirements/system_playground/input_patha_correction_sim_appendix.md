# Appendix for 
[input_patha_correction_sim.md](input_patha_correction_sim.md])

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


