# structure.md
### Structure as admissibility geometry (TS Path A / IdOB bench)

**Theory spine:** [../papers/idob_s2m_theory.md](../papers/idob_s2m_theory.md) §2.3–2.5  
**Meaning tables:** [../02_meaning_groups/dimensions.md](../02_meaning_groups/dimensions.md)  
**Date:** 2026-08-26; two-geometry alignment 2026-08-27

---

# 0. Alignment (read first)

This file keeps the functional-attribute catalog below. Read it under the theory spine:

- Path A is a **research vehicle** for a structure-to-meaning crossing. It does not claim to be cognition.
- Where this file says "cognition" or "cognition machine," read: **the Path A operational stake** — deterministic, observable interpretation of an utterance as structure plus an intended-projection stand-in.
- Structure and meaning are **two geometries**, not one geometry with two views.

## Feel

Structure is the **landscape and the roads**: what shapes of talk exist, which routes a projection may legally travel. No meaning scores live on the road. The utterance-shape *is* classified here (six IDs → key). The thought-object is *not* born here.

## What structure is / is not

| Structure is | Structure is not |
|--------------|------------------|
| Discrete admissibility geometry | The six meaning axes |
| Meaning-blind classification of talk-shape | Intended projection M |
| field, role, object, gradient, universe, subfield | physicality … spatiality |
| What makes a crossing *legal to attempt* | The object proposed into being |

Names must not trade places. Do not list structure fields as physicality, sociality, …

## Same-utterance example (structure side only)

"The rock burst open." Teaching IDs (not scores): field ~ action/event-of-break; role ~ patient-like rock; object ~ rock; gradient ~ dynamic; universe ~ everyday physical; subfield ~ 0 or finer. One key. Meaning weights for this line live in dimensions.md, not on this card.

"The project deadline is Friday." Different six-tuple → different key. That is structure doing its job before any physicality number exists.

## How to use the catalog below

Sections 1–9 remain the attribute list and evaluation criteria. Use them to judge whether the six IDs, key, and legality map are doing road-work. If an attribute requires structure to *score meaning* or to *be* cognition, prefer the theory paper.

Empty map after a valid key (S_unmapped) is allowed. Structure can exist with no M yet.

---

# 1. Purpose of This Document

This document defines **Structure** for TS Path A — not as a schema, not as a YAML file, not as a Python script, but as a **requirement**.

Structure is the **first constraint** required for TS Path A to realize the crossing. It is defined not only by what it *is*, but by what it is **expected to enable**.

TS is a theory of a structure-to-meaning crossing (see theory paper). Path A is the machine realization of that theory. Structure is the geometric foundation that makes Path A possible.

This document explains:

- what structure must accomplish
- why the crossing requires these properties
- how Path A realizes them
- how the YAML and Python files implement them
- how to evaluate whether structure is fulfilling its role

Structure is revisable. Structure is falsifiable. Structure is defined by **functional necessity**, not by tradition.

---

# 2. Minimal functional theory (this file's original list)

TS does not claim to define cognition in the scientific sense — no such definition exists.

TS claims Path A operationalizes a **minimal, deterministic interpretation of human communication** sufficient to make the crossing visible.

This minimal list (from the original draft) asserts:

1. Path A constructs structured packets (IdOBs).
2. These objects have **geometry** (Structure), **content** (Meaning), and **stance** (Identity) — two geometries plus pressure, not one space.
3. The crossing is **progressive**, not instantaneous.
4. Utterances may contain **multiple** semantic objects.
5. Interpretation is **identity-conditioned** (CIE pressures M; key stays).
6. Meaning moves in a structured space **after** structure admits it.
7. The crossing is **observable** through behavior (meaning deltas, identity deltas, freeze status).
8. The crossing is **measurable** if Path A logs those fields honestly.

Structure is the first constraint that makes this realizable.

---

# 3. Why Structure Exists

Structure exists because Path A cannot operate on raw text.

Path A requires:

- admissible IdOB shapes
- deterministic fingerprints
- meaning group legality
- identity envelope initialization (without baking CIE into the key)
- freeze geometry (named halt, not invented by structure scores)
- routing metadata
- multi-object admissibility
- continuity of keys under small talk-shape changes
- progressive interpretation

