# 📘 path_b_appendix.md  
### Path B Operational Examples (Replay‑Accurate, TP‑Accurate, Log‑Accurate)

This appendix shows **exact, concrete, low‑level examples** of Path B execution.

Each example includes:

- **TP Before** (Path A output only)  
- **Primitive Operation**  
- **Log Entry Written**  
- **TP After** (Path B reference fields added)  
- **Object Passed Forward**  

This appendix is the *runtime‑accurate* version of Path B behavior.

---

# A.1 Primitive Examples (Replay‑Accurate)

---

## A.1.1 — REx‑prm Example (Expression Extractor)

### **TP Before (Path A output only)**

```json
{
  "message": { "meaning": "Explain Bayesian updating" },
  "intent": "explain",
  "topic": "Bayesian updating",
  "tone_hint": "gentle",
  "constraints": ["avoid equations"],
  "audience": "non-technical",
  "channel_hint": "text",
  "semantic_core_ref": "<id1>",
  "pathB": {}
}
```

---

### **Operation**

REx reads Path A fields and extracts the **expression slice**:

- intent → "simple explanation"  
- tone → "gentle"  
- constraints → ["avoid equations"]  
- audience → "non-technical"  
- channel → "text"  

---

### **Log Entry Written**

```
rex_slice_log[id2] = {
  "intent": "simple explanation",
  "tone": "gentle",
  "constraints": ["avoid equations"],
  "audience": "non-technical",
  "channel": "text"
}
```

---

### **TP After**

```json
{
  "pathB": {
    "rex_slice_ref": "id2"
  }
}
```

---

### **Object Passed Forward (RP‑ref)**

```json
{
  "intent": "simple explanation",
  "tone": "gentle",
  "constraints": ["avoid equations"],
  "audience": "non-technical",
  "channel": "text"
}
```

---

## A.1.2 — RPlan‑prm Example (Realization Planner)

### **TP Before**

```json
{
  "pathB": {
    "rex_slice_ref": "id2"
  }
}
```

---

### **Operation**

RPlan generates **candidate plans**:

- Plan A: 3‑sentence analogy  
- Plan B: bullet‑point explanation  
- Plan C: short story‑based explanation  

---

### **Log Entry Written**

```
rplan_candidates_log[id3] = {
  "plans": [
    {
      "structure": "3-sentence analogy",
      "tone": "gentle",
      "pacing": "short",
      "channel": "text",
      "constraints": ["avoid equations"]
    },
    {
      "structure": "bullet explanation",
      "tone": "gentle",
      "pacing": "medium",
      "channel": "text",
      "constraints": ["avoid equations"]
    },
    {
      "structure": "story-based explanation",
      "tone": "gentle",
      "pacing": "medium",
      "channel": "text",
      "constraints": ["avoid equations"]
    }
  ]
}
```

---

### **TP After**

```json
{
  "pathB": {
    "rex_slice_ref": "id2",
    "rplan_candidates_ref": "id3"
  }
}
```

---

### **Object Passed Forward (RPlan‑ref)**

```json
{
  "plans": [
    { "structure": "3-sentence analogy", ... },
    { "structure": "bullet explanation", ... },
    { "structure": "story-based explanation", ... }
  ]
}
```

---

## A.1.3 — RPU‑prm Example (Realization Plan Updater)

### **TP Before**

```json
{
  "pathB": {
    "rex_slice_ref": "id2",
    "rplan_candidates_ref": "id3"
  }
}
```

---

### **Operation**

RPU applies:

- governance rules  
- coherence rules  
- style adjustments  
- timing adjustments  

RPU selects **Plan A** and applies adjustments:

- softened transitions  
- removed jargon  
- ensured gentle tone  

---

### **Log Entries Written**

#### Selected Plan

```
rpu_selected_plan_log[id4] = {
  "plan": {
    "structure": "3-sentence analogy",
    "tone": "gentle",
    "pacing": "smooth",
    "channel": "text",
    "constraints": ["avoid equations"]
  }
}
```

#### Adjustments

```
rpu_adjustments_log[id5] = {
  "governance_adjustments": ["removed jargon"],
  "coherence_adjustments": ["aligned tone with history"],
  "style_adjustments": ["softened transitions"],
  "timing_adjustments": ["smoothed pacing"]
}
```

---

### **TP After**

```json
{
  "pathB": {
    "rex_slice_ref": "id2",
    "rplan_candidates_ref": "id3",
    "rpu_selected_plan_ref": "id4",
    "rpu_adjustments_ref": "id5"
  }
}
```

