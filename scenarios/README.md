# WhenMathPrays Scenarios

## Overview

Scenarios are structured experiments that explore relationship dynamics using the General Relational Physics (GRP) framework. Each scenario defines primitive event sequences (v, r, f, a, S) that model specific relational contexts—from romantic love to battlefield hate, from parent-child bonds to spiritual practices.

**⚠️ CRITICAL:** Before creating scenarios, read the [Primitive Modeling Guide](../docs/scenarios/primitive_modeling_guide.md). Understanding the M1/M2 perspective framework is essential - this is the #1 source of modeling errors.

## Quick Start

### Running a Scenario

```bash
# Copy the on-disk template, point SUBJECTS at CSVs in data/library/, then:
python scenarios/my_scenario.py
```

Scenarios are Python files next to `_TEMPLATE.py`. There is no `scenarios/library/` directory. CSV primitive sequences live in `data/library/`.

### Creating a New Scenario

1. Copy the template (on disk at `scenarios/_TEMPLATE.py`):
   ```bash
   cp scenarios/_TEMPLATE.py scenarios/my_scenario.py
   ```

2. Edit the configuration section:
   - Update scenario name, author, date
   - Define subjects with CSV file paths
   - Set initial γ_self values
   - Customize weights if needed

3. Fill in the docstring with:
   - Background (what's happening?)
   - Research question (what are you exploring?)
   - Hypothesis (what do you expect?)
   - Validation criteria (how to verify?)

4. Run it (`_TEMPLATE.py` ends with `validate_and_run(globals())`):
   ```bash
   python scenarios/my_scenario.py
   ```

## Directory Structure

```
scenarios/
├── README.md              ← You are here
├── _TEMPLATE.py           ← Copy this to create new scenarios
├── config_schema.py       ← Configuration validation schema
├── validator.py           ← Validates scenario config before run (`validate_and_run(globals())`)
└── runner.py              ← Execution engine
```

CSV libraries (not under `scenarios/`):

```
data/library/
├── love/
├── hate/
├── relational/
└── spiritual/
```

## Available Scenario CSVs

Python scenario scripts are not stored under `scenarios/library/` (that directory does not exist). Primitive CSVs currently on disk:

### Love (`data/library/love/`)
- `single_dating_to_love_M1.csv` / `_M2.csv`
- `romeo_juliet_M1.csv` / `_M2.csv`
- `the_notebook_M1.csv` / `_M2.csv` (and `_mod` variants)
- `mature_love_M1.csv`
- `dog_hachiko_M1.csv`

### Other categories
CSV folders also exist at `data/library/hate/`, `data/library/relational/`, and `data/library/spiritual/`.

## Data Files

CSV files defining primitive sequences are stored in `data/library/` with matching structure:

```
data/
├── library/
│   ├── love/
│   │   ├── single_dating_to_love_M1.csv
│   │   ├── single_dating_to_love_M2.csv
│   │   └── ...
│   ├── hate/
│   ├── relational/
│   └── spiritual/
└── templates/           ← Generic relationship patterns
    ├── betrayal_and_repair.csv
    ├── steady_positive_growth.csv
    └── ...
```

## Understanding Results

Scenarios generate:
- **Trajectory plots** - γ_self movement in complex plane over time
- **CSV outputs** - Numerical trajectory data in `results/`
- **Terminal output** - Summary statistics and validation checks

Key metrics:
- **Final |γ_self|** - Love magnitude at end of scenario
- **Quadrant location** — Q1 (Together + Connection), Q2 (Alone + Connection), Q3 (Alone + Disconnection), Q4 (Together + Disconnection); see [`docs/PRIMITIVES_AND_RELATIONAL_SPACE.md`](../docs/PRIMITIVES_AND_RELATIONAL_SPACE.md)
- **Trajectory shape** - Linear climb, oscillation, saturation, etc.

## Documentation

For deeper understanding of scenario design philosophy, validation criteria, and research methodology, see:

- **[docs/scenarios/README.md](../docs/scenarios/README.md)** - Comprehensive design guide
- **[docs/SCENARIO_CONFIGURATION_GUIDE.md](../docs/SCENARIO_CONFIGURATION_GUIDE.md)** - Configuration details
- **[docs/scenario_generator_requirements.md](../docs/scenario_generator_requirements.md)** - Automated generation specs

## Support Files

- **config_schema.py** - Defines required and optional scenario configuration fields
- **validator.py** - Pre-execution validation (checks CSV files exist, config complete)
- **runner.py** - Execution engine (loads CSV, runs love equation, generates plots)
- **_TEMPLATE.py** - Fully documented template for creating new scenarios

## Tips

1. **Start with templates** - Copy `_TEMPLATE.py` rather than writing from scratch
2. **Use data/templates/** - Pre-built patterns for common relationship dynamics
3. **Document thoroughly** - Future you (and others) will thank you
4. **Validate early** - The validator catches config issues before execution
5. **Compare subjects** - Include multiple subjects in one scenario to contrast trajectories

## Questions?

See [docs/scenarios/README.md](../docs/scenarios/README.md) for detailed design guidance, or start from `_TEMPLATE.py` and CSVs in `data/library/`.