Structure provides these.

Structure is not meaningful by itself. Structure is meaningful because **Path A needs it**.

---

# 4. The Structural Attributes Required

Below is the list of structural attributes Path A requires for the crossing. If an attribute fails, the road is broken.

Each attribute includes Functional Requirement, Why the crossing needs it, Path A Realization, Examples grounded in YAML/Python.

## 4.1 Deterministic Structural Key (Replay Stability)

**Requirement:** Same six IDs → same structural_key → same shape.

**Why:** Replay and testability.

**Path A Realization:** `make_structural_key.py` fingerprints the six IDs deterministically.

**Example:** From `structure_card.examples.yaml` (IDs may be integers or teaching labels depending on revision):

```
semantic_field_id
semantic_role_id
semantic_object_id
gradient_id
universe_id
subfield_id
```

## 4.2 Unique Routing Geometry (No Collisions)

**Requirement:** Different talk-shapes must not collapse into the same structural_key without a logged reason.

**Why:** Ambiguous geometry → ambiguous legality → fog at the door.

**Path A Realization:** Six IDs form the key. Orthogonality of IDs is a hypothesis to convict, not a theorem.

## 4.3 Coverage of communication space (no silent holes)

**Requirement:** A significant share of ordinary utterances must take *some* usable structure. Empty meaning map after a valid key is allowed. "No card at all" as the usual case is a hole.

**Why:** If structure cannot represent an utterance, Path A cannot begin.

**Path A Realization:** Schema and examples span action, state, event, tasks; four toy cards do not prove coverage.

## 4.4 Progressive Routing Capability

**Requirement:** Structure must support stage-by-stage crossing:

```
Structure → Meaning → Identity pressure → Freeze
```

**Why:** The crossing is progressive.

**Path A Realization:** `run_01_inspect_structure.py` prints geometry only (no meaning floats).

## 4.5 Detailed Routing Capability

**Requirement:** Structure must support fine-grained routing: roles, objects, gradients, universes, subfields.

**Why:** Fine geometry determines meaning legality.

**Path A Realization:** All six IDs are present in the schema.

## 4.6 General Routing Capability

**Requirement:** Structure must provide geometry that later stages can route (TR / later Path A modules).

**Why:** Routing is how the packet moves.

**Path A Realization:** Structure feeds the map and rank; this bench stops at IdOB handoff.

## 4.7 Local Predictability Between cards

**Requirement:** Small changes in utterance-shape → small, intentional changes in the six-tuple.

**Why:** Near-neighbor discrimination.

**Path A Realization:** Changing only `subfield_id` should change the key predictably.

## 4.8 Meaning Group Legality

**Requirement:** Structure must determine which meaning groups are allowed.

**Why:** Meaning must be constrained by geometry.

**Path A Realization:** Map keyed by card/key; field and role are primary levers.

**Example:** A repair-shaped card may legalize PERSON, OBJECT, LOCATION groups — those are meaning groups, not structure IDs.

## 4.9 Prototype Meaning Vector Initialization

**Requirement:** Structure plus the map must make a first M *admissible*. Structure does not write the six floats.

**Why:** Meaning cannot begin without a legal prototype.

**Path A Realization:** Selected group supplies group_dimensions; that is meaning geometry.

## 4.10 Identity Envelope Initialization

**Requirement:** Structure may *cue* which CIE is plausible. Structure must not bake CIE into the key.

**Why:** Identity pressures M after the road is fixed.

**Path A Realization:** gradient_id and universe_id may inform routing features; CIE lives in meaning-side modulation.

## 4.11 Freeze Stability

**Requirement:** Structure must remain fixed while freeze is decided on M / identity deltas / budget.

**Why:** Freeze is named halt of the stand-in, not a new structure score.

**Path A Realization:** resolution_status is not a seventh structure ID.

## 4.12 Multi-Object Admissibility

**Requirement:** Structure must allow multiple meaning objects when the utterance has more than one structural object.

**Why:** Talk is often multi-object.

