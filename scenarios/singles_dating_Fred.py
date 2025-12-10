"""
SCENARIO: Singles Dating to Love - Fred
AUTHOR: CuriousOne
DATE: 2025-12-04

BACKGROUND:
Fred is entering a dating relationship starting from initial attraction (strangers at origin).
Over 60 days, Fred shows eager but moderate initial love, experiences an early wobble when
pressing the pace too fast, then repairs by slowing down and listening. The trajectory shows
ego moderation and love rising as trust develops.

RESEARCH QUESTION:
How does a person with ego-heavy tendencies navigate early dating dynamics when their partner
needs more space? Can repair occur through pacing adjustments and active listening?

HYPOTHESIS:
Starting from origin (strangers), Fred's trajectory will show:
1. Rapid movement toward love (positive imaginary) in first week
2. Wobble around day 14 when pressing pace causes partner pullback
3. Repair phase (days 21-35) as Fred slows down and listens
4. Stabilization in Q2 (Ego/Love) with rising love magnitude through day 60

VALIDATION CRITERIA:
- Trajectory should show Q2 movement (negative real, positive imaginary)
- Wobble should be visible around day 14 (dip or lateral movement)
- Final love magnitude should reach ~0.55-0.60 range
- Ego should moderate (real component become less negative) over time

NOTES:
This scenario uses primitives that reflect ego moderation: visibility stays consistent,
resonance shows the wobble and recovery, fidelity increases steadily, altruism grows as
Fred learns to listen, and Shared Breath increases as comfort develops.
"""

# === CONFIGURATION ===

HELP = False  # Set to True to show help documentation and exit

SCENARIO_NAME = "Singles Dating to Love - Fred"
AUTHOR = "CuriousOne"
DATE_CREATED = "2025-12-04"

SUBJECTS = [
    {
        'name': 'Fred',
        'csv_file': 'data/single_dating_to_love_M1.csv',
        'gamma_self_0': 0.0 + 0.0j,  # Strangers at origin
        'custom_weights': {},  # Use all default weights
    },
]

# Time interpretation
TIME_UNIT = "days"
TIME_SCALE = 1.0  # Use CSV time values as-is

# Output preferences
SAVE_PLOTS = True
SHOW_PLOTS = False
OUTPUT_DIR = "results"

# === END CONFIGURATION ===

if __name__ == "__main__":
    from scenarios.validator import validate_and_run
    validate_and_run(globals())
