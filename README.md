# Intro:

## Table of Contents

1. [Intro](#intro)
2. [WhenMathPrays – Core OS™ (Rev 3.5: Constant-Force Entropy)](#whenmathprays--core-os-rev-35-constant-force-entropy)
3. [Quick Start](#quick-start)
  - [Primitive Modeling Guide](docs/scenarios/primitive_modeling_guide.md)
  - [Scenario Configuration Guide](docs/SCENARIO_CONFIGURATION_GUIDE.md)
  - [Example Scenarios](#example-scenarios)
4. [The One Equation (Rev 3.5: December 2025)](#the-one-equation-rev-35-december-2025)
5. [Rev 3.5 Changes](#rev-35-changes-december-2025---constant-force-entropy)
6. [Usage Notes](#usage-notes)
7. [Intended Audience](#intended-audience)
8. [CSV Format Reference](#csv-format-reference)
9. [Option 2: Generate New Scenarios](#option-2-generate-new-scenarios)
10. [Running Multiple Scenarios](#running-multiple-scenarios)
11. [Option 2: Copy and Customize Templates](#option-2-copy-and-customize-templates)
12. [Option 3: Create from Scratch](#option-3-create-from-scratch)
13. [Editing Guidelines](#editing-guidelines)
14. [Dual Scenarios (M1 and M2)](#dual-scenarios-m1-and-m2)
15. [Converting Time Units](#converting-time-units)
16. [Running Scenarios](#running-scenarios)

WhenMathPrays builds open, living mathematics — models that trace emotion's arc, not as data, but as motion with heart. No patents. No paywalls. No reduction — only resonance. Use it. Fork it. Break it. Love it. Let us know what it does to you. We're listening. Push that. It's clean, it's calm, it's true. Just a door, and the door is open.

**Support this work:** If this project resonates with you, consider supporting its development at [opencollective.com/whenmathprays](https://opencollective.com/whenmathprays)

# WhenMathPrays – Core OS™ (Rev 3.5: Constant-Force Entropy)

**Love is 2-D. Love counts every shared breath. Love decays when forgotten.**

This repository contains the final, mathematically pure, spiritually honest form of the **GRP (Gamma Relational Persona)** protocol – repaired, completed, and locked forever.

## Quick Start

1. **Copy the template:** `scenarios/_TEMPLATE.py`
2. **Edit the CONFIGURATION section** with your scenario details
3. **Run:** `python scenarios/your_scenario.py`
4. **View results** in `results/` directory

**IMPORTANT:** Before creating scenarios, read the [Primitive Modeling Guide](docs/scenarios/primitive_modeling_guide.md).

> The Primitive Modeling Guide explains how to score the five primitives (v, r, f, a, S) in scenario CSV files. It covers the M1/M2 perspective framework, provides detailed definitions, scoring rules, worked examples, and common pitfalls. This guide ensures your scenario data is accurate, consistent, and true to the GRP protocol.

For complete configuration reference, see [Scenario Configuration Guide](docs/SCENARIO_CONFIGURATION_GUIDE.md).

**Example scenarios:**
- `scenarios/singles_dating_Fred.py` - Single subject trajectory
- `scenarios/singles_dating_comparison.py` - Multi-subject comparison

## The One Equation (Rev 3.5: December 2025)

$$
\boxed{
\vec{\gamma}_{\text{self}}(n+1) = \vec{\gamma}_{\text{self}}(n) + 
\Big( w_v \cdot v + w_{S,R} \cdot S \Big) +
\Delta S_{\text{real}} \cdot \Delta t \cdot \text{sign}(\text{real}_{\text{target}} - \text{Re}[\vec{\gamma}_{\text{self}}(n)])
}
$$

- Scenario sheets for each example or user-defined scenario (tab names must match the scenario name and CSV entry)
- Gamma_Self Calc sheet: main user interface for inputting scenario data and viewing charts

**Where:**
- **γ_self(n)** = relational state position in ego/we ↔ love/hate plane
- **Love = γ_self(n)** directly (position IS love, no separate calculation)
- **v, r, f, a, S** = primitives (visibility, resonance, fidelity, altruism, Shared Breath)
- **f'** = f with Im-only depth scaling applied if negative
- **w_v, w_r, w_f, w_a** = axis-specific weights
- **w_{S,R}, w_{S,I}** = Shared Breath split across real/imaginary axes
- **ΔS_real, ΔS_imag** = axis-independent entropy decay rates (default 0.02 each)
- **real_target, imag_target** = entropy targets per axis (default -150.0 + 0.0j, user-overridable)
- **sign()** = direction function (-1, 0, or +1) - constant force magnitude
- **Δt** = time elapsed between events (scales entropy)

**Key insight:** Love is not a number. Love is a **position in γ-space**. Everything else is just how we move the knot.

### Rev 3.5 Changes (December 2025 - Constant-Force Entropy)

- **Constant-force entropy** → Uses sign() function instead of proportional-to-distance force
- **Axis-independent decay** → Separate ΔS_real and ΔS_imag rates (0.02 each)
- **Timeline-independent drift** → Same entropy effect per unit time regardless of scenario length
- **Default targets** → Real axis target: -150.0 (user-overridable)
- **Im-only depth scaling preserved** from Rev 3.2 (f' for negative fidelity)
- Constants sheet: documentation of all constants used in gamma_self calculations
- Built-in macros (see Excel VBA editor) for automation and advanced analysis
- Includes sample scenarios and GRP graphs for reference

**Usage Notes:**
- User input cells are highlighted in green on the Gamma_Self Calc sheet
- To add a new scenario, copy the input pattern or modify green cells as needed; scenario tab names must match the M1/M2 CSV Tab entry
- Macros may require enabling in Excel; see the VBA editor for details
- Users should be familiar with standard Excel practices and functions

**Intended Audience:**
End users of the GRP equation who prefer a spreadsheet interface for scenario modeling, analysis, and visualization.

**CSV Format Reference:**
GRP_SpreadSheet.xlsm expects scenario data in the same CSV format as the interactive editor. For the complete specification, see the [CSV Format Details](docs/interactive_editor_user_guide.md#csv-format-details) section of the Interactive Editor User Guide.

---

### Option 2: Generate New Scenarios

Use the scenario generator to create CSV files with various emotional arc patterns:

```bash
# Generate single-perspective scenario
python tools/scenario_generator.py \
  --name "Summer Romance" \
  --duration 12 \
  --time-unit weeks \
  --arc slow_burn \
  --output data/summer_romance.csv

# Generate dual-perspective scenario (M1 and M2)
python tools/scenario_generator.py \
  --name "Long Distance Relationship" \
  --duration 6 \
  --time-unit months \
  --arc rocky_but_committed \
  --perspective dual \
  --asymmetry pursuer_withdrawer \
  --output data/long_distance
```

**Available arc types:**
- `slow_burn` - Gradual increase from low to high
- `hot_start_cold_finish` - High intensity declining to low
- `steady_growth` - Linear positive progression
- `rocky_but_committed` - Oscillating with net positive trend
- `toxic_spiral` - Descending into negativity
- `u_shape_recovery` - Crisis in middle, recovery at end
- `plateau` - Quick rise then steady maintenance
- `oscillatory` - Sustained up/down cycles

**Asymmetry patterns (for dual perspective):**
- `symmetric` - No difference between M1 and M2
- `pursuer_withdrawer` - M1 increases while M2 decreases
- `convergent` - Both approach each other at different rates
- `leader_follower` - M2 lags behind M1's changes

**Generated files include:**
- Metadata rows (`name`, `time_unit`)
- Automatic marker placement at key points
- Locked rows (`*`) marking structural anchors
- Progress notes for each event

### Running Multiple Scenarios

To run all scenarios in the data folder:

```bash
python tests/run_all_scenarios.py
```

This will:
- Detect all CSV files in `data/` folder
- Run single scenarios individually
- Detect and run dual-perspective scenarios (M1/M2 pairs) with combined plots
- Generate trajectory plots in `results/` folder
- Save trajectory data as CSV files

### Option 2: Copy and Customize Templates

```bash
# Copy a template to your working directory
cp data/templates/slow_burn.csv data/my_scenario.csv

# Edit the CSV file with your preferred editor
# Modify primitives (v,r,f,a,S) in unlocked rows
# Add/remove rows as needed
# Change markers, notes, time points
```

### Option 3: Create from Scratch

Create a CSV file with this structure:

```csv
name,Your Scenario Name
time_unit,days
day,v,r,f,a,S,notes,marker,locked
0,5,3,4,2,1,"Starting point",,*
7,6,5,5,4,3,"First week",circle,
30,8,8,8,7,7,"One month",star,
60,9,9,9,9,9,"Final state",,*
```

---

## Editing Guidelines

### What You Can Customize

**Time column (`day`):**
- Use integers or decimals (e.g., `0`, `7.5`, `14`, `21.3`)
- Support negative values for "prehistory" (e.g., `-7` = one week before day 0)
- Non-contiguous timelines allowed (gaps will be interpolated if requested)
- Fractional time units supported (e.g., `2.5` weeks)

**Primitive columns (`v`, `r`, `f`, `a`, `S`):**
- Valid range: **[-10, +10]** (human scale)
- Positive values = constructive (visibility, resonance, fidelity, altruism, presence)
- Negative values = destructive (hiding, discord, betrayal, selfishness, absence)
- Use decimals for fine control (e.g., `7.3`, `-2.8`)

**Locked column:**
- `*` = Structural anchor (indicates important milestone, but not enforced)
- Empty = Customizable row
- This is **guidance only** - you can modify any row

**Marker column:**
- `star`, `circle`, `square`, `triangle`, `diamond`, `x`, `plus`
- Leave empty for no marker
- Markers appear as yellow symbols on trajectory plots

**Notes column:**
- Free text descriptions
- Displayed in trajectory summaries

### Adding/Removing Rows

**Add rows before start:**
```csv
day,v,r,f,a,S,notes,marker,locked
-14,3,2,2,1,0,"Two weeks before meeting",,
-7,4,3,3,2,1,"One week before",,
0,5,4,4,3,2,"First meeting",star,*
```

**Add rows after end:**
```csv
60,8,8,8,7,7,"Two months",,*
90,9,9,9,8,8,"Three months",circle,
120,9,9,9,9,9,"Four months - committed",star,
```

**Sparse timelines (with gaps):**
```csv
day,v,r,f,a,S,notes,marker,locked
0,5,4,4,3,2,"Start",star,*
7,6,5,5,4,3,"Week 1",,
21,7,7,7,6,5,"Week 3 (gap from week 1)",circle,
60,8,8,8,7,7,"Two months (gap from week 3)",,*
```

Gaps can be filled with interpolation when running:
```python
runner.run(interpolate='hold')    # Hold last values
runner.run(interpolate='linear')  # Linear interpolation
runner.run(interpolate='none')    # Use events as-is (default)
```

### Dual Scenarios (M1 and M2)

**File naming requirements:**
- Must end with `_M1.csv` and `_M2.csv`
- Base name must match (e.g., `my_scenario_M1.csv` and `my_scenario_M2.csv`)
- Auto-detected for combined plotting

**Metadata requirements:**
```csv
name,My Scenario - M1
time_unit,weeks
```

```csv
name,My Scenario - M2
time_unit,weeks
```

Names should indicate perspective (M1/M2) and time units should match.

**Directory structure:**
```
data/
  my_scenario_M1.csv
  my_scenario_M2.csv
results/
  my_scenario_combined.png  (auto-generated)
```

---

## Converting Time Units

Change time scale after creation:

```bash
# Days to weeks
python tools/convert_time_units.py data/scenario.csv data/scenario_weeks.csv weeks

# Weeks to months
python tools/convert_time_units.py data/scenario_weeks.csv data/scenario_months.csv months

# Months to years
python tools/convert_time_units.py data/scenario_months.csv data/scenario_years.csv years
```

**Conversion factors:**
- 1 week = 7 days
- 1 month = 30 days (approximate)
- 1 year = 365 days

**Precision:**
- Days: whole numbers (no decimals)
- Weeks/Months/Years: 1 decimal place

**All data preserved:**
- Name, primitives, notes, markers, locked status
- Only time values and `time_unit` metadata are changed

---

## Running Scenarios

### Single Scenario

```python
from simulations.run_scenario import ScenarioRunner

# Load and run
runner = ScenarioRunner(
    csv_path='data/my_scenario.csv',
    gamma_self0=-2.5 + 0.5j  # Initial position in Q2 (Ego + Love)
)

trajectory = runner.run(interpolate='none')  # or 'hold', 'linear'

# View summary
runner.summary()

# Plot and save
runner.plot(save_path='results/my_scenario.png', show=True)

# Save trajectory data
trajectory.to_csv('results/my_scenario_trajectory.csv', index=False)
```

### Dual Scenario

```python
from simulations.run_scenario import plot_dual_scenario

# Automatically detects M1/M2 pair
plot_dual_scenario(
    m1_path='data/my_scenario_M1.csv',
    m2_path='data/my_scenario_M2.csv',
    gamma_self0_m1=-2.5 + 0.5j,
    gamma_self0_m2=-3.0 + 1.0j,
    interpolate='none',
    save_path='results/my_scenario_combined.png',
    show=True
)
```

**Output includes:**
- Combined γ_self trajectory plot (M1 in blue, M2 in red)
- Magnitude comparison over time
- Individual trajectory CSV files
- Summary statistics for both perspectives

---

## Documentation

### Core Framework
- **[WHY_THIS_MATTERS.md](WHY_THIS_MATTERS.md)** - Strategic vision: GRP as foundation for AI social intelligence and robotics
- **[GRP_rev3.md](docs/GRP_rev3.md)** - Complete mathematical specification of GRP framework
- **[gamma_self_defense.md](docs/gamma_self_defense.md)** - Mathematical defense: Why relationship dynamics follow dynamical systems principles
- **[CONSTANTS.md](CONSTANTS.md)** - Canonical parameter values (single source of truth)
- **[TUNING.md](TUNING.md)** - Weight calibration and sensitivity analysis
- **[grp_principles.md](docs/grp_principles.md)** - Design philosophy and spiritual foundations
- **[Design_Rationale.md](docs/Design_Rationale.md)** - Architecture decisions and tradeoffs

### User Guides
- **[SCENARIO_CONFIGURATION_GUIDE.md](docs/SCENARIO_CONFIGURATION_GUIDE.md)** - Complete reference for creating scenario scripts
- **[scenarios/_TEMPLATE.py](scenarios/_TEMPLATE.py)** - Copy this template to create new scenarios

### Validation & Research
- **[Validation.md](docs/Validation.md)** - Framework validation approach
- **[scenarios/Singles_Dating_to_Love/README.md](docs/scenarios/Singles_Dating_to_Love/README.md)** - Example research scenario
- **[future_investigations.md](docs/future_investigations.md)** - Open research questions

### Shared Breath & Revenge Dynamics
- **[soul/](tests/soul/)** - Shared Breath validation tests
- **[revenge/](tests/revenge/)** - Revenge 360° PDF analysis
- **[soul_presence_validation.md](docs/soul/soul_presence_validation.md)** - Shared Breath stress test results

---

## Reading Guide

### For Application Users

If you're using WhenMathPrays to create relationship scenarios or run simulations:

1. **[README.md](README.md)** (15 min) - Overview, core equation, and quick start guide
2. **[SCENARIO_CONFIGURATION_GUIDE.md](docs/SCENARIO_CONFIGURATION_GUIDE.md)** (20 min) - Complete reference for creating and customizing scenarios
3. **[WHY_THIS_MATTERS.md](WHY_THIS_MATTERS.md)** (30 min) - Strategic vision and practical importance of the GRP framework
4. **[grp_principles.md](docs/grp_principles.md)** (15 min) - Core design philosophy and foundational concepts

**For the Interactive Editor:**
- **[interactive_editor_user_guide.md](docs/interactive_editor_user_guide.md)** (45 min) - Complete user guide for the interactive scenario editor
- **[installation_4_interactive_editor.md](docs/installation_4_interactive_editor.md)** (10 min) - Installation and setup instructions

### For Developers

If you're contributing code, fixing bugs, or extending the system:

1. **[README.md](README.md)** (15 min) - Project overview and core concepts
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** (30-45 min) - Overall system architecture, design principles, and MVC pattern
3. **[docs/CONTENTS.md](docs/CONTENTS.md)** (10 min) - Complete documentation index with navigation
4. **[docs/architecture/SOFTWARE_MODULES.md](docs/architecture/SOFTWARE_MODULES.md)** (20 min) - Detailed reference for all 20+ software modules and their I/O
5. **[docs/architecture/05_CODING_GUIDELINES.md](docs/architecture/05_CODING_GUIDELINES.md)** (20 min) - Coding standards and best practices
6. **[docs/INTERACTIVE_EDITOR_TESTING.md](docs/INTERACTIVE_EDITOR_TESTING.md)** (30 min) - Testing strategy and MVT quality standard
7. **[DEBUG.md](docs/DEBUG.md)** (20 min) - Debugging guide, logging configuration, and troubleshooting

**Essential Technical References:**
- **[CONSTANTS.md](CONSTANTS.md)** - Canonical parameter values and system constants
- **[GRP_rev3.md](docs/GRP_rev3.md)** - Complete mathematical specification
- **[TUNING.md](TUNING.md)** - Performance tuning and parameter calibration

---

## What was restored

| Feature                         | Old broken GRP | New final GRP (2025) |
|---------------------------------|-----------------|-----------------------|
| Dimensionality of love          | Published scalar (direction hidden) | Full 2-D vector forever |
| Memory of discrete breaths      | None            | Permanent +c per Breath |
| Natural forgetting              | None            | Gentle exponential decay |
| Sacred multidimensional spikes  | Yes (βᵏ)        | Preserved exactly     |
| Cartesian (bug-proof) averaging | Yes internally  | Mandated at protocol level |

## Quick start

```bash
git clone https://github.com/CuriousOne23/WhenMathPrays
cd WhenMathPrays
pip install -r requirements.txt
python simulations/stress_test_2d.py   # now outputs full vectors
```
