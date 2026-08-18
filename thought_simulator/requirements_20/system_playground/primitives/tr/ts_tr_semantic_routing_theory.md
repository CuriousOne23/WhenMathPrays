# ⭐ **ts_tr_semantic_routing_theory.md — Part 1 of 4**  
### *Theoretical Foundation for the Thought Router (TR)*  
### *Semantic Routing Theory for Path‑A*

---

# **1. Purpose of TR (Semantic Routing Problem)**

The Thought Router (TR) is the **semantic routing engine** of Path‑A.  
Its purpose is to convert stabilized Path‑A signals into a deterministic **semantic routing vector** that RB can use to select the correct basin:

- structural  
- semantic  
- identity  
- correction  
- commit  

TR is the only primitive that produces the `TP.TR` block.  
It does not modify meaning, identity, commitments, or freeze signatures.  
It is a **pure semantic‑routing computation**.

TR integrates:

- semantic‑layer cues  
- semantic‑adjacent cues  
- identity‑conditioned meaning  
- continuity signals  
- commitments  
- freeze signatures  
- curvature  
- semantic lineage  
- invariant drift  
- residue topology  
- routing metadata  

TR’s output is a deterministic vector:

$$
TR_v = f(\text{Path-A signals})
$$

which RB consumes to make basin decisions.

---

# **2. TR Input Envelope (Formal Read‑Set)**

TR reads only **frozen or stabilized** fields.  
Each field must have a producer, freeze point, stability rule, and usage rule.

### **2.1 STPX Cues (Semantic‑Layer Extraction)**  
- **Producer:** STPX  
- **Freeze:** OB freeze  
- **Content:** semantic‑layer hash, frame markers  
- **Usage:** semantic stability, semantic drift, semantic underspecification

### **2.2 Semantic Meaning‑Semantics**  
- **Producer:** TPU + IdOB  
- **Freeze:** TPU commit boundary  
- **Usage:** stance, intent, affect, shading, tension

### **2.3 idob_semantics**  
- **Producer:** IdOB  
- **Freeze:** per‑cycle freeze  
- **Usage:** identity‑conditioned meaning, commitments, referent lineage

### **2.4 Semantic Lineage**  
- **Producer:** IdOB  
- **Freeze:** per‑cycle  
- **Usage:** lineage_additions, epistemic_delta_h

### **2.5 Continuity Signals**  
- **Producer:** CE + MCB  
- **Freeze:** CE freeze + per‑cycle  
- **Usage:** stance/direction/coherence continuity

### **2.6 Identity Continuity Flags**  
- **Producer:** IdOB  
- **Freeze:** per‑cycle  
- **Usage:** identity stability, identity drift

### **2.7 Commitments**  
- **Producer:** IdOB  
- **Freeze:** commit freeze  
- **Usage:** commitment/reservation mapping

### **2.8 Freeze Signatures**  
- **Producer:** Identity layer  
- **Freeze:** commit freeze  
- **Usage:** hard constraints on TR mapping

### **2.9 DCB Curvature**  
- **Producer:** DCB  
- **Freeze:** per‑cycle  
- **Usage:** tension, semantic drift, identity drift

### **2.10 Routing Metadata**  
- **Producer:** RBU  
- **Freeze:** per‑cycle  
- **Usage:** routing_fields{} construction

### **2.11 Semantic Importance Residues**  
- **Producer:** SmOB  
- **Freeze:** OB freeze  
- **Usage:** politeness, affect, shading

### **2.12 Referent Lineage**  
- **Producer:** IdOB  
- **Freeze:** per‑cycle  
- **Usage:** lineage_additions, identity drift

### **2.13 Qualifier Lineage**  
- **Producer:** IdOB  
- **Freeze:** per‑cycle  
- **Usage:** stance/direction/coherence mapping

### **2.14 Invariant Drift ($\Delta H$)**  
- **Producer:** invariant relational model  
- **Freeze:** per‑cycle  
- **Usage:** epistemic_delta_h

