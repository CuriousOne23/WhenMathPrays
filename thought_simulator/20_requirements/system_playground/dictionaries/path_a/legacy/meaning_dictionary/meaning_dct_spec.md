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
The following fields **must** appear in every dictionary entry.  
Entries missing any of these fields are invalid and must be rejected by the batch‑entry script.

- `id`  
- `word`  
- `identity_anchor`  
- `meaning_signature.primitive`  
- `meaning_signature.invariants`  
- `routing_signature.route_class`  
- `routing_signature.constraints`

These fields form the core semantic and routing structure required by TS specifications (20.105, 20.31, 20.37).

### **2.2 Optional Fields**
These fields may be included for clarity or documentation but are not required for TS determinism.

- `notes`  
- future extension fields (declared in schema)

Optional fields must not affect routing, invariants, or meaning signatures.

---

### **2.3 Conditionally Required Fields**
Some fields are required only when certain primitives or routing classes are used.  
These rules ensure deterministic meaning interpretation while allowing flexibility across lexical categories.

#### **2.3.1 meaning_signature.cue_envelope**
Cue envelopes are:

- **Required** for:  
  - `modifier`  
  - `relation`

- **Optional** for:  
  - `agent`  
  - `action`  
  - `state`

Modifiers and relations rely on contextual activation/suppression, while agents, actions, and states often do not.

#### **2.3.2 cue_envelope.triggers / suppressors**
If a cue envelope is present:

- At least **one** of the following must be provided:  
  - `triggers`  
  - `suppressors`

An empty cue envelope is invalid.

#### **2.3.3 Routing constraints for specific route classes**
Some route classes may define additional constraints in future schema versions.  
If the schema specifies such constraints, they become conditionally required.

#### **2.3.4 Schema enforcement**
The batch‑entry script must:

- reject entries missing required fields  
- reject entries missing conditionally required fields when applicable  
- accept entries omitting optional fields  
- provide clear error messages indicating missing or invalid fields  
- revalidate all entries when the schema changes  

This ensures the dictionary remains deterministic, consistent, and aligned with TS specifications.

---

### **2.4 Optional but Recommended Fields**

#### **grammatical_identity** *(optional, recommended)*  
Defines the grammatical class of the word.  
Not required for TS semantic routing, but recommended for future syntactic and morphological extensions.

```yaml
grammatical_identity:
  pos: <noun|verb|adjective|adverb|relation-marker>
```

This field is optional in the schema but recommended for new entries.

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

The meaning dictionary is validated against a single authoritative schema file:

```
system_playground/dictionaries/path_a/meaning_dictionary_schema.yaml
```

This file defines the structure of dictionary entries, including:

- required fields  
- optional fields  
- conditionally required fields  
- allowed primitives  
- allowed routing classes  
- field types  
- constraints  
- schema version  

The schema file is the **single source of truth** for dictionary structure.  
CSV or JSON batch-entry files do **not** define schema and do **not** trigger schema change detection.

---

### **4.1 Schema File Format**

The schema is stored as a **YAML file** because YAML supports:

- nested structures  
- field typing  
- constraints  
- readability  
- easy diffing and version control  

This format allows the batch-entry script to load and validate entries deterministically.

---

### **4.2 Schema Versioning**

The schema file includes a version number:

```yaml
schema_version: 1.0.0
```

This version increments whenever:

- fields are added  
- fields are removed  
- fields are renamed  
- field types change  
- constraints change  
- allowed values change  

Versioning allows the script to detect schema evolution reliably.

---

### **4.3 Schema Change Detection**

Schema change detection is triggered **only** when the schema definition file changes.

The script compares:

- previous schema version  
- current schema version  
- previous field structure  
- current field structure  

If differences are found:

- added fields  
- removed fields  
- renamed fields  
- changed types  
- changed constraints  

The script warns:

```
WARNING: The meaning dictionary schema has changed.
Applying the new schema will affect ALL dictionary entries.

Proceed? (y/n)
```

CSV or JSON batch-entry files **never** trigger schema change detection.  
They are validated *against* the schema, not used to define it.

---

### **4.4 Global Revalidation**

If the user chooses to proceed:

- the entire dictionary is revalidated against the new schema  
- entries requiring modification are reported  
- automatic fixes are applied where possible  
- invalid entries are rejected with detailed error messages  

This ensures the dictionary remains deterministic and consistent.

---

### **4.5 Schema Update Report**

After applying a schema update, the script generates:

```
schema_update_report.md
```

This report includes:

- summary of schema changes  
- list of affected dictionary entries  
- automatic corrections applied  
- entries requiring manual correction  
- validation results  

This provides full transparency for schema evolution.

Yes — Section 4 needs that addition, and it’s the right architectural move.  
And since I can see your **meaning_dct_spec.md** in your active tab, I’ll give you the exact text you should add, written to match the tone and structure of the existing spec.

Below is the **precise subsection** you should insert into Section 4, right after **4.1 Schema File Format** (or at the end of Section 4 if you prefer). It integrates cleanly with the rest of the document.

---

### **4.6 Missing Schema File Handling**

If the schema file:

```
system_playground/dictionaries/path_a/meaning_dictionary_schema.yaml
```

is not found when the dictionary-entry script starts, the program must:

1. **Warn the user** that the schema file is missing:

```
ERROR: meaning_dictionary_schema.yaml not found.
The meaning dictionary cannot be validated or modified without a schema.
No changes have been applied.
```

2. **Exit immediately** without performing any operations, including:
   - adding entries  
   - modifying entries  
   - deleting entries  
   - revalidating the dictionary  

3. **Guarantee safety** by ensuring:
   - no partial updates occur  
   - no dictionary corruption is possible  
   - no assumptions are made about schema structure  

The schema file is the authoritative definition of dictionary structure.  
Without it, the program cannot safely interpret or validate any dictionary entries.

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

## **7. Examples**

### **7.1 Agent Example**
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

### **7.2 Modifier Example**
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

## **8. Index Files**
The script maintains:

- alphabetical index  
- primitive → word index  
- anchor → word index  
- routing class → word index  

---

## **9. Summary**
This specification defines the complete structure, rules, and workflow for maintaining the Path A Meaning Dictionary. All dictionary entries must conform to this spec.

---
