# scenarios/validator.py
"""
Validation and help system for GRP scenario configurations.
Validates config before execution and provides help documentation.
"""

import sys
from pathlib import Path
from typing import Dict, Any
import pandas as pd

from scenarios.config_schema import (
    REQUIRED_FIELDS, OPTIONAL_FIELDS, SUBJECT_FIELDS,
    CSV_REQUIRED_COLUMNS, CSV_TIME_COLUMN_ALIASES
)


def validate_and_run(config_globals: Dict[str, Any]):
    """
    Validate scenario configuration and run if valid.
    
    Args:
        config_globals: globals() dictionary from scenario script
    """
    # Check for help flag
    if config_globals.get('HELP', False):
        show_help()
        sys.exit(0)
    
    # Validate configuration
    errors = validate_config(config_globals)
    
    if errors:
        print("=" * 70)
        print("CONFIGURATION ERRORS")
        print("=" * 70)
        for error in errors:
            print(f"❌ {error}")
        print("=" * 70)
        print("\nFix the errors above and try again.")
        print("Set HELP = True in your scenario script for configuration guidance.")
        sys.exit(1)
    
    # Check for warnings (non-fatal issues)
    warnings = check_warnings(config_globals)
    if warnings:
        print("=" * 70)
        print("WARNINGS")
        print("=" * 70)
        for warning in warnings:
            print(f"⚠️  {warning}")
        print("=" * 70)
        print()
    
    # Configuration valid, proceed to runner
    from scenarios.runner import run_scenario
    run_scenario(config_globals)


def validate_config(config: Dict[str, Any]) -> list:
    """
    Validate scenario configuration.
    
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    # Check required fields
    for field, spec in REQUIRED_FIELDS.items():
        if field not in config:
            errors.append(f"Missing required field: {field}")
            continue
        
        value = config[field]
        expected_type = spec['type']
        
        if not isinstance(value, expected_type):
            errors.append(
                f"{field} must be {expected_type.__name__}, got {type(value).__name__}"
            )
    
    # Validate SUBJECTS if present
    if 'SUBJECTS' in config:
        subjects = config['SUBJECTS']
        
        if not isinstance(subjects, list):
            errors.append("SUBJECTS must be a list")
        elif len(subjects) == 0:
            errors.append("SUBJECTS list cannot be empty")
        else:
            for i, subject in enumerate(subjects):
                subject_errors = validate_subject(subject, i)
                errors.extend(subject_errors)
    
    # Validate optional fields if present
    for field, spec in OPTIONAL_FIELDS.items():
        if field in config:
            value = config[field]
            expected_type = spec['type']
            
            if value is not None and not isinstance(value, expected_type):
                errors.append(
                    f"{field} must be {expected_type.__name__}, got {type(value).__name__}"
                )
    
    return errors


def validate_subject(subject: Any, index: int) -> list:
    """Validate a single subject configuration."""
    errors = []
    prefix = f"SUBJECTS[{index}]"
    
    if not isinstance(subject, dict):
        errors.append(f"{prefix} must be a dictionary")
        return errors
    
    # Check required subject fields
    for field, spec in SUBJECT_FIELDS.items():
        if spec['required'] and field not in subject:
            errors.append(f"{prefix} missing required field: {field}")
            continue
        
        if field in subject:
            value = subject[field]
            expected_type = spec['type']
            
            # Special handling for complex numbers
            if expected_type == complex:
                if not isinstance(value, (complex, int, float)):
                    errors.append(
                        f"{prefix}.{field} must be a complex number, got {type(value).__name__}"
                    )
            elif not isinstance(value, expected_type):
                errors.append(
                    f"{prefix}.{field} must be {expected_type.__name__}, got {type(value).__name__}"
                )
    
    # Validate CSV file exists
    if 'csv_file' in subject:
        csv_path = Path(subject['csv_file'])
        if not csv_path.exists():
            errors.append(f"{prefix}.csv_file does not exist: {subject['csv_file']}")
        else:
            # Validate CSV structure
            csv_errors = validate_csv(csv_path, prefix)
            errors.extend(csv_errors)
    
    return errors


def validate_csv(csv_path: Path, prefix: str) -> list:
    """Validate CSV file structure."""
    errors = []
    
    try:
        df = pd.read_csv(csv_path)
        
        # Check for time column (flexible name)
        time_col = None
        for alias in CSV_TIME_COLUMN_ALIASES:
            if alias in df.columns:
                time_col = alias
                break
        
        if time_col is None:
            errors.append(
                f"{prefix}.csv_file missing time column (expected one of: {', '.join(CSV_TIME_COLUMN_ALIASES)})"
            )
        
        # Check for required primitive columns
        for col in CSV_REQUIRED_COLUMNS:
            if col not in df.columns and col != 'step':  # 'step' is handled by time_col check
                errors.append(f"{prefix}.csv_file missing required column: {col}")
        
        # Check for at least one row of data
        if len(df) == 0:
            errors.append(f"{prefix}.csv_file contains no data rows")
        
    except Exception as e:
        errors.append(f"{prefix}.csv_file could not be read: {str(e)}")
    
    return errors


def check_warnings(config: Dict[str, Any]) -> list:
    """
    Check for non-fatal issues that should warn the user.
    
    Returns:
        List of warning messages
    """
    warnings = []
    
    # Check if output file will be overwritten
    if 'SCENARIO_NAME' in config and config.get('SAVE_PLOTS', True):
        output_dir = Path(config.get('OUTPUT_DIR', 'results'))
        scenario_name = config['SCENARIO_NAME']
        
        # Sanitize filename
        safe_name = "".join(c for c in scenario_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        
        output_file = output_dir / f"{safe_name}.png"
        if output_file.exists():
            warnings.append(f"Output file will be overwritten: {output_file}")
    
    # Check for unusual time scales
    time_scale = config.get('TIME_SCALE', 1.0)
    if time_scale < 0.1 or time_scale > 10.0:
        warnings.append(f"Unusual TIME_SCALE value: {time_scale} (typically 0.1 to 10.0)")
    
    return warnings


def show_help():
    """Display configuration help documentation."""
    help_file = Path(__file__).parent.parent / "docs" / "SCENARIO_CONFIGURATION_GUIDE.md"
    
    if help_file.exists():
        print(help_file.read_text(encoding='utf-8'))
    else:
        # Fallback inline help if file doesn't exist
        print("""
