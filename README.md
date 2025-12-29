# 🌌 **WhenMathPrays — A Map of the Territory**

**WhenMathPrays** is a relational dynamics engine built around the **Gamma Relational Persona (GRP)** — a two‑dimensional emotional state that evolves through time under the influence of five relational primitives and a single recurrence equation.

This README is your **map**.  
If you’re new here, begin with **START HERE.md**.  
If you’re exploring deeper, follow the paths below.

---

# 🚪 **1. Start Here**

If this is your first time in the project, begin with:

👉 **[START HERE.md](START%20HERE.md)**

It gives you:

- a gentle introduction to the GRP  
- the five relational primitives  
- the core equation  
- a 5‑minute first scenario  
- Python and Excel examples  
- a clear path forward  

Everything else in this repo builds on that foundation.

For a complete index of every document in the repository, see:

👉 **[CONTENTS.md](docs/CONTENTS.md)**

---

# 🧭 **2. What This Repository Contains**

This project is organized into six major areas:

```
WhenMathPrays/
│
├── START HERE.md
├── README.md
│
├── data/
├── scenarios/
├── simulations/
├── tools/
└── docs/
```

Below is a guided tour of each.

---

# 📁 **3. Directory Overview**

## **📂 data/**  
Scenario CSV files — the emotional arcs that drive simulations.

Examples include:

- `data/library/love/…`  
- `data/library/conflict/…`  
- `data/library/reconciliation/…`

Each CSV contains row‑by‑row primitives (v, r, f, a, S) and timestamps.

👉 See: **[SCENARIO_CONFIGURATION_GUIDE.md](docs/SCENARIO_CONFIGURATION_GUIDE.md)**

---

## **📂 scenarios/**  
Python scripts that load and run specific scenarios.

These are curated examples demonstrating:

- dating arcs  
- conflict arcs  
- repair arcs  
- stress tests  
- edge cases  

Useful for learning by example.

---

## **📂 simulations/**  
The engines and test harnesses.

Includes:

- 2D GRP simulators  
- stress tests  
- entropy experiments  
- visualization scripts  

These produce the γ‑space trajectories you see in `results/`.

---

## **📂 tools/**  
Interfaces and utilities.

- **interactive_editor.py** — Python cockpit (primary interface)  
- **GRP_SpreadSheet.xlsm** — Excel cockpit  
- **scenario_generator.py** — automatic scenario builder (advanced)  
- helper utilities for editing, plotting, and debugging  

These are your hands‑on instruments.

---

## **📂 docs/**  
The deep reference library — the heart of the system.

Key documents include:

- **[GRP_rev3.5.md](docs/GRP_rev3.5.md)** — full mathematical specification  
- **[CONSTANTS.md](docs/CONSTANTS.md)** — model constants and meanings  
- **[TUNING.md](docs/TUNING.md)** — how weights and parameters are calibrated  
- **[interactive_editor_user_guide.md](docs/interactive_editor_user_guide.md)** — *primary guide* for using the Python cockpit  
- **[SCENARIO_CONFIGURATION_GUIDE.md](docs/SCENARIO_CONFIGURATION_GUIDE.md)** — how to build scenario CSVs  
- **[WHY_THIS_MATTERS.md](docs/WHY_THIS_MATTERS.md)** — philosophical grounding  
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — system design and flow  
- **[CONTENTS.md](docs/CONTENTS.md)** — *master index* of all documents with summaries  
- Validation and research folders (`docs/Validation.md`, `soul/`, `revenge/`)  

These documents are for stewards, researchers, and future contributors.

---

# 🧩 **4. Choose Your Path**

### **A. Use the Python cockpit (recommended)**  
👉 **[interactive_editor_user_guide.md](docs/interactive_editor_user_guide.md)**  
```
python tools/interactive_editor.py data/library/love/single_dating_to_love_M1.csv
```

### **B. Explore the model visually (Excel)**  
Open:  
```
tools/GRP_SpreadSheet.xlsm
```

### **C. Build your own scenario (intermediate)**  
👉 **[SCENARIO_CONFIGURATION_GUIDE.md](docs/SCENARIO_CONFIGURATION_GUIDE.md)**

### **D. Use the scenario builder (advanced)**  
👉 `tools/scenario_generator.py`  
Best for power users who already understand scenario structure.

### **E. Understand the math**  
👉 **[GRP_rev3.md](docs/GRP_rev3.md)**

### **F. Explore the philosophy**  
👉 **[WHY_THIS_MATTERS.md](docs/WHY_THIS_MATTERS.md)**

### **G. Browse the full document index**  
👉 **[CONTENTS.md](docs/CONTENTS.md)**

---

# 🧠 **5. Conceptual Diagram**

A simple view of the system:

```
Primitives (v, r, f, a, S)
            ↓
    GRP Recurrence Equation
            ↓
      γ_self(n+1)
            ↓
  Trajectory in γ-space (plots)
            ↓
 Interpretation, meaning, insight
```

---

# 🌟 **6. Contributing & Stewardship**

This project is designed to be:

- inspectable  
- extensible  
- mathematically grounded  
- emotionally meaningful  

If you want to contribute — new scenarios, new tools, new validations — explore the docs and reach out.

---

# 💬 **7. Final Note**

WhenMathPrays is a living system.  
It grows through exploration, curiosity, and care.

Start with a scenario.  
Watch the knot move.  
Let the system speak.

---