---

### **Object Passed Forward**

```json
{
  "plan": {
    "structure": "3-sentence analogy",
    "tone": "gentle",
    "pacing": "smooth",
    "channel": "text",
    "constraints": ["avoid equations"]
  }
}
```

---

## A.1.4 — ReB‑prm Example (Realization Basin)

### **TP Before**

```json
{
  "pathB": {
    "rpu_selected_plan_ref": "id4",
    "rpu_adjustments_ref": "id5"
  }
}
```

---

### **Operation**

ReB stabilizes:

- pacing  
- tone  
- flow  
- channel formatting  

---

### **Log Entry Written**

```
reb_output_log[id6] = {
  "final_behavior_summary": "gentle 3-sentence analogy explaining Bayesian updating",
  "pacing": "smooth",
  "tone": "gentle",
  "channel": "text"
}
```

---

### **TP After**

```json
{
  "pathB": {
    "rex_slice_ref": "id2",
    "rplan_candidates_ref": "id3",
    "rpu_selected_plan_ref": "id4",
    "rpu_adjustments_ref": "id5",
    "reb_output_ref": "id6"
  }
}
```

---

### **External Output**

A gentle, smooth, 3‑sentence analogy explaining Bayesian updating.

---

# A.2 Process Examples (Replay‑Accurate)

These examples show **process‑level** Path B behavior using the same TP/log model.

---

## A.2.1 — RPlan‑prc Example

### Input  
Expression slice: “formal tone, long answer allowed.”

### Operation  
RPlan‑prc generates:

- structured essay  
- step‑by‑step explanation  
- definition‑first plan  

### Output  
Written to `rplan_candidates_log[idX]`.

---

## A.2.2 — RSelect‑prc Example

### Input  
Two candidate plans:

- Plan A: neutral tone  
- Plan B: warm tone  

### Operation  
User emotional state = “anxious.”  
Warm tone preferred.

### Output  
Selected plan → `rpu_selected_plan_log[idY]`.

---

## A.2.3 — RStyle‑prc Example

### Input  
Plan: neutral tone.

### Operation  
User preference: “encouraging tone.”

### Output  
Style adjustments → `rpu_adjustments_log[idZ]`.

---

## A.2.4 — RTiming‑prc Example

### Input  
Plan: long paragraph.

### Operation  
RTiming‑prc transforms:

- long paragraph → 3 short paragraphs  

### Output  
Timing adjustments → `rpu_adjustments_log[idZ2]`.

---

## A.2.5 — RChannel‑prc Example

### Input  
Plan includes visual metaphors.

### Operation  
Channel = text‑only.

### Output  
Channel‑appropriate plan → `rpu_selected_plan_log[idZ3]`.

---

# A.3 Reference Object Examples

These examples show the **actual shapes** of Path B reference objects.

---

## A.3.1 — RP‑ref Example

```json
{
  "intent": "simple explanation",
  "tone": "gentle",
  "constraints": ["avoid equations"],
  "audience": "non-technical",
  "channel": "text"
}
```

---

## A.3.2 — RPlan‑ref Example

```json
{
  "plans": [
    { "structure": "3-sentence analogy", ... },
    { "structure": "bullet explanation", ... }
  ]
}
```

---

## A.3.3 — RStyle‑ref Example

```json
{
  "tone": "gentle",
  "warmth": 0.7,
  "formality": "low"
}
```

---

## A.3.4 — RTiming‑ref Example

```json
{
  "sentence_length": "short",
  "pause_density": "low"
}
```

---

## A.3.5 — RChannel‑ref Example

```json
{
  "channel": "text",
  "multimodal": false
}
```

---

# A.4 TS‑Concept Examples

These examples show how TS‑concepts influence Path B logs.

---

## A.4.1 — BC‑tsc Example (Behavioral Coherence)

Plan uses humor.  
User is grieving.  
BC‑tsc rejects humor.

→ RPU adjustments log records: `"removed humor"`.

---

## A.4.2 — SC‑tsc Example (Style Coherence)

Plan tone = neutral.  
History tone = warm.

→ RPU adjustments log records: `"aligned tone with history"`.

---

## A.4.3 — TC‑tsc Example (Timing Coherence)

Plan pacing = abrupt.

→ RPU adjustments log records: `"smoothed pacing"`.

---

## A.4.4 — CC‑tsc Example (Channel Coherence)

Plan includes visual references.  
Channel = text‑only.

→ RPU adjustments log records: `"removed visual metaphors"`.

---

# End of path_b_appendix.md
```

---