**Path A Realization:** Roles and objects determine multi-object admissibility; IdOB must not invent objects structure denied.

## 4.13 Independence of Structural Dimensions

**Requirement:** Each structural ID should be able to change without being a rename of another ID.

**Why:** Collapsed IDs → collapsed keys.

**Path A Realization:** Six IDs; independence is to be tested, not declared complete.

## 4.14 Coverage (no dead zones as the usual case)

**Requirement:** Structure should cover a significant share of domains this instrument cares about.

**Why:** Missing domains → missing roads.

**Path A Realization:** Examples span multiple domains; coverage remains an open hand-check.

## 4.15 Local smoothness (no unnecessary cliffs)

**Requirement:** Small changes in utterance-shape should not leap to an unrelated key without a reason.

**Why:** Discrimination vs chaos.

**Path A Realization:** Schema should support smooth transitions; cliffs are revision signals.

## 4.16 Compositionality

**Requirement:** Structure must allow composing roles, objects, gradients.

**Why:** Utterance-shape is compositional.

**Path A Realization:** Schema is a product of slots, not a single opaque blob.

## 4.17 Minimality

**Requirement:** Structure should not grow extra IDs without a named revision.

**Why:** Extra slots without a job are fog.

**Path A Realization:** This revision uses exactly six IDs plus optional residue/features.

## 4.18 Expandability

**Requirement:** Structure must allow future expansion as a new revision.

**Why:** The theory will move.

**Path A Realization:** Residue and feature tags allow extension without putting meaning in the key.

## 4.19 Machine Realizability

**Requirement:** Structure must be implementable in code.

**Why:** A research vehicle must run.

**Path A Realization:** Python scripts implement structure deterministically.

## 4.20 Human Interpretability

**Requirement:** Structure must be understandable by humans.

**Why:** Feel + rigor. The road must be readable.

**Path A Realization:** YAML examples are readable; lesson 01 prints IDs and refuses meaning floats.

---

# 5. The Structure Schema (YAML)

The schema in `structure_card.schema.yaml` defines the six IDs:

```
semantic_field_id:
semantic_role_id:
semantic_object_id:
gradient_id:
universe_id:
subfield_id:
```

These IDs are not the whole definition of structure. They are the **implementation** of the attributes listed above.

Each ID must be evaluated by:

> Does this ID contribute to admissibility, key, and legality? If it is being used as a meaning score, it must be revised.

---

# 6. The Structure Code (Python)

### make_structural_key.py
Implements deterministic fingerprinting. Realizes: replay, uniqueness, machine realizability.

### run_01_inspect_structure.py
Prints structure cards and keys. Must not print meaning floats. Realizes: meaning-blind inspection.

---

# 7. Examples (YAML)

`structure_card.examples.yaml` demonstrates different structures, different keys, unmapped geometry. These examples show how structure affects *legality of the crossing*, not cognition-as-verdict.

---

# 8. Evaluation Criteria

Structure must be evaluated by:

### Does it produce deterministic keys?
If not → failure.

### Does it avoid unexplained collisions?
If not → failure.

### Does a significant share of ordinary talk take a card?
If not → routing hole → concern now. Four toys do not answer this.

### Does it support progressive crossing?
If not → failure.

### Does it support detailed routing (six slots)?
If not → failure.

### Does it support local predictability?
If not → failure.

### Does it constrain meaning groups without scoring M?
If not → failure (names traded places).

### Does CIE leave the key unchanged?
If not → two geometries collapsed.

### Can a valid key have an empty map?
If not → empty birth forbidden → door is fake.

### Is it minimal and expandable only by named revision?
If not → future fog.

Structure is revisable. Structure must evolve as the theory evolves.

---

# 9. Summary

Structure is defined by what the crossing requires: a meaning-blind road.

Structure is the minimal geometric constraint system required for Path A to:

- fingerprint talk-shape
- admit meaning groups
- leave identity off the key
- allow named freeze later
- support multi-object admissibility
- stay deterministic and readable

If the schema fails any required attribute, it must be revised.

Structure is the first constraint of the Path A crossing. It is not meaning geometry.
