#!/usr/bin/env python3
"""
Interactive Editor Performance Validation Script

This script validates performance characteristics of DEBUGGING AND VALIDATION INFRASTRUCTURE
components of the interactive editor. It measures the speed of low-level validation functions
used for AI-assisted debugging of time/index synchronization issues.

PURPOSE:
- Track performance of debugging utilities, not user interface operations
- Detect regressions in validation infrastructure after code changes
- Ensure debugging tools remain fast and reliable for AI assistance
- Provide performance baseline for baseline communication protocol functions

SCOPE:
- Currently tests baseline protocol validation functions as representative sample
- Uses synthetic data representing debugging scenarios
- Measures on-demand validation performance (not real-time UI operations)
- Framework designed for future expansion to additional debugging components

Usage:
    python verification/interactive_editor_performance_validation.py

The script will:
1. Test baseline protocol validation functions with synthetic data
2. Run performance benchmarks against established baselines
3. Report performance deltas and validation status
4. Flag potential regressions for investigation

This serves as a quick performance sanity check for debugging infrastructure after any code modifications.
"""

import sys
import os
import time
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import required modules
from tools.editor.baseline_protocol import BaselineDebugLog

@dataclass
class PerformanceResult:
    """Result of a performance test."""
    function_name: str
    data_size: int
    avg_time_ms: float
    delta_from_baseline: float = 0.0

@dataclass
class ValidationResult:
    """Result of validation testing."""
    function_name: str
    test_passed: bool
    details: str
    performance_results: List[PerformanceResult] = None

class MockEvent:
    """Mock event for testing."""
    def __init__(self, time: float):
        self.time = time

