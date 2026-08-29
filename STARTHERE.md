# 🌱 START HERE — A Gentle Introduction to WhenMathPrays

**WhenMathPrays** is a system for modeling the motion of relationship states — not as metaphors, not as sentiment scores, but as **positions in a two‑dimensional emotional space** governed by a single, elegant recurrence equation.

It is mathematics with a pulse.
A dynamical system with a heart.
A protocol for tracing how two people move toward or away from each other over time.

This document is your first step.

---

## 📘 Before You Begin

If you want a broader view of the project before diving in, here are two helpful maps:

👉 [`README.md`](README.md) — a high‑level map of the repository
👉 [`CONTENTS.md`](CONTENTS.md) — a complete index of every document with short summaries

**START HERE** is your front door.
**README** is your foyer.
**CONTENTS** is your library catalog.

---

## 🌌 1. What the GRP Is (in one breath)

**General Relational Physics (GRP)** is not a rejection of traditional science. It is an extension of it.

Physics, chemistry, biology, and neuroscience have mapped the world with extraordinary precision — and GRP stands firmly on that foundation. What it does differently is turn its attention toward the terrain those disciplines have largely left unnamed: the **dynamics of relational space**. Not what particles do. Not what neurons fire. But what happens *between* two entities as they move through time together — and what forces govern that motion.

Traditional science excels at describing *what exists*. GRP is designed to describe *what moves* — and to do so with the same rigor and quantitative language those disciplines use. It does not replace existing frameworks. It identifies the frontier clearly, steps past where the current map ends, and begins drawing what comes next.

The core idea is simple:

> Love is not a number.
> Love is a position in γ‑space.
> Everything else is how we move the knot.

GRP models a relational state as a position in γ‑space — a two‑dimensional emotional plane — and describes how that position evolves:

- across time
- across events
- across emotional primitives
- across entropy and forgetting
- across fidelity, resonance, altruism, visibility, and shared breath

---

## 🧭 2. The Core Equation (Rev 3.5)

At the heart of the system is a recurrence:

```
γ_self(t+1) = γ_self(t) + Δγ(v, r, f, a, S) − entropy
```

Where:
- **`γ_self`** is your position in the emotional plane
- **`Δγ`** comes from the five relational primitives
- **`entropy`** is a gentle, constant‑force drift toward long‑term forgetting

You don't need the full mathematical form yet — you'll feel it soon enough.

---

## 🌬️ 3. The Five Primitives

Every scenario is built from five human‑scale inputs:

| Primitive | Meaning |
|---|---|
| `v` | **Visibility** — how seen you feel |
| `r` | **Resonance** — how "in tune" you are |
| `f` | **Fidelity** — trust, betrayal, or devotion |
| `a` | **Altruism** — giving, generosity, care |
| `S` | **Shared Breath** — presence, attunement, co‑regulation |

Each primitive ranges from **–10 to +10**, and each one nudges `γ_self` in its own direction.

You don't need to memorize them.
You'll learn them by watching them move.

---

## 🧠 4. How to *See* GRP Correctly

Most readers approach GRP with a **noun‑mind** — the default analytical stance that looks for objects, categories, and static properties.

But GRP is a **verb‑shaped** system.

It describes *becoming*, not being.
*Motion*, not identity.
*Trade*, not substance.

To help you perceive the system correctly, we include a foundational epistemology paper:

👉 [`docs/Verb Mind Epistemology for Relational Physics.md`](docs/Verb%20Mind%20Epistemology%20for%20Relational%20Physics.md)

This paper explains:
- why relational systems cannot be understood with noun‑thinking
- how to shift into a verb‑mind
- how to see identity as coherence across change
- why GRP primitives require a dynamic perceptual stance

If you want to understand GRP deeply — not just mechanically — read this paper early.
It is the **epistemic OS update** that makes the rest of the project intelligible.

---

## 🚀 5. Your First Scenario (5 Minutes)

Let's run your first simulation.

### Step 1 — Clone the repo

