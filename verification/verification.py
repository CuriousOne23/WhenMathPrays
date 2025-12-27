#!/usr/bin/env python3
"""
Automated Verification Script for WhenMathPrays Interactive Editor

This script provides automated verification capabilities by parsing and validating
state logs to ensure they contain expected operations and structure.

Usage:
    python verification.py entropy_verification_state_log_20251217_145008.log

The script will:
1. Parse the state log file
2. Validate log structure and completeness
3. Check for expected operation patterns
4. Report verification status
"""

import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import required modules for basic validation
from tools.editor.debug_config import get_logger

_logger = get_logger('verification')

@dataclass
class LogValidationResult:
    """Result of log validation."""
    is_valid: bool
    total_operations: int
    operation_types: Dict[str, int]
    warnings: List[str]
    errors: List[str]
    session_info: Dict[str, str]

class LogValidator:
    """Validates state log files for structure and completeness."""

    def __init__(self, log_file: Path):
        self.log_file = log_file

    def validate_log(self) -> LogValidationResult:
        """Validate the log file structure and content."""
        result = LogValidationResult(
            is_valid=True,
            total_operations=0,
            operation_types={},
            warnings=[],
            errors=[],
            session_info={}
        )

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Validate header
            self._validate_header(content, result)

            # Count operations
            self._count_operations(content, result)

            # Validate operation structure
            self._validate_operations(content, result)

            # Check for warnings/errors in log
            self._check_warnings_errors(content, result)

        except Exception as e:
            result.is_valid = False
            result.errors.append(f"Failed to parse log file: {e}")

        return result

    def _validate_header(self, content: str, result: LogValidationResult):
        """Validate log header contains required information."""
        # Check for session info
        session_match = re.search(r'Session:\s*([^\n]+)', content)
        if session_match:
            result.session_info['session'] = session_match.group(1)

        python_match = re.search(r'Python:\s*([^\n]+)', content)
        if python_match:
            result.session_info['python'] = python_match.group(1)

        platform_match = re.search(r'Platform:\s*([^\n]+)', content)
        if platform_match:
            result.session_info['platform'] = platform_match.group(1)

        # Check for loaded files
        m1_match = re.search(r'M1:\s*([^\n]+)', content)
        if m1_match:
            result.session_info['m1_file'] = m1_match.group(1)

        m2_match = re.search(r'M2:\s*([^\n]+)', content)
        if m2_match:
            result.session_info['m2_file'] = m2_match.group(1)

        # Check total operations
        total_match = re.search(r'Total operations:\s*(\d+)', content)
        if total_match:
            result.session_info['total_operations'] = total_match.group(1)

        warnings_match = re.search(r'Warnings:\s*(\d+)', content)
        if warnings_match:
            result.session_info['warnings'] = warnings_match.group(1)

    def _count_operations(self, content: str, result: LogValidationResult):
        """Count operations by type."""
        # Find all operation blocks
        operation_pattern = r'\[(\d+)\]\s+(\w+)'
        matches = re.findall(operation_pattern, content)

        result.total_operations = len(matches)

        for _, op_type in matches:
            result.operation_types[op_type] = result.operation_types.get(op_type, 0) + 1

    def _validate_operations(self, content: str, result: LogValidationResult):
        """Validate operation structure."""
        # Check that operations have required fields
        operation_blocks = re.findall(
            r'\[(\d+)\]\s+(\w+)\s+Time:\s+([^\n]+)\s+Entity:\s+([^\n]+)\s+Location:\s+([^\n]+)\s+Changes:\s+([^[\n]+)',
            content,
            re.MULTILINE | re.DOTALL
        )

        if len(operation_blocks) != result.total_operations:
            result.warnings.append(
                f"Found {len(operation_blocks)} complete operations but {result.total_operations} operation headers"
            )

        # Validate operation numbers are sequential (allowing for non-starting-at-1)
        op_numbers = [int(match[0]) for match in operation_blocks]
        if op_numbers:
            min_op = min(op_numbers)
            max_op = max(op_numbers)
            expected_count = max_op - min_op + 1

            if len(op_numbers) != expected_count:
                result.warnings.append(
                    f"Operation numbers not sequential: expected {expected_count} operations, found {len(op_numbers)}"
                )

            # Check for duplicates
            if len(set(op_numbers)) != len(op_numbers):
                result.errors.append("Duplicate operation numbers found")

    def _check_warnings_errors(self, content: str, result: LogValidationResult):
        """Check for warnings and errors in the log content."""
        warning_count = len(re.findall(r'\bWARNING\b', content, re.IGNORECASE))
        error_count = len(re.findall(r'\bERROR\b', content, re.IGNORECASE))

        if warning_count > 0:
            result.warnings.append(f"Found {warning_count} warnings in log")

        if error_count > 0:
            result.errors.append(f"Found {error_count} errors in log")

