# WhenMathPrays Scenarios

## Overview

Scenarios are structured experiments that explore relationship dynamics using the Gamma Revenge Protocol (GRP) framework. Each scenario defines primitive event sequences (v, r, f, a, S) that model specific relational contexts—from romantic love to battlefield hate, from parent-child bonds to spiritual practices.

**⚠️ CRITICAL:** Before creating scenarios, read the [Primitive Modeling Guide](../docs/scenarios/primitive_modeling_guide.md). Understanding the M1/M2 perspective framework is essential - this is the #1 source of modeling errors.

## Quick Start

### Running a Scenario

```bash
# Run a specific scenario
python scenarios/library/love/romeo_juliet.py

# Run from project root
python -m scenarios.library.love.romeo_juliet
```

### Creating a New Scenario

1. Copy the template:
   ```bash
   cp scenarios/_TEMPLATE.py scenarios/library/love/my_scenario.py
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

4. Run it:
   ```bash
   python scenarios/library/love/my_scenario.py
   ```

## Directory Structure

```
scenarios/
├── README.md              ← You are here
├── _TEMPLATE.py           ← Copy this to create new scenarios
├── config_schema.py       ← Configuration validation schema
├── validator.py           ← Validates scenario config before run
├── runner.py              ← Execution engine
└── library/               ← Curated scenario collection
    ├── love/              ← Romantic love scenarios
    ├── hate/              ← Conflict and hate dynamics
    ├── relational/        ← Non-romantic bonds (parent/child, breakup)
    └── spiritual/         ← Spiritual practices (Buddha, meditation)
```

## Available Scenarios

### Love Scenarios (`library/love/`)
- **Singles Dating** - Two strangers navigate early dating dynamics
- **Romeo & Juliet** - Intense forbidden love (coming soon)
- **The Notebook** - Classic love story arc (coming soon)
- **Ego Love (Saturday Night Fever)** - Self-focused love (coming soon)
- **Mature Love** - Q1 quadrant mature bond (coming soon)
- **Dog Faithfulness (Hachiko)** - Unconditional loyalty (coming soon)

### Hate Scenarios (`library/hate/`)
- **Battlefield (Rambo)** - Combat hate dynamics (coming soon)
- **Group Company Hate** - Communal/organizational hate (coming soon)

### Relational Scenarios (`library/relational/`)
- **Parent/Child** - Q1 quadrant bond (coming soon)
- **Breakup** - Relationship dissolution (coming soon)

### Spiritual Scenarios (`library/spiritual/`)
- **Buddha** - Spiritual practice dynamics (coming soon)

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
- **Quadrant location** - Q1 (safety/ego), Q2 (ego/love), Q3 (love/sorrow), Q4 (sorrow/safety)
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

See [docs/scenarios/README.md](../docs/scenarios/README.md) for detailed design guidance, or check existing scenarios in `library/` for working examples.
