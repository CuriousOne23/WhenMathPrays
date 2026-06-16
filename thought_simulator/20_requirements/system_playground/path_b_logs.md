# 📘 **path_b_logs.md**  
### *Canonical Log Stores for Path B (Realization Trace Storage)*  
### *Thought Simulator — Path B Specification Layer*

---

# **1. Overview**

Path B primitives do **not** store large objects directly in the TP.  
Instead, they write **references** into:

```
TP.pathB.*
```

Each reference points to a record in one of the **Path B log stores** defined here.

These logs are:

- append‑only  
- immutable  
- small  
- replayable  
- deterministic  
- DRAM‑resident (fast)  

This file defines the **shape**, **invariants**, and **usage** of each log.

---

# **2. Log Store Architecture**

All Path B logs follow the same pattern:

```
<log_name>[RefID] = <immutable_record>
```

Where:

- **RefID** is a small integer or UUID  
- **immutable_record** is a small JSON‑like object  
- logs never delete or mutate entries  
- logs are append‑only  

This ensures:

- full replayability  
- deterministic reconstruction  
- low memory footprint  
- clean separation of meaning vs. realization  

---

# **3. Log Stores**

Below are the canonical Path B logs.

---

# **3.1 REx Slice Log**

### **Name:** `rex_slice_log`  
### **Written by:** `REx‑prm`  
### **Referenced by:** `TP.pathB.rex_slice_ref`

### **Record Shape**
```
{
  intent: string,            # e.g., "simple explanation"
  tone: string,              # e.g., "gentle"
  constraints: [string],     # e.g., ["avoid equations"]
  audience: string,          # e.g., "non-technical"
  channel: string            # e.g., "text"
}
```

### **Invariants**
- Must be written exactly once per turn.
- Must reflect only expression‑relevant fields.
- Must not contain meaning‑side fields (Path A domain).

---

# **3.2 RPlan Candidate Log**

### **Name:** `rplan_candidates_log`  
### **Written by:** `RPlan‑prm`  
### **Referenced by:** `TP.pathB.rplan_candidates_ref`

### **Record Shape**
```
{
  plans: [
    {
      structure: string,     # e.g., "3-sentence analogy"
      tone: string,          # e.g., "gentle"
      pacing: string,        # e.g., "short"
      channel: string,       # e.g., "text"
      constraints: [string]  # inherited from REx slice
    },
    ...
  ]
}
```

### **Invariants**
- Must contain ≥ 1 plan.
- Plans must be immutable once written.
- Plans must be realizable by ReB‑prm.

---

# **3.3 RPlan Metadata Log (Optional)**

### **Name:** `rplan_metadata_log`  
### **Written by:** `RPlan‑prm`  
### **Referenced by:** (optional future field)

### **Record Shape**
```
{
  generation_method: string,   # e.g., "template", "heuristic"
  scoring_method: string,      # e.g., "coherence-first"
  notes: [string]              # developer/debug notes
}
```

### **Invariants**
- Optional in v0.1.
- Useful for debugging and replay introspection.

---

# **3.4 RPU Selected Plan Log**

### **Name:** `rpu_selected_plan_log`  
### **Written by:** `RPU‑prm`  
### **Referenced by:** `TP.pathB.rpu_selected_plan_ref`

### **Record Shape**
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

### **Invariants**
- Must reflect the final plan after all adjustments.
- Must be consistent with RPU adjustments log.

---

# **3.5 RPU Adjustments Log**

### **Name:** `rpu_adjustments_log`  
### **Written by:** `RPU‑prm`  
### **Referenced by:** `TP.pathB.rpu_adjustments_ref`

### **Record Shape**
```
{
  governance_adjustments: [string],   # e.g., ["removed jargon"]
  coherence_adjustments: [string],    # e.g., ["aligned tone with history"]
  style_adjustments: [string],        # e.g., ["increased warmth"]
  timing_adjustments: [string]        # e.g., ["shortened sentences"]
}
```

### **Invariants**
- Must record all adjustments, even if empty.
- Must reflect TS‑concept decisions.

---

# **3.6 ReB Output Log**

### **Name:** `reb_output_log`  
### **Written by:** `ReB‑prm`  
### **Referenced by:** `TP.pathB.reb_output_ref`

### **Record Shape**
```
{
  final_behavior_summary: string,   # e.g., "gentle 3-sentence analogy"
  pacing: string,                   # e.g., "smooth"
  tone: string,                     # e.g., "gentle"
  channel: string                   # e.g., "text"
}
```

### **Invariants**
- Must be the last Path B write for the turn.
- Must reflect the final external behavior.

---

# **4. Replay Rules**

Replay reconstructs Path B by reading logs in this order:

1. `rex_slice_log[TP.pathB.rex_slice_ref]`  
2. `rplan_candidates_log[TP.pathB.rplan_candidates_ref]`  
3. `rpu_selected_plan_log[TP.pathB.rpu_selected_plan_ref]`  
4. `rpu_adjustments_log[TP.pathB.rpu_adjustments_ref]`  
5. `reb_output_log[TP.pathB.reb_output_ref]`  

Replay must:

- require no LLM inference  
- be deterministic  
- reconstruct the entire realization pipeline  

---

# **5. Memory Footprint**

Typical record sizes:

- REx slice: **200–400 bytes**  
- RPlan candidates: **1–3 KB**  
- RPU selected plan: **200–400 bytes**  
- RPU adjustments: **200–500 bytes**  
- ReB output: **200–400 bytes**

Total per turn: **~7–13 KB** (15–25 KB worst case)

This is trivial for DRAM.

---

# **6. Versioning**

```
schema_version: 0.1
last_updated: 2026-06-16
author: CuriousOne (Jeff)
```

---

# **End of path_b_logs.md**

---
