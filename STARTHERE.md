# 🌱 **START HERE — A Gentle Introduction to WhenMathPrays**

**WhenMathPrays** is a system for modeling the motion of relationship states — not as metaphors, not as sentiment scores, but as **positions in a two‑dimensional emotional space** governed by a single, elegant recurrence equation.

It is mathematics with a pulse.  
A dynamical system with a heart.  
A protocol for tracing how two people move toward or away from each other over time.

This document is your first step.

---

# 📘 **Before You Begin**

If you want a broader view of the project before diving in, here are two helpful maps:

- 👉 **[README.md](README.md)** — a high‑level map of the repository  
- 👉 **[CONTENTS.md](docs/CONTENTS.md)** — a complete index of every document with short summaries  

**START HERE** is your front door.  
**README** is your foyer.  
**CONTENTS** is your library catalog.

---

# 🌌 **1. What the GRP Is (in one breath)**

The **Gamma Relational Persona (GRP)** is a model that describes how a relational state evolves:

- across time  
- across events  
- across emotional primitives  
- across entropy and forgetting  
- across fidelity, resonance, altruism, visibility, and shared breath  

The core idea is simple:

> **Love is not a number.  
> Love is a position in γ‑space.  
> Everything else is how we move the knot.**

---

# 🧭 **2. The Core Equation (Rev 3.5)**

At the heart of the system is a recurrence:

\[
\gamma_{\text{self}}(n+1) = \gamma_{\text{self}}(n) + \Delta\gamma + \text{entropy}
\]

Where:

- **γ_self** is your position in the emotional plane  
- **Δγ** comes from the five relational primitives  
- **entropy** is a gentle, constant‑force drift toward long‑term forgetting  

You don’t need the full mathematical form yet — you’ll feel it soon enough.

---

# 🌬️ **3. The Five Primitives**

Every scenario is built from five human‑scale inputs:

| Primitive | Meaning |
|----------|---------|
| **v** | Visibility — how seen you feel |
| **r** | Resonance — how “in tune” you are |
| **f** | Fidelity — trust, betrayal, or devotion |
| **a** | Altruism — giving, generosity, care |
| **S** | Shared Breath — presence, attunement, co‑regulation |

Each primitive ranges from **–10 to +10**, and each one nudges γ_self in its own direction.

You don’t need to memorize them.  
You’ll learn them by watching them move.

---

# 🚀 **4. Your First Scenario (5 Minutes)**

Let’s run your first simulation.

### **Step 1 — Clone the repo**
```
git clone https://github.com/CuriousOne23/WhenMathPrays
cd WhenMathPrays
```

### **Step 2 — Install dependencies**
```
pip install -r requirements.txt
```

---

## **Option A — Run a Scenario in Python (recommended for newcomers)**

You can run any scenario CSV through the Python cockpit.

Here is a real example using one of the library scenarios:

```
python tools/interactive_editor.py data/library/love/single_dating_to_love_M1.csv
```

This opens the interactive editor, loads the scenario, and lets you explore or modify the emotional arc.

After running it, look in the `results/` folder for a PNG plot of the γ‑trajectory.

---

## **Option B — Explore the Model Visually (Excel Cockpit)**

If you prefer a **hands‑on, visual interface**, open the Excel cockpit:

```
tools/GRP_SpreadSheet.xlsm
```

Inside the workbook:

- Enter your initial γ_self in **C4**  
- Enter your primitives row‑by‑row starting at **row 9**  
- Press the **Run GRP** macro button  
- Watch the γ_self trajectory populate in column **H**  

This interface is perfect for:

- experimenting with primitives  
- seeing the recurrence unfold step‑by‑step  
- teaching the model  
- quick scenario sketching  
- debugging intuition  

The Excel cockpit and Python cockpit produce the **same dynamics** — just through different lenses.

---

### **Step 4 — Open the generated plot (Python path)**  
Look in the `results/` folder for a PNG file.

You’ll see a curve — a path — a motion through γ‑space.

That motion *is* the relationship.

### **Step 5 — Change something**  
Open the CSV (Python) or the primitive row (Excel) and edit any value:

- increase resonance  
- decrease fidelity  
- add a betrayal  
- add a repair  
- add a moment of shared breath  

Run again.  
Watch the trajectory shift.

You’ve just learned the GRP by doing.

---

# 🧩 **5. Where to Go Next**

Now that you’ve seen the system move, choose your path:

### **A. Use the Python cockpit (recommended)**  
👉 **[interactive_editor_user_guide.md](docs/interactive_editor_user_guide.md)**

### **B. Explore the model visually (Excel)**  
Open:  
```
tools/GRP_SpreadSheet.xlsm
```

### **C. Build your own scenario (intermediate)**  
👉 **[SCENARIO_CONFIGURATION_GUIDE.md](docs/SCENARIO_CONFIGURATION_GUIDE.md)**

### **D. Use the scenario builder (advanced)**  
👉 `tools/scenario_generator.py`  
This tool is powerful but not beginner‑friendly.  
Use it once you understand scenario structure and primitive arcs.

### **E. Understand the math**  
👉 **[GRP_rev3.md](docs/GRP_rev3.md)**

### **F. Explore the philosophy**  
👉 **[WHY_THIS_MATTERS.md](docs/WHY_THIS_MATTERS.md)**

### **G. Browse the full document index**  
👉 **[CONTENTS.md](docs/CONTENTS.md)**

### **H. Return to the map of the territory**  
👉 **[README.md](README.md)**

---

# 🗺️ **6. The Map of the Territory**

```
WhenMathPrays/
│
├── START HERE.md          ← You are here
├── README.md              ← Map of the repo
│
├── data/                  ← Scenario CSVs
├── scenarios/             ← Example scenario scripts
├── simulations/           ← Engines and tests
├── tools/                 ← Editors, spreadsheets, generators
│
└── docs/                  ← Deep reference library
    ├── GRP_rev3.md
    ├── CONSTANTS.md
    ├── TUNING.md
    ├── WHY_THIS_MATTERS.md
    ├── SCENARIO_CONFIGURATION_GUIDE.md
    ├── interactive_editor_user_guide.md
    ├── CONTENTS.md
    ├── ARCHITECTURE.md
    └── ...
```

Everything has a place.  
Everything has a purpose.  
You can explore at your own pace.

---

# 🌟 **7. Final Note**

This project is alive.  
It is meant to be explored, questioned, extended, and felt.

You don’t need to understand everything at once.  
Just start with a scenario.  
Watch the knot move.  
Let the system teach you.

Welcome to WhenMathPrays.

---
