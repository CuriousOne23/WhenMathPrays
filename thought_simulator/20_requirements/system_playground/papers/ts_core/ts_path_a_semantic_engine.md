# ts_path_a_semantic_engine.md

## 1. Purpose of Path A

Path A is the **semantic engine** of Thought Simulator (TS).

Its job is to:

- construct and stabilize **meaning** for each user turn,
- independent of grammar, syntax, or surface form,
- and deliver a deterministic **semantic snapshot representation (SSR‑A)** to downstream systems (including Path B).

Path A operates in a **verb‑thinking, geometric** mode:

- it decomposes input into **semantic roles** (agent, action, state, relation, modifier),
- projects them onto a **semantic manifold** built in pre‑work,
- validates them against **invariants, cue envelopes, and routing signatures**,
- and selects the lowest‑entropy valid binding as the committed meaning.

Grammar, syntax, and expression are explicitly **out of scope** for Path A.  
Those belong to Path B.

---

## 2. Semantic primitives

Path A decomposes meaning using **semantic primitives**, not grammatical categories.

### 2.1 Primitive set

The core primitive set:

- **agent**  
  Entity that can act, bear identity, and participate in agent‑routes.

- **action**  
  Event, process, or operation that requires participants (agent, object, etc.).

- **state**  
  Condition or configuration that can hold, change, or persist.

- **relation**  
  Binding or linkage between entities, states, or actions.

- **modifier**  
  Refiner of other primitives (e.g., qualities, degrees, constraints).

Each dictionary entry in Path A is anchored to **exactly one primitive** per semantic identity.

### 2.2 Primitive role vs grammar

Primitive roles are **semantic**, not grammatical:

- “agent” is not “subject”,
- “object” is not a primitive; it is a **role** derived from relation + action,
- “modifier” is not “adjective/adverb”; it is a semantic refiner.

Path A never uses Part of Speech (POS) tags, parse trees, or grammatical roles to determine primitives.

---

## 3. Invariants

**Invariants** are truth constraints that must always hold for a semantic identity.

They are the backbone of semantic stability.

### 3.1 Definition

For a given semantic identity (e.g., “dog” as agent):

- invariants specify **non‑negotiable truths** about that identity,
- they must be satisfied in any valid binding,
- violation of invariants invalidates the candidate meaning.

Example (informal):

- “dog” (agent):  
  - animate  
  - has_identity  
  - participates_in_agent_route

- “chased” (action):  
  - requires_agent  
  - requires_object

### 3.2 Role in Path A

Path A uses invariants to:

- filter out impossible meanings,
- prevent nonsensical bindings (“The fall chased the cat”),
- enforce semantic coherence independent of grammar.

Invariants are part of the **pre‑work manifold**: they define allowed regions of semantic space.

---

## 4. Cue envelopes

**Cue envelopes** control when a semantic identity is activated or suppressed.

They are the interface between **context** and **meaning**.

### 4.1 Definition

A cue envelope contains:

- **triggers**: contextual signals that activate a meaning,
- **suppressors**: signals that deactivate or down‑weight a meaning.

Examples:

- “bank” (financial institution):  
  - triggers: finance, money, loan, interest  
  - suppressors: river, slope, geography

- “bank” (river bank):  
  - triggers: river, water, slope, geography  
  - suppressors: loan, interest, currency

### 4.2 Role in Path A

Path A uses cue envelopes to:

- select which semantic identities are **eligible** in the current context,
- disambiguate polysemous words,
- maintain continuity across turns via **identity_anchor** and context cues.

Cue envelopes are also part of the **pre‑work manifold**: they define activation regions.

---

## 5. Routing signatures and identity anchors

Path A does **semantic routing**, not grammatical routing.

### 5.1 Routing signatures

A **routing signature** defines how a semantic identity can bind to other primitives.

It specifies:

- route class (e.g., agent‑route, action‑route, relation‑route, modifier‑route),
- constraints on what it can bind to and how.

Examples:

- “dog” (agent):  
  - route_class: agent‑route  
  - constraints: must_bind_to_action_as_agent

- “chased” (action):  
  - route_class: action‑route  
  - constraints: must_bind_agent_and_object

Routing signatures ensure that:

- agents bind to actions,
- objects bind via relations to actions,
- modifiers bind to appropriate targets,
- invalid bindings are rejected.

### 5.2 Identity anchors

**Identity anchors** maintain semantic continuity across turns.

They encode:

