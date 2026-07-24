# TS Dictionary Examples
These examples illustrate how dictionary entries behave inside the Thought Simulator (TS) across Path A (meaning construction), KnB (boundary interpretation), and Path B (expression mapping).

---

## 1. Entity Example — `agent` (kn_1001)

**Meaning (Path A)**  
An *agent* is an entity capable of intentional action.  
It participates in relational structures such as:
- `can_perform` → `action`
- `performed_by` ← `action`

**Boundary Interpretation (KnB)**  
KnB stabilizes the concept as a coarse-level semantic anchor in the `semantic_core` region.

**Expression Mapping (Path B)**  
Expression surfaces:  
- `noun_surface` → “the agent”, “an agent”, “this agent”

**Example Sentences**
- “The agent initiates the process.”  
- “Identify the agent responsible.”

---

## 2. Entity Example — `object` (kn_1002)

**Meaning (Path A)**  
An *object* is a passive entity that receives actions.  
Relations include:
- `receives_action` ← `action`

**Boundary Interpretation (KnB)**  
KnB maps this to a stable region in the semantic manifold (`semantic_core`).

**Expression Mapping (Path B)**  
Expression surfaces:
- `noun_surface` → “the object”, “an object”

**Example Sentences**
- “The object is moved.”  
- “Describe the object.”

---

## 3. Event Example — `action` (kn_1003)

**Meaning (Path A)**  
An *action* is an event performed by an agent and applied to an object.  
Relations:
- `performed_by` → `agent`
- `applied_to` → `object`

**Boundary Interpretation (KnB)**  
KnB identifies this as part of the `semantic_flow` region — a dynamic relational cluster.

**Expression Mapping (Path B)**  
Expression surfaces:
- `verb_surface` → “performs”, “moves”, “acts”, “applies”

**Example Sentences**
- “The agent performs an action.”  
- “What action was taken?”

---

## 4. Property Example — `property` (kn_1004)

**Meaning (Path A)**  
A *property* is an attribute describing an entity.  
Relations:
- `describes` → `object`

**Boundary Interpretation (KnB)**  
KnB places this in the `semantic_descriptor` region.

**Expression Mapping (Path B)**  
Expression surfaces:
- `adjective_surface` → “red”, “large”, “stable”

**Example Sentences**
- “The object has a property.”  
- “Describe the property of the agent.”

---

## 5. State Example — `state` (kn_1005)

**Meaning (Path A)**  
A *state* is a condition in which an entity exists.  
Relations:
- `applies_to` → `agent`
- `applies_to` → `object`

**Boundary Interpretation (KnB)**  
KnB maps this to the `semantic_state` region — stable condition space.

**Expression Mapping (Path B)**  
Expression surfaces:
- `adjective_surface` → “active”, “idle”, “stable”
- `noun_surface` → “the state”, “a state”

**Example Sentences**
- “The agent is in a stable state.”  
- “Describe the object's current state.”

---

## Summary
These examples demonstrate how dictionary entries:
- anchor meaning in Path A  
- stabilize through KnB  
- project onto expression surfaces in Path B  
- support manifold geometry  
- enable deterministic RSG/RG behavior  

This file should grow as the dictionary expands.
