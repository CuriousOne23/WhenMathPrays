# WhenMathPrays

> *Mathematics with a pulse. A dynamical system with a heart.*

**WhenMathPrays** is a framework for modeling the motion of relationship states — not as metaphors or sentiment scores, but as positions in a two-dimensional emotional space governed by a single, elegant recurrence equation. It is a protocol for tracing how two people (or two perspectives on one person) move toward or away from each other over time.

This is not a mood tracker. It is not a personality model. It is a **dynamical system** — one that asks: *given who we are and what has happened between us, where are we now, and where are we headed?*

---

## 🗺️ How to Navigate This Repository

Three documents serve as your entry points, each at a different level of depth:

| Document | Role | Start here if… |
|---|---|---|
| [`STARTHERE.md`](STARTHERE.md) | **Front door** — a gentle, hands-on introduction | You are new to the project |
| [`README.md`](README.md) *(this file)* | **Foyer** — a conceptual map of the territory | You want a structured overview before diving in |
| [`CONTENTS.md`](CONTENTS.md) | **Library catalog** — a complete index of every document | You are looking for a specific file or reference |

**Recommended reading order for evaluators and researchers:**
1. This README (conceptual framing)
2. [`WHY_THIS_MATTERS.md`](WHY_THIS_MATTERS.md) (philosophical motivation)
3. [`docs/Verb Mind Epistemology for Relational Physics.md`](docs/Verb%20Mind%20Epistemology%20for%20Relational%20Physics.md) (epistemic foundation)
4. [`docs/GRP_rev3.5.md`](docs/GRP_rev3.5.md) (the mathematics)
5. [`STARTHERE.md`](STARTHERE.md) (hands-on engagement with the system)

---

## 🌌 What Is the GRP?

**General Relational Physics (GRP)** is not a rejection of traditional science. It is an extension of it.

Classical physics, chemistry, biology, and neuroscience have mapped the world with extraordinary precision — and GRP stands firmly on that foundation. What it does differently is turn its attention toward the terrain those disciplines have largely left unnamed: the **dynamics of relational space**. Not what particles do. Not what neurons fire. But what happens *between* two entities as they move through time together — and what forces govern that motion.

Traditional science excels at describing *what exists*. GRP is designed to describe *what moves* — and to give researchers a rigorous, quantitative language for a domain where such language has been conspicuously absent. It does not replace existing frameworks. It identifies the frontier clearly, steps past where the current map ends, and begins drawing what comes next.

The result is a model that treats relationship not as a category or a state, but as a **trajectory in γ-space** — a two-dimensional emotional plane governed by a recurrence equation that is as precise as it is human-legible.

### The Core Equation (Rev 3.5)

At the heart of the system is a recurrence relation:

```
γ_self(t+1) = γ_self(t) + Δγ(v, r, f, a, S) − entropy
```

Where:
- **`γ_self`** is your current position in the relational plane
- **`Δγ`** is the net displacement contributed by the five relational primitives
- **`entropy`** is a gentle, constant-force drift representing forgetting and natural decay over time

The trajectory of `γ_self` across a scenario *is* the relationship. Every inflection point is an event. Every plateau is a period of stasis. Every divergence is a rupture.

### The Five Relational Primitives

Every scenario is built from five inputs, each ranging from **−10 to +10**:

| Symbol | Primitive | What it measures |
|---|---|---|
| `v` | **Visibility** | How seen, recognized, and acknowledged you feel |
| `r` | **Resonance** | How "in tune" or harmonically matched you feel with the other |
| `f` | **Fidelity** | Trust, devotion, or betrayal — the integrity of the bond |
| `a` | **Altruism** | Giving, generosity, and care directed toward the other |
| `S` | **Shared Breath** | Presence, attunement, and co-regulation — the felt sense of being together |

These are not abstract variables. They are distillations of the forces that actually move people toward or away from each other. The model works because the primitives are human-legible: you can describe any relational event in their terms.

---