- which semantic identity is currently active for a word,
- how that identity persists or shifts across sentences,
- how prior SSR‑A influences current interpretation.

Example:

- Turn 1: “The bank approved the loan.”  
  → identity_anchor(bank) = financial institution.

- Turn 2: “The bank was steep.”  
  → Path A detects mismatch and shifts identity_anchor(bank) to river bank.

Identity anchors are part of the manifold’s **continuity fields**.

---

## 6. Semantic manifold and entropy H

Path A operates on a **semantic manifold** constructed in pre‑work.

### 6.1 Semantic manifold

The manifold encodes:

- invariant surfaces (where constraints hold),
- cue‑activation regions,
- routing compatibility zones,
- identity continuity fields,
- contradiction pressure,
- stability vs instability regions.

It is the **geometric substrate** of meaning.

Path A does not invent meaning; it **projects** candidate interpretations onto this manifold.

### 6.2 Entropy H

After projection, Path A computes **semantic entropy H**:

- H measures contradiction pressure, cue instability, routing tension, and identity discontinuity,
- low H = stable, coherent meaning,
- high H = unstable, ambiguous, or contradictory meaning.

Entropy is written to an interpretation scoring field (e.g., `tp_entropy_score`) and used to rank valid bindings.

Crucially:

- H is **not** the primary selector,
- it is a **diagnostic** applied **after** invariant and routing validation.

---

## 7. Path A binding algorithm

Path A’s core operation is **semantic binding**: selecting a meaning for each word and constructing a coherent graph.

### 7.1 Candidate generation

For each word in the input:

1. Retrieve all **semantic identities** from the dictionary:
   - each with primitive, invariants, cue envelope, routing signature, identity anchor.

2. Apply **cue envelopes**:
   - discard identities whose triggers are not activated or whose suppressors are strongly active.

### 7.2 Manifold validation

For each remaining candidate identity:

1. Check **invariants**:
   - if violated → reject candidate.

2. Check **routing signatures**:
   - attempt to bind primitives into a semantic graph (agent, action, state, relation, modifier),
   - if routing constraints cannot be satisfied → reject candidate.

3. Check **identity continuity**:
   - compare with prior SSR‑A and identity_anchor,
   - if continuity is strongly violated without contextual justification → down‑weight or reject.

Only candidates that pass these checks are considered **valid bindings**.

### 7.3 Entropy scoring and selection

For each valid binding:

1. Project onto the **semantic manifold**.
2. Compute **entropy H**:
   - contradiction pressure,
   - cue instability,
   - routing tension,
   - identity discontinuity.

Selection rule:

- If only one valid binding exists → choose it.
- If multiple valid bindings exist → choose the one with **lowest entropy H**.

Invalid bindings are discarded before entropy is considered.

---

## 8. SSR‑A: Path A’s output

The final output of Path A is **SSR‑A** (Semantic Snapshot Representation – Path A).

SSR‑A contains:

- semantic graph:
  - agents, actions, states, relations, modifiers,
  - their bindings and roles,
- invariant satisfaction status,
- cue envelope activations,
- routing configuration,
- identity anchors for key entities,
- entropy score H,
- any flags for unresolved ambiguity or contradiction.

SSR‑A is:

- **deterministic** at commit time,
- **grammar‑independent**,
- the **sole input** to Path B’s expression engine.

Path B does not reinterpret meaning; it expresses SSR‑A.

---

## 9. Relation to Path B

Path A and Path B are **strictly separated**:

- **Path A**:
  - meaning engine,
  - verb‑thinking,
  - semantic primitives,
  - invariants, cues, routing, manifold, entropy,
  - produces SSR‑A.

- **Path B**:
  - expression engine,
  - noun‑thinking / grammar,
  - syntax, morphology, style, narrative structure,
  - takes SSR‑A and generates language.

Path A never uses:

- POS tags,
- parse trees,
- grammatical roles,
- token probabilities.

Path B never alters:

- primitives,
- invariants,
- routing decisions,
- identity anchors.

This separation is fundamental to TS.

---

## 10. Comparison: Grammar/POS vs TS Semantic Routing

A reader coming from Natural Language Processing (NLP) or linguistics will naturally assume that meaning is extracted from **grammar**, **syntax**, or **POS tags**. Path A does not use any of these. This section provides a direct comparison between the traditional grammatical organization of language and TS’s semantic routing architecture.

### 10.1 Grammar/POS: Noun‑Thinking

Traditional language systems (linguistics, NLP, LLMs) organize language around **objects**:

- nouns  
- verbs  
- adjectives  
- subjects  
- objects  
- clauses  
- POS tags  
- dependency trees  

These structures are **static** and **categorical**. They describe *what the word is* in the sentence. Grammar is fundamentally **noun‑thinking**:

> Grammar describes objects and their positions.

It focuses on:

- categories  
- labels  
- identity  
- surface structure  
- syntactic roles  

Meaning is inferred *after* grammatical parsing.

### 10.2 TS Semantic Routing: Verb‑Thinking

TS organizes language around **relations and roles**, not categories:

- agent  
- action  
- state  
- relation  
- modifier  

These primitives describe *what the word does* in the meaning graph. Semantic routing is fundamentally **verb‑thinking**:

> Semantics describes objects and the relations they participate in.

It focuses on:

- invariants  
- cue envelopes  
- routing signatures  
- identity continuity  
- manifold projection  
- entropy stability  

Meaning is constructed *before* any expression or grammar.

### 10.3 Why Grammar and Semantics Diverge

Grammar is a **surface‑form system**:

- It tells you how words are arranged.
- It tells you what category a word belongs to.
- It tells you the syntactic role (subject, object, modifier).

TS semantics is a **meaning‑form system**:

- It tells you what role the entity plays (agent, object, modifier).
- It tells you what invariants must hold.
- It tells you how meaning binds into a graph.
- It tells you whether the interpretation is stable (entropy H).

Grammar is **parsed**.  
Semantics is **projected** onto the pre‑work manifold.

### 10.4 Example: “The dog chased the cat.”

**Grammar/POS view (noun‑thinking):**

- “dog” = noun  
- “chased” = verb  
- “cat” = noun  
- “dog” = subject  
- “cat” = object  

Meaning is inferred from syntactic structure.

**TS semantic routing (verb‑thinking):**

- “dog” → agent (invariants: animate, has_identity)  
- “chased” → action (invariants: requires_agent, requires_object)  
- “cat” → object via relation (invariants: object_of_action)  

Meaning is constructed from **semantic identity**, not grammar.

### 10.5 Pre‑work: The Machine Exercises the Mapping

All semantic routing rules — primitives, invariants, cue envelopes, routing signatures, identity anchors, manifold geometry — are defined in **pre‑work**.

Path A does not “learn” meaning.  
Path A does not “infer” meaning from grammar.  
Path A does not “guess” meaning from tokens.

Instead:

> The machine exercises the mapping defined in pre‑work.

The semantic manifold provides:

- invariant surfaces  
- cue activation regions  
- routing compatibility zones  
- identity continuity fields  
- entropy curvature  

Path A simply projects candidate meanings onto this manifold and selects the lowest‑entropy valid binding.

### 10.6 Summary Table

| Aspect | Grammar/POS (Noun‑Thinking) | TS Semantic Routing (Verb‑Thinking) |
|-------|------------------------------|-------------------------------------|
| Organizes language by | categories, labels | roles, relations |
| Core units | nouns, verbs, adjectives | agent, action, state, relation, modifier |
| Focus | objects | interactions |
| Structure | static | dynamic |
| Meaning source | inferred from syntax | constructed from invariants + cues |
| Mechanism | parsing | manifold projection |
| Stability | none | entropy H |
| Pre‑work | grammar rules | semantic manifold |

### 10.7 Why TS Requires Semantic Routing

Grammar is insufficient for deterministic meaning because:

- grammar cannot enforce invariants,  
- grammar cannot encode cue envelopes,  
- grammar cannot maintain identity continuity,  
- grammar cannot compute semantic entropy,  
- grammar cannot route meaning.

TS requires a **semantic engine** because meaning is fundamentally **relational**, **geometric**, and **verb‑driven**.

Path A is that engine.


## 11. Implications and uniqueness

Path A introduces a **new computational paradigm**:

- meaning is routed, not grammar,
- words have **semantic identities** with primitives, invariants, cues, and routing signatures,
- interpretation is a **geometric projection** onto a semantic manifold,
- stability is measured via **entropy H**,
- ambiguity is resolved by **valid binding + lowest entropy**, not by grammatical heuristics.

No existing NLP, linguistic, or AI system:

- uses semantic primitives with invariants and cue envelopes,
- performs deterministic semantic routing,
- operates on a pre‑work semantic manifold,
- separates meaning (Path A) from expression (Path B) in this way.

Path A is the **core semantic engine** of Thought Simulator and the foundation for all downstream routing, truth‑relations, and expression.

---
