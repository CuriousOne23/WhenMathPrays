# Scenario Design Guide

## Purpose

This directory contains deep documentation for designing, validating, and analyzing WhenMathPrays scenarios. For practical "how to run" information, see [scenarios/README.md](../../scenarios/README.md) in the main codebase.

**⚠️ START HERE:** Read [Primitive Modeling Guide](primitive_modeling_guide.md) first. The M1/M2 perspective framework is non-intuitive and requires deliberate attention - even experienced modelers slip into incorrect "theory of mind" scoring.

## What Are Scenarios?

Scenarios are **structured relational experiments** that explore how primitive events (v, r, f, a, S) combine to produce complex emotional trajectories. Each scenario models a specific relational context—romantic love, battlefield hate, parent-child bonds, spiritual practices—with the goal of validating the Gamma Revenge Protocol (GRP) framework and understanding love/hate dynamics.

## Design Philosophy

### 1. Event-Driven, Not Time-Driven

The love equation operates in **event space**, not time space. Primitives represent discrete relational events:
- **v (visibility)** - "I see you / you see me"
- **r (resonance)** - "We vibe / we're in sync"
- **f (fidelity)** - "I'm faithful / I follow through"
- **a (agency)** - "I act / I take initiative"
- **S (soul presence)** - "I'm authentically present"

Time mapping is applied **after** event sequence generation. One scenario might sample daily, another weekly, another at irregular intervals.

### 2. Primitives Are Valence-Neutral

Primitives measure **engagement intensity**, not direction. A high visibility (v) event could be:
- Looking into someone's eyes with love
- Glaring at someone with hate

The γ_self **angle** (quadrant location) determines whether engagement manifests as love or hate. Primitives modulate magnitude, not polarity.

### 3. Quadrants Define Relational Mode

```
        Imaginary Axis (Love/Sorrow)
                  |
         Q2       |       Q1
    (Ego/Love)    |    (Safety/Ego)
                  |
------------------+------------------ Real Axis (Safety/Sorrow)
                  |
         Q3       |       Q4
   (Love/Sorrow)  |  (Sorrow/Safety)
                  |
```

- **Q1 (Safety/Ego)** - Secure attachment, healthy boundaries (mature love, parent/child)
- **Q2 (Ego/Love)** - Passionate engagement, risk-taking (Romeo & Juliet, new love)
- **Q3 (Love/Sorrow)** - Grief, loss, longing (breakup, death of loved one)
- **Q4 (Sorrow/Safety)** - Withdrawal, protection, healing

Hate dynamics typically appear in **negative real** space (opposite of Q1/Q4 safety).

## Scenario Structure

### Required Elements

Every scenario must define:

1. **SCENARIO_NAME** - Clear, descriptive title
2. **AUTHOR** - Who created this scenario
3. **DATE_CREATED** - When it was created
4. **SUBJECTS** - List of subjects with:
   - `name` - Subject identifier
   - `csv_file` - Path to primitive data (relative to project root)
   - `gamma_self_0` - Initial γ_self (complex number)
   - `custom_weights` - Optional weight overrides (dict)

### Recommended Documentation

The scenario docstring should answer:

**BACKGROUND:** What's the relational situation?
- Context, characters, dynamics
- What's happening between subjects?

**RESEARCH QUESTION:** What are you exploring?
- Specific question the scenario addresses
- What aspect of GRP you're testing

**HYPOTHESIS:** What do you expect?
- Predicted trajectory shape
- Expected quadrant progression
- Final γ_self magnitude range

**VALIDATION CRITERIA:** How do you know it's working?
- Specific metrics (final |γ_self|, quadrant location)
- Trajectory shape expectations
- Qualitative patterns to look for

**NOTES:** Additional context
- Assumptions, limitations
- Implementation details
- Literature references

## Creating Scenarios

### Step 1: Define the Context

Start with a clear relational situation:
- **Romeo & Juliet**: Forbidden love, intense passion, high stakes
- **Battlefield Hate**: Combat dynamics, enemy engagement
- **Parent/Child**: Unconditional love, safety provision

### Step 2: Design Primitive Sequences

Create CSV files in `data/library/[category]/` with columns:
```
time, v, r, f, a, S
```

Primitive values:
- **Human scale:** [-10, +10] - intuitive
- **Computer scale:** [0, 1] - normalized
- **Conversion:** `(human / 20) + 0.5`

Use `data/templates/` for common patterns:
- `steady_positive_growth.csv` - Linear increase
- `betrayal_and_repair.csv` - Trust violation → recovery
- `oscillatory_style.csv` - On-again/off-again dynamics

### Step 3: Set Initial Conditions

Define `gamma_self_0` based on starting relationship:
- **Strangers:** `0.0 + 0.0j` (origin)
- **Established bond:** Non-zero (appropriate quadrant)
- **Post-conflict:** Negative real (sorrow/threat)

