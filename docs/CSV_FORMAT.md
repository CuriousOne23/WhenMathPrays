# CSV Format Specification

This document is the authoritative reference for the CSV file format used in the WhenMathPrays project for scenario data, including both the interactive editor and scenario scripts.

---

## Overview

CSV files define the timeline of relational primitives for a scenario. Each row represents an event or time point, and each column encodes a primitive or metadata.

---

## Metadata Rows (Required)

The first rows of the CSV must specify scenario metadata:

- `name,<string>` — Scenario or subject name
- `time_unit,<string>` — Unit for the time column (e.g., days, weeks, months, years, events)
- `gamma_self_0,<complex>` — Initial gamma_self state (e.g., -5+0j)

Example:
```
name,Fred
time_unit,days
gamma_self_0,-5+0j
```

---

## Data Columns (Required & Optional)

### Required Columns
- `day` (or `step`, `event`, `time`, `time_index`): Time index (float or integer)
- `v`: Visibility
- `r`: Resonance
- `f`: Fidelity
- `a`: Altruism
- `S`: Shared Breath

### Optional Columns
- `notes`: Human-readable context for each event
- `marker`: Marker for editor tracking (e.g., star, circle)
- `locked`: Lock status (True/False or 1/0)

Example header:
```
day,v,r,f,a,S,notes,marker,locked
```

---


## Primitive Scaling and Reference

**Scale:**
- All primitives (`v`, `r`, `f`, `a`, `S`) are rated on a human scale from -10 (maximally negative) to +10 (maximally positive), with 0 as neutral.

**Reference:**
- Ratings are always from the perspective of the subject (e.g., M1 or M2). For example, in an M1 file, the value represents what M1 feels in regard to M2 (i.e., what M2 makes M1 feel). It is NOT what M1 thinks M2 feels, nor what M1 "should" feel. This convention ensures that each primitive is directly tractable and comparable across scenarios and subjects.

**Rationale for Tractability:**
- By always using the subject's own perspective, the data is unambiguous and can be consistently interpreted and compared. This avoids the confusion of "second-order" feelings (e.g., what M1 thinks M2 feels about M1), which are much harder to rate and validate.

**Practical Examples:**
- If M1 feels deeply trusted by M2 at day 14, `f` (Fidelity) might be +8.
- If M1 feels abandoned by M2 at day 21, `v` (Visibility) might be -7.
- If M2 feels inspired by M1 at day 10, then in the M2 file, `r` (Resonance) might be +9.
- If M2 feels betrayed by M1 at day 30, then in the M2 file, `f` (Fidelity) might be -10.

**Summary Table:**
| Value | Meaning (from subject's perspective) |
|-------|-------------------------------------|
| -10   | Maximally negative (e.g., betrayal, abandonment, cruelty) |
| 0     | Neutral (no event, typical interaction) |
| +10   | Maximally positive (e.g., profound moment, breakthrough) |

**Tip:**
If in doubt, ask: "How did this event make the subject feel about the other person, in this moment?" Rate that feeling directly.

---

## Value Ranges
- Primitives: -10 to +10 (float or integer)
- Time: float or integer (fractional times allowed)
- Notes: free text
- Marker: string (optional, for editor use)
- Locked: boolean or integer (optional, for editor use)

---

## Dual-Perspective Conventions
- Use `_M1` and `_M2` suffixes in filenames for dual-perspective scenarios.
- Each file should use the subject's perspective for all primitive ratings.

---

## Example CSV (Full)
```
name,Fred
time_unit,days
gamma_self_0,-5+0j
day,v,r,f,a,S,notes,marker,locked
0,5,0,2,2,0,Initial condition: eager but moderate love,,
7,5,2,2,3,1,First date: strong attraction developing,,
14,5,-2,2,3,-1,Early wobble: pressing pace - M2 pulls back,,
21,5,2,5,5,3,Repair begins: slows down and listens,,
28,5,5,5,5,5,Shared rhythm: casual comfort - ego softens,,
35,5,7,7,7,7,Repair complete: trust growing - balanced,,
42,6,8,8,8,8,Stable connection: ego moderated - love rising,,
49,7,9,9,9,9,Steady connection: playful and secure,,
56,8,9,9,9,10,Higher plateau: feels secure,,
60,8,9,9,9,10,Outcome: stable relationship - strong love,,
```

---

## Edge Cases & Compatibility
- Fractional time values are supported (e.g., 2.5 days).
- Integer-only and mixed-precision time columns are allowed.
- Extra columns are ignored by the editor and scripts.
- Backward compatibility: Older CSVs without optional columns are still supported.

---

## FAQ & Troubleshooting
- **Q:** What if I want to rate from M1's view of M2's feelings?  
**A:** Always rate from the subject's own feelings for tractability.
- **Q:** Can I use other column names for time?  
**A:** Yes, aliases like `step`, `event`, `time`, or `time_index` are accepted.
- **Q:** What if I omit optional columns?  
**A:** The system will still work; optional columns are for enhanced features.

---

For further details, see the scenario configuration and editor user guide. All other documentation should link to this file for CSV format and primitive reference details.