def validate_interactive_editor_functionality(result: LogValidationResult) -> List[tuple[str, bool]]:
    """Validate that the log contains expected interactive editor operations."""
    rules = []

    # Required operation types for interactive editor functionality
    required_operations = {
        'redo_edit_primitive': 'Drag primitive operations',
        'redo_reset_primitive': 'Double-click reset operations',
        'redo_insert_event_before': 'Insert time primitive operations',
        'switch_perspective': 'M1/M2 perspective switching',
        'undo_reset_primitive': 'Undo reset operations (CTRL+Z)',
        'undo_edit_primitive': 'Undo edit operations (CTRL+Z)',
        'undo_insert_event_before': 'Undo insert operations (CTRL+Z)',
    }

    operation_types = result.operation_types

    # Check for each required operation type
    for op_type, description in required_operations.items():
        has_operation = operation_types.get(op_type, 0) > 0
        rules.append((f"Has {description}", has_operation))

    # Additional validation rules
    total_operations = result.total_operations
    rules.append(("Has sufficient operations (>100)", total_operations > 100))

    # Check for dual perspective support
    has_m1 = 'm1_file' in result.session_info
    has_m2 = 'm2_file' in result.session_info
    rules.append(("Dual perspective support (M1 & M2)", has_m1 and has_m2))

    # Check for clean execution
    warnings_in_session = result.session_info.get('warnings', '0')
    has_no_warnings = warnings_in_session == '0'
    rules.append(("Clean execution (no warnings)", has_no_warnings))

    return rules

def run_verification(log_file: Path) -> Dict[str, Any]:
    """Run the complete verification process."""
    _logger.info(f"Starting verification for log: {log_file.name}")

    validator = LogValidator(log_file)
    result = validator.validate_log()

    # Additional validation rules
    validation_rules = [
        ("Has session info", bool(result.session_info)),
        ("Has operations", result.total_operations > 0),
        ("No errors in log", len(result.errors) == 0),
        ("Operations are sequential", len(result.warnings) == 0 or "sequential" not in str(result.warnings)),
    ]

    # Special validation for interactive editor functionality verification
    if 'interactive_editor_functionality' in log_file.name:
        interactive_rules = validate_interactive_editor_functionality(result)
        validation_rules.extend(interactive_rules)

    # Overall validation
    overall_valid = result.is_valid and len(result.errors) == 0

    verification_results = {
        'status': 'PASSED' if overall_valid else 'FAILED',
        'log_file': str(log_file),
        'validation_result': {
            'is_valid': result.is_valid,
            'total_operations': result.total_operations,
            'operation_types': result.operation_types,
            'warnings': result.warnings,
            'errors': result.errors,
            'session_info': result.session_info
        },
        'validation_rules': validation_rules,
        'overall_valid': overall_valid
    }

    _logger.info(f"Verification complete: {verification_results['status']}")
    return verification_results

def main():
    """Main entry point for verification script."""
    parser = argparse.ArgumentParser(description='Automated verification for WhenMathPrays')
    parser.add_argument('log_file', help='Path to the state log file for verification')

    args = parser.parse_args()

    # Determine log file path
    log_path = Path(args.log_file)
    if not log_path.is_absolute():
        # Assume it's in the verification directory
        verification_dir = Path(__file__).parent
        log_path = verification_dir / args.log_file

    if not log_path.exists():
        print(f"ERROR: Log file not found: {log_path}")
        sys.exit(1)

    # Run verification
    results = run_verification(log_path)

    # Print results
    print("\n" + "="*60)
    print("VERIFICATION RESULTS")
    print("="*60)
    print(f"Status: {results['status']}")
    print(f"Log File: {results['log_file']}")

    session = results['validation_result']['session_info']
    if 'session' in session:
        print(f"Session: {session['session']}")
    if 'total_operations' in session:
        print(f"Total Operations: {session['total_operations']}")
    if 'warnings' in session:
        print(f"Warnings: {session['warnings']}")

    print(f"Operations Found: {results['validation_result']['total_operations']}")

    if results['validation_result']['operation_types']:
        print("\nOperation Breakdown:")
        for op_type, count in sorted(results['validation_result']['operation_types'].items()):
            print(f"  {op_type}: {count}")

    if results['validation_result']['warnings']:
        print(f"\nWarnings ({len(results['validation_result']['warnings'])}):")
        for warning in results['validation_result']['warnings']:
            print(f"  - {warning}")

    if results['validation_result']['errors']:
        print(f"\nErrors ({len(results['validation_result']['errors'])}):")
        for error in results['validation_result']['errors']:
            print(f"  - {error}")

    print("\nValidation Rules:")
    for rule_name, passed in results['validation_rules']:
        status = "✓" if passed else "✗"
        print(f"  {status} {rule_name}")

    print("="*60)

    # Exit with appropriate code
    sys.exit(0 if results['overall_valid'] else 1)

if __name__ == '__main__':
    main()