### **2.15 Residue Topology**  
- **Producer:** semantic residue topology  
- **Freeze:** implicit  
- **Usage:** epistemic_delta_h, lineage_additions

---

# **3. TR Output Envelope (Formal Write‑Set)**

TR writes the full `TP.TR` block.  
Each field must have:

- meaning  
- type  
- allowed values  
- determinism rules  
- SSR projection rules  
- consumer (RB, GB)

### **3.1 stance**  
- **Meaning:** conversational stance (supportive, neutral, adversarial, etc.)  
- **Type:** ordinal  
- **Usage:** RB basin selection (identity vs semantic)

### **3.2 intent**  
- **Meaning:** communicative intent (inform, request, correct, etc.)  
- **Type:** categorical  
- **Usage:** RB correction basin gating

### **3.3 affect**  
- **Meaning:** emotional shading  
- **Type:** ordinal  
- **Usage:** semantic drift detection

### **3.4 epistemic_shading**  
- **Meaning:** confidence, uncertainty, speculation  
- **Type:** ordinal  
- **Usage:** identity basin gating

### **3.5 tension**  
- **Meaning:** curvature‑derived instability  
- **Type:** ordinal  
- **Usage:** structural/semantic basin gating

### **3.6 politeness**  
- **Meaning:** politeness level  
- **Type:** ordinal  
- **Usage:** semantic adjacency interpretation

### **3.7 commitment**  
- **Meaning:** commitment strength  
- **Type:** ordinal  
- **Usage:** identity basin gating

### **3.8 reservation**  
- **Meaning:** hedging or reservation  
- **Type:** ordinal  
- **Usage:** semantic drift detection

### **3.9 logical_structure**  
- **Meaning:** structural logic markers  
- **Type:** categorical  
- **Usage:** structural basin gating

### **3.10 epistemic_delta_h**  
- **Meaning:** invariant drift  
- **Type:** integer or ordinal  
- **Usage:** identity basin gating

$$
\Delta H = H_{t+1} - H_t
$$

### **3.11 lineage_additions[]**  
- **Meaning:** semantic lineage extensions  
- **Type:** list  
- **Usage:** identity continuity

### **3.12 routing_fields{}**  
- **Meaning:** routing‑relevant semantic metadata  
- **Type:** dictionary  
- **Usage:** RB basin scoring

---

# **4. Mapping Theory (Core Section)**  
TR’s job is to map stabilized Path‑A signals into a deterministic semantic routing vector.  
This section defines the mapping families, invariants, and example procedures for each TR field.

Each TR field has:

- **Allowed Inputs**  
- **Mapping Family**  
- **Deterministic Ordering Rules**  
- **Stability Rules**  
- **Example Mapping (Provisional)**  

Below is the theory for each field.

---

## **4.1 stance**  
### Allowed Inputs  
- semantic meaning‑semantics  
- idob_semantics  
- qualifier lineage  
- continuity signals  
- semantic importance residues  
- curvature (identity component)

### Mapping Family  
Ordinal stance classification:

- supportive  
- neutral  
- adversarial  
- corrective  
- exploratory  

### Deterministic Ordering  
Stance must be stable under identity continuity:

$$
stance_{t+1} = stance_t \quad \text{if identity stable}
$$

### Stability Rules  
- stance cannot oscillate unless curvature indicates drift  
- stance must respect commitments and freeze signatures

### Example Mapping  
If semantic meaning‑semantics indicates “request for correction” and curvature is low:

```
stance = corrective
```

---

## **4.2 intent**  
### Allowed Inputs  
- semantic meaning‑semantics  
- STPX cues  
- semantic adjacency  
- continuity signals

### Mapping Family  
Categorical intent classification:

- inform  
- request  
- correct  
- clarify  
- commit  
- speculate  

### Deterministic Ordering  
Intent must be monotonic under continuity:

$$
intent_{t+1} = intent_t \quad \text{unless semantic-layer hash changes}
$$

### Stability Rules  
- intent must not contradict commitments  
- intent must not violate freeze signatures

### Example Mapping  
If STPX indicates a frame marker for “question”:

```
intent = request
```

---

## **4.3 affect**  
### Allowed Inputs  
- semantic adjacency  
- semantic importance residues  
- curvature (semantic component)

### Mapping Family  
Ordinal affect classification:

- positive  
- neutral  
- negative  

### Deterministic Ordering  
Affect must be stable unless semantic adjacency changes.

### Example Mapping  
If semantic adjacency indicates affective markers:

```
affect = positive
```

---

## **4.4 epistemic_shading**  
### Allowed Inputs  
- semantic meaning‑semantics  
- invariant drift  
- semantic lineage  
- commitments  
- freeze signatures

### Mapping Family  
Ordinal shading classification:

- confident  
- neutral  
- uncertain  
- speculative  

### Deterministic Ordering  
Shading must respect commitments:

$$
shading_{t+1} \le shading_t \quad \text{if commitment strong}
$$

### Example Mapping  
If invariant drift is high:

```
epistemic_shading = uncertain
```

---

## **4.5 tension**  
### Allowed Inputs  
- DCB curvature  
- semantic drift  
- identity drift  
- structural drift

### Mapping Family  
Ordinal tension classification:

- low  
- medium  
- high  

### Deterministic Ordering  
Tension must be monotonic with curvature:

$$
tension = g(curvature)
$$

### Example Mapping  
If curvature instability is detected:

```
tension = high
```

---

## **4.6 politeness**  
### Allowed Inputs  
- semantic adjacency  
- semantic importance residues  
- qualifier lineage

### Mapping Family  
Ordinal politeness classification:

- polite  
- neutral  
- direct  

### Deterministic Ordering  
Politeness must respect identity continuity.

### Example Mapping  
If semantic adjacency indicates hedging:

```
politeness = polite
```

---

## **4.7 commitment**  
### Allowed Inputs  
- commitments  
- identity continuity  
- semantic lineage  
- freeze signatures

### Mapping Family  
Ordinal commitment classification:

- weak  
- medium  
- strong  

### Deterministic Ordering  
Commitment must be stable under freeze signatures:

$$
commitment_{t+1} = commitment_t \quad \text{if freeze signatures present}
$$

### Example Mapping  
If IdOB indicates strong commitment:

```
commitment = strong
```

---

## **4.8 reservation**  
### Allowed Inputs  
- semantic adjacency  
- semantic meaning‑semantics  
- epistemic shading  
- invariant drift

### Mapping Family  
Ordinal reservation classification:

- none  
- mild  
- strong  

### Deterministic Ordering  
Reservation increases with epistemic uncertainty.

### Example Mapping  
If shading = speculative:

```
reservation = strong
```

---

## **4.9 logical_structure**  
### Allowed Inputs  
- STPX cues  
- structural residue  
- semantic-layer hash

### Mapping Family  
Categorical logic markers:

- conditional  
- causal  
- contrastive  
- additive  
- corrective  

### Deterministic Ordering  
Logical structure must be stable unless STPX hash changes.

### Example Mapping  
If STPX indicates “if/then”:

```
logical_structure = conditional
```

---

## **4.10 epistemic_delta_h**  
### Allowed Inputs  
- invariant drift  
- semantic lineage  
- residue topology  
- identity continuity

### Mapping Family  
Ordinal or integer drift measure:

$$
\Delta H = H_{t+1} - H_t
$$

### Deterministic Ordering  
Epistemic delta must be monotonic with invariant drift.

### Example Mapping  
If invariant drift increases:

```
epistemic_delta_h = +1
```

---

## **4.11 lineage_additions[]**  
### Allowed Inputs  
- semantic lineage  
- referent lineage  
- qualifier lineage  
- commitments  
- freeze signatures

### Mapping Family  
List of lineage extensions.

### Deterministic Ordering  
Lineage additions must be bounded:

$$
|lineage\_additions| \le k
$$

### Example Mapping  
If new referent detected:

```
lineage_additions.append(new_referent)
```

---

