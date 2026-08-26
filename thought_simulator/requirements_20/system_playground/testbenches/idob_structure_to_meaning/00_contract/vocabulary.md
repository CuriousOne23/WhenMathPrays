# IdOB vocabulary (this bench revision)

One-line definitions. Official names preferred.

## Structure (meaning-blind)

| Name | Job |
|------|-----|
| `semantic_field_id` | Which semantic field the geometry sits in |
| `semantic_role_id` | Role in that field |
| `semantic_object_id` | Object slot in the geometry |
| `gradient_id` | Dynamic / gradient class of the geometry |
| `universe_id` | Which universe the geometry is drawn from |
| `subfield_id` | Subfield inside the field |
| `structural_hash` / `structural_key` | Fingerprint of the six IDs only |
| `residue_hash` / `residue_code` | Constraint-tension fingerprint; still not meaning |
| `routing_signature` | `struct_hash` + feature hashes for routing / ranking signals |
| `identity_metadata` | Tags/vector adjacent to structure; not baked into the hash |

## Meaning groups and six fields

| Name | Job |
|------|-----|
| `group_id` | Stable id of a meaning group |
| `group_name` | Human label (e.g. ACTION.physical.motion) |
| `primitive` | ENTITY / ACTION / EVENT / STATE / QUALITY / ... |
| `group_dimensions` | Prototype six-vector for the group |
| `physicality` | How much the meaning is physical object/action |
| `sociality` | Social / interpersonal weight |
| `temporality` | Time / event / change weight |
| `intentionality` | Agency / purpose weight |
| `materiality` | Matter / transformation weight |
| `spatiality` | Place / path / geometry weight |
| `meaning_semantics` | IdOB current six-vector M |

## Identity and search

| Name | Job |
|------|-----|
| `identity_envelope` / CIE | Local conversational identity of this utterance |
| `identity_importance` / `alpha` | How hard CIE pushes M |
| `identity_tags` | Coarse stance tags (e.g. physical, scientific) |
| `identity_vector` | Numeric identity pressure used in M' = M + alpha I |
| `identity_delta` | Change in identity vector across cycles |
| `meaning_delta_h` | ||M_i - M_{i-1}|| |
| `idob_search_budget_min` / `max` | Cycle bounds (4-6 in the papers) |
| `resolution_status` | Why the run froze |
| `ready_for_ouba` | Handoff flag; this bench stops here |

## Stop reasons (must match the actual halt)

- `stable` — meaning delta below epsilon
- `identity_stable` — identity delta below epsilon first
- `budget_exhausted` — max cycles hit
- `time_exhausted` — supervisor forced stop

A packet that says `stable` when the halt was budget is an instrument error.

---

# 📘 **Appendix A — Clarifying Questions for Slide 00_contract (Q&A with Examples + 2D Tables)**

This appendix collects foundational questions asked during the 00_contract learning walk and provides precise, field‑name‑level answers aligned with the IdOB vocabulary definitions in this bench revision.  
Examples and 2D tables are included to make the concepts concrete.

---

## **Q1 — What are the three major categories of an IdOB packet?**

**A:** IdOB packets contain three distinct categories:

### **1. Structure (meaning‑blind)**  
Fields:  
`semantic_field_id`, `semantic_role_id`, `semantic_object_id`,  
`gradient_id`, `universe_id`, `subfield_id`,  
`structural_hash`, `residue_hash`, `routing_signature`, `identity_metadata`

**Example:**  
For **“Henry fixed the Craftsman table in New York.”**  
- `semantic_field_id = ACTION.repair`  
- `semantic_role_id = agent/patient/location`  
- `semantic_object_id = object.table`  
- `gradient_id = physical_action`  
- `universe_id = everyday_tasks`  

---

### **2. Meaning groups and six fields**  
Fields:  
`group_id`, `group_name`, `primitive`, `group_dimensions`,  
`physicality`, `sociality`, `temporality`, `intentionality`, `materiality`, `spatiality`,  
`meaning_semantics`

**Example:**  
Meaning groups:  
- PERSON → “Henry”  
- OBJECT → “Craftsman table”  
- LOCATION → “New York”

---

### **3. Identity and search**  
Fields:  
`identity_envelope`, `identity_importance`, `identity_tags`,  
`identity_vector`, `identity_delta`, `meaning_delta_h`,  
`idob_search_budget_min/max`, `resolution_status`, `ready_for_ouba`

**Example:**  
Identity may apply tags like:  
- `identity_tags = ["repair","task"]`

---

## **Q2 — What exactly are the six meaning fields?**

**A:**  
`physicality`, `sociality`, `temporality`, `intentionality`, `materiality`, `spatiality`

**Example:**  
For “Craftsman table”:  
- `physicality = high`  
- `materiality = high`  