class InteractiveEditorValidator:
    """Validates debugging and validation infrastructure performance.

    This class specifically measures the performance of low-level validation functions
    used for AI-assisted debugging of time/index synchronization issues. It does NOT
    measure user interface performance or real-time editor operations.

    Currently focuses on baseline protocol validation functions as a representative sample
    of debugging infrastructure. Future versions may expand to include additional
    debugging/validation components while maintaining this focused purpose.
    """

    def __init__(self):
        self.baseline_performance = self._load_baseline_performance()

    def _load_baseline_performance(self) -> Dict[str, Dict[int, float]]:
        """
        Load baseline performance data for regression detection.

        ⚠️  CRITICAL WARNING FOR DEVELOPERS ⚠️
        ======================================

        DO NOT MODIFY THESE BASELINE NUMBERS unless you have:
        1. Confirmed a significant, permanent performance change
        2. Run tests multiple times (5+ runs) for statistical significance
        3. Updated the documentation in interactive_editor_performance_baseline.md
        4. Committed both files together with detailed explanation

        IF YOU ARE TEMPTED TO CHANGE THESE NUMBERS:
        - STOP! Read interactive_editor_performance_baseline.md first
        - Ask: "Is this a real performance change or just noise?"
        - Ask: "Have I followed the proper change process?"
        - Ask: "Will this break future regression detection?"

        BASELINE PERFORMANCE DATA STORAGE:
        ================================
        This data is hardcoded in the script for simplicity and reliability.
        It represents established performance measurements from December 18, 2025.

        DATA FORMAT:
        -----------
        {function_name: {data_size: expected_time_ms, ...}, ...}

        Where:
        - function_name: Name of the validation function being tested
        - data_size: Number of synthetic events used in the test (10, 100, 1000, 10000)
        - expected_time_ms: Expected execution time in milliseconds (averaged over 10 runs)

        WHAT THE NUMBERS REPRESENT:
        --------------------------
        These are wall-clock execution times for debugging/validation functions:
        - validate_consistency: Checks time/index synchronization consistency
        - snapshot_mappings: Creates time<->index mapping dictionaries
        - check_marker_consistency: Validates marker positions against events

        The data sizes represent different scenario scales:
        - 10 events: Small debugging scenarios
        - 100 events: Medium debugging scenarios
        - 1000 events: Large debugging scenarios
        - 10000 events: Stress testing for debugging infrastructure

        UPDATING BASELINES:
        ------------------
        Only update these numbers when establishing NEW baseline measurements after:
        1. Significant performance improvements
        2. Hardware/environment changes
        3. Establishing initial baselines for new functions

        CHANGE PROCESS:
        1. Run tests multiple times (5+ runs) for statistical significance
        2. Update this hardcoded dictionary
        3. Update interactive_editor_performance_baseline.md documentation
        4. Commit both files with clear explanation
        5. Test that changes don't break functionality

        DOCUMENTATION REQUIREMENTS:
        - Update baseline date and measurements in .md file
        - Explain reason for change in commit message
        - Link to related issues/PRs documenting the performance investigation

        DO NOT CHANGE these numbers for:
        - Temporary performance fluctuations
        - Different hardware (use environment-specific baselines)
        - Minor code changes that shouldn't affect performance
        """
        # ⚠️  BASELINE PERFORMANCE MEASUREMENTS - DO NOT MODIFY WITHOUT CAUTION ⚠️
        # These numbers represent established performance baselines from December 18, 2025
        # Format: {function_name: {num_events: expected_ms, ...}}
        # Source: interactive_editor_performance_baseline.md
        #
        # BEFORE CHANGING: Read the change process in interactive_editor_performance_baseline.md
        # ASK YOURSELF: Is this a significant, permanent change? Is it reproducible? Is it expected?
        return {
            # validate_consistency: Checks event count, time ordering, bounds
            'validate_consistency': {
                10: 0.01,      # 10 events: ~0.01ms expected
                100: 0.02,     # 100 events: ~0.02ms expected
                1000: 0.15,    # 1000 events: ~0.15ms expected
                10000: 1.06    # 10000 events: ~1.06ms expected
            },
            # snapshot_mappings: Creates time<->index mapping dictionaries
            'snapshot_mappings': {
                10: 0.01,      # 10 events: ~0.01ms expected
                100: 0.01,     # 100 events: ~0.01ms expected
                1000: 0.11,    # 1000 events: ~0.11ms expected
                10000: 1.29    # 10000 events: ~1.29ms expected
            },
            # check_marker_consistency: Validates marker positions vs events
            'check_marker_consistency': {
                10: 0.01,      # 10 events: ~0.01ms expected
                100: 0.10,     # 100 events: ~0.10ms expected
                1000: 0.63,    # 1000 events: ~0.63ms expected
                10000: 7.17    # 10000 events: ~7.17ms expected
            }
        }

    def create_test_data(self, size: int) -> tuple:
        """Create test data for validation."""
        events = [MockEvent(i * 0.1) for i in range(size)]
        # Create markers for all events, not just min(100, size)
        marker_positions = {(i * 0.1, 'v'): i for i in range(size)}
        return events, marker_positions

    def benchmark_function(self, func_name: str, func, *args, runs: int = 10) -> PerformanceResult:
        """Benchmark a function and return performance result."""
        # Extract data size based on function
        if func_name == 'validate_consistency':
            data_size = args[2]  # gamma_length parameter
        elif func_name == 'snapshot_mappings':
            data_size = len(args[1]) if len(args) > 1 else 0  # events parameter
        elif func_name == 'check_marker_consistency':
            data_size = len(args[1]) if len(args) > 1 else 0  # events parameter
        else:
            data_size = 0

        # Run benchmark
        start_time = time.time()
        for _ in range(runs):
            func(*args)
        total_time = time.time() - start_time
        avg_time_ms = (total_time / runs) * 1000

        # Calculate delta from baseline
        baseline_time = self.baseline_performance.get(func_name, {}).get(data_size, 0)
        delta = ((avg_time_ms - baseline_time) / baseline_time * 100) if baseline_time > 0 else 0

        return PerformanceResult(func_name, data_size, avg_time_ms, delta)

    def validate_consistency_function(self) -> ValidationResult:
        """Test the validate_consistency function."""
        try:
            # Test with good data
            events, _ = self.create_test_data(10)
            result = BaselineDebugLog.validate_consistency('M1', events, 10)

            if not result['is_consistent']:
                return ValidationResult('validate_consistency', False, "Failed consistency check on valid data")

            # Test with bad data (non-monotonic times)
            bad_events = [MockEvent(1.0), MockEvent(0.5)]  # Out of order
            result = BaselineDebugLog.validate_consistency('M1', bad_events, 2)

            if result['is_consistent']:
                return ValidationResult('validate_consistency', False, "Should have detected time ordering issue")

            # Performance test
            perf_results = []
            for size in [10, 100, 1000]:
                events, _ = self.create_test_data(size)
                perf = self.benchmark_function('validate_consistency',
                                             BaselineDebugLog.validate_consistency,
                                             'M1', events, size)
                perf_results.append(perf)

            return ValidationResult('validate_consistency', True,
                                  "All tests passed", perf_results)

        except Exception as e:
            return ValidationResult('validate_consistency', False, f"Exception: {e}")

    def validate_snapshot_function(self) -> ValidationResult:
        """Test the snapshot_mappings function."""
        try:
            events, _ = self.create_test_data(10)
            result = BaselineDebugLog.snapshot_mappings('M1', events)

            # Check structure
            required_keys = ['perspective', 'timestamp', 'time_to_index', 'index_to_time', 'event_count']
            for key in required_keys:
                if key not in result:
                    return ValidationResult('snapshot_mappings', False, f"Missing key: {key}")

            if result['event_count'] != 10:
                return ValidationResult('snapshot_mappings', False, "Incorrect event count")

            # Check mappings
            if len(result['time_to_index']) != 10 or len(result['index_to_time']) != 10:
                return ValidationResult('snapshot_mappings', False, "Incorrect mapping sizes")

            # Performance test
            perf_results = []
            for size in [10, 100, 1000]:
                events, _ = self.create_test_data(size)
                perf = self.benchmark_function('snapshot_mappings',
                                             BaselineDebugLog.snapshot_mappings,
                                             'M1', events)
                perf_results.append(perf)

            return ValidationResult('snapshot_mappings', True,
                                  "All tests passed", perf_results)

        except Exception as e:
            return ValidationResult('snapshot_mappings', False, f"Exception: {e}")

    def validate_marker_function(self) -> ValidationResult:
        """Test the check_marker_consistency function."""
        try:
            events, marker_positions = self.create_test_data(10)
            result = BaselineDebugLog.check_marker_consistency('M1', marker_positions, events)

            # Check structure
            required_keys = ['perspective', 'marker_count', 'valid_markers', 'invalid_markers', 'issues']
            for key in required_keys:
                if key not in result:
                    return ValidationResult('check_marker_consistency', False, f"Missing key: {key}")

            # Performance test
            perf_results = []
            for size in [10, 100]:
                events, marker_positions = self.create_test_data(size)
                perf = self.benchmark_function('check_marker_consistency',
                                             BaselineDebugLog.check_marker_consistency,
                                             'M1', marker_positions, events)
                perf_results.append(perf)

            return ValidationResult('check_marker_consistency', True,
                                  "All tests passed", perf_results)

        except Exception as e:
            return ValidationResult('check_marker_consistency', False, f"Exception: {e}")

    def run_validation(self) -> List[ValidationResult]:
        """Run all validation tests."""
        print("Running Interactive Editor Performance Validation...")
        print("=" * 50)

        results = []
        results.append(self.validate_consistency_function())
        results.append(self.validate_snapshot_function())
        results.append(self.validate_marker_function())

        return results

    def print_results(self, results: List[ValidationResult]):
        """
        Print validation results and performance deltas.

        ⚠️  PASS/FAIL CRITERIA REMINDER ⚠️
        ===================================

        IMPORTANT: This script reports performance deltas for MONITORING purposes only.
        It does NOT fail tests based on performance thresholds by design.

        - PASS/FAIL is based on FUNCTIONAL CORRECTNESS only
        - Performance regressions are flagged for investigation but don't break builds
        - This prevents false failures from normal system variation (±10%)

        If you want to change this behavior, see:
        - interactive_editor_performance_baseline.md for threshold rationale
        - Consider --strict-performance flag for CI/CD environments

        PASS/FAIL CRITERIA:
        ==================
        Current Implementation:
        - PASS/FAIL based solely on FUNCTIONAL CORRECTNESS (does the validation work?)
        - Performance deltas are REPORTED for monitoring but do NOT cause test failure
        - This allows performance regression tracking without breaking CI/CD on minor variations

        Performance Threshold Logic:
        - Minor variations (±10%): Expected due to system load, caching, measurement precision
        - Significant regressions (>+10%): Flag for investigation (currently informational only)
        - Critical regressions (>+50%): Immediate attention required (currently informational only)

        Why No Automatic Failure on Performance?
        ----------------------------------------
        1. Development environment variation (CPU load, background processes)
        2. Measurement precision (±1-2% typical for millisecond timing)
        3. Caching effects and JIT compilation warmup
        4. Focus on functional correctness as hard requirement
        5. Performance monitoring as trend analysis, not binary pass/fail

        Future Enhancement:
        Consider adding --strict-performance flag to enforce thresholds in CI/CD environments
        with more controlled testing conditions.
        """
        print("\nValidation Results:")
        print("=" * 50)

        all_passed = True
        for result in results:
            status = "✓ PASS" if result.test_passed else "✗ FAIL"
            print(f"{result.function_name}: {status}")
            print(f"  Details: {result.details}")

            if result.performance_results:
                print("  Performance:")
                for perf in result.performance_results:
                    delta_str = f" ({perf.delta_from_baseline:+.1f}%)" if perf.delta_from_baseline != 0 else ""
                    print(f"    {perf.data_size} items: {perf.avg_time_ms:.2f}ms{delta_str}")

            if not result.test_passed:
                all_passed = False
            print()

        print("=" * 50)
        overall_status = "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"
        print(f"Overall: {overall_status}")

        return all_passed

def main():
    """Main validation function."""
    validator = InteractiveEditorValidator()
    results = validator.run_validation()
    success = validator.print_results(results)

    # Return appropriate exit code for CI/CD
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()