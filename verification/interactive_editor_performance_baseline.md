# Interactive Editor Performance Baseline

## Overview

This file contains baseline performance measurements for **debugging and validation infrastructure** components of the interactive editor. These measurements serve as a reference point for detecting performance regressions in the baseline communication protocol validation functions after code changes, refactoring, or architecture modifications.

## Scope and Purpose

**What This Measures:**
- Performance of low-level validation functions used for debugging time/index synchronization issues
- On-demand debugging utilities that AIs and developers use to validate coordinate space consistency
- Infrastructure performance, not user interface responsiveness

**What This Does NOT Measure:**
- Full user interface scenarios (moving primitives, inserting events, etc.)
- User interaction response times
- GUI rendering performance
- Real-time editor operations

**Current Focus:** Baseline protocol validation functions as a representative sample. Future versions may expand to include additional interactive editor debugging components.

## Test Environment

- **Date**: December 18, 2025
- **Platform**: Windows 11
- **Python Version**: 3.14.1
- **Hardware**: Standard development workstation

## Baseline Performance Measurements

Performance tests were conducted with synthetic data across different scenario sizes. Each measurement represents the average of 10 runs.

### Baseline Protocol Validation Functions (milliseconds)

| Data Size | validate_consistency | snapshot_mappings | check_marker_consistency | Total |
|-----------|---------------------|------------------|------------------------|-------|
| 10 events | 0.01 | 0.01 | 0.01 | 0.03 |
| 100 events | 0.02 | 0.01 | 0.10 | 0.13 |
| 1,000 events | 0.15 | 0.11 | 0.63 | 0.89 |
| 10,000 events | 1.06 | 1.29 | 7.17 | 9.52 |

### Test Methodology

- **validate_consistency**: Tests event count matching, time ordering, and bounds validation
- **snapshot_mappings**: Creates time↔index mapping dictionaries
- **check_marker_consistency**: Validates marker positions against event data (uses 100 markers for larger tests)
- **Measurements**: Wall-clock time in milliseconds, averaged over 10 runs each
- **Data**: Synthetic events with times 0.0, 0.1, 0.2, ... and neutral primitive values

### Performance Characteristics

- **Scaling**: Linear with data size (O(N) complexity)
- **Overhead**: Effectively zero during normal operation (functions called on-demand only)
- **Memory**: Temporary allocations only, no persistent state
- **Comparison**: 2-3 orders of magnitude faster than trajectory computation

## Usage After Code Changes

Run this validation after any significant code changes to detect performance impact:

```bash
# After code changes, refactoring, or architecture modifications
python verification/interactive_editor_performance_validation.py

# Check for performance regressions in the output deltas
# Investigate any significant positive deltas (>+10%)
```

## Future Performance Tracking

When running performance tests in the future:

1. Use the same test methodology (10 runs average, same data patterns)
2. Compare against these baseline numbers
3. Flag any regression >10% for investigation
4. Update this file when significant performance changes occur

### Baseline Data Storage and Updates

**Storage Location**: Performance baseline data is hardcoded in `verification/interactive_editor_performance_validation.py` in the `_load_baseline_performance()` method for simplicity and reliability.

## ⚠️ CRITICAL WARNINGS FOR FUTURE DEVELOPERS

**Before making ANY changes to performance baselines or criteria:**

### 🚨 RED FLAGS - STOP AND THINK

**❌ NEVER change baselines because:**
- "The tests are failing and I need to make them pass"
- "I made a small change and performance got worse"
- "The numbers look wrong to me"
- "CI/CD is failing and I need a quick fix"
- "I don't understand why the numbers are what they are"

**❌ NEVER change thresholds because:**
- "The current thresholds are too strict/lenient"
- "I want different pass/fail behavior"
- "The numbers don't make sense to me"
- "I need the tests to behave differently"

### ✅ ONLY change when ALL of these are true:
- You have investigated and confirmed a **real, significant performance change**
- The change is **reproducible across multiple test runs**
- You have **documented evidence** of the root cause
- The change is **expected and beneficial** (not a regression)
- You have followed the **complete change process** below

### 🛡️ SAFEGUARDS AGAINST COMMON MISTAKES