### Step 4: Choose Weights (Optional)

Default weights work for most scenarios. Customize only if modeling specific dynamics:
- `c` (breath efficacy): How quickly primitives integrate
- Primitive weights: Relative importance of v, r, f, a, S

See [TUNING.md](../TUNING.md) for weight guidelines.

### Step 5: Define Validation Criteria

Be specific:
- ❌ "Should show love"
- ✅ "Final |γ_self| should reach 0.55-0.65 (moderate love)"
- ✅ "Trajectory should enter Q2 by event 10, stabilize in Q1 by event 30"

## Validation Process

The `validator.py` checks:
1. Required fields present
2. CSV files exist
3. gamma_self_0 is valid complex number
4. Subjects list is non-empty

**Manual validation** (your responsibility):
1. Does trajectory match hypothesis?
2. Does final |γ_self| fall in expected range?
3. Does quadrant progression make sense?
4. Do results align with research question?

## Directory Structure

```
docs/scenarios/
├── README.md                    ← You are here
└── library/                     ← Individual scenario documentation
    ├── love/
    │   ├── romeo_juliet.md      ← Deep dive on Romeo & Juliet
    │   └── ...
    ├── hate/
    │   └── battlefield_rambo.md
    ├── relational/
    │   ├── parent_child.md
    │   └── breakup.md
    └── spiritual/
        └── buddha.md
```

Each individual scenario document contains:
- Research literature/film references
- Detailed analysis of results
- Comparison with other scenarios
- Lessons learned

## Scenario Categories

### Love Scenarios

Model positive engagement, bonding, romantic dynamics:
- Singles dating, Romeo & Juliet, mature love
- Focus on Q1/Q2 trajectories
- High positive primitives

### Hate Scenarios

Model conflict, combat, adversarial dynamics:
- Battlefield hate, group/organizational hate
- Focus on negative real space
- High primitives but negative γ_self real component

### Relational Scenarios

Model non-romantic bonds and transitions:
- Parent/child, friendship, breakup
- Varied quadrant usage
- Context-dependent primitive patterns

### Spiritual Scenarios

Model spiritual practices, self-love, transcendence:
- Meditation, prayer, self-compassion
- Often starting at origin, moving to Q1
- Soul presence (S) emphasized

## Best Practices

### DO:
- ✅ Document thoroughly (hypothesis, validation criteria)
- ✅ Start with existing templates
- ✅ Use human-readable primitive scales
- ✅ Include multiple subjects for comparison
- ✅ Version control your CSV files
- ✅ Record actual results vs. hypothesis

### DON'T:
- ❌ Skip validation criteria
- ❌ Use time scale without event justification
- ❌ Modulate primitive polarity by quadrant (they're valence-neutral)
- ❌ Assume default weights work for extreme cases
- ❌ Forget to check final trajectory against hypothesis

## Advanced Topics

### Multi-Subject Scenarios

Compare different starting conditions or primitive sequences:
```python
SUBJECTS = [
    {'name': 'Ann', 'csv_file': 'data/.../ann.csv', 'gamma_self_0': 0.0},
    {'name': 'Fred', 'csv_file': 'data/.../fred.csv', 'gamma_self_0': 0.0},
]
```

### Custom Weights

Override specific weights for targeted exploration:
```python
'custom_weights': {
    'c': 0.3,  # Slower integration
    'w_v': 2.0,  # Double visibility impact
}
```

### Time Interpretation

Map event space to real time:
```python
TIME_UNIT = "days"      # or "weeks", "months", "events"
TIME_SCALE = 1.0        # Multiply CSV time values
```

## Related Documentation

- **[SCENARIO_CONFIGURATION_GUIDE.md](../SCENARIO_CONFIGURATION_GUIDE.md)** - Detailed config options
- **[scenario_generator_requirements.md](../scenario_generator_requirements.md)** - Automated generation
- **[TUNING.md](../TUNING.md)** - Weight tuning guidance
- **[ARCHITECTURE.md](../ARCHITECTURE.md)** - Overall system design

## Research Questions

Scenarios help answer:
- How do different primitive patterns produce love vs. hate?
- What distinguishes healthy (Q1) from passionate (Q2) love?
- How does betrayal (fidelity drop) affect trajectories?
- What role does soul presence play in bonding?
- Can hate dynamics be transformed into love? Under what conditions?

Each scenario is an experiment. Document, measure, iterate.

## Contributing Scenarios

To contribute a new scenario:

1. Design and validate locally
2. Document thoroughly (docstring + separate .md file)
3. Run and record results
4. Compare results vs. hypothesis
5. Place in appropriate category (`library/love/`, etc.)
6. Update `scenarios/README.md` with your scenario in the list

Quality over quantity. One well-documented, validated scenario > ten undocumented experiments.
