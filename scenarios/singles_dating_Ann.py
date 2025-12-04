"""
SCENARIO: Singles Dating to Love - Ann
AUTHOR: CuriousOne
DATE: 2025-12-04

BACKGROUND:
Ann is entering the same dating relationship as Fred, but from a more cautious starting position.
Over 60 days, Ann starts guarded (cautious but with some baseline love), feels pressure on the
first date and pulls back, then gradually warms as Fred adjusts pacing. The trajectory shows
agency rising and love strengthening as safety is established.

RESEARCH QUESTION:
How does a cautious person navigate early dating when their partner initially presses too fast?
Can trust develop after an early wobble if the partner adjusts their approach?

HYPOTHESIS:
Starting from origin (strangers), Ann's trajectory will show:
1. Minimal movement initially, guarded stance (low primitives)
2. Pullback around day 7 (first date pressure causes negative primitives)
3. Slow warming from day 21 onward as Fred slows pace
4. Steady rise in Q2 (Ego/Love) with stronger final love magnitude than Fred by day 60

VALIDATION CRITERIA:
- Trajectory should show Q2 movement (negative real, positive imaginary)
- Early pullback visible (days 7-14) with low or negative primitives
- Recovery visible from day 21 onward with increasing primitives
- Final love magnitude should reach ~0.57-0.60 range (slightly higher than Fred)
- Agency should rise (visibility/resonance increase) after trust established

NOTES:
This scenario demonstrates a cautious attachment style responding to pace adjustment.
The primitives reflect guarded initial state, pressure response (negative values day 7),
then gradual opening as safety is demonstrated through Fred's behavioral changes.
"""

# === CONFIGURATION ===

HELP = False  # Set to True to show help documentation and exit

SCENARIO_NAME = "Singles Dating to Love - Ann"
AUTHOR = "CuriousOne"
DATE_CREATED = "2025-12-04"

SUBJECTS = [
    {
        'name': 'Ann',
        'csv_file': 'data/single_dating_to_love_M2.csv',
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
