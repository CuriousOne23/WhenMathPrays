# **meaning_dct_spec.md — Full Specification (Preview)**  
*(This is the content the task will generate as a complete Markdown document.)*

---

## **1. Purpose of This Specification**
The Path A Meaning Dictionary defines the deterministic semantic structure used by TS to interpret words. This specification describes:

- the dictionary schema  
- required and optional fields  
- invariants and constraints  
- cue envelope structure  
- routing signature structure  
- identity anchor rules  
- batch‑entry formats (CSV + JSON)  
- validation rules  
- schema evolution rules  
- examples  

This document is the canonical reference for all meaning dictionary entries.

---

## **2. Dictionary Schema Overview**
Each dictionary entry is a YAML object with the following structure:

```yaml
- id: <unique_id>
  word: <surface_form>
  identity_anchor: <anchor_id>
  meaning_signature:
    primitive: <agent|action|state|relation|modifier>
    invariants:
      - <invariant>
    cue_envelope:
      triggers:
        - <cue_trigger>
      suppressors:
        - <cue_suppressor>
  routing_signature:
    route_class: <route_class>
    constraints:
      - <routing_constraint>
  notes: <optional_free_text>
```

### **2.1 Required Fields**
- `id`  
- `word`  
- `identity_anchor`  
- `meaning_signature.primitive`  
- `meaning_signature.invariants`  
- `routing_signature.route_class`  
- `routing_signature.constraints`

### **2.2 Optional Fields**
- `notes`  
- future extension fields (declared in schema)

---

## **3. Field Definitions**

### **3.1 id**
A globally unique identifier for the dictionary entry.  
Format: `idnt_<word>_<hash>`  
Generated automatically if omitted.

### **3.2 word**
The surface form of the lexical item.

### **3.3 identity_anchor**
A stable semantic anchor used across TS subsystems.  
Must be unique.

### **3.4 meaning_signature**
Defines the semantic structure of the word.

#### **primitive**
One of:
- `agent`  
- `action`  
- `state`  
- `relation`  
- `modifier`

#### **invariants**
Semantic truths that must always hold.

#### **cue_envelope**
Defines activation/suppression conditions.

- `triggers`: cues that activate meaning  
- `suppressors`: cues that deactivate meaning  

### **3.5 routing_signature**
Defines how the word participates in routing.

#### **route_class**
Examples:
- `agent-route`  
- `object-route`  
- `modifier-route`  
- `relation-route`

#### **constraints**
Routing constraints required for deterministic interpretation.

### **3.6 notes**
Optional human-readable commentary.

---

## **4. Schema File**
The schema is stored in:

```
system_playground/dictionaries/path_a/meaning_dictionary_schema.yaml
```

It defines:

- required fields  
- optional fields  
- allowed primitives  
- allowed routing classes  
- field types  
- constraints  
- schema version  

---

## **5. Batch Entry Formats**

### **5.1 CSV Format**
Flat entries only.

```
operation,word,primitive,identity_anchor,invariants,cue_triggers,cue_suppressors,route_class,routing_constraints,notes
new,person,agent,,has_identity,context_agent,context_nonagent,agent-route,must_bind_to_action,
modify,system,object,idnt_system_123,exists,context_object,,object-route,must_bind_to_state,
delete,obsolete_word,,,,,,,,
```

### **5.2 JSON Format**
Supports nested structures.

```json
[
  {
    "operation": "new",
    "word": "person",
    "meaning_signature": {
      "primitive": "agent",
      "invariants": ["has_identity"],
      "cue_envelope": {
        "triggers": ["context_agent"],
        "suppressors": ["context_nonagent"]
      }
    },
    "routing_signature": {
      "route_class": "agent-route",
      "constraints": ["must_bind_to_action"]
    }
  }
]
```

---

## **6. Validation Rules**

### **6.1 Required Field Validation**
Entries missing required fields are rejected.

### **6.2 Primitive Validation**
Must match allowed primitives.

### **6.3 Identity Anchor Validation**
Must be unique.

### **6.4 Invariant Validation**
Must contain at least one invariant.

### **6.5 Cue Envelope Validation**
Triggers and suppressors must be lists.

### **6.6 Routing Validation**
Route class and constraints must be valid.

### **6.7 YAML Structural Validation**
All entries must parse cleanly.

---

## **7. Schema Evolution Rules**

### **7.1 Schema Versioning**
Schema includes a version number.

### **7.2 Change Detection**
If the schema changes:

- added fields  
- removed fields  
- renamed fields  
- changed types  
- changed constraints  

The script warns:

```
WARNING: Schema has changed. Applying the new schema will affect ALL dictionary entries.
Proceed? (y/n)
```

### **7.3 Global Revalidation**
If user proceeds:

- entire dictionary is revalidated  
- entries requiring modification are reported  
- automatic fixes applied where possible  
- rejected entries listed  

### **7.4 Schema Update Report**
Generated as:

```
schema_update_report.md
```

---

## **8. Examples**

### **8.1 Agent Example**
```yaml
- id: idnt_person_8f3a
  word: person
  identity_anchor: idnt_person_8f3a
  meaning_signature:
    primitive: agent
    invariants:
      - has_identity
    cue_envelope:
      triggers:
        - context_agent
      suppressors:
        - context_nonagent
  routing_signature:
    route_class: agent-route
    constraints:
      - must_bind_to_action
  notes: ""
```

### **8.2 Modifier Example**
```yaml
- id: idnt_big_2a9c
  word: big
  identity_anchor: idnt_big_2a9c
  meaning_signature:
    primitive: modifier
    invariants:
      - modifies_object
    cue_envelope:
      triggers:
        - context_size
      suppressors:
        - context_irrelevant
  routing_signature:
    route_class: modifier-route
    constraints:
      - must_bind_to_noun
  notes: ""
```

---

## **9. Index Files**
The script maintains:

- alphabetical index  
- primitive → word index  
- anchor → word index  
- routing class → word index  

---

## **10. Summary**
This specification defines the complete structure, rules, and workflow for maintaining the Path A Meaning Dictionary. All dictionary entries must conform to this spec.

---
