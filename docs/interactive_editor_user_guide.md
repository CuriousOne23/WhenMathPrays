# Interactive Scenario Editor - User Guide

**Version:** Phase 3.3 Complete  
**Last Updated:** December 13, 2025  
**Program Location:** `tools/interactive_editor.py`

> **Note:** Architecture refactoring planned for improved debugging and maintainability. User-facing functionality and command-line interface will remain unchanged. See [Entry Point Consolidation Plan](architecture/entry_point_consolidation_plan.md) for technical details.

---

## Table of Contents
1. [Overview](#overview)
2. [Application States](#application-states)
3. [Getting Started](#getting-started)
4. [User Interface](#user-interface)
5. [Basic Workflow](#basic-workflow)
6. [Features in Detail](#features-in-detail)
7. [Use Cases & Examples](#use-cases--examples)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The Interactive Scenario Editor is a graphical diagnostic tool for analyzing and customizing GRP (Gamma Relational Protocol) relationship scenarios. It provides real-time visualization of how primitive relationship variables (v, r, f, a, S) influence the gamma_self trajectory.

**Primary Uses:**
1. **Scenario Customization** - Modify specific events in a relationship timeline to explore different outcomes
2. **Diagnostic Analysis** - Understand which events dominate relationship trajectories
3. **Sensitivity Testing** - See immediate impact of primitive changes on gamma_self evolution
4. **Data Validation** - Lock known data points and vary unknowns to test GRP fidelity

**Phase 3.3 Status:** ✅ **COMPLETE** - Dual-perspective editing with overlay visualization, robust file loading, and flexible workspace

---

## Application States

The editor manages multiple state domains that determine behavior and available actions. Understanding these states helps you use the editor effectively.

### State Domains & Indicators

#### 1. **PERSPECTIVE STATE** → *Which viewpoint are you editing?*

**Purpose:** Enables dual-perspective relationship editing from either Member 1 (M1) or Member 2 (M2) viewpoint.

**Active States:**
- **M1 Perspective Active** 
  - **Indicator:** Solid blue line under M1 radio button, M1 trajectory solid
  - **Behavior:** Editing M1 events, M2 shown as faded reference
  - **Save Target:** `*_M1_modified.csv`
  
- **M2 Perspective Active**
  - **Indicator:** Solid blue line under M2 radio button, M2 trajectory solid  
  - **Behavior:** Editing M2 events, M1 shown as faded reference
  - **Save Target:** `*_M2_modified.csv`

**Transitions:**
- Click M1/M2 radio buttons
- Press Tab or Space key
- Preserves modifications when switching

**File Loading Sub-States:**
- **Dual-Perspective Loaded:** Both M1 and M2 files loaded independently
- **Single-Perspective Loaded:** Same file in both perspectives (enables conversion)
- **M1-Default:** M1 or dual-file load starts with M1 selected
- **M2-Default:** M2-only file load starts with M2 selected

---

#### 2. **EDIT STATE** → *Are changes temporary or committed?*

**Purpose:** Provides real-time preview during editing while protecting against accidental changes.

**Active States:**

**2.1 IDLE (No Active Edit)**
- **Indicator:** All markers filled (solid color)
- **Behavior:** No ongoing edits, all changes committed
- **Available Actions:** Drag any marker, lock/unlock events, insert/delete

**2.2 PREVIEW (Temporary Edit)**
- **Indicator:** Hollow markers (outline only), orange preview trajectory
- **Behavior:** Live preview of trajectory impact, changes not yet committed
- **Available Actions:** 
  - Continue dragging to adjust
  - Click marker to commit preview
  - Double-click marker or ESC to cancel
- **Data State:** Changes stored in `model.preview_changes`, not written to events

**2.3 COMMITTED (Changes Saved to Model)**
- **Indicator:** Hollow → filled transition, numbered marker labels appear
- **Behavior:** Change written to model, marker pinned on gamma_self trajectory
- **Available Actions:** Further edits, undo (Ctrl+Z), save to file
- **Data State:** Event modified, `modified_primitives` updated, ready for file save

**Transitions:**
- Idle → Preview: Start dragging marker
- Preview → Committed: Release mouse or click hollow marker
- Preview → Idle: Double-click hollow marker or press ESC (cancels)
- Committed → Idle: Ctrl+Z undo
- Committed → File Saved: Click Save button or Ctrl+S

---

#### 3. **MODIFICATION STATE** → *Which events have been changed?*

**Purpose:** Tracks which events differ from original CSV baseline for undo/redo and visual feedback.

**Per-Event States:**

**3.1 UNMODIFIED**
- **Indicator:** No numbered label, marker at original position
- **Behavior:** Event matches CSV baseline
- **Visual:** Standard marker style

**3.2 MODIFIED**
- **Indicator:** Numbered label on marker (event index), pinned marker on trajectory
- **Behavior:** One or more primitives differ from baseline
- **Visual:** Marker shows number, corresponding gamma_self marker pinned
- **Data:** Event time stored in `modified_primitives` with set of modified primitive names

**3.3 PARTIALLY MODIFIED**
- **Indicator:** Some primitives numbered, others not
- **Behavior:** Mixed modification state across primitives at same time
- **Example:** Event 7 has modified resonance (7r) but unmodified visibility

**Transitions:**
- Unmodified → Modified: Commit change different from baseline
- Modified → Unmodified: Reset to baseline (double-click) or undo
- Any → File Saved: Save button writes modified_primitives to CSV

---

#### 4. **LOCK STATE** → *Which events are protected from editing?*

**Purpose:** Protects critical events from accidental modification or deletion.

**Per-Event States:**

**4.1 UNLOCKED (Editable)**
- **Indicator:** No lock icon, standard marker appearance
- **Behavior:** Can drag primitives, delete event, insert before event
- **Available Actions:** All edit operations

**4.2 LOCKED (Protected)**
- **Indicator:** Lock icon on marker
- **Behavior:** Cannot drag, cannot delete, can insert before
- **Available Actions:** Right-click to unlock, view/click only
- **Persistence:** Lock state saved to CSV `locked` column

**Special Lock Rules:**
- First and last events: Implicitly protected (cannot delete regardless of lock)
- Locked events: Can still be used as insertion points
- Lock persists across sessions via CSV

**Transitions:**
- Right-click marker: Toggle lock state
- Load CSV: Restore lock state from `locked` column

---

#### 5. **UNDO/REDO STATE** → *Can you reverse or repeat actions?*

**Purpose:** Provides reversible editing with full command history.

**Stack States:**

**5.1 CAN UNDO**
- **Indicator:** Undo button enabled, Ctrl+Z available
- **Behavior:** Previous commands available to reverse
- **Available:** After any modifying operation (edit, insert, delete)

**5.2 CAN REDO**
- **Indicator:** Redo button enabled, Ctrl+Y available
- **Behavior:** Undone commands available to re-apply
- **Available:** After undo operation

**5.3 CLEAN (At Save Point)**
- **Indicator:** No asterisk in window title
- **Behavior:** Current state matches last file save
- **Available:** Immediately after save operation

**5.4 DIRTY (Unsaved Changes)**
- **Indicator:** Asterisk (*) in window title
- **Behavior:** Modifications exist since last save
- **Available:** After any change

**Special State:**
**5.5 IN_UNDO_REDO (Executing Reversal)**
- **Internal State:** Prevents recursive undo command creation
- **Behavior:** Temporarily disables creating new undo commands while applying old ones
- **Not Visible:** User-facing only through command execution

---

#### 6. **TRAJECTORY COMPUTATION STATE** → *Is the trajectory up-to-date?*

**Purpose:** Manages computationally expensive gamma_self ODE calculation with debouncing.

**Active States:**

**6.1 CURRENT (Displayed Trajectory Matches Data)**
- **Indicator:** Trajectory stable, no recomputation in progress
- **Behavior:** Display reflects all committed changes

**6.2 SCHEDULED (Recomputation Pending)**
- **Indicator:** Debounce timer active during preview drag
- **Behavior:** Waiting for drag to pause before recomputing
- **Trigger:** During continuous marker dragging

**6.3 COMPUTING (Calculating Trajectory)**
- **Indicator:** Brief computation (usually <50ms)
- **Behavior:** Running gamma_self ODE for all time points
- **Trigger:** Debounce timer expired or immediate recompute requested

**Computation Modes:**
- **With Preview:** Includes `preview_changes` in computation (during drag)
- **Committed Only:** Uses only saved changes (after release, undo, load)
- **Immediate:** No debouncing (after save, undo, perspective switch)

**Auto-Zoom Behavior:**
- **Initial Load:** Auto-zoom enabled (fits full trajectory)
- **Subsequent Updates:** Auto-zoom disabled (preserves user zoom/pan)

---

#### 7. **FILE STATE** → *What file are you working with?*

**Purpose:** Tracks file provenance and save targets for proper CSV output.

**Active States:**

**7.1 ORIGINAL FILE**
- **Indicator:** Filename without `_modified` suffix
- **Behavior:** Editing original data file
- **Save Target:** Creates new `*_modified.csv` file

**7.2 MODIFIED FILE**  
- **Indicator:** Filename with `_modified.csv` suffix
- **Behavior:** Editing previously saved modifications
- **Save Target:** Overwrites current `*_modified.csv`

**7.3 UNSAVED CHANGES**
- **Indicator:** Asterisk (*) in window title
- **Behavior:** In-memory changes not written to disk
- **Save Target:** Next save destination determined by perspective + original filename

**File Resolution States:**
- **M1 Found / M2 Found:** Both companion files exist
- **M1 Only:** No M2 companion, M1 loaded to both perspectives
- **M2 Only:** No M1 companion, M2 loaded to both perspectives  
- **Missing File:** File not found error state

---

#### 8. **UI INTERACTION STATE** → *What is the user currently doing?*

**Purpose:** Determines cursor behavior, available keyboard shortcuts, and visual feedback.

**Mouse States:**

**8.1 IDLE (No Mouse Interaction)**
- **Behavior:** Standard cursor, all shortcuts available

**8.2 HOVERING (Mouse Over Draggable Element)**
- **Indicator:** Cursor changes to hand/pointer
- **Behavior:** Marker highlights, ready to drag

**8.3 DRAGGING (Mouse Down + Moving)**
- **Indicator:** Hollow marker, orange preview trajectory
- **Behavior:** Real-time trajectory update, debounced recomputation

**8.4 CLICKING (Single Click)**
- **Behavior:** Depends on modifiers:
  - No modifier: Select for note editing
  - Shift: Place diagnostic marker (counterfactual)
  - Ctrl: Delete event
  - Ctrl+Shift: Insert event

**Keyboard Modifier States:**
- **Ctrl Held:** Delete mode enabled
- **Shift Held:** Diagnostic mode enabled  
- **Ctrl+Shift Held:** Insert mode enabled
- **No Modifiers:** Normal edit mode

**Panel Focus States:**
- **Primitives Panel Active:** Editing primitive values
- **Trajectory Panel Active:** Sampling gamma_self positions
- **Controls Panel Active:** Editing widgets (name, notes, gamma_self_0)

---

#### 9. **WORKSPACE LAYOUT STATE** → *How is the UI arranged?*

**Purpose:** Manages flexible dock-based workspace configuration.

**Dock Visibility States:**
- **All Visible:** Primitives, Trajectory, Controls all showing
- **Selective:** One or more docks hidden via View menu
- **Detached:** Dock undocked to separate window (multi-monitor)

**Layout States:**
- **Default:** 3-column (Primitives | Trajectory | Controls)
- **Custom:** User rearranged docks
- **Saved:** Layout persisted to QSettings
- **Restored:** Layout loaded from previous session

**Panel Size States:**
- **Default Sizes:** Primitives=500px, Trajectory=700px, Controls=300px
- **User Resized:** Dragged dock dividers to custom widths
- **Docked:** Panel attached to main window
- **Floating:** Panel detached as separate window

---

### State Transition Examples

**Example 1: Basic Edit Flow**
```
IDLE (unmodified, unlocked) 
  → drag marker → PREVIEW (hollow marker, orange trajectory)
  → release → COMMITTED (filled, numbered label)
  → Ctrl+S → FILE SAVED (written to CSV)
```

**Example 2: Perspective Switch**
```
M1 ACTIVE (editing M1, M2 shown faded)
  → Click M2 radio button
  → M2 ACTIVE (editing M2, M1 shown faded)
  [Modifications preserved in both perspectives]
```

**Example 3: Undo/Redo Flow**
```
COMMITTED (event modified)
  → Ctrl+Z → UNDONE (modification reversed, can redo)
  → Ctrl+Y → RE-COMMITTED (modification re-applied)
```

**Example 4: Lock Protection**
```
UNLOCKED (can edit)
  → Right-click → LOCKED (protected, lock icon visible)
  → Attempt drag → BLOCKED (no effect, still locked)
  → Right-click → UNLOCKED (editable again)
```

**Example 5: File Resolution**
```
Load M1 file
  → Companion search → M2 FOUND
  → Dual-perspective loaded (both files independent)

Load M2 file  
  → Companion search → M1 NOT FOUND
  → Single-perspective loaded (M2 in both slots, M2 selected)
```

---

### State-Based Feature Availability

| Action | Required State | Blocked By |
|--------|---------------|------------|
| **Drag Marker** | Unlocked + Not First/Last | Locked, Preview Active |
| **Delete Event** | Unlocked + Not First/Last + ≥3 events | Locked, First Event, Last Event |
| **Insert Event** | Not Before First | First Event Target |
| **Lock/Unlock** | Any Event | None |
| **Undo** | Undo Stack Not Empty | Clean Stack |
| **Redo** | Redo Stack Not Empty | No Undone Commands |
| **Switch Perspective** | Dual-Perspective Loaded | None (works in single too) |
| **Save** | Any | None (commits previews first) |
| **Diagnostic Marker** | Any Event | None (read-only operation) |

---

---

## Getting Started

### Installation & Requirements

**New to the Interactive Editor?** See the [Installation Guide](installation_4_interactive_editor.md) for step-by-step setup instructions.

**Requirements:**
- Python 3.8+
- PySide6 (Qt framework)
- pyqtgraph
- numpy
- pandas
- GRP core library (`core/love.py`)

### CSV File Format Requirements

**For complete CSV format specification, see [CSV Scenario Format](../README.md#csv-scenario-format) in the main README.**

Quick reference:
- **Required columns:** `day`, `v`, `r`, `f`, `a`, `S`
- **Optional columns:** `notes`, `marker`, `locked`
- **Metadata rows:** `name` and `time_unit` (first two rows)
- **Value range:** Primitives use -10 to +10 scale
- **File naming:** Dual-perspective scenarios must use `_M1.csv` and `_M2.csv` suffixes

### Running the Editor

```bash
python tools/interactive_editor.py <csv_file>
```

**Examples:**
```bash
# Load M1 file (automatically finds M2 if available)
python tools/interactive_editor.py data/single_dating_to_love_M1.csv

# Load M2 file (automatically finds M1 if available)
python tools/interactive_editor.py data/single_dating_to_love_M2.csv

# Load any CSV file (works with or without _M1/_M2 suffix)
python tools/interactive_editor.py data/my_scenario.csv
```

### File Loading Behavior

The editor intelligently handles different file scenarios:

**Dual-Perspective Files:**
- **Load M1 with M2 present:** Loads both perspectives, M1 selected by default
- **Load M2 with M1 present:** Loads both perspectives, M1 selected by default

**Single-Perspective Files:**
- **Load M1-only:** Loads into both M1 and M2 slots, M1 selected by default
- **Load M2-only:** Loads into both M1 and M2 slots, M2 selected by default
- **Benefit:** Can edit from either perspective and save to M1 or M2, enabling easy conversion between perspectives

**Error Handling:**
- **File not found:** Clear error message
- **Wrong file type:** Requires `.csv` extension, displays helpful error
- **M1/M2 detection:** Automatically detects `_M1` or `_M2` in filename

### Perspective Switching

Use the **Perspective Switcher** widget (M1/M2 radio buttons) in the controls panel:
- **M1 Button:** View and edit from Member 1's perspective
- **M2 Button:** View and edit from Member 2's perspective
- **Visual indicators:** Solid blue line under active perspective, dashed blue line under inactive
- **Overlay rendering:** Inactive perspective shown as faded dotted lines for comparison
- **Independent names:** Each perspective can have its own scenario name

---

## User Interface

### Layout (Phase 3.1 - Flexible Workspace)
The editor uses a flexible dock-based layout with three main panels:

**Left Panel - Primitives:**
- Visibility (v) - Blue
- Resonance (r) - Orange  
- Fidelity (f) - Green
- Altruism (a) - Red
- Shared Breath (S) - Purple
- Vertical stacked plots with synchronized time axes
- Shows active perspective as solid lines, inactive as faded dotted lines

**Center Panel - Gamma_Self Trajectory:**
- Complex plane plot showing relationship state evolution
- X-axis: Ego ← → We (Real axis)
- Y-axis: Hate ← → Love (Imaginary axis)
- Markers: Green circle = Start, Red square = End
- Shows active trajectory as solid line, inactive as dotted line

**Right Panel - Editor Controls:**
- **Perspective Switcher:** M1/M2 radio buttons with visual indicators
- **Name Editor:** Editable scenario name field with Apply button
- **Note Editor:** Event annotation editor with Apply/Clear buttons
- **Gamma_Self_0 Editor:** Initial position editor
- **Primitive Readout Gauge:** Shows last edited marker
- **Gamma_Self Readout Gauge:** Shows clicked trajectory position
- **Insertion Options:** Configure new event parameters

**View Menu:** Show/hide individual panels, save/restore workspace layout

### Diagnostic Gauges

**Perspective Switcher (Phase 3.2):**
- Radio buttons for M1/M2 perspective selection
- Visual indicators: Solid blue line under active, dashed blue line under inactive
- Keyboard shortcuts: Tab or Space to toggle between perspectives

**Name Editor (Phase 3.2):**
- Editable text field for scenario name
- Each perspective can have independent names
- Apply button commits name changes
- Enter key also applies changes

**Note Editor (Phase 3.2):**
- Multi-line text editor for event annotations
- Click on any primitive marker to load its event's notes
- Notes are shared across all primitives at the same time point
- Apply button saves notes, Clear button removes them
- Shows current event time in label

**Primitive Readout Gauge:**
- Displays last edited marker information
- Shows marker ID (e.g., "7r" = event 7, resonance)
- Shows Y-value of the primitive
- Updates on marker drag release
- Cleared when pressing '0' (reset view)

**Gamma_Self Position Readout:**
- Displays X,Y coordinates on trajectory
- Click on gamma_self plot to sample position
- Useful for recording specific trajectory points
- Persists until next click

**Gamma_Self_0 Editor (Phase 2.1):**
- Edit initial relationship position
- Real and imaginary components
- Reset button restores default (0+0j)

### Save Button & Controls
Located in the toolbar at the top of the window:
- **Save Button:** Save CSV to `data/` folder with `_modified` suffix
- **Ctrl+S:** Keyboard shortcut for save
- **Automatic perspective handling:** Saves to M1_modified or M2_modified based on active perspective

**Save Behavior:**
- M1 perspective active → saves to `*_M1_modified.csv`
- M2 perspective active → saves to `*_M2_modified.csv`
- Single-file scenarios: Can save to either M1 or M2, enabling perspective conversion

---

## Basic Workflow

### 1. Load a Scenario
```bash
# Standard dual-perspective load
python tools/interactive_editor.py data/single_dating_to_love_M1.csv

# Load M2 file (finds M1 automatically)
python tools/interactive_editor.py data/single_dating_to_love_M2.csv

# Single-file load (converts to dual-perspective internally)
python tools/interactive_editor.py data/my_scenario_M1.csv
```

### 2. Switch Perspectives (Phase 3.2)
- Click **M1** or **M2** radio button in controls panel
- Use **Tab** or **Space** key to toggle
- Active perspective shows solid lines, inactive shows faded dotted lines
- Each perspective has independent name and can be edited separately

### 3. Edit Primitives
- **Drag markers vertically** on any primitive plot to change values
- Markers become **hollow** while in preview mode
- Gamma_self trajectory updates in real-time (orange preview)
- **Click on markers** to add/edit notes for that event (opens Note Editor)

### 4. Save or Cancel Changes
- **Click hollow marker** to continue editing from that position
- **Double-click hollow marker** to cancel and revert to original
- **Press ESC** to cancel all previews and revert to last saved state

### 5. Lock/Unlock Events
- **Right-click** on any marker to toggle lock status
- Locked events show with a lock icon
- Locked events cannot be dragged (useful for anchoring known data)

### 6. Save Your Work
- **Click Save button** or **Press Ctrl+S**
- Saving automatically commits all preview changes (hollow → filled)
- Modified events automatically marked with numbered labels
- CSV includes `marker` and `locked` columns for persistence
- Saves to appropriate M1_modified or M2_modified file based on active perspective

---

## Features in Detail

### Robust File Loading (Phase 3.3)

The editor intelligently handles various file scenarios:

**Automatic M1/M2 Detection:**
- Detects `_M1` or `_M2` suffix in filename
- Automatically searches for companion file (M1 ↔ M2)
- Loads both files when available for dual-perspective editing

**Single-File Flexibility:**
- **M1-only files:** Loaded into both perspectives, M1 selected by default
- **M2-only files:** Loaded into both perspectives, M2 selected by default
- **Benefit:** Enables easy conversion between perspectives - edit from either M1 or M2 and save to desired perspective

**Error Handling:**
- **File not found:** Clear error message with file path
- **Invalid file type:** Must be `.csv` extension, shows helpful error
- **Missing companion:** Info message shows single-perspective mode with conversion capability

**Examples:**
```bash
# Load M1 with M2 present → Dual-perspective editing
python tools/interactive_editor.py data/scenario_M1.csv
# Output: Loading dual-perspective data: M1: ..._M1.csv, M2: ..._M2.csv

# Load M1-only → Single file in both perspectives
python tools/interactive_editor.py data/solo_M1.csv  
# Output: M1-only: Loaded into both perspectives (M1 selected)
#         You can edit from either perspective and save to M1 or M2

# Load M2-only → Single file in both perspectives, M2 selected
python tools/interactive_editor.py data/solo_M2.csv
# Output: M2-only: Loaded into both perspectives (M2 selected)
#         You can edit from either perspective and save to M1 or M2
```

### Dual-Perspective Overlay (Phase 3.3)

**Visual Comparison:**
- Active perspective: Solid lines, full opacity, interactive
- Inactive perspective: Dotted lines, faded opacity (40%), non-interactive
- Both trajectories visible simultaneously for comparison

**Line Indicators:**
- Solid blue line under active perspective radio button
- Dashed blue line under inactive perspective radio button
- Visual feedback matches plot style (solid vs dotted)

**Independent Editing:**
- Each perspective maintains separate primitive values
- Switching perspectives preserves modifications
- Names, notes, and modifications tracked per perspective

### Auto-Marking System
When you modify a primitive value:
1. The event is automatically marked with its event index number
2. A numbered label appears on all modified primitives for that event
3. The marker is **pinned** at the gamma_self position where the change was committed
4. Pinned markers remain fixed on the trajectory plot even if you make further edits
5. Saved CSV includes `marker` column with event index for modified events

### Marker Visual System
- **Filled marker** (solid color) = Original or committed value
- **Hollow marker** (outline only) = Preview/modified value  
- **Original marker** (semi-transparent) = Baseline value shown when modified
- **Numbered labels** = Event index for tracking modifications
- **Black X marker** = Counterfactual Explorer marker (hypothetical scenarios, not saved)

### CSV Output Format
Saved CSV files include:
```csv
name,single_dating_to_love_M1
time_unit,days
gamma_self_0,-5+0j
day,v,r,f,a,S,notes,marker,locked
0,5,0,2,2,0,Initial condition: eager but moderate love,,
7,5,2,2,3,1,First date: strong attraction developing,7,
14,5,-2,2,3,-1,Early wobble: pressing pace,14,true
```

- `marker` column: Populated with event index for modified events (used by plotting scripts)
- `locked` column: Set to "true" for locked events, preserving lock state across sessions
- Blank entries mean unmodified/unlocked

### Keyboard Shortcuts

**Editing:**
- `ESC` - Cancel all preview changes
- `G` - Edit gamma_self_0 initial position (starting point)
- `Tab` or `Space` - Toggle between M1/M2 perspectives
- `Ctrl+Click` - Delete event (non-locked events only, excludes first/last)
- `Ctrl+Shift+Click` - Insert event before nearest marker (creates time gap)
- `Ctrl+Z` - Undo last action (deletion or insertion)
- `Ctrl+Y` or `Ctrl+Shift+Z` - Redo action

**View Controls:**
- `+` or `=` - Zoom in (panel under cursor)
- `-` - Zoom out (panel under cursor)
- `0` - Reset view to auto-fit (clears primitive gauge)

**Save:**
- `Ctrl+S` - Save (auto-commits all previews and saves CSV)

---

## Use Cases & Examples

### 1. Scenario Customization
**Goal:** Adjust a scenario to explore different relationship outcomes

**Workflow:**
1. Load baseline scenario: `python tools/interactive_editor.py data/baseline.csv`
2. Drag primitives to modify specific events (e.g., increase resonance at day 21)
3. Watch gamma_self trajectory update in real-time
4. Save modified version: Click Save button
5. Output: `data/baseline_modified.csv`

**Use Primitive Gauge:** Track which primitive values you're setting

### 2. Diagnostic Analysis  
**Goal:** Identify which events dominate the trajectory

**Workflow:**
1. Load scenario with known outcome
2. Lock key events (right-click markers)
3. Perturb individual unlocked events one at a time
4. Observe trajectory sensitivity in real-time
5. Use gamma_self readout to record critical trajectory points

**Use Gamma_Self Gauge:** Click trajectory points to sample coordinates for analysis

### 3. Data Validation
**Goal:** Test if GRP can reproduce observed relationship trajectory

**Workflow:**
1. Create scenario with known gamma_self waypoints
2. Use gamma_self gauge to verify trajectory passes through target points
3. Lock events corresponding to known data
4. Adjust unlocked events to improve trajectory fit
5. Validate with re-run: `python simulations/run_scenario.py data/scenario_modified.csv`

### 4. Sensitivity Testing
**Goal:** Understand impact of primitive changes on outcomes

**Workflow:**
1. Press 'F' to enable fixed view (prevents auto-zoom)
2. Modify single primitive at one event
3. Observe trajectory deviation magnitude
4. Use primitive gauge to record exact values tested
5. Cancel (ESC) to test different values, or save when satisfied

### 5. Counterfactual Explorer (NEW)
**Definition:** *Counterfactual thinking* is a clinical psychology term for exploring "what might have been" - examining how outcomes would differ if past events had unfolded differently. This tool provides real-time counterfactual analysis for relationship trajectories.

**Goal:** Test how changing a single primitive value would affect the final outcome without modifying the actual data

**Workflow:**
1. **Shift+Click** on any primitive plot at the desired Y-value (near an event time)
2. A black **X marker** appears at the clicked position (snapped to nearest event)
3. A black **X marker** appears on the gamma_self trajectory showing the **counterfactual outcome** if that primitive had the clicked value
4. Both **readout gauges update** showing the hypothetical primitive value and resulting gamma_self position
5. **Drag the X marker** up/down to explore different counterfactual scenarios in real-time
6. **Shift+Click elsewhere** to test a different primitive/event (previous X markers clear automatically)

**Use Cases:**
- "What if resonance had been higher at day 14?" (counterfactual exploration)
- "How much would increasing altruism at day 21 improve the outcome?" (sensitivity analysis)
- "Would lowering visibility at day 7 prevent the final breakup?" (intervention testing)

**Note:** Counterfactual markers (X) are **exploratory only** - they don't modify your data. Use regular marker dragging to actually commit changes.

### 6. Delete Events (NEW - Phase 2.2)
**Goal:** Remove unwanted or placeholder events from a scenario

**Workflow:**
1. **Ctrl+Click** on any marker to delete that event
2. Event is removed from all primitive plots and trajectory
3. **Undo with Ctrl+Z** to restore deleted event if needed
4. **Redo with Ctrl+Y** to re-delete

**Validation Rules:**
- ✅ Can delete: Unlocked middle events (not first or last)
- ❌ Cannot delete: First event (start position)
- ❌ Cannot delete: Last event (final outcome)
- ❌ Cannot delete: Locked events (right-click to unlock first)

### 7. Insert Events (NEW - Phase 2.3)
**Goal:** Add time gaps before important events to insert new developmental stages or details

**Workflow:**
1. **Ctrl+Shift+Click** near any marker (except the first) to insert a new event before it
2. New event appears at the clicked marker's original time with **all primitives set to zero**
3. The clicked marker and all subsequent markers **shift forward** by the time delta to the previous event
4. **Undo with Ctrl+Z** to remove inserted event and restore original times
5. **Redo with Ctrl+Y** to re-insert

**Example - Inserting before day 21:**

**Before insertion:**
- Events at days: `[0, 14, 21, 28]`
- Delta = 21 - 14 = 7 days

**After Ctrl+Shift+Click near day 21:**
- Events at days: `[0, 14, 21(new zeros), 28, 35]`
- New event at day 21: `v=0, r=0, f=0, a=0, S=0` (shown as **cyan markers** at y=0)
- Old day-21 event → day 28
- Old day-28 event → day 35

**Visual Indicators:**
- **Cyan/turquoise markers at y=0** indicate newly inserted events that need editing
- **Vertical dashed lines** mark the insertion time
- **Drag the cyan markers** up or down to set primitive values

**Use Cases:**
- "Add a transitional event between days 14 and 21 to model gradual repair"
- "Insert time before breakup event to explore preventive interventions"
- "Create space for additional developmental stages in complex scenarios"

**Validation Rules:**
- ✅ Can insert: Before any event except the first
- ❌ Cannot insert: Before first event (start time cannot change)
- 📝 After insertion: **Drag cyan markers** to set the new event's primitive values
- 🔄 Full undo/redo support
- ❌ Cannot delete: When only 2 events remain (need at least start + end)

**Use Cases:**
- Remove placeholder events inserted during scenario generation
- Clean up scenarios with too many time points
- Delete events that were added experimentally and no longer needed
- Simplify complex scenarios for clearer analysis

**Undo/Redo Support:**
- Full undo/redo for event deletion via Ctrl+Z / Ctrl+Y
- Deleted events restored with all primitive values, notes, and lock status
- Works seamlessly with other undo actions (primitive edits, resets)

---

## Advanced Features

### Preview System
The editor uses a sophisticated preview/save workflow:
- **Preview mode:** Drag markers to see instant trajectory feedback (hollow markers)
- **Save to commit:** Click Save button to lock changes (hollow → filled)
- **Pinned markers:** Saved changes pin gamma_self position on trajectory
- **Incremental editing:** Click hollow markers to continue editing from preview position

### Gamma_Self_0 Editing
Press `G` to edit the initial relationship state:
- **Real part:** Ego ↔ We axis (e.g., -5 for exes, 0 for strangers, +5 for friends)
- **Imaginary part:** Hate ↔ Love axis (e.g., -3 for bitterness, 0 for neutral, +8 for love)
- Trajectory recomputes from new starting point

### Fixed View Mode
Press `F` to toggle:
- **OFF (default):** Auto-zoom adjusts to show full trajectory
- **ON:** Zoom/pan locked, useful for comparing small changes

### Multi-Primitive Markers
When multiple primitives are modified at the same event:
- All modified primitives show numbered labels
- All are tracked on gamma_self plot
- CSV `marker` column records the event once

---

## Tips & Best Practices

1. **Start with 'F' (fixed view)** when doing sensitivity analysis to maintain consistent scale
2. **Lock known data first** before exploring variations
3. **Use primitive gauge** to document exact values for reproducibility  
4. **Use gamma_self gauge** to record critical trajectory waypoints
5. **Use Counterfactual Explorer (Shift+Click)** for quick "what-if" analysis without modifying data
6. **Drag counterfactual X markers** to explore a range of alternative scenarios before committing changes
7. **Save frequently** - Each save creates `_modified` version, preserving original
8. **Save incrementally** - Save after each major change rather than editing many events at once
9. **Use screenshot tools** to capture trajectory visualizations for reports (PNG export temporarily disabled)

---

## CSV Format Details

### Input Format (Minimal)
```csv
name,scenario_name
time_unit,days
gamma_self_0,-5+0j
day,v,r,f,a,S,notes
0,5,0,2,2,0,Initial condition
7,5,2,2,3,1,First date
...
```

### Output Format (With Markers)
```csv
name,scenario_name
time_unit,days
gamma_self_0,-5+0j
day,v,r,f,a,S,notes,marker,locked
0,5,0,2,2,0,Initial condition,,
7,5,2,2,3,1,First date,7,
14,5,-2,2,3,-1,Early wobble,14,true
```

**Columns:**
- `marker`: Event index (integer) for modified events, blank for unmodified
- `locked`: "true" for locked events, blank for unlocked
- Both columns are **optional** - if missing, no markers/locks on load

---

## Troubleshooting

**Issue:** Editor won't start  
**Solution:** Check Python version (3.8+), verify matplotlib installed: `pip install matplotlib`

**Issue:** Markers won't drag  
**Solution:** Check if event is locked (right-click to unlock)

**Issue:** Trajectory not updating  
**Solution:** Ensure you're dragging vertically (Y-axis only), check console for errors

**Issue:** Save button not working  
**Solution:** Ensure output directory (`data/`) exists and is writable

**Issue:** Gauges not showing values  
**Solution:** Primitive gauge: Drag a marker to update. Gamma_self gauge: Click on trajectory plot

**Issue:** CSV won't load  
**Solution:** Verify format matches specification, check for `gamma_self_0` metadata line. File must have `.csv` extension.

**Issue:** No M2 file found message
**Solution:** This is normal for single-perspective scenarios. You can still switch between M1 and M2 to edit and save to either perspective.

**Issue:** Overlay lines not visible
**Solution:** Ensure you have both M1 and M2 data loaded. Single-file scenarios show the same data in both perspectives (not overlaid).

**Issue:** Wrong perspective selected on load
**Solution:** M2-only files load with M2 selected. M1-only or dual-perspective files load with M1 selected.

**Issue:** Save creates wrong filename (M1 vs M2)
**Solution:** Active perspective determines save filename. Switch to desired perspective before saving.

---

## Future Enhancements (Phase 4+)

See [interactive_edit_roadmap.md](interactive_edit_roadmap.md) for roadmap:
- Inverse editing (drag gamma_self to suggest primitives)
- Automated sensitivity analysis
- Constraint validation tools
- Trajectory-to-event mapping (click gamma_self to show notes)

---

## Related Documentation

- **Installation:** [installation_4_interactive_editor.md](installation_4_interactive_editor.md)
- **Program:** `tools/interactive_editor.py`
- **Requirements & Roadmap:** [interactive_edit_roadmap.md](interactive_edit_roadmap.md)
- **Architecture:** [ARCHITECTURE.md](../ARCHITECTURE.md)
- **Main README:** [README.md](../README.md)
- **Scenario Configuration:** [SCENARIO_CONFIGURATION_GUIDE.md](SCENARIO_CONFIGURATION_GUIDE.md)

---

**Questions or Issues?** See [interactive_edit_roadmap.md](interactive_edit_roadmap.md) for known issues and future plans.