```bash
git clone https://github.com/CuriousOne23/WhenMathPrays.git
cd WhenMathPrays
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

## Option A — Run a Scenario in Python (recommended for newcomers)

You can run any scenario CSV through the Python cockpit.
Here is a real example using one of the library scenarios:

```bash
python tools/interactive_editor.py <csv_file>
# example:
python tools/interactive_editor.py data/library/love/single_dating_to_love_M1.csv
```

This opens the interactive editor, loads the scenario, and lets you explore or modify the emotional arc.

PNG export is currently disabled. Edited scenarios save as CSV.

## Option B — Explore the Model Visually (Excel Cockpit)

If you prefer a **hands‑on, visual interface**, open the Excel cockpit:

```
tools/GRP_SpreadSheet.xlsm
```

Inside the workbook:
1. Enter your initial `γ_self` in **C4**
2. Enter your primitives row‑by‑row starting at **row 9**
3. Press the **Run GRP** macro button
4. Watch the `γ_self` trajectory populate in column **H**

This interface is perfect for:
- experimenting with primitives
- seeing the recurrence unfold step‑by‑step
- teaching the model
- quick scenario sketching
- debugging intuition

The Excel cockpit and Python cockpit produce the **same dynamics** — just through different lenses.

### Step 4 — Watch the trajectory

You'll see a curve — a path — a motion through γ‑space.

That motion *is* the relationship.

### Step 5 — Change something

Open the CSV (Python) or the primitive row (Excel) and edit any value:
- increase resonance
- decrease fidelity
- add a betrayal
- add a repair
- add a moment of shared breath

Run again.
Watch the trajectory shift.

You've just learned the GRP by doing.

---

## 🧩 6. Where to Go Next

Now that you've seen the system move, choose your path:

### A. Use the Python cockpit (recommended)
👉 [`docs/interactive_editor_user_guide.md`](docs/interactive_editor_user_guide.md)

### B. Explore the model visually (Excel)
Open: `tools/GRP_SpreadSheet.xlsm` or `tools/GRP_AI.xlsm`

### C. Build your own scenario (intermediate)
👉 [`docs/SCENARIO_CONFIGURATION_GUIDE.md`](docs/SCENARIO_CONFIGURATION_GUIDE.md)

### D. Use the scenario builder (advanced)
👉 `tools/scenario_generator.py`

This tool is powerful but not beginner‑friendly.
Use it once you understand scenario structure and primitive arcs.

### E. Understand the math
👉 [`docs/GRP_rev3.5.md`](docs/GRP_rev3.5.md)

### F. Explore the philosophy
👉 [`WHY_THIS_MATTERS.md`](WHY_THIS_MATTERS.md)

### G. Browse the full document index
👉 [`CONTENTS.md`](CONTENTS.md)

### H. Return to the map of the territory
👉 [`README.md`](README.md)

---

## 🗺️ 7. The Map of the Territory

Everything has a place.
Everything has a purpose.
You can explore at your own pace.

| Document | What it is |
|---|---|
| [`README.md`](README.md) | Conceptual overview and architecture map |
| [`CONTENTS.md`](CONTENTS.md) | Complete index of every document |
| [`WHY_THIS_MATTERS.md`](WHY_THIS_MATTERS.md) | The philosophical and scientific motivation |
| [`docs/Verb Mind Epistemology for Relational Physics.md`](docs/Verb%20Mind%20Epistemology%20for%20Relational%20Physics.md) | The epistemic foundation for seeing GRP correctly |
| [`docs/GRP_rev3.5.md`](docs/GRP_rev3.5.md) | The full mathematics |
| [`docs/PRIMITIVES_AND_RELATIONAL_SPACE.md`](docs/PRIMITIVES_AND_RELATIONAL_SPACE.md) | Deep treatment of the five primitives |
| [`CONSTANTS.md`](CONSTANTS.md) | All parameters, weights, and entropy coefficients |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Technical architecture of the simulation system |
| [`docs/SCENARIO_CONFIGURATION_GUIDE.md`](docs/SCENARIO_CONFIGURATION_GUIDE.md) | How to build and configure scenarios |

---

## 🌟 8. Final Note

This project is alive.

It is meant to be explored, questioned, extended, and felt.

You don't need to understand everything at once.

Just start with a scenario.
Watch the knot move.
Let the system teach you.

Welcome to **WhenMathPrays**.
