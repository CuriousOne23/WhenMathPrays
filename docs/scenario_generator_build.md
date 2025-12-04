# Scenario Generator - Build Plan

**Date:** December 3, 2025  
**Status:** Architecture & Requirements Phase

---

## Overview

The scenario generator creates CSV files for relationship trajectory simulations with flexible time units, extensible timelines, and various emotional arc templates. This document captures the architectural requirements and phased implementation plan.

---

## Core Requirements

### 1. Time Unit Flexibility
- **Supported Units:** days, weeks, months, years
- **Fractional Units:** Handle inputs like "2.5 weeks" or "3.5 months" (convert to base unit)
- **User-Controlled:** Users can specify time unit when generating scenario
- **Convertible:** Users can change time units after creation (days → weeks → months → years)

### 2. Timeline Extension
- **Add Before:** Users can add time points before day 0 (prehistory, negative time values)
- **Add After:** Users can extend timeline beyond initial endpoint
- **Non-Contiguous:** Support gaps in timeline (not every day/week must have an event)
- **Dynamic:** Timeline length determined by scenario type and user preferences

### 3. Time Unit Selection Logic
When user doesn't specify, auto-select based on duration:
- **< 100 days** → use days
- **100-700 days (~14-100 weeks)** → use weeks
- **> 700 days (~2+ years)** → use months
- **> 3650 days (~10+ years)** → use years

User can always override auto-selection.

### 4. CSV Format Enhancement
Add `time_unit` metadata row (similar to existing `name` row):

```csv
name,Slow Burn Romance
time_unit,weeks
day,v,r,f,a,S,notes,marker,locked
0,2,1,2,1,0,Initial meeting,,*
4,3,2,3,2,1,First month together,circle,
12,5,4,5,4,3,Growing connection,star,
24,7,6,7,6,5,Falling in love,,*
```

**Notes:**
- Column still named `day` (legacy compatibility)
- `time_unit` metadata indicates what the values represent
- Default to "days" if `time_unit` not specified (backward compatible)

---

## Phased Implementation

### Phase 1: Core CSV Time Metadata (Foundation)
**Priority:** FIRST - everything else builds on this

**Changes:**
1. Update CSV format specification in README
2. Modify `simulations/run_scenario.py`:
   - `_load_csv()` reads `time_unit` metadata (like it reads `name`)
   - Store time_unit in ScenarioRunner instance
   - Use time_unit for axis labels in plots (e.g., "Time (weeks)" instead of hardcoded "Day")
   - Default to "days" if not present
3. Update existing template CSVs to include `time_unit,days` metadata
4. Test with single_dating scenarios

**Benefits:**
- Backward compatible (old CSVs without time_unit still work)
- Foundation for all time-related features
- Improves plot clarity

---

### Phase 2: Time Unit Conversion Utility
**Priority:** SECOND - enables user flexibility

**Create:** `tools/convert_time_units.py`

**Functionality:**
```python
def convert_time_units(input_csv, output_csv, target_unit):
    """
    Convert time units in a scenario CSV.
    
    Args:
        input_csv: Path to source CSV
        output_csv: Path to save converted CSV
        target_unit: 'days', 'weeks', 'months', or 'years'
    
    Conversion factors:
        1 week = 7 days
        1 month = 30 days (approximate)
        1 year = 365 days
    
    Process:
        1. Read input CSV with name and time_unit metadata
        2. Determine current time unit from metadata
        3. Calculate conversion factor (current → target)
        4. Multiply all time column values by conversion factor
        5. Round to appropriate precision (whole numbers for days, 1 decimal for weeks/months/years)
        6. Update time_unit metadata to target_unit
        7. Write output CSV with all other data preserved
    """
```

**Example Usage:**
```bash
python tools/convert_time_units.py data/scenario.csv data/scenario_weeks.csv weeks
```

**Features:**
- Preserves name, markers, locked status, primitives, notes
- Handles both integer and fractional time values
- Updates time_unit metadata automatically
- Command-line interface for easy use

**Edge Cases:**
- Non-contiguous time points (just convert each individually)
- Negative time values (prehistory) - conversion works the same
- Fractional results (2.3 weeks) - preserve 1 decimal place

---

### Phase 3: Timeline Extension Support
**Priority:** THIRD - enhances existing scenarios

**Changes to `simulations/run_scenario.py`:**
1. **Support Negative Time Values:**
   - Allow `day` column to have negative values (e.g., -14, -7, 0, 7, 14)
   - Interpret as time before the "reference point" (day 0)
   - Useful for "what led up to this moment" scenarios

2. **Support Non-Contiguous Timelines:**
   - Don't assume every day/week has an event
   - Fill gaps with last-known primitive values (hold constant until next event)
   - Or: linear interpolation between events (user preference)

