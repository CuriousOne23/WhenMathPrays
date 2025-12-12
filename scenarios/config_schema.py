# scenarios/config_schema.py
"""
Configuration schema for GRP scenario scripts.
Single source of truth for all configuration options.
"""

REQUIRED_FIELDS = {
    'SCENARIO_NAME': {
        'type': str,
        'description': 'Descriptive name for this research scenario',
        'example': '"Singles Dating to Love - Fred"',
    },
    'AUTHOR': {
        'type': str,
        'description': 'Your name or identifier',
        'example': '"CuriousOne"',
    },
    'SUBJECTS': {
        'type': list,
        'description': 'List of subjects, each with: name, csv_file, gamma_self_0, custom_weights',
        'example': "[{'name': 'Fred', 'csv_file': 'data/singles_Fred.csv', 'gamma_self_0': 0.0+0.0j, 'custom_weights': {}}]",
    },
}

OPTIONAL_FIELDS = {
    'HELP': {
        'type': bool,
        'default': False,
        'description': 'Set to True to display configuration help and exit',
        'example': 'False',
    },
    'DATE_CREATED': {
        'type': str,
        'default': None,
        'description': 'When this scenario configuration was created',
        'example': '"2025-12-04"',
    },
    'TIME_UNIT': {
        'type': str,
        'default': 'days',
        'description': 'What the CSV step column represents: "days", "weeks", "months", "years", "events"',
        'example': '"days"',
    },
    'TIME_SCALE': {
        'type': float,
        'default': 1.0,
        'description': 'Multiplier for time values (1.0 = as-is, 0.5 = half speed, 2.0 = double speed)',
        'example': '1.0',
    },
    'SAVE_PLOTS': {
        'type': bool,
        'default': True,
        'description': 'Save plots to OUTPUT_DIR',
        'example': 'True',
    },
    'SHOW_PLOTS': {
        'type': bool,
        'default': False,
        'description': 'Display plots interactively',
        'example': 'False',
    },
    'OUTPUT_DIR': {
        'type': str,
        'default': 'results',
        'description': 'Directory where results will be saved',
        'example': '"results"',
    },
}

SUBJECT_FIELDS = {
    'name': {
        'required': True,
        'type': str,
        'description': 'Subject identifier (e.g., "Fred", "Ann")',
    },
    'csv_file': {
        'required': True,
        'type': str,
        'description': 'Path to CSV file containing primitives (step,v,r,f,a,S,notes)',
    },
    'gamma_self_0': {
        'required': True,
        'type': complex,
        'description': 'Starting position in γ-space (e.g., 0.0+0.0j for strangers)',
    },
    'custom_weights': {
        'required': False,
        'type': dict,
        'description': 'Dictionary of weight overrides (empty {} uses defaults from CONSTANTS.md)',
    },
}

AVAILABLE_WEIGHTS = {
    'w_v': {
        'default': 0.8,
        'description': 'Visibility weight (real axis)',
    },
    'w_r': {
        'default': 1.0,
        'description': 'Resonance weight (imaginary axis)',
    },
    'w_f': {
        'default': 1.2,
        'description': 'Fidelity weight (imaginary axis, strongest by default)',
    },
    'w_a': {
        'default': 0.6,
        'description': 'Altruism weight (imaginary axis)',
    },
    'w_S_R': {
        'default': 0.5,
        'description': 'Shared Breath contribution to real axis',
    },
    'w_S_I': {
        'default': 0.5,
        'description': 'Shared Breath contribution to imaginary axis',
    },
    'delS': {
        'default': 0.02,
        'description': 'Entropy drift magnitude per time unit',
    },
    'gamma_entropy_attractor': {
        'default': '-8.0+0.0j',
        'description': 'Target position for entropy pull (default: far left Ego axis)',
    },
    'entropy_per_event': {
        'default': False,
        'description': 'Apply entropy per event (True) or per time unit (False)',
    },
}

CSV_REQUIRED_COLUMNS = ['step', 'v', 'r', 'f', 'a', 'S']
CSV_OPTIONAL_COLUMNS = ['notes']
CSV_TIME_COLUMN_ALIASES = ['step', 'event', 'time', 'day', 'week', 'month', 'year', 'time_index']
