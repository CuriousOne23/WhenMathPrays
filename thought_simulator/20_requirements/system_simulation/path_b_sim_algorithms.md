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

## 7. Operational ranges and interpretations

This section summarizes the **expected range of operation** for each metric and how to interpret **low / optimum / high** values.

### 7.1 Meaning drift `drift`

- **Range:**  
  - Theoretically:  

$$
drift \ge 0
$$

  - For Path B (by design):  

$$
drift = 0.00
$$

- **Interpretation:**  
  - **Low / Optimum:** drift = 0.00 → no semantic change (required for Path B).  
  - **High:** any drift > 0 → invariant violation; Path B must be treated as incorrect.

---

### 7.2 Surface variation entropy H

- **Range:**  

$$
0 \le H \le H\_{\max}
$$

  where $H\_{\max}$ depends on vocabulary and output length.

- **Interpretation:**  
  - **Low:** $H \approx 0.0$ → nearly identical surface forms across seeds (rigid expression).  
  - **Optimum:** moderate $H$ (e.g., 0.2–0.6 in current sims) → healthy variation with stable meaning.  
  - **High:** very large $H$ → highly unstable expression; may hurt replay/debuggability.

---

### 7.3 Plan fidelity $\text{plan\\_fidelity}$

- **Range:**  

  $$
  0 \le \text{plan\\_fidelity} \le 1
  $$

- **Interpretation:**  
  - **Low:** < 0.8 → realized output frequently deviates from planned structure.  
  - **Optimum:** $\ge 0.95$ (e.g., 0.97 in B3) → output closely follows the plan.  
  - **High (near 1.0):** ideal; plan is faithfully realized.

---

### 7.4 Step alignment ratio $\text{step\\_alignment\\_ratio}$

- **Range:**  

$$
0 \le \text{step\\_alignment\\_ratio} \le 1
$$

- **Interpretation:**  
  - **Low:** < 0.8 → step ordering/roles often misaligned.  
  - **Optimum:** $\ge 0.9$ → realized structure matches planned sequence.  
  - **High (near 1.0):** ideal; steps are correctly ordered and fulfilled.

---

### 7.5 Replay hash match rate

- **Range:**  

$$
0 \le \text{replay\_hash\_match\_rate} \le 1
$$

- **Interpretation:**  
  - **Low:** < 1.0 → nondeterminism or logging gaps; replay is not exact.  
  - **Optimum / Required:**  

$$
\text{replay\\_hash\\_match\\_rate} = 1.0
$$

    for identical inputs and seed.  
  - **High:** cannot exceed 1.0.

---

### 7.6 Tone compliance $\text{tone\\_compliance}$

- **Range:**  

$$
0 \le \text{tone\\_compliance} \le 1
$$

- **Interpretation:**  
  - **Low:** < 0.8 → tone frequently misses the target.  
  - **Optimum:** $\ge 0.95$ (e.g., 0.96 in B4) → tone closely matches requested profile.  
  - **High (near 1.0):** ideal; tone is essentially perfect.

---

### 7.7 Seed sensitivity index $\text{seed\\_sensitivity}$

- **Range:**  

$$
0 \le \text{seed\\_sensitivity}
$$

  (upper bound depends on chosen distance metric).

- **Interpretation:**  
  - **Low:** near 0.0 → almost no variation across seeds (rigid expression).  
  - **Optimum:** small‑to‑moderate values (e.g., 0.2–0.4 as in B2/B6) → healthy stylistic variation with stable meaning.  
  - **High:** very large values → expression may be too unstable; harder to reason about.

---

### 7.8 Structural divergence $\text{structural\\_divergence}$

- **Range:**  

$$
0 \le \text{structural\\_divergence} \le 1
$$

- **Interpretation:**  
  - **Low:** near 0.0 → alternative plans are structurally almost identical.  
  - **Optimum:** moderate values (e.g., $\approx 0.4–0.5$ as in B7) → genuinely different structures with identical meaning.  
  - **High:** near 1.0 → radically different structures; still acceptable if drift remains 0.0.

---

### 7.9 Output stability $\text{output\\_stability}$

- **Range:**  

$$
0 \le \text{output\\_stability} \le 1
$$

- **Interpretation:**  
  - **Low:** < 0.8 → outputs vary significantly under load; fragile behavior.  
  - **Optimum:** $\ge 0.9$ (e.g., 0.93 in B8) → stable behavior even under stress.  
  - **High (near 1.0):** ideal; highly stable realization.

---

### 7.10 Latency and memory deltas

- **Latency delta:** typically expressed as percentage change vs. baseline.

