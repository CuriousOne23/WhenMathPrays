# 📘 **path_b_tp_schema.md**  
### *Canonical TP Schema for Path B (Realization Trace)*  
### *Thought Simulator — Path B Specification Layer*

---

# **1. Overview**

Path B does **not** modify meaning‑side TP fields.  
Path B writes its **realization trace** into:

```
TP.pathB.*
```

This trace is:

- append‑only  
- reference‑based  
- replayable  
- deterministic  
- small (references only)  

All heavy objects live in external logs (see `path_b_logs.md`).

---

# **2. Namespace Structure**

```
TP
 ├── message                # Path A meaning
 ├── intent
 ├── topic
 ├── tone_hint
 ├── constraints
 ├── audience
 ├── channel_hint
 ├── semantic_core_ref
 ├── pathA.*                # Path A trace
 └── pathB.*                # Path B trace (defined below)
```

---

# **3. Path B TP Schema**

Below is the **canonical** set of fields Path B writes.

Each field stores a **reference ID** pointing to a record in the Path B log store.

---

## **3.1 REx‑prm Fields**

### **`TP.pathB.rex_slice_ref`**
**Type:** `RefID`  
**Description:**  
Pointer to the expression slice extracted by REx‑prm.

**Referenced object shape (in logs):**
```
{
  intent: string,
  tone: string,
  constraints: [string],
  audience: string,
  channel: string
}
```

**Invariant:**  
- Must be written exactly once per turn.  
- Must not overwrite previous turns.

---

## **3.2 RPlan‑prm Fields**

### **`TP.pathB.rplan_candidates_ref`**
**Type:** `RefID`  
**Description:**  
Pointer to the full set of candidate realization plans.

**Referenced object shape:**
```
{
  plans: [
    {
      structure: string,
      tone: string,
      pacing: string,
      channel: string,
      constraints: [string]
    },
    ...
  ]
}
```

**Invariant:**  
- Must contain ≥ 1 plan.  
- Plans must be immutable once written.

---

## **3.3 RPU‑prm Fields**

### **`TP.pathB.rpu_selected_plan_ref`**
**Type:** `RefID`  
**Description:**  
Pointer to the final selected plan after governance + coherence adjustments.

**Referenced object shape:**
```
{
  plan: {
    structure: string,
    tone: string,
    pacing: string,
    channel: string,
    constraints: [string]
  }
}
```

---

### **`TP.pathB.rpu_adjustments_ref`**
**Type:** `RefID`  
**Description:**  
Pointer to the list of adjustments applied by RPU‑prm.

**Referenced object shape:**
```
{
  governance_adjustments: [string],
  coherence_adjustments: [string],
  style_adjustments: [string],
  timing_adjustments: [string]
}
```

**Invariant:**  
- Adjustments must be recorded even if empty.  
- Must reflect all TS‑concept decisions.

---

## **3.4 ReB‑prm Fields**

### **`TP.pathB.reb_output_ref`**
**Type:** `RefID`  
**Description:**  
Pointer to the final stabilized realization output.

**Referenced object shape:**
```
{
  final_behavior_summary: string,
  pacing: string,
  tone: string,
  channel: string
}
```

**Invariant:**  
- Must be the last Path B write for the turn.  
- Must reflect the final behavior emitted externally.

---

# **4. Field Lifecycle**

| Stage | Primitive | TP Writes | Notes |
|------|-----------|-----------|-------|
| 1 | REx‑prm | `rex_slice_ref` | Expression slice extracted |
| 2 | RPlan‑prm | `rplan_candidates_ref` | All candidate plans |
| 3 | RPU‑prm | `rpu_selected_plan_ref`, `rpu_adjustments_ref` | Final plan + adjustments |
| 4 | ReB‑prm | `reb_output_ref` | Final stabilized behavior |

---

# **5. Replay Rules**

Replay of Path B is performed by:

1. Reading `TP.pathB.rex_slice_ref`  
2. Reading `TP.pathB.rplan_candidates_ref`  
3. Reading `TP.pathB.rpu_selected_plan_ref`  
4. Reading `TP.pathB.rpu_adjustments_ref`  
5. Reading `TP.pathB.reb_output_ref`  

Replay must reconstruct:

- the expression slice  
- the candidate plans  
- the selected plan  
- the adjustments  
- the final behavior  

Replay must **not** require any LLM inference.

---

# **6. Invariants**

### **6.1 Path B never modifies Path A fields**
Meaning and realization remain strictly separated.

### **6.2 All Path B writes are references**
No large objects are stored inline in TP.

### **6.3 All Path B writes are append‑only**
No overwriting within a turn.

### **6.4 All referenced objects are immutable**
Logs are append‑only.

### **6.5 TP must remain small**
Total Path B footprint per turn: **< 200 bytes** (references only).

---

# **7. Versioning**

```
schema_version: 0.1
last_updated: 2026-06-16
author: CuriousOne (Jeff)
```

---

# **End of path_b_tp_schema.md**

---.