**If you're considering changing baselines:**
1. **STOP** - Don't make the change yet
2. **INVESTIGATE** - Run tests 5+ times, check environment, verify methodology
3. **DOCUMENT** - Write down exactly what changed and why
4. **REVIEW** - Have someone else verify your findings
5. **TEST** - Ensure changes don't break anything else

**If performance tests are "failing":**
- **Don't change baselines** - investigate why performance changed
- Check: Environment differences? Code changes? Hardware issues?
- Document findings before considering any baseline updates

**If you inherit this code and don't understand it:**
- **READ THIS DOCUMENT FIRST** - Don't assume you know what to change
- **ASK QUESTIONS** - Contact original authors or team members
- **TEST CAREFULLY** - Don't make changes without understanding impact

### Decision Framework: When to Change

**❓ Questions to Ask Before Making Changes:**

1. **Is this a significant, permanent change?**
   - Expected: Yes - performance improvement, hardware upgrade, new baseline establishment
   - Unexpected: No - temporary fluctuation, minor code change, environment variation

2. **Is the change reproducible across multiple runs?**
   - Expected: Yes - consistent measurements over 5+ runs, same environment
   - Unexpected: No - sporadic results, environment-dependent

3. **Is the change meaningful (>10% delta)?**
   - Expected: Yes - represents real performance change beyond measurement noise
   - Unexpected: No - within normal variation (±10%)

4. **Does this affect the core purpose (debugging infrastructure performance)?**
   - Expected: Yes - changes to validation/debugging functions, not UI performance
   - Unexpected: No - UI changes that shouldn't affect debugging tools

5. **Is this change expected and beneficial?**
   - Expected: Yes - performance improvement, optimization, hardware upgrade
   - Unexpected: No - unexpected regression, unexplained slowdown

### Best Practices for Changes

**✅ DO:**
- Run tests multiple times (minimum 5 runs) to establish statistical significance
- Use same environment/hardware as original baseline measurements
- Document the reason for change with specific measurements
- Update both code and documentation in the same commit
- Test that changes don't break existing functionality
- Consider impact on CI/CD and automated testing

**❌ DON'T:**
- Update baselines for minor fluctuations or one-off measurements
- Change thresholds without clear rationale and testing
- Update baselines without updating documentation
- Make changes based on single test runs
- Change pass/fail criteria without team discussion

### Process for Making Changes

**Phase 1: Investigation**
1. Observe consistent performance change over multiple runs
2. Verify change is reproducible across different test sessions
3. Confirm change is meaningful (>10% from baseline)
4. Identify root cause (code change, environment, hardware)

**Phase 2: Validation**
1. Run comprehensive performance tests (5-10 sessions)
2. Calculate statistical significance of results
3. Verify change doesn't break functional correctness
4. Document all measurements and conditions

**Phase 3: Implementation**
1. Update hardcoded baseline data in `verification/interactive_editor_performance_validation.py`
2. Update this documentation file with new measurements and date
3. Update any related comments explaining the change
4. Test that updated script works correctly

**Phase 4: Documentation & Review**
1. Create commit with clear message explaining the change
2. Update any related issue/PR documentation
3. Notify team of baseline changes
4. Monitor for any unexpected side effects

### Where to Record Changes

**Primary Documentation:**
- `verification/interactive_editor_performance_baseline.md` - Update baseline table, date, and change rationale
- `verification/interactive_editor_performance_validation.py` - Update hardcoded data and comments

**Secondary Documentation:**
- Git commit message - Explain what changed and why
- Related issues/PRs - Link to performance investigation
- `verification/README.md` - Update if process changes

**Change Log Format:**
```markdown
## Baseline Update: [Date]

**Reason:** [Brief explanation - e.g., "Performance improvement from algorithm optimization"]

**Measurements:**
- Environment: [Hardware, OS, Python version]
- Test runs: [Number of runs averaged]
- Statistical significance: [Confidence level]

**Changes:**
- validate_consistency: [old]ms → [new]ms ([+/-X%])
- snapshot_mappings: [old]ms → [new]ms ([+/-X%])
- check_marker_consistency: [old]ms → [new]ms ([+/-X%])

**Validation:** [How change was verified - functional tests passed, etc.]
```