$$
\Delta\text{latency} \approx +0\% \text{ to } +10\%
$$

  - **Low / Optimum:** small positive delta (e.g., +0–5%) under stress.  
  - **Acceptable:** up to +10% in heavy B8‑style loads.  
  - **High:** larger increases suggest performance tuning needed.

- **Memory delta:** similarly, percentage change vs. baseline.

$$
\Delta\text{memory} \approx +0\% \text{ to } +10\%
$$

  - **Low / Optimum:** +0–5%.  
  - **Acceptable:** up to +10% under stress.  
  - **High:** beyond that indicates inefficient plan or realization structures.

---

# 8. Target Operating Envelope (TOE)

The **Target Operating Envelope (TOE)** defines the expected, acceptable, and optimal ranges for all Path B metrics under normal and stress conditions. These values come from the validated B‑series simulations and the architectural invariants of Path B.

This table is meant for engineers, reviewers, and implementers to quickly understand **what “good” looks like** for each metric.

---

## 8.1 Summary Table (GitHub‑safe)

| Metric | Symbol / Formula | Expected Range | Optimum | Low / Warning | High / Violation |
|--------|------------------|----------------|---------|----------------|------------------|
| Meaning Drift | $drift$ | $0.00$ | $0.00$ | Any > 0 = **violation** | Any > 0 |
| Surface Variation Entropy | $H$ | 0.1–0.6 | 0.2–0.4 | < 0.1 (too rigid) | > 0.6 (unstable) |
| Plan Fidelity | $\text{plan\\_fidelity}$ | 0.9–1.0 | ≥ 0.95 | < 0.9 | < 0.8 severe |
| Step Alignment Ratio | $\text{step\\_alignment\\_ratio}$ | 0.9–1.0 | ≥ 0.95 | < 0.9 | < 0.8 severe |
| Replay Hash Match Rate | $1.0$ | $1.0$ | $1.0$ | < 1.0 nondeterminism | < 1.0 |
| Tone Compliance | $\text{tone\\_compliance}$ | 0.9–1.0 | ≥ 0.95 | < 0.9 | < 0.8 |
| Seed Sensitivity Index | $\text{seed\\_sensitivity}$ | 0.2–0.4 | 0.25–0.35 | < 0.1 rigid | > 0.5 unstable |
| Structural Divergence | $\text{structural\\_divergence}$ | 0.3–0.6 | ≈ 0.4–0.5 | < 0.2 too similar | > 0.7 too divergent |
| Output Stability | $\text{output\\_stability}$ | 0.9–1.0 | ≥ 0.93 | < 0.9 | < 0.85 |
| Latency Delta | $\Delta\text{latency}$ | +0–10% | +0–5% | > +10% | > +15% |
| Memory Delta | $\Delta\text{memory}$ | +0–10% | +0–5% | > +10% | > +15% |

---

## 8.2 GitHub‑safe equations for each metric

### Meaning Drift

  
$$
drift = \lVert H_{\text{sem\\_before}} - H_{\text{sem\\_after}} \rVert
$$
  

Target:  
$drift = 0.00$

---

### Surface Variation Entropy

  
$$
H = - \sum_{t} p(t)\,\log_2 p(t)
$$
  

---

### Plan Fidelity

  
$$
\text{plan\\_fidelity} =
\frac{\text{matching\\_steps}}{\text{total\\_planned\\_steps}}
$$
  

---

### Step Alignment Ratio

  
$$
\text{step\\_alignment\\_ratio} =
\frac{\text{aligned\\_steps}}{\text{total\\_steps}}
$$
  

---

### Tone Compliance

  
$$
\text{tone\\_compliance} =
\cos\!\left(\vec{o},\,\vec{t}\right)
$$
  

---

### Seed Sensitivity

  
$$
\text{seed\\_sensitivity} =
\frac{2}{n(n-1)}
\sum_{i<j} d(O_i, O_j)
$$
  

---

### Structural Divergence

  
$$
\text{structural\\_divergence} \in [0,1]
$$
  

---

## 8.3 Interpretation Notes

- **Meaning drift must always be zero.**  
  Any nonzero value is a **hard invariant violation**.

- **Entropy, seed sensitivity, and structural divergence** should be **moderate**, not extreme.  
  Too low → rigid, brittle expression.  
  Too high → unstable, noisy expression.

- **Replay hash must always match.**  
  This is the core determinism guarantee.

- **Tone compliance** is a soft constraint but should remain high (≥ 0.95).

- **Latency and memory deltas** are performance indicators, not correctness indicators.  
  They matter for scaling and parallel execution.

---
