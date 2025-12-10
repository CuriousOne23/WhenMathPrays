# Scenario Configuration Guide

**Complete reference for GRP scenario scripts**

---

## Quick Start

1. Copy `scenarios/_TEMPLATE.py` to create a new scenario
2. Edit the **CONFIGURATION** section with your parameters
3. Run: `python scenarios/your_scenario.py`
4. Results saved to `results/` directory

---

## Configuration Reference

### Basic Settings

#### `SCENARIO_NAME` (required)
**Type:** string  
**Description:** Descriptive name for your research scenario  
**Example:** `"Singles Dating to Love - Fred"`

This name appears in plots and output files.

#### `AUTHOR` (required)
**Type:** string  
**Description:** Your name or identifier  
**Example:** `"CuriousOne"`

#### `DATE_CREATED` (optional)
**Type:** string  
**Description:** When you created this scenario configuration  
**Example:** `"2025-12-04"`

---

### Subjects Configuration

#### `SUBJECTS` (required)
**Type:** list of dictionaries  
**Description:** One or more subjects to simulate. Each subject is a dictionary with these fields:

##### Subject Fields:

**`name`** (required)
- **Type:** string
- **Description:** Subject identifier (e.g., "Fred", "Ann", "Alice")
- **Example:** `"Fred"`

**`csv_file`** (required)
- **Type:** string
- **Description:** Path to CSV file containing primitives data
- **Format:** CSV must have columns: `step,v,r,f,a,S,notes` (or `event`/`time`/`day` instead of `step`)
- **Example:** `"data/singles_dating_Fred.csv"`

**`gamma_self_0`** (required)
- **Type:** complex number
- **Description:** Starting position in γ-space
- **Common values:**
  - `0.0 + 0.0j` - Strangers at origin
  - `5.0 + 3.0j` - Already friends (moderate We/Love)
  - `-3.0 + 8.0j` - Post-conflict but high love
  - `8.0 + 0.0j` - Strong "We" but neutral love/hate
- **Example:** `0.0 + 0.0j`

