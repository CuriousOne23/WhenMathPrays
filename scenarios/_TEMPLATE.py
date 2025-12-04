# scenarios/_TEMPLATE.py
"""
====================================================================
SCENARIO: [Your Scenario Name Here]
====================================================================

AUTHOR: CuriousOne
DATE: [YYYY-MM-DD]

BACKGROUND:
[Describe the relational scenario you're modeling. What is happening
between the subjects? What is the context?]

RESEARCH QUESTION:
[What specific question are you trying to answer with this scenario?]

HYPOTHESIS:
[What do you expect to see? What trajectory or outcome do you predict?]

VALIDATION CRITERIA:
[How will you know if the model is working correctly?
- What should the final |γ_self| range be?
- What quadrant should subjects end in?
- What patterns should emerge?]

NOTES:
[Any additional context, assumptions, or implementation details]

====================================================================
"""

# === CONFIGURATION (EDIT THIS SECTION) ===

HELP = False  # Set to True to display configuration help

SCENARIO_NAME = "[Your Scenario Name]"
AUTHOR = "CuriousOne"
DATE_CREATED = "2025-12-04"

# Subject(s) to run - add more dictionaries to compare multiple subjects
SUBJECTS = [
    {
        'name': 'Subject1',                      # Subject identifier
        'csv_file': 'data/your_data.csv',        # Path to primitives CSV
        'gamma_self_0': 0.0 + 0.0j,              # Starting position (0+0j = strangers)
        'custom_weights': {},                     # Empty = use all defaults
    },
    # Uncomment to add comparison subject:
    # {
    #     'name': 'Subject2',
    #     'csv_file': 'data/subject2_data.csv',
    #     'gamma_self_0': 0.0 + 0.0j,
    #     'custom_weights': {'w_f': 1.4},        # Higher fidelity weight
    # },
]

# Time interpretation
TIME_UNIT = "days"     # What CSV step column represents: "days", "weeks", "months", "events"
TIME_SCALE = 1.0       # Multiplier: 1.0 = as-is, 0.5 = half speed, 2.0 = double speed

# Output preferences
SAVE_PLOTS = True      # Save plots to OUTPUT_DIR
SHOW_PLOTS = False     # Display plots interactively
OUTPUT_DIR = "results" # Where to save results

# === END CONFIGURATION ===

"""
====================================================================
DO NOT EDIT BELOW THIS LINE
====================================================================
"""

if __name__ == "__main__":
    from scenarios.validator import validate_and_run
    validate_and_run(globals())