## 🧭 GRP and the Scientific Frontier

Science does not advance by discarding what it knows. It advances by naming what it doesn't know yet — and then building the tools to study it.

GRP operates in the space that existing disciplines approach but do not yet fully occupy:

| Discipline | What it covers | What it leaves open |
|---|---|---|
| Neuroscience | Neural correlates of emotion and attachment | The relational dynamics *between* nervous systems |
| Psychology | Individual behavior, attachment styles, affect | Quantitative trajectory modeling of dyadic motion |
| Physics | Laws governing matter, energy, and spacetime | The physics of meaning, attention, and relational force |
| Systems theory | Feedback loops and emergent behavior | Human-scale primitives driving relational state change |

GRP does not claim to replace any of these. It claims that between them lies an unmapped region — one with its own primitives, its own conservation laws, and its own geometry — and that the tools to study it rigorously now exist.

This repository is the first working implementation.

---

## 🧠 How to See This System Correctly

Most readers approach GRP with a **noun-mind** — the default analytical stance that looks for objects, categories, and static properties. GRP resists that framing.

GRP is a **verb-shaped system**. It describes *becoming*, not *being*. *Motion*, not identity. *Trade*, not substance.

The epistemological prerequisite for understanding GRP deeply — not just mechanically — is described in:

> 📄 [`docs/Verb Mind Epistemology for Relational Physics.md`](docs/Verb%20Mind%20Epistemology%20for%20Relational%20Physics.md)

This paper explains why relational systems cannot be understood with noun-thinking, how to shift into a verb-mind, and how to perceive identity as coherence across change. Read it early. It is the **epistemic OS update** that makes the rest of the project intelligible.

---

## 🏗️ Architecture Overview

WhenMathPrays is organized into two major layers: **the theoretical framework** and **the interactive simulation system**.

### Layer 1 — Theoretical Framework (`docs/`, root markdown files)

The foundational documents describe the mathematics, primitives, constants, and philosophical grounding of General Relational Physics. Key files:

| Document | Contents |
|---|---|
| [`docs/GRP_rev3.5.md`](docs/GRP_rev3.5.md) | The full mathematical specification of the GRP recurrence system |
| [`docs/PRIMITIVES_AND_RELATIONAL_SPACE.md`](docs/PRIMITIVES_AND_RELATIONAL_SPACE.md) | Deep treatment of each primitive and the structure of γ-space |
| [`CONSTANTS.md`](CONSTANTS.md) | All tunable parameters, weights, and entropy coefficients |
| [`docs/GRP_GLOSSARY.md`](docs/GRP_GLOSSARY.md) | Canonical definitions for all terms used across the project |
| [`WHY_THIS_MATTERS.md`](WHY_THIS_MATTERS.md) | The philosophical and scientific motivation for the framework |
| [`THE_STORY_OF_GRP.md`](docs/THE_STORY_OF_GRP.md) | The human narrative of how this system came to be |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Technical architecture of the interactive editor and simulation system |

### Layer 2 — Interactive Simulation System (`tools/`, `scenarios/`, `results/`, `core/`)

The simulation layer provides two interfaces for running scenarios:

#### Python Cockpit (Recommended)
A full interactive editor built in PyQt with:
- **Primitive Panel** — drag-and-drop editing of all five primitive arcs across time
- **Trajectory Panel** — live visualization of the `γ_self` trajectory as primitives are modified
- **Dual-Perspective Mode** — edit M1 (Person 1's view) and M2 (Person 2's view) independently, with overlay visualization
- **Full Undo/Redo** — Command pattern with per-perspective undo stacks
- **CSV I/O** — scenarios load from and save to structured CSV files. PNG export is currently disabled (PyQtGraph migration)

#### Excel Cockpit (`tools/GRP_SpreadSheet.xlsm`, `tools/GRP_AI.xlsm`)
A hands-on spreadsheet interface for visual exploration:
1. Enter your initial `γ_self` in cell `C4`
2. Enter primitive values row-by-row starting at row 9
3. Press **Run GRP** macro
4. Watch the trajectory populate in column `H`