3. **Update Plot Labels:**
   - X-axis shows negative values if present
   - Timeline starts at min(time) not 0

**Use Cases:**
- "Two weeks before they met..." (negative time)
- Monthly check-ins over years (sparse timeline)
- Key events only (wedding, crisis, resolution) with gaps

**Implementation:**
```python
def _interpolate_timeline(self, df):
    """
    Fill gaps in timeline between specified events.
    
    Options:
        - hold: Use last-known values until next event
        - linear: Linear interpolation between events
        - zero: Fill gaps with zeros (baseline state)
    """
```

---

### Phase 4: Scenario Generator
**Priority:** FOURTH - automation tool

**Create:** `tools/scenario_generator.py`

**Input Parameters:**
```python
def generate_scenario(
    name: str,              # Scenario name
    duration: float,        # e.g., 77, 2.5, 12
    time_unit: str,         # 'days', 'weeks', 'months', 'years'
    arc_type: str,          # Template shape (see Arc Types below)
    num_events: int = None, # Number of time points (auto if None)
    perspective: str = 'single' # 'single', 'dual' (creates M1+M2)
) -> str:                   # Returns path to created CSV(s)
```

**Arc Types (Templates):**
1. **slow_burn** - Gradual increase from low to high
2. **hot_start_cold_finish** - High intensity declining to low
3. **steady_growth** - Linear positive progression
4. **rocky_but_committed** - Oscillating with net positive trend
5. **toxic_spiral** - Descending into negativity
6. **u_shape_recovery** - Down then back up (crisis → repair)
7. **plateau** - Quick rise then steady maintenance
8. **oscillatory** - Sustained cycling (up/down patterns)

**Auto-Event Calculation:**
If `num_events` not specified:
- **Days:** 1 event per 7 days (weekly snapshots)
- **Weeks:** 1 event per 4 weeks (monthly snapshots)
- **Months:** 1 event per month
- **Years:** 1 event per 3 months (quarterly)

**Fractional Duration Handling:**
- Convert to base unit in days
- Example: 2.5 weeks → 17.5 days → round to 18 days
- Or: Keep as 2.5 time units with fractional time points (0, 0.5, 1.0, 1.5, 2.0, 2.5)

**Dual Perspective (M1/M2):**
When `perspective='dual'`:
- Generate two CSVs: `{name}_M1.csv` and `{name}_M2.csv`
- Apply asymmetry patterns:
  - **Pursuer/Withdrawer:** M1 increases while M2 decreases (or vice versa)
  - **Convergent:** Both move toward each other at different rates
  - **Divergent:** Both move apart at different rates
  - **Leader/Follower:** M1 changes first, M2 follows with delay

**Locked Points:**
- Always lock first and last time points (structural anchors)
- Optionally lock key turning points (user can customize later)

**Markers:**
- Place markers at key trajectory points (start, midpoint, crisis, resolution, end)
- User can customize which points get markers

**Output:**
```csv
name,Generated Slow Burn Romance
time_unit,weeks
day,v,r,f,a,S,notes,marker,locked
0.0,2,1,2,1,0,Initial meeting,star,*
2.0,3,2,3,2,1,Early dating,,
4.0,4,3,4,3,2,Growing interest,circle,
8.0,6,5,6,5,4,Deepening connection,,
12.0,7,6,7,6,5,Falling in love,star,*
```

**Command-Line Interface:**
```bash
# Generate single perspective
python tools/scenario_generator.py \
  --name "Summer Romance" \
  --duration 12 \
  --time-unit weeks \
  --arc slow_burn \
  --output data/summer_romance.csv

# Generate dual perspective
python tools/scenario_generator.py \
  --name "Long Distance" \
  --duration 6 \
  --time-unit months \
  --arc rocky_but_committed \
  --perspective dual \
  --output data/long_distance
```

---

## Design Principles

### 1. Backward Compatibility
- Old CSVs without `time_unit` metadata still work (default to "days")
- Existing column names unchanged (`day` not renamed to `time`)
- All current functionality preserved

### 2. Extensibility
- Easy to add new arc types (template functions)
- Easy to add new time units if needed (e.g., "hours" for micro-timescale)
- Conversion utility separate from generator (modular)

### 3. User Control
- Generator creates starting point, user can customize
- Templates have locked/unlocked guidance
- Time units user-selectable, not just auto-determined

### 4. Simplicity First
- Don't build complex interactive editor yet (Phase 1-4 sufficient)
- Command-line tools are simple and scriptable
- CSV files remain human-readable and editable

---

## Integration with Existing System

### Files to Modify:
1. **simulations/run_scenario.py**
   - Add time_unit metadata reading
   - Update axis labels to use time_unit
   - Support negative time values
   - Support non-contiguous timelines (interpolation)