### Changing Pass/Fail Criteria

**When to Change Thresholds:**
- New performance testing practices adopted
- Different hardware/environment requirements
- Experience shows current thresholds are inappropriate
- Changes to testing methodology

**Process for Threshold Changes:**
1. **Justification**: Document why current thresholds don't work
2. **Research**: Review industry standards and similar projects
3. **Testing**: Validate new thresholds with historical data
4. **Implementation**: Update code and documentation
5. **Communication**: Explain changes to team and stakeholders

**Threshold Change Documentation:**
```markdown
## Threshold Update: [Date]

**Previous Thresholds:**
- Minor: ±[old]%
- Significant: >+[old]%
- Critical: >+[old]%

**New Thresholds:**
- Minor: ±[new]%
- Significant: >+[new]%
- Critical: >+[new]%

**Rationale:** [Detailed explanation of why thresholds changed]

**Validation:** [How new thresholds were tested and validated]
```

## 🛡️ FINAL SAFEGUARDS

**If you find yourself wanting to change these baselines or thresholds:**

1. **STOP** - Don't make the change
2. **READ** - This entire document from top to bottom
3. **QUESTION** - Ask yourself if this meets ALL the criteria above
4. **VERIFY** - Run multiple tests, document everything
5. **REVIEW** - Have someone else check your work
6. **DOCUMENT** - Follow the exact change log format

**Remember:** These baselines protect against performance regressions. Changing them incorrectly can hide real performance problems or create false alarms. When in doubt, preserve the existing baselines and investigate the root cause instead.

**Contact:** If you're unsure about any aspect of performance baseline management, contact the original authors or team leads before making changes.

### Understanding Performance Deltas

When the validation script reports performance deltas, they are calculated as:

```
delta = ((current_time - baseline_time) / baseline_time) * 100
```

**Interpreting Delta Values:**
- **Negative delta (-X%)**: Current performance is **X% faster** than baseline (improvement)
- **Positive delta (+X%)**: Current performance is **X% slower** than baseline (regression)  
- **Zero delta (0%)**: Performance matches baseline exactly

**Examples:**
- `-50%`: Current run is 50% faster than baseline (2x improvement)
- `+25%`: Current run is 25% slower than baseline (4/5 the speed)
- `0%`: No change from baseline

**Regression Thresholds:**
- **Minor**: ±10% (normal variation, acceptable)
- **Significant**: >+10% (investigate potential performance regression)
- **Critical**: >+50% (immediate investigation required)

**Why These Thresholds?**
- **±10% Minor threshold**: Accounts for normal system variation (CPU load, caching, measurement precision, background processes)
- **>+10% Significant threshold**: Indicates potential performance regression requiring investigation
- **>+50% Critical threshold**: Suggests major performance degradation needing immediate attention
- **Rationale**: Based on typical software performance testing practices where 10% represents meaningful change beyond noise, while allowing for expected variation in development environments

**Note**: Small variations (±10%) are normal due to system load, caching, and measurement precision. Only consistent significant regressions should trigger concern.

## Maintaining Fidelity and Purpose

**Core Purpose:** This baseline tracks performance of debugging/validation infrastructure functions, not user interface performance. The focus is on ensuring that AI-assisted debugging tools remain fast and reliable.

**Fidelity Guidelines:**
- Keep measurements focused on debugging utilities, not UI operations
- Use synthetic data that represents debugging scenarios, not user workflows
- Maintain on-demand execution model (functions called only when debugging)
- Preserve linear O(N) scaling expectations for validation functions

**Future Expansion Considerations:**
- When adding new performance tests, clearly document whether they measure debugging infrastructure or UI performance
- Consider separate baselines for different categories (debugging vs. UI vs. computation)
- Update this documentation when expanding scope to maintain clarity
- Ensure new tests follow the same synthetic data and controlled benchmarking approach

## Validation Functions Tested

- `BaselineDebugLog.validate_consistency(perspective, events, gamma_length)`
- `BaselineDebugLog.snapshot_mappings(perspective, events)`
- `BaselineDebugLog.check_marker_consistency(perspective, marker_positions, events)`

See `docs/baseline_communication_protocol.md` for detailed function documentation.