Both interfaces implement the same General Relational Physics dynamics — they are different lenses on the same system.

### Software Architecture Principles

The interactive editor follows **MVC + Command pattern** with strict separation of concerns:

| Component | Role |
|---|---|
| `EditorModel` | Central state container; single source of truth for all scenario data |
| `EditorController` | Mediator; all inter-component communication flows through it |
| `PrimitivePanelPyQtGraph` | View; drag-and-drop primitive editing interface |
| `TrajectoryPanelPyQtGraph` | View; live trajectory visualization |
| `Command Classes` | Atomic operations enabling undo/redo with full state integrity |
| `EditorState` | Centralized enum-based state machine replacing scattered boolean flags |

All code contributions must meet the **MVT standard**:
- **M** (Modeled): Clean architecture following established patterns
- **V** (Verifiable): Observable behavior with clear success criteria
- **T** (Testable): Manual test checklists and/or automated tests

### The `thought_simulator/` Sub-Project

`thought_simulator/` is a self-contained research sub-project organized by engineering phase:

| Directory | Contents |
|---|---|
| `thought_simulator/system_architecture/` | System architecture specifications and design governance |
| `thought_simulator/thought_simulator_req/` | Requirements, design specs, and flow-down protocols |
| `thought_simulator/verification/` | Verification methodology and test capsules |
| `thought_simulator/thought_simulator_playground/` | Prototype implementations (TR Router, IB, TB, Basin prototypes) |
| `thought_simulator/thought_simulator_design/` | Design documentation and formal specifications |
| `thought_simulator/program_governance/` | Bot/EVENT home |
| `thought_simulator/requirements_20/` | Collaborative 20-series requirement layer |
| `thought_simulator/requirements_20/system_playground/simulation/` | Path A machine (landed 2026-08-28): `ts_kernel/` plus `pipelines/lineup_idob_mcb` |

---

## 📁 Repository Structure

```
WhenMathPrays/
│
├── 📄 README.md               ← You are here (conceptual map)
├── 📄 STARTHERE.md            ← Front door for new readers
├── 📄 CONTENTS.md             ← Complete document index
├── 📄 ARCHITECTURE.md         ← Interactive editor technical architecture
├── 📄 WHY_THIS_MATTERS.md     ← Philosophical motivation
├── 📄 CONSTANTS.md            ← Mathematical parameters and weights
├── 📄 TUNING.md               ← Guidance for calibrating the system
│
├── 📁 core/                   ← GRP math engine (the recurrence computation)
├── 📁 tools/                  ← Interactive editor, scenario generator, utilities
│   └── editor/                ← PyQtGraph-based cockpit (MVC + Command)
├── 📁 scenarios/              ← Python scenario runners (_TEMPLATE.py, validator, runner)
├── 📁 data/                   ← Scenario CSV libraries (`data/library/`) and templates
├── 📁 results/                ← Generated trajectory plots (PNG)
├── 📁 simulations/            ← Python scenario runners (not batch output dumps)
├── 📁 docs/                   ← Research papers, guides, and narrative documents
│   └── architecture/          ← Architecture decision records and refactoring plans
├── 📁 assets/                 ← Icons and miscellaneous assets (Excel cockpits are in tools/)
├── 📁 testbenches/            ← Formal test benches
├── 📁 tests/                  ← Automated test suite
├── 📁 verification/           ← Verification capsules and test procedures
├── 📁 scripts/                ← Utility and automation scripts
├── 📁 logs/                   ← Baseline and run logs
├── 📁 skins/                  ← UI theme configurations
├── 📁 mcps/                   ← Model context protocol tooling
└── 📁 thought_simulator/      ← Standalone thought simulation sub-project
```

---

## ⚡ Quick Start