2. **README.md**
   - Document time_unit metadata row
   - Document time conversion utility
   - Document scenario generator usage

3. **Existing templates** (data/templates/*.csv)
   - Add time_unit,days metadata row
   - Validate they still run correctly

### New Files to Create:
1. **tools/convert_time_units.py** - Time unit conversion utility
2. **tools/scenario_generator.py** - Scenario generation tool
3. **tests/test_time_conversion.py** - Unit tests for conversion
4. **tests/test_scenario_generator.py** - Unit tests for generator

---

## Testing Strategy

### Phase 1 Tests:
- Load CSV with time_unit metadata → verify it's read correctly
- Load CSV without time_unit → verify default to "days"
- Plot with time_unit=weeks → verify axis label says "Time (weeks)"
- Backward compatibility with existing scenarios

### Phase 2 Tests:
- Convert days → weeks → verify time values scaled by 1/7
- Convert weeks → days → verify time values scaled by 7
- Convert months → years → verify time values scaled by 1/12
- Round-trip conversion (days → weeks → days) → verify minimal precision loss
- Convert CSV with markers/locked → verify all preserved

### Phase 3 Tests:
- Scenario with negative time values → verify plot shows prehistory
- Scenario with gaps (0, 7, 21, 60) → verify interpolation works
- Non-contiguous timeline → verify trajectory computed correctly

### Phase 4 Tests:
- Generate each arc type → verify primitive patterns correct
- Generate with fractional duration (2.5 weeks) → verify time points correct
- Generate dual perspective → verify M1/M2 asymmetry
- Generate with different time units → verify appropriate event spacing
- Auto-event calculation → verify reasonable number of points

---

## Future Enhancements (Beyond Phase 4)

### Interactive Waveform Editor
(Already designed, see earlier discussion)
- 3-panel layout: M1 primitives, M2 primitives, gamma_self plane
- Bidirectional editing: primitives ↔ gamma_self
- Radio button selection for M1/M2
- Drag-and-drop interface
- Real-time trajectory updates

**Decision:** Defer this until Phase 1-4 are complete and validated. The command-line tools + manual CSV editing may be sufficient for most use cases.

### Additional Features:
- **Batch generation:** Create multiple scenarios from parameter sweep
- **Scenario library:** Curated collection of real-world patterns
- **Validation suite:** Ensure generated scenarios are physically plausible
- **Stochastic variation:** Add noise/randomness to generated primitives
- **Event annotations:** Rich markdown notes for key trajectory points

---

## Open Questions

1. **Interpolation preference:** Hold-constant vs linear for gaps?
   - Probably user preference with default
   - Hold-constant more conservative (no new data)
   - Linear smoother for visualization

2. **Fractional time precision:** How many decimals?
   - 1 decimal for weeks/months/years (2.5 weeks)
   - 0 decimals for days (whole days only)
   - Could be user preference

3. **Negative time notation:** Day -7 or "Week -1"?
   - Use same unit as rest of timeline
   - Just negative numbers in time column

4. **Dual perspective asymmetry patterns:** How to specify?
   - Could be part of arc_type: "slow_burn_pursuer_withdrawer"
   - Or separate parameter: --asymmetry pursuer_withdrawer
   - Or generated then user customizes

5. **Time unit aliases:** Support "wk" for "weeks", "mo" for "months"?
   - Probably yes for CLI convenience
   - Normalize internally to full names

---

## Dependencies

- **Python standard library:** csv, argparse, pathlib
- **NumPy/Pandas:** For time series interpolation
- **Matplotlib:** Already used for plotting
- **No new external dependencies required**

---

## Timeline Estimate

- **Phase 1 (Core Metadata):** 2-3 hours
  - Update CSV format
  - Modify run_scenario.py
  - Update templates
  - Test backward compatibility

- **Phase 2 (Conversion Utility):** 3-4 hours
  - Write convert_time_units.py
  - CLI interface
  - Comprehensive testing
  - Documentation

- **Phase 3 (Timeline Extension):** 2-3 hours
  - Support negative values
  - Interpolation logic
  - Plot updates
  - Testing

- **Phase 4 (Scenario Generator):** 6-8 hours
  - Arc type templates
  - Generator logic
  - Dual perspective
  - CLI interface
  - Testing
  - Documentation

**Total:** ~15-20 hours for complete implementation

---

## Success Criteria

✅ **Phase 1:** User can specify time_unit in CSV, plots show correct axis labels  
✅ **Phase 2:** User can convert existing scenarios between time units  
✅ **Phase 3:** User can create scenarios with prehistory and sparse timelines  
✅ **Phase 4:** User can generate new scenarios from command line with various arc types  

**Overall:** Users can efficiently create, modify, and visualize relationship trajectories across any timescale from days to years.

---

*This document will be updated as implementation progresses.*
