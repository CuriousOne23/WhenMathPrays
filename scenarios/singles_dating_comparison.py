"""
SCENARIO: Singles Dating to Love - Fred vs Ann (Comparison)
AUTHOR: CuriousOne
DATE: 2025-12-04

BACKGROUND:
Fred and Ann are entering a dating relationship from different starting positions and with
different relational styles. Fred is ego-heavy and eager, pressing the pace initially. Ann
is cautious and guarded, needing more space. Over 60 days, they experience an early wobble
around day 14 when Fred's pace causes Ann to pull back, then both adjust and repair through
day 35, finally stabilizing in healthy connection by day 60.

RESEARCH QUESTION:
How do two people with different attachment styles (eager vs cautious) navigate early dating
dynamics? What does successful repair look like when partners adjust their pacing in response
to each other's needs?

HYPOTHESIS:
Starting from origin (strangers), the comparison will show:
1. Fred moves faster initially (more positive primitives) vs Ann's guarded start
2. Both experience wobble around day 14 (Fred sees partner pullback, Ann feels pressure)
3. Repair phase (days 21-35) shows convergence as both adjust
4. Final trajectories both in Q2 (Ego/Love) with Ann reaching slightly higher love magnitude
5. Fred's ego moderates (less negative real) while Ann's agency rises (more visibility)

VALIDATION CRITERIA:
- Both trajectories should reach Q2 (negative real, positive imaginary)
- Fred should show higher initial primitives than Ann
- Ann should show negative primitives around day 7 (first date pressure)
- Trajectories should converge in repair phase (days 21-35)
- Final love magnitudes: Fred ~0.55, Ann ~0.57 (Ann slightly higher)
- Comparison plot should show distinct paths that converge toward similar outcome

NOTES:
This comparison scenario demonstrates complementary repair dynamics: Fred learns to moderate
pace and ego, Ann learns to trust and engage more actively. The primitives capture how both
partners adjust their behavior in response to each other's needs. This is a realistic model
of successful early relationship navigation with different attachment styles.
"""

# === CONFIGURATION ===

HELP = False  # Set to True to show help documentation and exit

SCENARIO_NAME = "Singles Dating to Love - Fred vs Ann"
AUTHOR = "CuriousOne"
DATE_CREATED = "2025-12-04"

SUBJECTS = [
    {
        'name': 'Fred',
        'csv_file': 'data/single_dating_to_love_M1.csv',
        'gamma_self_0': 0.0 + 0.0j,  # Strangers at origin
        'custom_weights': {},  # Use all default weights
    },
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