For “Henry”:  
- `sociality = high`  
- `intentionality = high`

---

## **Q3 — Where do literal names like “Henry”, “Ann”, “New York”, “Craftsman” go?**

**A:**  
Literal names appear **only** in:

- `meaning_semantics`

They do **not** appear in:

- `group_id`, `group_name`, `primitive`, `group_dimensions`

**Example:**  
`meaning_semantics = "Henry"`  
`meaning_semantics = "New York"`

---

## **Q4 — Do names ever appear in Structure?**

**A:** No.  
Structure is meaning‑blind.

**Example:**  
Structure records:  
- `semantic_role_id = agent`  
not `"Henry"`.

---

## **Q5 — Do names ever appear in Identity?**

**A:** No.  
Identity modifies meaning but does not contain names.

**Example:**  
Identity may contain:  
- `identity_tags = ["repair"]`  
but never `"Henry"`.

---

## **Q6 — When Path A receives a user message, is it trying to fill all fields in all three categories?**

**A:** Yes.  
Path A populates:

- Structure fields  
- Meaning fields  
- Identity fields  

**Example:**  
For “Henry fixed the Craftsman table in New York,” Path A fills:

- Structure → ACTION.repair  
- Meaning → PERSON, OBJECT, LOCATION rows  
- Identity → stance tags like “repair”, “task”

---

## **Q7 — In the Meaning table, are all columns describing observations about the same object?**

**A:** Yes.  
Each row = one meaning group.  
Each column = one observation about that group.

**Example:**  
Row for “New York”:  
- `group_id = LOCATION`  
- `spatiality = very high`  
- `meaning_semantics = "New York"`

---

## **Q8 — Do Structure and Identity also have 2D tables?**

**A:** Yes, but with different shapes:

- **Structure:** 1 row  
- **Identity:** 1 row  
- **Meaning:** multiple rows  

---

## **Q9 — What is `universe_id`?**

**A:**  
`universe_id` identifies the **universe of discourse** for the structure.  
It contains no meaning.

**Example:**  
`universe_id = everyday_tasks`

---

# 🟦 **Structure Table (1 row)**

```
+------------------------+---------------------------+------------------------+--------------+--------------+--------------+------------------+----------------+
| semantic_field_id      | semantic_role_id          | semantic_object_id     | gradient_id  | universe_id  | subfield_id  | structural_hash  | residue_hash   |
+------------------------+---------------------------+------------------------+--------------+--------------+--------------+------------------+----------------+
| ACTION.repair          | agent/patient/location    | object.table           | physical_act | everyday     | tasks        | <hash>           | <hash>         |
+------------------------+---------------------------+------------------------+--------------+--------------+--------------+------------------+----------------+
```

---

# 🟩 **Meaning Table (multi‑row)**

```
+----------------+---------------------------+-----------+--------------------+-------------+-----------+-------------+----------------+-------------+-----------+----------------------+
| group_id       | group_name                | primitive | group_dimensions   | physicality | sociality | temporality | intentionality | materiality | spatiality | meaning_semantics     |
+----------------+---------------------------+-----------+--------------------+-------------+-----------+-------------+----------------+-------------+-----------+----------------------+
| PERSON         | ENTITY.person.human       | ENTITY    | <proto six-vector> | high        | high      | present     | high           | low         | medium    | "Henry"              |
+----------------+---------------------------+-----------+--------------------+-------------+-----------+-------------+----------------+-------------+-----------+----------------------+
| OBJECT         | OBJECT.furniture.table    | OBJECT    | <proto six-vector> | high        | low       | neutral     | none           | high        | medium    | "Craftsman table"    |
+----------------+---------------------------+-----------+--------------------+-------------+-----------+-------------+----------------+-------------+-----------+----------------------+
| LOCATION       | LOCATION.city             | LOCATION  | <proto six-vector> | high        | medium    | present     | low            | low         | very high | "New York"           |
+----------------+---------------------------+-----------+--------------------+-------------+-----------+-------------+----------------+-------------+-----------+----------------------+
```

---

# 🟥 **Identity Table (1 row)**

```
+----------------------+------------------------+------------------+----------------+------------------+-------------------+---------------------+----------------------+
| identity_envelope    | identity_importance    | identity_tags    | identity_vector | identity_delta   | meaning_delta_h   | resolution_status   | ready_for_ouba       |
+----------------------+------------------------+------------------+----------------+------------------+-------------------+---------------------+----------------------+
| <envelope>           | <alpha>                | ["repair","task"]| <vector>        | <delta>          | <delta_h>         | stable              | true                 |
+----------------------+------------------------+------------------+----------------+------------------+-------------------+---------------------+----------------------+
```

---

# 📘 **Appendix A Complete**

