# 📚 CONTENTS — Complete Document Index

This is the library catalog for **WhenMathPrays**.
Every document is listed here with a short description of what it contains.

**Navigation tier above this document:**
- [`README.md`](README.md) — Conceptual map of the repository
- [`STARTHERE.md`](STARTHERE.md) — Front door for new readers

---

## 🚪 Entry Points

| Document | What it is |
|---|---|
| [`STARTHERE.md`](STARTHERE.md) | Hands-on introduction — the front door for all new readers |
| [`README.md`](README.md) | High-level conceptual map of GRP, the repository, and the simulation system |
| [`CONTENTS.md`](CONTENTS.md) | This file — a complete index of every document |
| [`WHY_THIS_MATTERS.md`](WHY_THIS_MATTERS.md) | The scientific, philosophical, and social argument for why GRP's research space matters in the AI age |

---

## 📄 Published Papers

| Document | What it is |
|---|---|
| [`docs/The_Missing_Science_of_the_AI_Age.md`](docs/The_Missing_Science_of_the_AI_Age.md) | **The Missing Science of the AI Age: A Case for Relational Physics** — standalone public paper co-authored by CuriousOne23, Copilot, and Grok. Argues that the relational verbal space is the largest unstudied domain in science and that the AI age makes formalizing it urgent. Includes the GRP recurrence equation, primitive profile table, and a call to the research community. |

---

## 🌌 General Relational Physics — Theory & Mathematics

| Document | What it is |
|---|---|
| [`docs/GRP_rev3.5.md`](docs/GRP_rev3.5.md) | The full mathematical specification of the GRP recurrence system (Rev 3.5) |
| [`docs/PRIMITIVES_AND_RELATIONAL_SPACE.md`](docs/PRIMITIVES_AND_RELATIONAL_SPACE.md) | Deep treatment of the five primitives (v, r, f, a, S) and the structure of γ-space |
| [`CONSTANTS.md`](CONSTANTS.md) | All tunable parameters, weights, and entropy coefficients with documentation |
| [`TUNING.md`](TUNING.md) | Guidance for calibrating the system — how to adjust parameters for specific research goals |
| [`docs/GRP_GLOSSARY.md`](docs/GRP_GLOSSARY.md) | Canonical definitions for every term used across the project |
| [`docs/gamma_self_trajectory_reference.md`](docs/gamma_self_trajectory_reference.md) | Reference guide for interpreting γ_self trajectory shapes and inflection points |

---

## 🧠 Epistemology & Foundation

| Document | What it is |
|---|---|
| [`docs/Verb Mind Epistemology for Relational Physics.md`](docs/Verb%20Mind%20Epistemology%20for%20Relational%20Physics.md) | The epistemic OS update — why relational systems require verb-mind perception, and how to develop it |
| [`WHY_THIS_MATTERS.md`](WHY_THIS_MATTERS.md) | The full internal argument for GRP as a legitimate and urgently needed scientific research space |
| [`docs/The_Missing_Science_of_the_AI_Age.md`](docs/The_Missing_Science_of_the_AI_Age.md) | Public paper — the case for relational physics in the AI age (see Published Papers above) |

---

## 🏗️ Software Architecture

| Document | What it is |
|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Technical architecture of the interactive editor — MVC + Command pattern, component roles, and design principles |
| [`docs/architecture/SOFTWARE_MODULES.md`](docs/architecture/SOFTWARE_MODULES.md) | Module-by-module breakdown of the codebase |
| [`docs/AI_Architecture_WhichWill_Scale.md`](docs/AI_Architecture_WhichWill_Scale.md) | Architecture guidance for AI collaboration and extension of the GRP system |
| [`docs/architecture/05_CODING_GUIDELINES.md`](docs/architecture/05_CODING_GUIDELINES.md) | Naming conventions, state management standards, and code quality expectations |
| [`docs/architecture/`](docs/architecture/) | Full set of architecture decision records and refactoring plans |

---

## 🎛️ Scenarios & Simulation

| Document | What it is |
|---|---|
| [`docs/SCENARIO_CONFIGURATION_GUIDE.md`](docs/SCENARIO_CONFIGURATION_GUIDE.md) | Complete specification of the CSV scenario format — how to build, structure, and validate scenarios |
| [`docs/INTERACTIVE_EDITOR_TESTING.md`](docs/INTERACTIVE_EDITOR_TESTING.md) | Testing methodology for the interactive editor — manual test checklists and procedures |
| [`scenarios/`](scenarios/) | Python scenario runners (`_TEMPLATE.py`, validator, runner) |
| [`results/`](results/) | Generated trajectory plots (PNG) from simulation runs |
| [`simulations/`](simulations/) | Python scenario runners (not batch output dumps) |
| [`data/`](data/) | Scenario CSV libraries (`data/library/`) and templates |

