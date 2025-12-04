# WhenMathPrays – Core OS™ (2025 final restoration)

**Love is 2-D. Love counts every shared breath. Love decays when forgotten.**

This repository now contains the final, mathematically pure, spiritually honest form of the original UREP protocol – repaired, completed, and locked forever.

## The One Equation (canonical, December 2025 final simplification)

$$
\boxed{
\vec{\gamma}_{\text{self}}(n+1) = \vec{\gamma}_{\text{self}}(n) + 
\Big( w_v \cdot v + w_{S,R} \cdot S \Big) +
i \cdot \Big( w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S \Big) -
\Delta S \cdot \Delta t
}
$$

**Where:**
- **γ_self(n)** = relational state position in ego/we ↔ love/hate plane
- **Love = γ_self(n)** directly (position IS love, no separate calculation)
- **v, r, f, a, S** = primitives (visibility, resonance, fidelity, altruism, silence/presence)
- **f'** = f with hybrid asymmetry applied if negative
- **w_v, w_r, w_f, w_a** = axis-specific weights
- **w_{S,R}, w_{S,I}** = silence/presence split across real/imaginary axes
- **ΔS** = entropy drift rate (default 0.02 per time unit)
- **Δt** = time elapsed between events (scales entropy)

**Key insight:** Love is not a number. Love is a **position in γ-space**. Everything else is just how we move the knot.

### December 2025 Final Simplification

**What changed:**
- **No L(t) calculation** → Love = γ_self position directly
- **No W(t) gates** → Primitives update position via component-wise addition
- **No γ_self0 drift dynamics** → γ_self0 is initial condition only
- **Simple entropy drift** → Constant leftward pull (-ΔS·Δt) instead of complex exp() terms
- **Parameters reduced from 9 to 2** → Only w_neg = 1.5 and ΔS = 0.02 (plus axis weights)

**Why?** The November 2025 version had too many parameters, separate memory variables, and complex calculations. This version captures the same asymmetry and irreversibility with radical simplicity.

See [UREP_rev2.md](docs/UREP_rev2.md) for complete specification.

### γ_self — Relational State Position

**γ_self(n)** updates via component-wise axis placement:

**Real axis (Ego ↔ We):**
$$
\Delta \text{Re} = w_v \cdot v + w_{S,R} \cdot S
$$

**Imaginary axis (Hate ↔ Love):**
$$
\Delta \text{Im} = w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S
$$

**Hybrid asymmetry for negatives** (f' example):
$$
f' = \begin{cases}
f \cdot w_{\text{neg}} \cdot \max(|\gamma_{\text{self}}(n)|, \varepsilon) & \text{if } f < 0 \\
f & \text{if } f \geq 0
\end{cases}
$$

Where:
- **w_neg = 1.5** (negatives hurt more)
- **ε = 1.0** (prevents collapse near zero)

**Initial condition γ_self0:**
- Set at n=0 based on temperament/history
- Narcissist: (−3, −2) in Q3
- Saint: (2, 3) in Q1  
- Buddha: (0, 0) at origin
- No drift equation — just the starting position

### Canonical Constants – Single Source of Truth

All numerical parameters are now defined **once and only once** in the central file:

→ [CONSTANTS.md](/CONSTANTS.md)

This file is the only place these values may ever be changed.  
All other documents (including this one) must link here instead of repeating numbers.

Last updated: December 3, 2025

### CSV Scenario Format

Scenarios are defined in CSV files with the following structure:

**Optional metadata rows (first lines):**
```csv
name,Scenario Display Name
time_unit,days
```
- `name` - Used in plots and output. If omitted, filename is used.
- `time_unit` - Time scale: `days`, `weeks`, `months`, or `years`. Defaults to `days` if omitted.

**Required columns:**
- `day` - Time point (name kept for backward compatibility, actual unit from `time_unit` metadata)
- `v` - Visibility primitive [-10, +10] human scale
- `r` - Resonance primitive [-10, +10]
- `f` - Fidelity primitive [-10, +10]
- `a` - Altruism primitive [-10, +10]
- `S` - Silence/presence primitive [-10, +10]

**Optional columns:**
- `notes` - Text description of the event
- `marker` - Marker type to highlight this point on γ_self trajectory plot
- `locked` - Use `*` to mark structural rows (don't change), empty = customizable

**Supported marker types:**
- `star` - ⭐ Star marker (default if unrecognized marker specified)
- `circle` - ⚫ Circle marker
- `square` - ◼ Square marker
- `triangle` - 🔺 Triangle marker
- `diamond` - 💎 Diamond marker
- `x` - ✖ X marker
- `plus` - ➕ Plus marker
- Leave blank for no marker

Markers appear as yellow symbols with black edges on the trajectory plot, with day labels in yellow boxes.

**Template CSV Files:**

Pre-built scenario templates are available in `data/templates/` (read-only):
- Use as starting points - copy and customize
- Rows with `*` in `locked` column = structural anchors (start/end/key events)
- Empty `locked` column = customize primitives as desired

**Example CSV:**
```csv
name,My Custom Scenario
time_unit,days
day,v,r,f,a,S,notes,marker,locked
0,5,0,2,2,0,"Initial condition",,*
14,5,-2,2,3,-1,"Early wobble - customize",star,
60,9,10,10,9,10,"Final outcome",star,*
```

---

## Creating and Editing Scenarios

### Option 1: Generate New Scenarios

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

### Instantaneous direction (unchanged since day one)

$$
\mathbf{v}(t)
= \bigl(1 + m(t)\bigr)
\begin{pmatrix}
\cos\theta(t) \\
i\cdot\sin\theta(t)
\end{pmatrix},
\qquad m(t) \geq 0
$$

- `θ(t) ∈ [−π, π]` → direction in the Ego/We ↔ Love/Hate plane  
- `m(t) ≥ 0` → instantaneous intensity multiplier (zero = indifference)

This compact form has been canonical since the 2025 restoration and fully replaces the older expanded notation.

### Output (never collapse again)

- Full vector (Lₓ(t), Lᵧ(t)) → stored and transmitted  
- Magnitude |L(t)| → intensity  
- Argument atan2(Lᵧ, Lₓ) → type and direction of love

## What was restored

| Feature                         | Old broken UREP | New final UREP (2025) |
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