### Prerequisites
```bash
git clone https://github.com/CuriousOne23/WhenMathPrays.git
cd WhenMathPrays
pip install -r requirements.txt
```

### Run a Scenario (Python)
```bash
python tools/interactive_editor.py <csv_file>
# example:
python tools/interactive_editor.py data/library/love/single_dating_to_love_M1.csv
```
PNG export is currently disabled. Edited scenarios save as CSV.

### Build Your Own Scenario
See [`docs/SCENARIO_CONFIGURATION_GUIDE.md`](docs/SCENARIO_CONFIGURATION_GUIDE.md) for the CSV format specification, or use the automated builder:
```bash
python tools/scenario_generator.py
```

### Explore Visually (Excel)
Open `tools/GRP_SpreadSheet.xlsm`, enter your values, and press **Run GRP**.

---

## 📚 Key Documents for Evaluators and Researchers

| If you want to understand… | Read… |
|---|---|
| The philosophical "why" | [`WHY_THIS_MATTERS.md`](WHY_THIS_MATTERS.md) |
| The perceptual stance required | [`docs/Verb Mind Epistemology for Relational Physics.md`](docs/Verb%20Mind%20Epistemology%20for%20Relational%20Physics.md) |
| The full mathematics | [`docs/GRP_rev3.5.md`](docs/GRP_rev3.5.md) |
| The five primitives in depth | [`docs/PRIMITIVES_AND_RELATIONAL_SPACE.md`](docs/PRIMITIVES_AND_RELATIONAL_SPACE.md) |
| The constants and calibration | [`CONSTANTS.md`](CONSTANTS.md) + [`TUNING.md`](TUNING.md) |
| How γ-trajectories are interpreted | [`docs/gamma_self_trajectory_reference.md`](docs/gamma_self_trajectory_reference.md) |
| The software architecture | [`ARCHITECTURE.md`](ARCHITECTURE.md) + [`docs/architecture/SOFTWARE_MODULES.md`](docs/architecture/SOFTWARE_MODULES.md) |
| AI collaboration and extension | [`docs/AI_Architecture_WhichWill_Scale.md`](docs/AI_Architecture_WhichWill_Scale.md) |
| The human story of the project | [`THE_STORY_OF_GRP.md`](docs/THE_STORY_OF_GRP.md) |
| Conversations that shaped the system | [`docs/Reality in Motion, Conversations.md`](docs/Reality%20in%20Motion,%20Conversations.md) |
| Everything, indexed | [`CONTENTS.md`](CONTENTS.md) |

---

## 🤝 Contributing

All contributions must meet the MVT standard (Modeled, Verifiable, Testable). See:
- [`docs/architecture/05_CODING_GUIDELINES.md`](docs/architecture/05_CODING_GUIDELINES.md) — Naming, state management, and coding standards
- [`docs/INTERACTIVE_EDITOR_TESTING.md`](docs/INTERACTIVE_EDITOR_TESTING.md) — Testing methodology

---

## 💬 A Note on What This Is

Science advances by two means: deepening what it knows, and honestly naming what it doesn't know yet.

General Relational Physics does the second. It honors every result that physics, biology, neuroscience, and psychology have produced — and then stands at the edge of those results and asks: *what is out here, past where the current tools reach?*

The answer this framework proposes is a specific, unmapped territory: the space of relational dynamics. The forces that move two people toward or away from each other. The geometry of care, presence, and rupture. The entropy that erodes connection quietly, whether or not anything dramatic happens.

These are not soft ideas dressed in scientific language. They are measurable. They are modelable. They are, with this framework, now tractable.

A relationship is not a number. It is not a score. It is a **trajectory in γ-space**, shaped by visibility, resonance, fidelity, altruism, and shared breath — and eroded, gently but always, by entropy.

This repository is an attempt to draw the first reliable map of that territory.

---

*Tagged: `relational-model` · `mathematical-expression` · `synthetic-life` · `identity-modeling` · `emotional-modeling` · `whenmathprays` · `gamma-self`*