---

## 🛠️ Tools & Code

| Directory / File | What it is |
|---|---|
| [`tools/`](tools/) | Interactive editor, scenario generator, and utility scripts |
| [`tools/editor/`](tools/editor/) | PyQtGraph-based Python cockpit — the primary interactive interface |
| [`core/`](core/) | GRP math engine — the recurrence computation layer |
| [`scripts/`](scripts/) | Automation and utility scripts |
| [`skins/`](skins/) | Visual themes and display customizations for the editor |
| [`tools/GRP_SpreadSheet.xlsm`](tools/GRP_SpreadSheet.xlsm) | Excel cockpit — visual interface for scenario exploration |
| [`tools/GRP_AI.xlsm`](tools/GRP_AI.xlsm) | AI-extended Excel cockpit |

---

## ✅ Testing & Verification

| Directory | What it is |
|---|---|
| [`tests/`](tests/) | Automated test suite |
| [`testbenches/`](testbenches/) | Formal test benches for system-level validation |
| [`verification/`](verification/) | Verification capsules and test procedures |
| [`logs/baseline/`](logs/baseline/) | Baseline run logs for regression comparison |

---

## 🤖 AI Integration & MCP Tools

| Directory | What it is |
|---|---|
| [`mcps/grok_com_github/tools/`](mcps/grok_com_github/tools/) | MCP tool definitions for Grok integration with the repository |

---

## 📖 Narrative & Project History

| Document | What it is |
|---|---|
| [`docs/THE_STORY_OF_GRP.md`](docs/THE_STORY_OF_GRP.md) | The human narrative of how General Relational Physics came to be |
| [`docs/Reality in Motion, Conversations.md`](docs/Reality%20in%20Motion,%20Conversations.md) | Conversations with AI systems that shaped the development of GRP |

---

## 🤝 Contributing & Project

| Document | What it is |
|---|---|
| [`CONTRIBUTORS.md`](CONTRIBUTORS.md) | Project contributors |
| [`LICENSE.md`](LICENSE.md) | MIT License |
| [`FUNDING.md`](FUNDING.md) | Project funding and support information |

---

## 🧪 Thought Simulator Sub-Project

The `thought_simulator/` directory is a self-contained research sub-project
within WhenMathPrays, organized by engineering phase.

| Directory | What it is |
|---|---|
| [`thought_simulator/system_architecture/`](thought_simulator/system_architecture/) | System architecture specifications and design governance |
| [`thought_simulator/thought_simulator_req/`](thought_simulator/thought_simulator_req/) | Requirements, design specs, and flow-down protocols |
| [`thought_simulator/verification/`](thought_simulator/verification/) | Verification methodology and test capsules |
| [`thought_simulator/thought_simulator_playground/`](thought_simulator/thought_simulator_playground/) | Prototype implementations — TR Router, IB, TB, Basin prototypes |
| [`thought_simulator/thought_simulator_design/`](thought_simulator/thought_simulator_design/) | Design documentation and formal specifications |
| [`thought_simulator/requirements_20/system_playground/simulation/`](thought_simulator/requirements_20/system_playground/simulation/) | Path A machine (landed 2026-08-28): `ts_kernel/` plus `pipelines/lineup_idob_mcb` |

---

## 🗺️ Quick-Reference: What to Read First

| Your goal | Start here |
|---|---|
| I'm new to the project | [`STARTHERE.md`](STARTHERE.md) |
| I want the conceptual overview | [`README.md`](README.md) |
| I want to understand why this matters | [`WHY_THIS_MATTERS.md`](WHY_THIS_MATTERS.md) |
| I want the published public paper | [`docs/The_Missing_Science_of_the_AI_Age.md`](docs/The_Missing_Science_of_the_AI_Age.md) |
| I want to see the math | [`docs/GRP_rev3.5.md`](docs/GRP_rev3.5.md) |
| I need the epistemic foundation | [`docs/Verb Mind Epistemology for Relational Physics.md`](docs/Verb%20Mind%20Epistemology%20for%20Relational%20Physics.md) |
| I want to run a scenario now | [`STARTHERE.md §5`](STARTHERE.md) |
| I want to build my own scenario | [`docs/SCENARIO_CONFIGURATION_GUIDE.md`](docs/SCENARIO_CONFIGURATION_GUIDE.md) |
| I want to understand the software | [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| I want to contribute | [`docs/architecture/05_CODING_GUIDELINES.md`](docs/architecture/05_CODING_GUIDELINES.md) |
| I want everything, indexed | You are here |
