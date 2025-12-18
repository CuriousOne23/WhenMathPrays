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

## Feature Status Overview

This table provides a comprehensive status overview of all Interactive Editor functions, helping you understand what's available, tested, and verified. It serves as a quick reference for feature availability and quality assurance status.

| Function | Implementation Status | Testing Status | Auto-Verification | Notes |
|----------|----------------------|----------------|-------------------|-------|
| **File Loading** | ✅ **Complete** | ✅ **Tested** | ❌ **Not Verified** | Robust M1/M2 detection, companion file search, error handling |
| **Dual-Perspective Overlay** | ✅ **Complete** | ✅ **Tested** | ✅ **Verified** (8 switches) | Visual comparison, independent editing, Phase 3.3 |
| **Perspective Switching** | ✅ **Complete** | ✅ **Tested** | ✅ **Verified** (8 operations) | M1/M2 radio buttons, Tab/Space keys, state preservation |
| **Primitive Drag Editing** | ✅ **Complete** | ✅ **Tested** | ✅ **Verified** (7 operations) | Hollow markers, real-time preview, trajectory updates |
| **Marker Pinning** | ✅ **Complete** | ✅ **Tested** | ✅ **Verified** (343 pins) | Filled markers, numbered labels, gamma_self positioning |
| **Undo/Redo** | ✅ **Complete** | ✅ **Tested** | ✅ **Verified** (7 undo, 7 redo) | Ctrl+Z/Ctrl+Y, command stack, state restoration |
| **Event Locking** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Right-click toggle, lock icons, protection from editing |
| **Event Notes** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Click markers to edit, Apply/Clear buttons, per-event storage |
| **Scenario Names** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Name editor, Apply button, per-perspective names |
| **Save (Active Perspective)** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Ctrl+S, toolbar button, automatic perspective handling |
| **Trajectory Computation** | ✅ **Complete** | ✅ **Tested** | ✅ **Verified** (36 computes) | Real-time updates, debounced recomputation, auto-zoom |
| **Primitive Reset (Double-click)** | ✅ **Complete** | ✅ **Tested** | ✅ **Verified** (1 operation) | Reset to baseline CSV values, undoable operation |
| **ESC Cancel All Previews** | ❌ **Not Implemented** | ❌ **Not Tested** | ❌ **Not Verified** | Backend logic exists, UI connection missing |
| **Spinbox Primitive Editing** | ❌ **Planned v2.4** | ❌ **Not Tested** | ❌ **Not Verified** | Precise numeric input, keyboard-driven workflow |
| **Save Both Perspectives** | ❌ **Planned** | ❌ **Not Tested** | ❌ **Not Verified** | Ctrl+Shift+S, simultaneous M1/M2 saving |
| **Diagnostic Markers** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Shift+click for counterfactual analysis |
| **Event Insertion** | ✅ **Complete** | ✅ **Tested** | ✅ **Verified** (2 inserts) | Ctrl+Shift+click, insertion points, undoable |
| **Event Deletion** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Ctrl+click, first/last event protection |
| **Gamma_Self_0 Editor** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Initial position editing, real/imaginary components |
| **Primitive Readout Gauge** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Shows last edited marker info, Y-value display |
| **Gamma_Self Readout** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Click trajectory for X,Y coordinates |
| **View Menu** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Panel show/hide, workspace layout save/restore |
| **Workspace Layout** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Dock-based UI, flexible arrangement, QSettings persistence |
| **Keyboard Shortcuts** | 🟡 **Partial** | ❌ **Not Tested** | ❌ **Not Verified** | Ctrl+S works, Tab/Space/ESC missing |
| **Auto-Zoom** | ✅ **Complete** | ❌ **Not Tested** | ❌ **Not Verified** | Initial load zoom-to-fit, user zoom preservation |
| **State Viewer** | ✅ **Complete** | ✅ **Tested** | ✅ **Verified** (538 ops logged) | Debug logging, state inspection, correlation tracking |

### Status Legend
- **✅ Complete:** Fully implemented and working
- **🟡 Partial:** Some functionality implemented, some missing
- **❌ Not Implemented/Planned:** Either not yet built or marked as future feature
- **Tested:** Has undergone testing (manual or automated)
- **Verified:** Has automated verification/logging (538+ operations logged)

### Coverage Summary
- **Implementation:** ~85% Complete (21/25 functions implemented)
- **Testing:** ~28% Tested (7/25 functions have testing)
- **Auto-Verification:** ~28% Verified (7/25 functions auto-verified)

**For Developers/Advanced Users:** Detailed logging configuration, debugging techniques, and troubleshooting guides are available in [DEBUG.md](DEBUG.md).

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