## **4.12 routing_fields{}**  
### Allowed Inputs  
- routing_metadata  
- semantic adjacency  
- semantic-layer cues  
- identity continuity  
- curvature

### Mapping Family  
Dictionary of routing‑relevant metadata.

### Deterministic Ordering  
Routing fields must be stable unless routing_metadata changes.

### Example Mapping  
If semantic drift detected:

```
routing_fields["semantic_drift"] = True
```

---

# **5. Epistemic Delta Theory ($\Delta H$)**  
Epistemic delta is the measure of invariant drift across cycles.

### Definition  
$$
\Delta H = H_{t+1} - H_t
$$

Where:

- $H_t$ is the invariant state at cycle $t$  
- $H_{t+1}$ is the invariant state at cycle $t+1$

### Sources of Drift  
- semantic lineage changes  
- identity continuity changes  
- residue topology changes  
- commitments  
- freeze signatures  
- curvature instability

### Properties  
- $\Delta H$ must be bounded  
- $\Delta H$ must be monotonic with drift  
- $\Delta H$ must be deterministic  
- $\Delta H$ must be SSR‑projectable

### Usage  
RB uses $\Delta H$ to detect:

- identity drift  
- semantic drift  
- commitment instability  
- freeze‑signature conflicts

---

# **6. Lineage Additions Theory**  
Lineage additions extend semantic lineage deterministically.

### Definition  
Lineage additions are:

```
new semantic lineage entries added by TR
```

### Sources  
- referent lineage  
- qualifier lineage  
- semantic lineage  
- commitments  
- freeze signatures

### Properties  
- lineage additions must be bounded  
- lineage additions must respect identity continuity  
- lineage additions must respect freeze signatures  
- lineage additions must be deterministic  
- lineage additions must be SSR‑projectable

### Usage  
RB uses lineage additions to detect:

- referent instability  
- qualifier instability  
- identity drift  
- semantic drift  

---

# **7. Routing Fields Theory**  
`routing_fields{}` is the structured semantic‑routing metadata that TR produces for RB.  
It is not meaning, not identity, not commitments — it is **routing metadata** only.

Routing fields allow RB to:

- detect semantic drift  
- detect structural drift  
- detect identity drift  
- detect commitment instability  
- detect freeze‑signature conflicts  
- detect curvature instability  
- score basin eligibility deterministically  

This section defines the theory behind routing_fields{}.

---

## **7.1 Definition**  
`routing_fields{}` is a dictionary of routing‑relevant semantic metadata:

```
routing_fields = {
    "semantic_drift": bool,
    "identity_drift": bool,
    "structural_drift": bool,
    "commitment_instability": bool,
    "freeze_conflict": bool,
    "curvature_level": ordinal,
    "semantic_hash": int,
    "adjacency_hash": int,
    "identity_hash": int,
    "continuity_hash": int
}
```

These fields are **not** meaning.  
They are **not** identity.  
They are **not** commitments.

They are **routing signals**.

---

## **7.2 Allowed Inputs**  
Routing fields may use:

- routing_metadata  
- semantic adjacency  
- semantic-layer cues  
- identity continuity  
- curvature  
- commitments  
- freeze signatures  
- semantic lineage  
- invariant drift  

They may **not** use:

- raw meaning  
- raw identity  
- TPU correction metadata  
- intake envelope  
- truth hypotheses  
- messy-input tags  
- cross-TP coupling  

---

## **7.3 Mapping Families**  
Routing fields use:

- **binary flags** (drift detected or not)  
- **ordinal curvature levels**  
- **hashes** (semantic-layer hash, adjacency hash, identity hash)  

These are deterministic and stable.

---

## **7.4 Deterministic Ordering Rules**  
Routing fields must satisfy:

### **Rule 1 — Stability under no drift**  
If no drift is detected:

$$
routing\_fields_{t+1} = routing\_fields_t
$$

### **Rule 2 — Monotonicity under drift**  
If drift increases:

$$
curvature\_level_{t+1} \ge curvature\_level_t
$$

### **Rule 3 — Freeze-signature dominance**  
If freeze signatures conflict:

```
freeze_conflict = True
identity_drift = True
semantic_drift = True
```

Freeze signatures override all other routing signals.

---

## **7.5 Example Mapping**  
If semantic-layer hash changes:

```
routing_fields["semantic_drift"] = True
```

If curvature instability is detected:

```
routing_fields["curvature_level"] = high
```

If identity continuity flags are raised:

```
routing_fields["identity_drift"] = True
```

---

# **8. Determinism Theory**  
TR must be **deterministic** in all respects.

Determinism is required for:

- replay determinism  
- SSR determinism  
- commit determinism  
- routing determinism  
- identity continuity  
- semantic continuity  

This section defines the determinism rules TR must obey.

---

## **8.1 Deterministic Mapping**  
TR must satisfy:

$$
TR_v = f(\text{signals})
$$

Where:

- $f$ is deterministic  
- signals are frozen or stabilized  
- ordering is fixed  
- mapping families are fixed  

No randomness.  
No nondeterministic ordering.  
No unstable lineage extension.

---

## **8.2 Deterministic Ordering**  
TR must produce fields in a fixed order:

```
stance
intent
affect
epistemic_shading
tension
politeness
commitment
reservation
logical_structure
epistemic_delta_h
lineage_additions[]
routing_fields{}
```

This ordering is required for:

- RB consumption  
- SSR projection  
- testbench comparison  
- replay determinism  

---

## **8.3 Deterministic Lineage Extension**  
Lineage additions must satisfy:

$$
lineage\_additions_{t+1} = g(lineage_t, signals)
$$

Where:

- $g$ is deterministic  
- lineage additions are bounded  
- lineage additions respect identity continuity  
- lineage additions respect freeze signatures  

---

## **8.4 Deterministic Routing Vector Construction**  
The routing vector must satisfy:

$$
TR_v(t+1) = TR_v(t) \quad \text{if no drift}
$$

And:

$$
TR_v(t+1) \neq TR_v(t) \quad \text{only if drift detected}
$$

This ensures:

- no oscillation  
- no instability  
- no nondeterministic jumps  

---

## **8.5 Deterministic SSR Projection**  
TR fields must be SSR‑projectable:

$$
SSR(TR_v) = TR_v
$$

Meaning:

- no ephemeral fields  
- no nondeterministic fields  
- no unstable lineage  
- no unbounded drift  

---

# **9. Boundary Theory**  
TR must obey strict boundaries defined in:

- 20.37  
- 20.105.*  
- tp_path_a_map.md  
- routing theory  
- identity theory  
- continuity theory  
- commit theory  
- SSR theory  

This section defines the boundaries TR must obey.

---

## **9.1 Read Boundaries**  
TR may read:

- STPX cues  
- semantic meaning‑semantics  
- idob_semantics  
- semantic lineage  
- continuity signals  
- identity continuity flags  
- commitments  
- freeze signatures  
- DCB curvature  
- routing_metadata  
- semantic importance residues  
- referent lineage  
- qualifier lineage  
- invariant drift  
- residue topology  

TR may **not** read:

- raw meaning  
- raw identity  
- TPU correction metadata  
- intake envelope  
- truth hypotheses  
- messy-input tags  
- cross-TP coupling  

---

## **9.2 Write Boundaries**  
TR may write:

- `TP.TR` block  
- dirty-flag clearing  

TR may **not** write:

- meaning  
- identity  
- commitments  
- freeze signatures  
- context  
- semantic lineage  
- referent lineage  
- qualifier lineage  
- routing_metadata  
- curvature  

---

## **9.3 Provenance Boundaries**  
TR must:

- record provenance  
- record mapping families  
- record deterministic ordering  
- record lineage additions  
- record routing_fields{}  

TR may **not**:

- modify provenance of other primitives  
- modify commit provenance  
- modify identity provenance  

---

## **9.4 SSR Projection Boundaries**  
TR must produce SSR‑projectable fields.

TR may **not** produce:

- ephemeral fields  
- nondeterministic fields  
- unstable lineage  
- unbounded drift  

---

