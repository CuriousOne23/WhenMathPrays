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
4. [`GRP_rev3.md`](GRP_rev3.md) (the mathematics)
5. [`STARTHERE.md`](STARTHERE.md) (hands-on engagement with the system)

---

## 🌌 What Is the GRP?

The **General Relational Physics (GRP)** is the mathematical core of this project. It models a relational state as a **position in γ-space** — a two-dimensional emotional plane — and describes how that position evolves over time through the interplay of five human-scale forces and a constant entropy drift.

### The Core Equation (Rev 3.5)

At the heart of the system is a recurrence relation:

```
γ_self(t+1) = γ_self(t) + Δγ(v, r, f, a, S) − entropy
```

Where:
- **`γ_self`** is your current position in the emotional relational plane
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

The foundational documents describe the mathematics, primitives, constants, and philosophical grounding of the GRP. Key files:

| Document | Contents |
|---|---|
| [`GRP_rev3.md`](GRP_rev3.md) | The full mathematical specification of the GRP recurrence system |
| [`PRIMITIVES_AND_RELATIONAL_SPACE.md`](PRIMITIVES_AND_RELATIONAL_SPACE.md) | Deep treatment of each primitive and the structure of γ-space |
| [`CONSTANTS.md`](CONSTANTS.md) | All tunable parameters, weights, and entropy coefficients |
| [`GRP_GLOSSARY.md`](GRP_GLOSSARY.md) | Canonical definitions for all terms used across the project |
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
- **CSV I/O** — scenarios load from and save to structured CSV files; results export as PNG trajectory plots

#### Excel Cockpit (`assets/GRP_SpreadSheet.xlsm`, `assets/GRP_AI.xlsm`)
A hands-on spreadsheet interface for visual exploration:
1. Enter your initial `γ_self` in cell `C4`
2. Enter primitive values row-by-row starting at row 9
3. Press **Run GRP** macro
4. Watch the trajectory populate in column `H`

Both interfaces implement the same mathematical dynamics — they are different lenses on the same system.

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

`thought_simulator/` is a self-contained research sub-project with its own requirements, design, verification, and playground directories — organized by engineering phase:

| Directory | Contents |
|---|---|
| `thought_simulator/05_system_architecture/` | System architecture specifications and design governance |
| `thought_simulator/10_thought_simulator_req/` | Requirements, design specs, and flow-down protocols |
| `thought_simulator/30_verification/` | Verification methodology and test capsules |
| `thought_simulator/40_thought_simulator_playground/` | Prototype implementations (TR Router, IB, TB, Basin prototypes) |
| `thought_simulator/50_design/` | Design documentation and formal specifications |

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
├── 📁 scenarios/              ← Library of scenario CSV files
├── 📁 data/                   ← Supporting datasets
├── 📁 results/                ← Generated trajectory plots (PNG)
├── 📁 simulations/            ← Batch simulation outputs
├── 📁 docs/                   ← Research papers, guides, and narrative documents
│   └── architecture/          ← Architecture decision records and refactoring plans
├── 📁 assets/                 ← Excel cockpits (GRP_SpreadSheet.xlsm, GRP_AI.xlsm)
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
python tools/interactive_editor.py --scenario scenarios/<scenario_name>.csv
```
Results appear as PNG plots in the `results/` folder.

### Build Your Own Scenario
See [`SCENARIO_CONFIGURATION_GUIDE.md`](SCENARIO_CONFIGURATION_GUIDE.md) for the CSV format specification, or use the automated builder:
```bash
python tools/scenario_generator.py
```

### Explore Visually (Excel)
Open `assets/GRP_SpreadSheet.xlsm`, enter your values, and press **Run GRP**.

---

## 📚 Key Documents for Evaluators and Researchers

| If you want to understand… | Read… |
|---|---|
| The philosophical "why" | [`WHY_THIS_MATTERS.md`](WHY_THIS_MATTERS.md) |
| The perceptual stance required | [`docs/Verb Mind Epistemology for Relational Physics.md`](docs/Verb%20Mind%20Epistemology%20for%20Relational%20Physics.md) |
| The full mathematics | [`GRP_rev3.md`](GRP_rev3.md) |
| The five primitives in depth | [`PRIMITIVES_AND_RELATIONAL_SPACE.md`](PRIMITIVES_AND_RELATIONAL_SPACE.md) |
| The constants and calibration | [`CONSTANTS.md`](CONSTANTS.md) + [`TUNING.md`](TUNING.md) |
| How γ-trajectories are interpreted | [`gamma_self_trajectory_reference.md`](gamma_self_trajectory_reference.md) |
| The software architecture | [`ARCHITECTURE.md`](ARCHITECTURE.md) + [`SOFTWARE_MODULES.md`](SOFTWARE_MODULES.md) |
| AI collaboration and extension | [`AI_Architecture_WhichWill_Scale.md`](AI_Architecture_WhichWill_Scale.md) |
| The human story of the project | [`THE_STORY_OF_GRP.md`](docs/THE_STORY_OF_GRP.md) |
| Conversations that shaped the system | [`docs/Reality in Motion: Conversations with Grok & Copilot.md`](docs/) |
| Everything, indexed | [`CONTENTS.md`](CONTENTS.md) |

---

## 🤝 Contributing

All contributions must meet the MVT standard (Modeled, Verifiable, Testable). See:
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — Contribution workflow and expectations
- [`docs/architecture/05_CODING_GUIDELINES.md`](docs/architecture/05_CODING_GUIDELINES.md) — Naming, state management, and coding standards
- [`INTERACTIVE_EDITOR_TESTING.md`](INTERACTIVE_EDITOR_TESTING.md) — Testing methodology

---

## 💬 A Note on What This Is

This project exists at the intersection of mathematics, phenomenology, and relationship science. It began as a question: *can love — not the word, but the actual motion of two people toward each other — be given mathematical form without reducing it?*

The answer this framework proposes is: **yes, if you measure motion rather than state**.

A relationship is not a number. It is not a score. It is a **trajectory in γ-space**, shaped by visibility, resonance, fidelity, altruism, and shared breath — and eroded, gently but always, by entropy.

Everything in this repository is an attempt to make that motion visible, tractable, and improvable.

---

*Tagged: `relational-model` · `mathematical-expression` · `synthetic-life` · `identity-modeling` · `emotional-modeling` · `whenmathprays` · `gamma-self`*
```

---