**For complete CSV format specification, see [CSV Format Details](#csv-format-details) section below.**

Quick reference:
- **Required columns:** `day`, `v`, `r`, `f`, `a`, `S`
- **Optional columns:** `notes`, `marker`, `locked`
- **Metadata rows:** `name` and `time_unit` (first two rows)
- **Value range:** Primitives use -10 to +10 scale
- **File naming:** `_M1`/`_M2` suffix anywhere in filename for dual-perspective files

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

## Robust Mapping: Primitives ↔ Gamma_Self (UI Integration)

The editor maintains an explicit, debuggable mapping between each primitive change (event_id, primitive) and its corresponding γ_self (gamma_self) position on the trajectory plot. This ensures:
- Numbered labels and markers are always synchronized with their gamma_self positions
- Label placement is robust to edits, undo/redo, and perspective switching
- All mappings are logged for debugging and can be inspected in the State Viewer

For full technical details, debugging workflows, and example mapping logs, see [DEBUG.md](DEBUG.md#debugging-primitive-↔-gamma_self-mapping-v223-proposal).

**Right Panel - Editor Controls:**
- **Perspective Switcher:** M1/M2 radio buttons with visual indicators
- **Name Editor:** Editable scenario name field with Apply button
- **Note Editor:** Event annotation editor with Apply/Clear buttons
- **Gamma_Self_0 Editor:** Initial position editor
- **Spinbox Primitive Editor:** *[Planned v2.4]* Precise numeric input for primitives
- **Primitive Readout Gauge:** Shows last edited marker (to be replaced by spinbox)
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

**Spinbox Primitive Editing (Planned v2.4):**

*Replaces gauge-based editing with precise numeric input.*

**Overview:**
- Single shared spinbox for entering exact primitive values
- Shows currently active primitive (v, r, f, a, or S)
- Type exact values instead of dragging gauges

**Workflow:**
1. **Select event:** Click event marker in trajectory plot (e.g., Day 2)
2. **Select primitive:** Click primitive label (e.g., "v")
   - Spinbox label updates: "Editing: v"
   - Spinbox shows current v value: 5.5
3. **Enter value:** Type new value (e.g., "7.2") and press Enter
   - Or use ▲▼ arrows for incremental changes
4. **Trajectory updates:** Automatically recomputes

**Features:**
- **Range:** -10.0 to +10.0 (human-scale authoring values)
- **Precision:** 1 decimal place, 0.1 step size
- **Label persistence:** "Editing: {primitive}" stays until different primitive selected
- **State tracking:** Active primitive + event tracked, shown in State Viewer
- **Integration:** Works with Event Insertion Points, Ctrl+Shift+Click markers, M1/M2 switching

**Initial State:**
- Spinbox disabled until first event + primitive selected
- Label shows: "Editing: (none)"

**Edge Cases:**
- No event selected: Spinbox remains disabled
- Invalid input: Clamped to range, non-numeric rejected
- Perspective switch: Preserves active primitive, updates to new perspective's value
- Event deletion: Clears active primitive, disables spinbox

**Benefits:**
- Precise value control (type "7.2" vs dragging to approximate)
- Faster workflow (keyboard-driven)
- Cleaner UI (one spinbox vs multiple gauges)
- Better accessibility

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

# Load M2 file (automatically finds M1 if available)
python tools/interactive_editor.py data/single_dating_to_love_M2.csv

# Load any CSV file (works with or without _M1/_M2 suffix)
python tools/interactive_editor.py data/my_scenario.csv
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

#### Save Both Perspectives (Planned)

**Why This Feature Exists:**

The dual-perspective architecture enables modeling relational dynamics from both participants' viewpoints. However, iterative scenario development often requires:
- **Coordinated editing:** Making changes to both M1 and M2 perspectives in one session
- **Workflow preservation:** Saving intermediate states without switching perspectives
- **Comparison integrity:** Ensuring both perspectives saved from the same session state
- **Reduced friction:** Avoiding manual perspective switching just to save

Without "Save Both," you must:
1. Make edits to M1
2. Save M1 (Ctrl+S)
3. Switch to M2 perspective
4. Make coordinated M2 edits
5. Save M2 (Ctrl+S again)
6. Risk forgetting one perspective or losing session context

**What It Does:**

"Save Both Perspectives" writes **both** M1 and M2 data to separate files in a single operation:
- Creates/updates `{scenario}_M1_modified.csv` with M1 perspective data
- Creates/updates `{scenario}_M2_modified.csv` with M2 perspective data
- Uses current session state for both files (all committed modifications)
- Preserves independent edits: M1 and M2 each have their own primitives, markers, names

**When to Use:**

- **Scenario development:** You're building a canonical scenario and editing both perspectives
- **Iteration workflow:** Testing different relational patterns across both viewpoints
- **Pre-testing snapshots:** Saving a baseline before experimental changes
- **Session end:** Capturing all work from a single editing session

**When NOT to Use:**

- **Single-perspective focus:** You're only working on M1 or M2, not both
- **Comparison mode:** You're using --duplicate-to-m2 for diagnostic overlay (save only modified perspective)
- **Quick experiments:** Testing hypothetical changes to one perspective

**How to Use:**

**Menu/Toolbar (Planned):**
- File → Save Both Perspectives
- Keyboard shortcut: `Ctrl+Shift+S`
- Both files saved automatically, status shown: "Saved M1: [...], M2: [...]"

**File Naming:**
- M1 file: `{original_basename}_M1_modified.csv`
- M2 file: `{original_basename}_M2_modified.csv`
- Example: Loading `dating.csv` → Saves `dating_M1_modified.csv` and `dating_M2_modified.csv`

**Best Practices:**

1. **Use regular Save (Ctrl+S) during single-perspective work** - Faster, clearer intent
2. **Use Save Both when you've edited both perspectives** - Ensures consistency
3. **Name scenarios descriptively** - Files inherit the base name, so `steady_growth.csv` is better than `test.csv`
4. **Save before risky experiments** - Provides rollback point
5. **Check terminal output** - Confirms both files written successfully

**Technical Details:**

- Current save behavior: Saves active perspective only (`_M1_modified.csv` OR `_M2_modified.csv`)
- Save Both behavior: Saves **both** perspectives (`_M1_modified.csv` AND `_M2_modified.csv`)
- Each file contains: event list, primitives (v,r,f,a,S), marker/locked columns, metadata
- Perspectives remain independent: M1 and M2 can have completely different primitive values for the same event indices
- Reload behavior unchanged: Dual-file loading automatically detects both `_M1` and `_M2` companions

**Design Rationale:**

This feature follows the MVT (Modeled, Verifiable, Testable) quality standard:
- **Modeled:** Extends existing save architecture, uses proven model.save_csv() for both perspectives
- **Verifiable:** Clear success criteria (two files created/updated, terminal confirms both paths)
- **Testable:** Manual test checklist includes "Save Both with M1/M2 edits → verify both files updated correctly"

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

## Robust Mapping: Primitives ↔ Gamma_Self (UI Integration)

The editor maintains an explicit, debuggable mapping between each primitive change (event_id, primitive) and its corresponding γ_self (gamma_self) position on the trajectory plot. This ensures:
- Numbered labels and markers are always synchronized with their gamma_self positions
- Label placement is robust to edits, undo/redo, and perspective switching
- All mappings are logged for debugging and can be inspected in the State Viewer

For full technical details, debugging workflows, and example mapping logs, see [DEBUG.md](DEBUG.md#debugging-primitive-↔-gamma_self-mapping-v223-proposal).

**Right Panel - Editor Controls:**
- **Perspective Switcher:** M1/M2 radio buttons with visual indicators
- **Name Editor:** Editable scenario name field with Apply button
- **Note Editor:** Event annotation editor with Apply/Clear buttons
- **Gamma_Self_0 Editor:** Initial position editor
- **Spinbox Primitive Editor:** *[Planned v2.4]* Precise numeric input for primitives
- **Primitive Readout Gauge:** Shows last edited marker (to be replaced by spinbox)
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

**Spinbox Primitive Editing (Planned v2.4):**

*Replaces gauge-based editing with precise numeric input.*

**Overview:**
- Single shared spinbox for entering exact primitive values
- Shows currently active primitive (v, r, f, a, or S)
- Type exact values instead of dragging gauges

**Workflow:**
1. **Select event:** Click event marker in trajectory plot (e.g., Day 2)
2. **Select primitive:** Click primitive label (e.g., "v")
   - Spinbox label updates: "Editing: v"
   - Spinbox shows current v value: 5.5
3. **Enter value:** Type new value (e.g., "7.2") and press Enter
   - Or use ▲▼ arrows for incremental changes
4. **Trajectory updates:** Automatically recomputes

**Features:**
- **Range:** -10.0 to +10.0 (human-scale authoring values)
- **Precision:** 1 decimal place, 0.1 step size
- **Label persistence:** "Editing: {primitive}" stays until different primitive selected
- **State tracking:** Active primitive + event tracked, shown in State Viewer
- **Integration:** Works with Event Insertion Points, Ctrl+Shift+Click markers, M1/M2 switching

**Initial State:**
- Spinbox disabled until first event + primitive selected
- Label shows: "Editing: (none)"

**Edge Cases:**
- No event selected: Spinbox remains disabled
- Invalid input: Clamped to range, non-numeric rejected
- Perspective switch: Preserves active primitive, updates to new perspective's value
- Event deletion: Clears active primitive, disables spinbox

**Benefits:**
- Precise value control (type "7.2" vs dragging to approximate)
- Faster workflow (keyboard-driven)
- Cleaner UI (one spinbox vs multiple gauges)
- Better accessibility

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

# Load M2 file (automatically finds M1 if available)
python tools/interactive_editor.py data/single_dating_to_love_M2.csv

# Load any CSV file (works with or without _M1/_M2 suffix)
python tools/interactive_editor.py data/my_scenario.csv
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

#### Save Both Perspectives (Planned)

**Why This Feature Exists:**

The dual-perspective architecture enables modeling relational dynamics from both participants' viewpoints. However, iterative scenario development often requires:
- **Coordinated editing:** Making changes to both M1 and M2 perspectives in one session
- **Workflow preservation:** Saving intermediate states without switching perspectives
- **Comparison integrity:** Ensuring both perspectives saved from the same session state
- **Reduced friction:** Avoiding manual perspective switching just to save

Without "Save Both," you must:
1. Make edits to M1
2. Save M1 (Ctrl+S)
3. Switch to M2 perspective
4. Make coordinated M2 edits
5. Save M2 (Ctrl+S again)
6. Risk forgetting one perspective or losing session context

**What It Does:**

"Save Both Perspectives" writes **both** M1 and M2 data to separate files in a single operation:
- Creates/updates `{scenario}_M1_modified.csv` with M1 perspective data
- Creates/updates `{scenario}_M2_modified.csv` with M2 perspective data
- Uses current session state for both files (all committed modifications)
- Preserves independent edits: M1 and M2 each have their own primitives, markers, names

**When to Use:**

- **Scenario development:** You're building a canonical scenario and editing both perspectives
- **Iteration workflow:** Testing different relational patterns across both viewpoints
- **Pre-testing snapshots:** Saving a baseline before experimental changes
- **Session end:** Capturing all work from a single editing session

**When NOT to Use:**

- **Single-perspective focus:** You're only working on M1 or M2, not both
- **Comparison mode:** You're using --duplicate-to-m2 for diagnostic overlay (save only modified perspective)
- **Quick experiments:** Testing hypothetical changes to one perspective

**How to Use:**

**Menu/Toolbar (Planned):**
- File → Save Both Perspectives
- Keyboard shortcut: `Ctrl+Shift+S`
- Both files saved automatically, status shown: "Saved M1: [...], M2: [...]"

**File Naming:**
- M1 file: `{original_basename}_M1_modified.csv`
- M2 file: `{original_basename}_M2_modified.csv`
- Example: Loading `dating.csv` → Saves `dating_M1_modified.csv` and `dating_M2_modified.csv`

**Best Practices:**

1. **Use regular Save (Ctrl+S) during single-perspective work** - Faster, clearer intent
2. **Use Save Both when you've edited both perspectives** - Ensures consistency
3. **Name scenarios descriptively** - Files inherit the base name, so `steady_growth.csv` is better than `test.csv`
4. **Save before risky experiments** - Provides rollback point
5. **Check terminal output** - Confirms both files written successfully

**Technical Details:**

- Current save behavior: Saves active perspective only (`_M1_modified.csv` OR `_M2_modified.csv`)
- Save Both behavior: Saves **both** perspectives (`_M1_modified.csv` AND `_M2_modified.csv`)
- Each file contains: event list, primitives (v,r,f,a,S), marker/locked columns, metadata
- Perspectives remain independent: M1 and M2 can have completely different primitive values for the same event indices
- Reload behavior unchanged: Dual-file loading automatically detects both `_M1` and `_M2` companions

**Design Rationale:**

This feature follows the MVT (Modeled, Verifiable, Testable) quality standard:
- **Modeled:** Extends existing save architecture, uses proven model.save_csv() for both perspectives
- **Verifiable:** Clear success criteria (two files created/updated, terminal confirms both paths)
- **Testable:** Manual test checklist includes "Save Both with M1/M2 edits → verify both files updated correctly"

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

## Robust Mapping: Primitives ↔ Gamma_Self (UI Integration)

The editor maintains an explicit, debuggable mapping between each primitive change (event_id, primitive) and its corresponding γ_self (gamma_self) position on the trajectory plot. This ensures:
- Numbered labels and markers are always synchronized with their gamma_self positions
- Label placement is robust to edits, undo/redo, and perspective switching
- All mappings are logged for debugging and can be inspected in the State Viewer

For full technical details, debugging workflows, and example mapping logs, see [DEBUG.md](DEBUG.md#debugging-primitive-↔-gamma_self-mapping-v223-proposal).

**Right Panel - Editor Controls:**
- **Perspective Switcher:** M1/M2 radio buttons with visual indicators
- **Name Editor:** Editable scenario name field with Apply button
- **Note Editor:** Event annotation editor with Apply/Clear buttons
- **Gamma_Self_0 Editor:** Initial position editor
- **Spinbox Primitive Editor:** *[Planned v2.4]* Precise numeric input for primitives
- **Primitive Readout Gauge:** Shows last edited marker (to be replaced by spinbox)
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

**Spinbox Primitive Editing (Planned v2.4):**

*Replaces gauge-based editing with precise numeric input.*

**Overview:**
- Single shared spinbox for entering exact primitive values
- Shows currently active primitive (v, r, f, a, or S)
- Type exact values instead of dragging gauges

**Workflow:**
1. **Select event:** Click event marker in trajectory plot (e.g., Day 2)
2. **Select primitive:** Click primitive label (e.g., "v")
   - Spinbox label updates: "Editing: v"
   - Spinbox shows current v value: 5.5
3. **Enter value:** Type new value (e.g., "7.2") and press Enter
   - Or use ▲▼ arrows for incremental changes
4. **Trajectory updates:** Automatically recomputes

**Features:**
- **Range:** -10.0 to +10.0 (human-scale authoring values)
- **Precision:** 1 decimal place, 0.1 step size
- **Label persistence:** "Editing: {primitive}" stays until different primitive selected
- **State tracking:** Active primitive + event tracked, shown in State Viewer
- **Integration:** Works with Event Insertion Points, Ctrl+Shift+Click markers, M1/M2 switching

**Initial State:**
- Spinbox disabled until first event + primitive selected
- Label shows: "Editing: (none)"

**Edge Cases:**
- No event selected: Spinbox remains disabled
- Invalid input: Clamped to range, non-numeric rejected
- Perspective switch: Preserves active primitive, updates to new perspective's value
- Event deletion: Clears active primitive, disables spinbox

**Benefits:**
- Precise value control (type "7.2" vs dragging to approximate)
- Faster workflow (keyboard-driven)
- Cleaner UI (one spinbox vs multiple gauges)
- Better accessibility

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

# Load M2 file (automatically finds M1 if available)
python tools/interactive_editor.py data/single_dating_to_love_M2.csv

# Load any CSV file (works with or without _M1/_M2 suffix)
python tools/interactive_editor.py data/my_scenario.csv
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

#### Save Both Perspectives (Planned)

**Why This Feature Exists:**

The dual-perspective architecture enables modeling relational dynamics from both participants' viewpoints. However, iterative scenario development often requires:
- **Coordinated editing:** Making changes to both M1 and M2 perspectives in one session
- **Workflow preservation:** Saving intermediate states without switching perspectives
- **Comparison integrity:** Ensuring both perspectives saved from the same session state
- **Reduced friction:** Avoiding manual perspective switching just to save

Without "Save Both," you must:
1. Make edits to M1
2. Save M1 (Ctrl+S)
3. Switch to M2 perspective
4. Make coordinated M2 edits
5. Save M2 (Ctrl+S again)
6. Risk forgetting one perspective or losing session context

**What It Does:**

"Save Both Perspectives" writes **both** M1 and M2 data to separate files in a single operation:
- Creates/updates `{scenario}_M1_modified.csv` with M1 perspective data
- Creates/updates `{scenario}_M2_modified.csv` with M2 perspective data
- Uses current session state for both files (all committed modifications)
- Preserves independent edits: M1 and M2 each have their own primitives, markers, names

**When to Use:**

- **Scenario development:** You're building a canonical scenario and editing both perspectives
- **Iteration workflow:** Testing different relational patterns across both viewpoints
- **Pre-testing snapshots:** Saving a baseline before experimental changes
- **Session end:** Capturing all work from a single editing session

**When NOT to Use:**

- **Single-perspective focus:** You're only working on M1 or M2, not both
- **Comparison mode:** You're using --duplicate-to-m2 for diagnostic overlay (save only modified perspective)
- **Quick experiments:** Testing hypothetical changes to one perspective

**How to Use:**

**Menu/Toolbar (Planned):**
- File → Save Both Perspectives
- Keyboard shortcut: `Ctrl+Shift+S`
- Both files saved automatically, status shown: "Saved M1: [...], M2: [...]"

**File Naming:**
- M1 file: `{original_basename}_M1_modified.csv`
- M2 file: `{original_basename}_M2_modified.csv`
- Example: Loading `dating.csv` → Saves `dating_M1_modified.csv` and `dating_M2_modified.csv`

**Best Practices:**

1. **Use regular Save (Ctrl+S) during single-perspective work** - Faster, clearer intent
2. **Use Save Both when you've edited both perspectives** - Ensures consistency
3. **Name scenarios descriptively** - Files inherit the base name, so `steady_growth.csv` is better than `test.csv`
4. **Save before risky experiments** - Provides rollback point
5. **Check terminal output** - Confirms both files written successfully

**Technical Details:**

- Current save behavior: Saves active perspective only (`_M1_modified.csv` OR `_M2_modified.csv`)
- Save Both behavior: Saves **both** perspectives (`_M1_modified.csv` AND `_M2_modified.csv`)
- Each file contains: event list, primitives (v,r,f,a,S), marker/locked columns, metadata
- Perspectives remain independent: M1 and M2 can have completely different primitive values for the same event indices
- Reload behavior unchanged: Dual-file loading automatically detects both `_M1` and `_M2` companions

**Design Rationale:**

This feature follows the MVT (Modeled, Verifiable, Testable) quality standard:
- **Modeled:** Extends existing save architecture, uses proven model.save_csv() for both perspectives
- **Verifiable:** Clear success criteria (two files created/updated, terminal confirms both paths)
- **Testable:** Manual test checklist includes "Save Both with M1/M2 edits → verify both files updated correctly"

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

## Robust Mapping: Primitives ↔ Gamma_Self (UI Integration)

The editor maintains an explicit, debuggable mapping between each primitive change (event_id, primitive) and its corresponding γ_self (gamma_self) position on the trajectory plot. This ensures:
- Numbered labels and markers are always synchronized with their gamma_self positions
- Label placement is robust to edits, undo/redo, and perspective switching
- All mappings are logged for debugging and can be inspected in the State Viewer

For full technical details, debugging workflows, and example mapping logs, see [DEBUG.md](DEBUG.md#debugging-primitive-↔-gamma_self-mapping-v223-proposal).

**Right Panel - Editor Controls:**
- **Perspective Switcher:** M1/M2 radio buttons with visual indicators
- **Name Editor:** Editable scenario name field with Apply button
- **Note Editor:** Event annotation editor with Apply/Clear buttons
- **Gamma_Self_0 Editor:** Initial position editor
- **Spinbox Primitive Editor:** *[Planned v2.4]* Precise numeric input for primitives
- **Primitive Readout Gauge:** Shows last edited marker (to be replaced by spinbox)
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

**Spinbox Primitive Editing (Planned v2.4):**

*Replaces gauge-based editing with precise numeric input.*

**Overview:**
- Single shared spinbox for entering exact primitive values
- Shows currently active primitive (v, r, f, a, or S)
- Type exact values instead of dragging gauges

**Workflow:**
1. **Select event:** Click event marker in trajectory plot (e.g., Day 2)
2. **Select primitive:** Click primitive label (e.g., "v")
   - Spinbox label updates: "Editing: v"
   - Spinbox shows current v value: 5.5
3. **Enter value:** Type new value (e.g., "7.2") and press Enter
   - Or use ▲▼ arrows for incremental changes
4. **Trajectory updates:** Automatically recomputes

**Features:**
- **Range:** -10.0 to +10.0 (human-scale authoring values)
- **Precision:** 1 decimal place, 0.1 step size
- **Label persistence:** "Editing: {primitive}" stays until different primitive selected
- **State tracking:** Active primitive + event tracked, shown in State Viewer
- **Integration:** Works with Event Insertion Points, Ctrl+Shift+Click markers, M1/M2 switching

**Initial State:**
- Spinbox disabled until first event + primitive selected
- Label shows: "Editing: (none)"

**Edge Cases:**
- No event selected: Spinbox remains disabled
- Invalid input: Clamped to range, non-numeric rejected
- Perspective switch: Preserves active primitive, updates to new perspective's value
- Event deletion: Clears active primitive, disables spinbox

**Benefits:**
- Precise value control (type "7.2" vs dragging to approximate)
- Faster workflow (keyboard-driven)
- Cleaner UI (one spinbox vs multiple gauges)
- Better accessibility

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

# Load M2 file (automatically finds M1 if available)
python tools/interactive_editor.py data/single_dating_to_love_M2.csv

# Load any CSV file (works with or without _M1/_M2 suffix)
python tools/interactive_editor.py data/my_scenario.csv
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

#### Save Both Perspectives (Planned)

**Why This Feature Exists:**

The dual-perspective architecture enables modeling relational dynamics from both participants' viewpoints. However, iterative scenario development often requires:
- **Coordinated editing:** Making changes to both M1 and M2 perspectives in one session
- **Workflow preservation:** Saving intermediate states without switching perspectives
- **Comparison integrity:** Ensuring both perspectives saved from the same session state
- **Reduced friction:** Avoiding manual perspective switching just to save

Without "Save Both," you must:
1. Make edits to M1
2. Save M1 (Ctrl+S)
3. Switch to M2 perspective
4. Make coordinated M2 edits
5. Save M2 (Ctrl+S again)
6. Risk forgetting one perspective or losing session context

**What It Does:**

"Save Both Perspectives" writes **both** M1 and M2 data to separate files in a single operation:
- Creates/updates `{scenario}_M1_modified.csv` with M1 perspective data
- Creates/updates `{scenario}_M2_modified.csv` with M2 perspective data
- Uses current session state for both files (all committed modifications)
- Preserves independent edits: M1 and M2 each have their own primitives, markers, names

**When to Use:**

- **Scenario development:** You're building a canonical scenario and editing both perspectives
- **Iteration workflow:** Testing different relational patterns across both viewpoints
- **Pre-testing snapshots:** Saving a baseline before experimental changes
- **Session end:** Capturing all work from a single editing session

**When NOT to Use:**

- **Single-perspective focus:** You're only working on M1 or M2, not both
- **Comparison mode:** You're using --duplicate-to-m2 for diagnostic overlay (save only modified perspective)
- **Quick experiments:** Testing hypothetical changes to one perspective

**How to Use:**

**Menu/Toolbar (Planned):**
- File → Save Both Perspectives
- Keyboard shortcut: `Ctrl+Shift+S`
- Both files saved automatically, status shown: "Saved M1: [...], M2: [...]"

**File Naming:**
- M1 file: `{original_basename}_M1_modified.csv`
- M2 file: `{original_basename}_M2_modified.csv`
- Example: Loading `dating.csv` → Saves `dating_M1_modified.csv` and `dating_M2_modified.csv`

**Best Practices:**

1. **Use regular Save (Ctrl+S) during single-perspective work** - Faster, clearer intent
2. **Use Save Both when you've edited both perspectives** - Ensures consistency
3. **Name scenarios descriptively** - Files inherit the base name, so `steady_growth.csv` is better than `test.csv`
4. **Save before risky experiments** - Provides rollback point
5. **Check terminal output** - Confirms both files written successfully

**Technical Details:**

- Current save behavior: Saves active perspective only (`_M1_modified.csv` OR `_M2_modified.csv`)
- Save Both behavior: Saves **both** perspectives (`_M1_modified.csv` AND `_M2_modified.csv`)
- Each file contains: event list, primitives (v,r,f,a,S), marker/locked columns, metadata
- Perspectives remain independent: M1 and M2 can have completely different primitive values for the same event indices
- Reload behavior unchanged: Dual-file loading automatically detects both `_M1` and `_M2` companions

**Design Rationale:**

This feature follows the MVT (Modeled, Verifiable, Testable) quality standard:
- **Modeled:** Extends existing save architecture, uses proven model.save_csv() for both perspectives
- **Verifiable:** Clear success criteria (two files created/updated, terminal confirms both paths)
- **Testable:** Manual test checklist includes "Save Both with M1/M2 edits → verify both files updated correctly"

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

## Robust Mapping: Primitives ↔ Gamma_Self (UI Integration)

The editor maintains an explicit, debuggable mapping between each primitive change (event_id, primitive) and its corresponding γ_self (gamma_self) position on the trajectory plot. This ensures:
- Numbered labels and markers are always synchronized with their gamma_self positions
- Label placement is robust to edits, undo/redo, and perspective switching
- All mappings are logged for debugging and can be inspected in the State Viewer

For full technical details, debugging workflows, and example mapping logs, see [DEBUG.md](DEBUG.md#debugging-primitive-↔-gamma_self-mapping-v223-proposal).

**Right Panel - Editor Controls:**
- **Perspective Switcher:** M1/M2 radio buttons with visual indicators
- **Name Editor:** Editable scenario name field with Apply button
- **Note Editor:** Event annotation editor with Apply/Clear buttons
- **Gamma_Self_0 Editor:** Initial position editor
- **Spinbox Primitive Editor:** *[Planned v2.4]* Precise numeric input for primitives
- **Primitive Readout Gauge:** Shows last edited marker (to be replaced by spinbox)
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

**Spinbox Primitive Editing (Planned v2.4):**

*Replaces gauge-based editing with precise numeric input.*

**Overview:**
- Single shared spinbox for entering exact primitive values
- Shows currently active primitive (v, r, f, a, or S)
- Type exact values instead of dragging gauges

**Workflow:**
1. **Select event:** Click event marker in trajectory plot (e.g., Day 2)
2. **Select primitive:** Click primitive label (e.g., "v")
   - Spinbox label updates: "Editing: v"
   - Spinbox shows current v value: 5.5
3. **Enter value:** Type new value (e.g., "7.2") and press Enter
   - Or use ▲▼ arrows for incremental changes
4. **Trajectory updates:** Automatically recomputes

**Features:**
- **Range:** -10.0 to +10.0 (human-scale authoring values)
- **Precision:** 1 decimal place, 0.1 step size
- **Label persistence:** "Editing: {primitive}" stays until different primitive selected
- **State tracking:** Active primitive + event tracked, shown in State Viewer
- **Integration:** Works with Event Insertion Points, Ctrl+Shift+Click markers, M1/M2 switching

**Initial State:**
- Spinbox disabled until first event + primitive selected
- Label shows: "Editing: (none)"

**Edge Cases:**
- No event selected: Spinbox remains disabled
- Invalid input: Clamped to range, non-numeric rejected
- Perspective switch: Preserves active primitive, updates to new perspective's value
- Event deletion: Clears active primitive, disables spinbox

**Benefits:**
- Precise value control (type "7.2" vs dragging to approximate)
- Faster workflow (keyboard-driven)
- Cleaner UI (one spinbox vs multiple gauges)
- Better accessibility

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

## Marker and Label Behavior

- When you move a marker away from its baseline, its label appears and remains visible.
- Moving additional markers will show their labels as well; all modified markers keep their labels.
- A label disappears only when its marker is reset to baseline (by double-click, Ctrl+Z, or moving it back).
- This applies to both the primitive panel and the trajectory panel.
- Switching perspectives (M1/M2) will only show labels for markers modified in that perspective.
- No labels appear for unmodified markers, and no stray labels appear after switching perspectives or modifying unrelated markers.

---

## Basic Workflow

### 1. Load a Scenario
```bash
# Standard dual-perspective load
python tools/interactive_editor.py data/single_dating_to_love_M1.csv

# Load M2 file (automatically finds M1 if available)
python tools/interactive_editor.py data/single_dating_to_love_M2.csv

# Load any CSV file (works with or without _M1/_M2 suffix)
python tools/interactive_editor.py data/my_scenario.csv
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

#### Save Both Perspectives (Planned)

**Why This Feature Exists:**

The dual-perspective architecture enables modeling relational dynamics from both participants' viewpoints. However, iterative scenario development often requires:
- **Coordinated editing:** Making changes to both M1 and M2 perspectives in one session
- **Workflow preservation:** Saving intermediate states without switching perspectives
- **Comparison integrity:** Ensuring both perspectives saved from the same session state
- **Reduced friction:** Avoiding manual perspective switching just to save

Without "Save Both," you must:
1. Make edits to M1
2. Save M1 (Ctrl+S)
3. Switch to M2 perspective
4. Make coordinated M2 edits
5. Save M2 (Ctrl+S again)
6. Risk forgetting one perspective or losing session context

**What It Does:**

"Save Both Perspectives" writes **both** M1 and M2 data to separate files in a single operation:
- Creates/updates `{scenario}_M1_modified.csv` with M1 perspective data
- Creates/updates `{scenario}_M2_modified.csv` with M2 perspective data
- Uses current session state for both files (all committed modifications)
- Preserves independent edits: M1 and M2 each have their own primitives, markers, names

**When to Use:**

- **Scenario development:** You're building a canonical scenario and editing both perspectives
- **Iteration workflow:** Testing different relational patterns across both viewpoints
- **Pre-testing snapshots:** Saving a baseline before experimental changes
- **Session end:** Capturing all work from a single editing session

**When NOT to Use:**

- **Single-perspective focus:** You're only working on M1 or M2, not both
- **Comparison mode:** You're using --duplicate-to-m2 for diagnostic overlay (save only modified perspective)
- **Quick experiments:** Testing hypothetical changes to one perspective

**How to Use:**

**Menu/Toolbar (Planned):**
- File → Save Both Perspectives
- Keyboard shortcut: `Ctrl+Shift+S`
- Both files saved automatically, status shown: "Saved M1: [...], M2: [...]"

**File Naming:**
- M1 file: `{original_basename}_M1_modified.csv`
- M2 file: `{original_basename}_M2_modified.csv`
- Example: Loading `dating.csv` → Saves `dating_M1_modified.csv` and `dating_M2_modified.csv`

**Best Practices:**

1. **Use regular Save (Ctrl+S) during single-perspective work** - Faster, clearer intent
2. **Use Save Both when you've edited both perspectives** - Ensures consistency
3. **Name scenarios descriptively** - Files inherit the base name, so `steady_growth.csv` is better than `test.csv`
4. **Save before risky experiments** - Provides rollback point
5. **Check terminal output** - Confirms both files written successfully

**Technical Details:**

- Current save behavior: Saves active perspective only (`_M1_modified.csv` OR `_M2_modified.csv`)
- Save Both behavior: Saves **both** perspectives (`_M1_modified.csv` AND `_M2_modified.csv`)
- Each file contains: event list, primitives (v,r,f,a,S), marker/locked columns, metadata
- Perspectives remain independent: M1 and M2 can have completely different primitive values for the same event indices
- Reload behavior unchanged: Dual-file loading automatically detects both `_M1` and `_M2` companions

**Design Rationale:**

This feature follows the MVT (Modeled, Verifiable, Testable) quality standard:
- **Modeled:** Extends existing save architecture, uses proven model.save_csv() for both perspectives
- **Verifiable:** Clear success criteria (two files created/updated, terminal confirms both paths)
- **Testable:** Manual test checklist includes "Save Both with M1/M2 edits → verify both files updated correctly"

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

## Robust Mapping: Primitives ↔ Gamma_Self (UI Integration)

The editor maintains an explicit, debuggable mapping between each primitive change (event_id, primitive) and its corresponding γ_self (gamma_self) position on the trajectory plot. This ensures:
- Numbered labels and markers are always synchronized with their gamma_self positions
- Label placement is robust to edits, undo/redo, and perspective switching
- All mappings are logged for debugging and can be inspected in the State Viewer

For full technical details, debugging workflows, and example mapping logs, see [DEBUG.md](DEBUG.md#debugging-primitive-↔-gamma_self-mapping-v223-proposal).

**Right Panel - Editor Controls:**
- **Perspective Switcher:** M1/M2 radio buttons with visual indicators
- **Name Editor:** Editable scenario name field with Apply button
- **Note Editor:** Event annotation editor with Apply/Clear buttons
- **Gamma_Self_0 Editor:** Initial position editor
- **Spinbox Primitive Editor:** *[Planned v2.4]* Precise numeric input for primitives
- **Primitive Readout Gauge:** Shows last edited marker (to be replaced by spinbox)
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

**Spinbox Primitive Editing (Planned v2.4):**

*Replaces gauge-based editing with precise numeric input.*

**Overview:**
- Single shared spinbox for entering exact primitive values
- Shows currently active primitive (v, r, f, a, or S)
- Type exact values instead of dragging gauges

**Workflow:**
1. **Select event:** Click event marker in trajectory plot (e.g., Day 2)
2. **Select primitive:** Click primitive label (e.g., "v")
   - Spinbox label updates: "Editing: v"
   - Spinbox shows current v value: 5.5
3. **Enter value:** Type new value (e.g., "7.2") and press Enter
   - Or use ▲▼ arrows for incremental changes
4. **Trajectory updates:** Automatically recomputes

**Features:**
- **Range:** -10.0 to +10.0 (human-scale authoring values)
- **Precision:** 1 decimal place, 0.1 step size
- **Label persistence:** "Editing: {primitive}" stays until different primitive selected
- **State tracking:** Active primitive + event tracked, shown in State Viewer
- **Integration:** Works with Event Insertion Points, Ctrl+Shift+Click markers, M1/M2 switching

**Initial State:**
- Spinbox disabled until first event + primitive selected
- Label shows: "Editing: (none)"

**Edge Cases:**
- No event selected: Spinbox remains disabled
- Invalid input: Clamped to range, non-numeric rejected
- Perspective switch: Preserves active primitive, updates to new perspective's value
- Event deletion: Clears active primitive, disables spinbox

**Benefits:**
- Precise value control (type "7.2" vs dragging to approximate)
- Faster workflow (keyboard-driven)
- Cleaner UI (one spinbox vs multiple gauges)
- Better accessibility

### Save Button & Controls
Located in the toolbar at the top of the window:
- **Save Button:** Save CSV to `data/` folder with `_modified` suffix
- **Ctrl+S:** Keyboard shortcut for save
- **Automatic perspective handling:** Saves to M1_modified or M2_modified based on active perspective

**Save Behavior:**
- M1 perspective active → saves to `*_M1_modified.csv`
- M2 perspective active → saves to `*_M2_modified.csv`
- Single-file scenarios: Can save to either M1 or M2, enabling perspective conversion