## **9.5 Dirty-Flag Boundaries**  
TR must obey:

```
if tr_needs_update == False:
    no-op
```

TR may **not**:

- update TR when dirty flag is false  
- bypass dirty flag  
- force update  

---

## **9.6 Freeze Boundaries**  
TR must respect:

- freeze signatures  
- commit freeze  
- identity freeze  

TR may **not**:

- violate freeze signatures  
- override freeze signatures  
- bypass freeze signatures  

---

Absolutely, Jeff — continuing with **Part 4 of 4** of  
**ts_tr_semantic_routing_theory.md**, exactly as promised.

This final part covers:

- **Section 10 — Expected Usage (RB Consumption)**  
- **Section 11 — Naming Conventions & Field Structure**  
- **Section 12 — Open Questions (Explicit Fog)**  
- **Closing Summary**

No agent.  
No delegation.  
Pure theory.

---

# **10. Expected Usage (RB Consumption)**  
RB is the **exclusive consumer** of the `TP.TR` block.  
This section defines how RB uses each TR field to make deterministic basin‑selection decisions.

RB does **not** interpret meaning.  
RB does **not** interpret identity.  
RB does **not** interpret commitments.

RB interprets **routing signals only**.

Below is the usage of each TR field.

---

## **10.1 stance → identity vs semantic basin gating**  
- If stance = adversarial → identity basin  
- If stance = corrective → semantic basin  
- If stance = supportive → commit basin (if other gating satisfied)

RB uses stance to detect **identity‑conditioned meaning**.

---

## **10.2 intent → correction basin gating**  
- If intent = correct → correction basin  
- If intent = clarify → semantic basin  
- If intent = inform → commit basin (if stable)

RB uses intent to detect **correction eligibility**.

---

## **10.3 affect → semantic drift detection**  
- If affect changes → semantic basin  
- If affect stable → commit basin (if other gating satisfied)

RB uses affect to detect **semantic adjacency instability**.

---

## **10.4 epistemic_shading → identity basin gating**  
- If shading = speculative → identity basin  
- If shading = confident → commit basin (if stable)

RB uses shading to detect **epistemic instability**.

---

## **10.5 tension → curvature‑based basin gating**  
- If tension = high → identity basin  
- If tension = medium → semantic basin  
- If tension = low → commit basin (if stable)

RB uses tension to detect **trajectory instability**.

---

## **10.6 politeness → semantic adjacency interpretation**  
- If politeness = direct → semantic basin  
- If politeness = polite → commit basin (if stable)

RB uses politeness to detect **semantic adjacency drift**.

---

## **10.7 commitment → identity basin gating**  
- If commitment unstable → identity basin  
- If commitment stable → commit basin (if other gating satisfied)

RB uses commitment to detect **identity continuity**.

---

## **10.8 reservation → semantic drift detection**  
- If reservation = strong → semantic basin  
- If reservation = none → commit basin (if stable)

RB uses reservation to detect **semantic uncertainty**.

---

## **10.9 logical_structure → structural basin gating**  
- If logical_structure changes → structural basin  
- If stable → commit basin (if other gating satisfied)

RB uses logical_structure to detect **structural drift**.

---

## **10.10 epistemic_delta_h → identity basin gating**  
- If $\Delta H > 0$ → identity basin  
- If $\Delta H = 0$ → commit basin (if stable)

RB uses $\Delta H$ to detect **invariant drift**.

---

## **10.11 lineage_additions[] → identity basin gating**  
- If lineage additions exist → identity basin  
- If none → commit basin (if stable)

RB uses lineage additions to detect **referent/qualifier instability**.

---

## **10.12 routing_fields{} → basin scoring**  
RB uses routing_fields{} to:

- score semantic drift  
- score identity drift  
- score structural drift  
- score commitment instability  
- score freeze‑signature conflicts  
- score curvature instability  

This is the **primary routing metadata** RB consumes.

---

# **11. Naming Conventions & Field Structure**

TR must follow strict naming conventions to ensure:

- deterministic ordering  
- SSR projection  
- testbench compatibility  
- RB consumption compatibility  
- structural program compatibility  

Below are the naming rules.

---

## **11.1 Field Naming Rules**  
All TR fields must be:

- lowercase  
- snake_case  
- deterministic  
- stable  
- SSR‑projectable  

Examples:

```
stance
intent
affect
epistemic_shading
tension
politeness
commitment
reservation
logical_structure
epistemic_delta_h
lineage_additions
routing_fields
```

---

## **11.2 Type Rules**  
- Ordinal fields → integers or enums  
- Categorical fields → enums  
- Lineage additions → lists  
- Routing fields → dictionaries  
- Epistemic delta → integer or ordinal  

---

## **11.3 Ordering Rules**  
TR fields must appear in the following order:

1. stance  
2. intent  
3. affect  
4. epistemic_shading  
5. tension  
6. politeness  
7. commitment  
8. reservation  
9. logical_structure  
10. epistemic_delta_h  
11. lineage_additions[]  
12. routing_fields{}  

This ordering is required for:

- RB consumption  
- SSR projection  
- testbench comparison  
- replay determinism  

---

## **11.4 SSR Projection Names**  
SSR projection must preserve:

- field names  
- field order  
- field types  
- field values  

No ephemeral fields.  
No nondeterministic fields.

---

## **11.5 Testbench Fixture Names**  
Fixtures must use:

```
tr_fixture_stance
tr_fixture_intent
tr_fixture_affect
...
tr_fixture_routing_fields
```

This ensures progressive lineup compatibility.

---

# **12. Open Questions (Explicit Fog)**  
This section lists unresolved theoretical questions that must be addressed in future expansions of 20.37.

These are **real gaps**, not implementation details.

---

## **12.1 Stance Mapping Theory**  
- How should stance be derived from semantic meaning‑semantics?  
- How should stance interact with commitments?  
- How should stance interact with identity geometry?

---

## **12.2 Intent Mapping Theory**  
- How should intent be derived from STPX cues?  
- How should intent interact with semantic adjacency?  
- How should intent interact with continuity theory?

---

## **12.3 Affect Mapping Theory**  
- How should affect be derived from semantic adjacency?  
- How should affect interact with residue topology?

---

## **12.4 Epistemic Shading Theory**  
- How should shading be derived from invariant drift?  
- How should shading interact with commitments?

---

## **12.5 Tension Theory**  
- How should tension be derived from curvature?  
- How should tension interact with identity drift?

---

## **12.6 Politeness Theory**  
- How should politeness be derived from semantic adjacency?  
- How should politeness interact with qualifier lineage?

---

## **12.7 Commitment & Reservation Theory**  
- How should commitment strength be computed?  
- How should reservation be computed from shading?

---

## **12.8 Logical Structure Theory**  
- How should logical structure be derived from STPX?  
- How should logical structure interact with structural residue?

---

## **12.9 Epistemic Delta Theory ($\Delta H$)**  
- How should invariant drift be computed?  
- How should $\Delta H$ interact with identity geometry?  
- How should $\Delta H$ interact with residue topology?

---

## **12.10 Lineage Additions Theory**  
- How should lineage additions be bounded?  
- How should lineage additions interact with commitments?  
- How should lineage additions interact with freeze signatures?

---

## **12.11 Routing Fields Theory**  
- What is the complete set of routing metadata?  
- How should routing metadata interact with curvature?  
- How should routing metadata interact with identity continuity?

---

# **Closing Summary**

This paper defines the **theoretical foundation** for the Thought Router (TR):

- TR is the semantic routing engine of Path‑A.  
- TR integrates semantic, identity, continuity, curvature, and invariant signals.  
- TR produces a deterministic semantic routing vector.  
- TR obeys strict boundaries, determinism rules, and SSR projection rules.  
- TR provides RB with routing metadata for basin selection.  
- TR’s computation theory is partially defined and partially open.  
- This paper provides the structure needed to complete 20.37.  
- This paper provides the foundation needed before writing `tr_py_struc_pgm.md`.