**`custom_weights`** (optional)
- **Type:** dictionary
- **Description:** Override default weights from CONSTANTS.md
- **Leave empty `{}` to use all defaults**
- **See [Weight Customization](#weight-customization) section below**
- **Example:** `{'w_f': 1.4, 'delS': 0.03}`

##### Single Subject Example:
```python
SUBJECTS = [
    {
        'name': 'Fred',
        'csv_file': 'data/singles_dating_Fred.csv',
        'gamma_self_0': 0.0 + 0.0j,
        'custom_weights': {},
    },
]
```

##### Multiple Subjects (Comparison):
```python
SUBJECTS = [
    {
        'name': 'Fred',
        'csv_file': 'data/singles_dating_Fred.csv',
        'gamma_self_0': 0.0 + 0.0j,
        'custom_weights': {},
    },
    {
        'name': 'Ann',
        'csv_file': 'data/singles_dating_Ann.csv',
        'gamma_self_0': 0.0 + 0.0j,
        'custom_weights': {'w_r': 1.2},  # Ann has higher resonance
    },
]
```

---

### Time Settings

#### `TIME_UNIT` (optional, default: "days")
**Type:** string  
**Description:** What the CSV step column represents  
**Options:** `"days"`, `"weeks"`, `"months"`, `"years"`, `"events"`  
**Example:** `"days"`

This is for interpretation only - used in plot labels and entropy scaling.

#### `TIME_SCALE` (optional, default: 1.0)
**Type:** float  
**Description:** Multiplier for time values  
**Examples:**
- `1.0` - Use CSV time values as-is
- `0.5` - Half speed (60 days becomes 30 days)
- `2.0` - Double speed (60 days becomes 120 days)
- `12.17` - Convert weeks to days (7 * 1.74 ≈ 12.17)

**Use case:** Run same CSV primitives at different time scales to test time sensitivity.

---

### Output Settings

#### `SAVE_PLOTS` (optional, default: True)
**Type:** boolean  
**Description:** Whether to save plots to OUTPUT_DIR  
**Example:** `True`

#### `SHOW_PLOTS` (optional, default: False)
**Type:** boolean  
**Description:** Whether to display plots interactively  
**Example:** `False`

Set to `True` to see plots immediately. Useful during development.

#### `OUTPUT_DIR` (optional, default: "results")
**Type:** string  
**Description:** Directory where results will be saved  
**Example:** `"results"`

Directory will be created if it doesn't exist.

---

### Help Flag

#### `HELP` (optional, default: False)
**Type:** boolean  
**Description:** Set to `True` to display this help and exit without running  
**Example:** `False`

**Usage:**
1. Set `HELP = True`
2. Run your scenario script
3. Read help documentation
4. Set `HELP = False`
5. Configure and run

---

## Weight Customization

The `custom_weights` dictionary in each subject allows you to override default weights from `CONSTANTS.md`.

### Available Weights

#### Axis Weights (Primitives → γ-space axes)

**`w_v`** (default: 0.8)
- **Description:** Visibility weight (real axis)
- **Effect:** How much showing up/being present moves you on Ego↔We axis
- **Example:** `{'w_v': 1.0}` - Increase visibility impact

**`w_r`** (default: 1.0)
- **Description:** Resonance weight (imaginary axis)
- **Effect:** How much attunement/synchrony moves you on Hate↔Love axis
- **Example:** `{'w_r': 1.2}` - Higher resonance sensitivity

**`w_f`** (default: 1.2)
- **Description:** Fidelity weight (imaginary axis, strongest by default)
- **Effect:** How much commitment impacts Love
- **Example:** `{'w_f': 1.4}` - Emphasize commitment importance

**`w_a`** (default: 0.6)
- **Description:** Altruism weight (imaginary axis)
- **Effect:** How much care acts move you on Hate↔Love axis
- **Example:** `{'w_a': 0.8}` - Increase altruism impact

**`w_S_R`** (default: 0.5)
- **Description:** Shared Breath contribution to real axis
- **Effect:** How shared silence affects Ego↔We

**`w_S_I`** (default: 0.5)
- **Description:** Shared Breath contribution to imaginary axis
- **Effect:** How shared silence affects Hate↔Love

#### Entropy Parameters

**`delS`** (default: 0.02)
- **Description:** Entropy drift magnitude per time unit
- **Effect:** How fast relationships decay without maintenance
- **Examples:**
  - `0.01` - Slower decay (more stable relationships)
  - `0.03` - Faster decay (require more effort to maintain)
  - `0.0` - Disable entropy (relationships don't decay)

**`gamma_entropy_attractor`** (default: -8.0+0.0j)
- **Description:** Target position for entropy pull
- **Default:** Far left Ego axis (isolated self-focus)
- **Examples:**
  - `-8.0 + 0.0j` - Default (pull toward Ego)
  - `-8.0 + 5.0j` - Q4 cult scenario (hateful-we pulled toward we/love)
  - `8.0 + 5.0j` - Q1 recovery (healthy ego toward love/connection)
  - `-8.0 - 5.0j` - Q3 despair (isolated ego into enmity)

**`entropy_per_event`** (default: False)
- **Description:** Apply entropy per event (True) or per time unit (False)
- **Effect:** 
  - `False` - Realistic: entropy scaled by time between events
  - `True` - Fixed entropy per event regardless of time spacing

### Example Weight Configurations

**High Commitment Scenario:**
```python
'custom_weights': {
    'w_f': 1.5,    # Emphasize fidelity
    'delS': 0.015,  # Slower decay (commitment stabilizes)
}
```

**Cult Formation (Q4):**
```python
'custom_weights': {
    'gamma_entropy_attractor': -8.0 + 5.0j,  # Pull toward we/love despite hate
    'delS': 0.03,  # Strong pull
}
```

**Fast-Moving Relationship:**
```python
'custom_weights': {
    'w_r': 1.3,    # High resonance
    'w_f': 1.5,    # High fidelity
    'delS': 0.01,  # Low decay (strong bond)
}
```

---

## CSV File Format

Your CSV file should contain relational primitives at each time step.

### Required Columns

- **`step`** (or `event`, `time`, `day`, `time_index`) - Time index
- **`v`** - Visibility primitive [-10 to +10]
- **`r`** - Resonance primitive [-10 to +10]
- **`f`** - Fidelity primitive [-10 to +10]
- **`a`** - Altruism primitive [-10 to +10]
- **`S`** - Shared Breath primitive [-10 to +10]

### Optional Columns

- **`notes`** - Human-readable context for each event
- **`marker`** - Event index for modified events (added by Interactive Editor)
- **`locked`** - Set to "true" for locked events (added by Interactive Editor)

### Example CSV (Basic):

```csv
step,v,r,f,a,S,notes
0,0,0,0,0,0,First meeting at coffee shop
1,5,4,3,2,1,Great conversation
5,6,5,5,4,3,Second date - dinner
10,7,6,6,5,4,First kiss
15,8,7,7,6,5,Meeting friends
20,8,8,8,7,6,Deep conversation about future
```

### Example CSV (With Interactive Editor Metadata):

```csv
name,scenario_name
time_unit,days
gamma_self_0,-5+0j
day,v,r,f,a,S,notes,marker,locked
0,5,0,2,2,0,Initial condition: eager but moderate love,,
7,5,2,2,3,1,First date: strong attraction developing,7,
14,5,-2,2,3,-1,Early wobble: pressing pace - M2 pulls back,14,true
21,5,2,5,5,3,Repair begins: slows down and listens,,
```

**Metadata Notes:**
- `marker` column: Populated with event index for events modified in Interactive Editor
- `locked` column: Set to "true" for events locked in Interactive Editor (prevents dragging)
- Both columns are **optional** - scenarios work fine without them

### Primitive Scale

Primitives use human-intuitive scale of **-10 to +10**:
- `-10` = Maximally negative (betrayal, abandonment, cruelty)
- `0` = Neutral (no event, typical interaction)
- `+10` = Maximally positive (profound moment, breakthrough)

The framework automatically normalizes to [-1, +1] for computation.

---

## Running Scenarios

### Basic Execution
```bash
python scenarios/your_scenario.py
```

### Show Help
Set `HELP = True` in your script and run, or read this document.

### List Available Scenarios
```bash
python -m scenarios.validator --list
```

### Output
- **Console:** Real-time progress, final results summary
- **Plots:** Saved to `OUTPUT_DIR` as PNG files
- **Data:** Trajectory data stored in ScenarioRunner (can be extended)

---

## Troubleshooting

### "Missing required field: SCENARIO_NAME"
You deleted or commented out a required configuration field. Check the template for required fields.

### "CSV file does not exist"
Check the path in `csv_file`. Paths are relative to where you run the script from.

### "CSV missing required column: v"
Your CSV doesn't have the primitives columns. See [CSV File Format](#csv-file-format) above.

### "Output file will be overwritten"
This is just a warning. Previous results will be replaced. Rename old files if you want to keep them.

### Plot doesn't show up
Set `SHOW_PLOTS = True`. Default is `False` to avoid blocking execution.

---

## Advanced Topics

### Comparing Multiple Scenarios
Create multiple scripts with different configurations and run them sequentially. Each produces its own output file.

### Batch Processing
Use a shell script or Python wrapper to run multiple scenarios:

```bash
# PowerShell
Get-ChildItem scenarios/*.py | ForEach-Object { python $_.FullName }
```

### Custom Analysis
The `ScenarioRunner.trajectory` contains full simulation data. You can access it programmatically:

```python
from scenarios.runner import run_scenario
# ... config ...
# Modify runner.py to return results instead of just printing
```

---

## See Also

- **[GRP_rev3.md](GRP_rev3.md)** - Full GRP mathematical specification
- **[CONSTANTS.md](../CONSTANTS.md)** - Default parameter values and ranges
- **[TUNING.md](../TUNING.md)** - Weight calibration guidance
- **[README.md](../README.md)** - Project overview and quick start
- **[scenarios/_TEMPLATE.py](../scenarios/_TEMPLATE.py)** - Copy this to start a new scenario

---

**Questions or issues?** Check the documentation above or examine existing scenario scripts for examples.