====================================================================
SCENARIO CONFIGURATION HELP
====================================================================

Help file not found: docs/SCENARIO_CONFIGURATION_GUIDE.md

Basic configuration structure:

SCENARIO_NAME = "Your Scenario Name"
AUTHOR = "CuriousOne"
DATE_CREATED = "2025-12-04"

SUBJECTS = [
    {
        'name': 'Fred',
        'csv_file': 'data/your_data.csv',
        'gamma_self_0': 0.0 + 0.0j,
        'custom_weights': {},
    },
]

TIME_UNIT = "days"
TIME_SCALE = 1.0

SAVE_PLOTS = True
SHOW_PLOTS = False
OUTPUT_DIR = "results"

For detailed documentation, see:
  - docs/GRP_rev3.md      - Full GRP specification
  - CONSTANTS.md          - Default parameter values
  - TUNING.md             - Weight calibration guidance
  - scenarios/_TEMPLATE.py - Copy this to start a new scenario

====================================================================
""")


def list_scenarios():
    """List all available scenario scripts."""
    scenarios_dir = Path(__file__).parent
    scripts = sorted(scenarios_dir.glob("*.py"))
    
    print("=" * 70)
    print("AVAILABLE SCENARIOS")
    print("=" * 70)
    
    for script in scripts:
        if script.name.startswith('_') or script.name in ['validator.py', 'runner.py', 'config_schema.py']:
            continue
        
        print(f"  • {script.name}")
    
    print("=" * 70)
    print(f"\nRun with: python scenarios/scenario_name.py")
    print("=" * 70)


if __name__ == "__main__":
    # Allow running validator standalone
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--list', '-l', 'list']:
            list_scenarios()
        else:
            print("Usage: python -m scenarios.validator --list")
    else:
        print("Usage: python -m scenarios.validator --list")
