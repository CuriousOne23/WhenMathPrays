"""
Test script to verify ObservabilityLog functionality.
"""

from observability import ObservabilityLog

# Test 1: Disabled by default
print("Test 1: ObservabilityLog disabled by default")
print(f"  is_enabled(): {ObservabilityLog.is_enabled()}")
ObservabilityLog.event("test_event", test_data="should not appear")
print(f"  get_log_file(): {ObservabilityLog.get_log_file()}")
print()

# Test 2: Enable explicitly
print("Test 2: Enable ObservabilityLog explicitly")
ObservabilityLog.initialize(enabled=True)
print(f"  is_enabled(): {ObservabilityLog.is_enabled()}")
print(f"  get_log_file(): {ObservabilityLog.get_log_file()}")
print()

# Test 3: Log some events
print("Test 3: Log structured events")
ObservabilityLog.section("=== TEST SECTION ===")
ObservabilityLog.event("application_start", input_path="test.csv")
ObservabilityLog.event("perspective_switch", old="M1", new="M2", label_count=5)
ObservabilityLog.event("add_marker_label", 
                       event_time=42.0, 
                       primitive="Volatility",
                       value=0.8,
                       perspective="M2")
print("  Events logged successfully")
print()

# Test 4: Check log file was created
import pathlib
log_file = ObservabilityLog.get_log_file()
if log_file and pathlib.Path(log_file).exists():
    print(f"Test 4: Log file created successfully")
    print(f"  Path: {log_file}")
    with open(log_file, 'r') as f:
        content = f.read()
    print(f"  Size: {len(content)} bytes")
    print(f"  Lines: {len(content.splitlines())}")
    print()
    print("  First 500 characters:")
    print(content[:500])
else:
    print("Test 4: FAILED - Log file not created")

print("\nAll tests complete!")
