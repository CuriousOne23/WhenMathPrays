# Path B Realization Algorithms Specification  
**GitHub‑Friendly Math Version**

**Document:** `path_b_algorithms.md`  
**Project:** Thought Simulator (WhenMathPrays)  
**Version:** 1.0  
**Purpose:** Provide engineers with precise, implementable algorithms for Path B primitives, including variables, constants, and formulas used in the validated simulation suite.

---

## 1. Core Principles

- Path B is **read‑only** on the semantic core (`TP` / `MTP`).  
- All operations are deterministic under fixed seed.  
- No semantic mutation, no meaning invention.  
- Constraints bind at the **plan level**, not token level.  
- Full replay support via structured logs.

---

## 2. Primitives

### 2.1 REx‑prm (Realization Extractor)

**Input:** `TP` state  
**Output:** expression slice (`ex_slice`)  
**Rule:** Extract expression‑relevant fields only; never modify `TP`.

```python
def rex_prm(tp_state):
    ex_slice = {
        "intent": tp_state.get("intent"),
        "tone_hint": tp_state.get("tone_hint"),
        "constraints": tp_state.get("constraints", []),
        "audience": tp_state.get("audience"),
        "channel": tp_state.get("channel"),
        "register": tp_state.get("register"),
        "length_hint": tp_state.get("length_hint"),
    }
    log("rex_slice_log", ex_slice)
    return ex_slice
```

---

### 2.2 RPlan‑prm (Plan Constructor)

**Input:** `ex_slice`  
**Output:** list of candidate plans  
**Rule:** Generate structurally valid plans respecting constraints.

```python
def rplan_prm(ex_slice):
    candidates = []
    for template in PLAN_TEMPLATES:
        if template.supports_channel(ex_slice["channel"]):
            plan = template.instantiate(ex_slice)
            candidates.append(plan)
    log("rplan_candidates_log", candidates)
    return candidates
```

---

### 2.3 RPU‑prm (Realization Plan Updater)

**Input:** candidate plans + governance rules  
**Output:** selected and adjusted plan  
**Rule:** Deterministic selection + constraint enforcement.

```python
def rpu_prm(candidates, governance):
    scored = []
    for plan in candidates:
        score = score_plan(plan, governance)
        scored.append((score, plan))

    scored.sort(key=lambda sp: (-sp[0], sp[1]["id"]))
    selected_score, selected_plan = scored[0]

    adjusted_plan, adjustments = apply_style_timing_channel(
        selected_plan, governance
    )

    log("rpu_selected_plan_log", {"id": selected_plan["id"], "score": selected_score})
    log("rpu_adjustments_log", adjustments)

    return adjusted_plan
```

---

### 2.4 ReB‑prm (Realization Basin / Output Binder)

**Input:** finalized plan  
**Output:** stabilized external behavior  
**Rule:** Realize deterministically, smooth pacing/tone, compute replay hash.

```python
def reb_prm(final_plan, seed):
    rng = DeterministicRNG(seed)
    realized_steps = []

    for step in final_plan["steps"]:
        text = realize_step(step, final_plan["style_profile"], rng)
        realized_steps.append({"step_id": step["id"], "text": text})

    output = join_steps(realized_steps, final_plan["channel"])

    log("reb_output_log", {
        "final_plan_id": final_plan["id"],
        "realized_steps": realized_steps,
        "output": output,
        "seed": seed,
    })

    return output
```

---

## 3. Variables, Constants & Formulas  
All formulas below are now in **GitHub‑friendly math formatting**.

---

### 3.1 Meaning Drift

Inline form: `$drift = 0.00$`

Block form:

  
$$
drift = \lVert H_{\text{sem\\_before}} - H_{\text{sem\\_after}} \rVert
$$
  

Where:

- $H_\text{sem\\_before}$ = semantic hash of TP before Path B  
- $H_\text{sem\\_after}$ = semantic hash after Path B (should be identical)

---

### 3.2 Surface Variation Entropy

Inline: $H = -\sum p(t)\log_2 p(t)$

  
$$
H = - \sum_{t} p(t)\,\log_2 p(t)
$$
  

Where $p(t)$ is token frequency across outputs from different seeds.

---

### 3.3 Plan Fidelity

  
$$
\text{plan\\_fidelity} = 
\frac{\text{matching\\_steps}}{\text{total\\_planned\\_steps}}
$$
  

---

### 3.4 Step Alignment Ratio

  
$$
\text{step\\_alignment\\_ratio} =
\frac{\text{aligned\\_steps}}{\text{total\\_steps}}
$$
  

---

### 3.5 Replay Hash

Inline: $replay\\_hash = hash(\text{canonical\\_payload})$

  
$$
replay\\_hash = \text{Hash}\left(
\text{serialize}\_{\text{stable}}(payload)
\right)
$$
  

Where `payload` includes all logs + output + seed.

---

### 3.6 Tone Compliance

  
$$
\text{tone\\_compliance} = 
\cos(\vec{o}, \vec{t})
$$
  

Where:

- $\vec{o}$ = embedding of output  
- $\vec{t}$ = embedding of tone exemplar  

Or rule‑based equivalent.

---

### 3.7 Seed Sensitivity Index

  
$$
\text{seed\\_sensitivity} =
\frac{2}{n(n-1)}
\sum_{i<j} d(O_i, O_j)
$$
  

Where $d$ is token‑ or embedding‑distance.

---

### 3.8 Structural Divergence

  
$$
\text{structural\\_divergence} \in [0,1]
$$
  

Computed via normalized structural difference between two valid plans.

---

## 4. Execution Flow

```
TP/MTP (read-only)
    ↓ REx-prm
    ↓ RPlan-prm
    ↓ RPU-prm
    ↓ ReB-prm
→ External Output
```

Invariants checked at each boundary.

---

## 5. Determinism & Purity Rules

- $seed$ fixed ⇒ identical output  
- No writes to $TP$ or $MTP$  
- Randomness bounded to expression layer  
- Drift invariant: $drift = 0.00$  
- Replay invariant: $replay\\_hash$ stable  

---

## 6. Implementation Guidance

- Use immutable structures for `TP`, `ex_slice`, and `Plan`.  
- Log every primitive with stable IDs.  
- Enforce constraints at plan level.  
- On failure: return structured failure state, never degrade silently.  
- Test replay by running same seed twice and comparing logs + output.

---
