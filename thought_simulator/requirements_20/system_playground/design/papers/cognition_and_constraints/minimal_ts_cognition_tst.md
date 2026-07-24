# Minimal TS Cognition Test
**File:** `minimal_ts_cognition_tst.md`
**Location:** `thought_simulator/20_requirements/system_playground`
**Version:** 0.1.0
**Date:** 2026-06-28

---

## 1. Purpose

This document specifies the smallest possible test harness for validating core Thought Simulator (TS) cognition behaviours:

- Identity-object (IdOB) registration and recall
- Manifold region traversal
- Ambiguous-instruction disambiguation
- Replay integrity
- End-to-end simulation flow

All sets are intentionally minimal so tests run fast and failures are easy to isolate.

---

## 2. Minimal Identity Object Set (IdOB × 5)

Each IdOB is the atomic unit of identity the TS tracks. The five below cover the five canonical IdOB roles.

| # | ID       | Label         | Role       | Seed Value              | Mutable |
|---|----------|---------------|------------|-------------------------|---------|
| 1 | `iob-A`  | `self`        | Anchor     | `"I"`                   | No      |
| 2 | `iob-B`  | `task`        | Goal       | `"solve(x)"`            | Yes     |
| 3 | `iob-C`  | `context`     | Frame      | `"session_start"`       | Yes     |
| 4 | `iob-D`  | `constraint`  | Limiter    | `"max_steps=10"`        | Yes     |
| 5 | `iob-E`  | `observer`    | Monitor    | `"log_all=true"`        | No      |

**Rules:**
- `iob-A` (Anchor) must always be present; its seed value is immutable.
- `iob-E` (Monitor) is read-only during simulation; writes to it must raise `IdOB_WriteViolation`.
- All other IdOBs may be updated by the simulation engine between steps.

---

## 3. Minimal Manifold (3 Regions)

The manifold is the cognitive state-space the TS navigates. Three regions are sufficient to exercise enter/traverse/exit logic.

```
┌─────────────────────────────────────────┐
│  Region Ω  (Undecided / Entry)          │
│  • Default region on simulation init    │
│  • Accepts any IdOB set                 │
│  • Transitions → Σ or Δ on first step   │
└───────────────┬────────────┬────────────┘
                │            │
        [clear] │            │ [ambiguous]
                ▼            ▼
 ┌──────────────────┐  ┌──────────────────┐
 │  Region Σ        │  │  Region Δ        │
 │  (Resolved)      │  │  (Conflict)      │
 │  • Goal reachable│  │  • Disambiguate  │
 │  • Execute steps │  │  • Re-emit IdOBs │
 │  • Exits → Ω on  │  │  • Exits → Σ or  │
 │    task complete │  │    HALT on fail  │
 └──────────────────┘  └──────────────────┘
```

| Region | Entry Condition                   | Exit Condition(s)                           |
|--------|-----------------------------------|---------------------------------------------|
| Ω      | `sim_init()`                      | Instruction parsed → Σ; Ambiguity → Δ       |
| Σ      | Instruction resolved              | Task complete → Ω; New ambiguity → Δ        |
| Δ      | Ambiguity detected in Ω or Σ      | Disambiguation succeeds → Σ; Timeout → HALT |

---

## 4. Ambiguous Instruction Test

### 4.1 Test Input

```
instruction: "Continue from where we left off and fix it."
```

### 4.2 Why It Is Ambiguous

| Ambiguity Token       | Problem                                                                    |
|-----------------------|----------------------------------------------------------------------------|
| `"Continue"`          | No prior context bound to `iob-C`                                          |
| `"where we left off"` | Session reference unknown; `iob-C = "session_start"` (uninitialised)       |
| `"fix it"`            | Referent of `"it"` unresolved; `iob-B` holds generic goal                  |

### 4.3 Expected TS Behaviour

1. **Parser** flags 3 unresolved references → emits `AMBIGUITY_DETECTED(count=3)`.
2. **Router** transitions manifold: `Ω → Δ`.
3. **Disambiguator** queries each IdOB in order of dependency:
   - Resolves `iob-C` first (frame) → attempts session-history lookup.
   - Resolves `iob-B` (goal) conditioned on `iob-C`.
   - Resolves implicit pronoun `"it"` → binds to `iob-B.seed`.
4. If all three resolve → emits `DISAMBIGUATION_OK` → `Δ → Σ`.
5. If any fails within `max_steps` (from `iob-D`) → emits `HALT(reason="disambiguation_timeout")`.

### 4.4 Pass Criteria

| Check                       | Expected Value  |
|-----------------------------|-----------------|
| Initial region              | `Ω`             |
| Region after parse          | `Δ`             |
| `AMBIGUITY_DETECTED.count`  | `3`             |
| Region after disambiguation | `Σ`             |
| IdOBs mutated               | `iob-B`, `iob-C`|
| IdOBs unchanged             | `iob-A`, `iob-E`|

---

## 5. Replay Test

The replay test verifies that re-feeding a recorded simulation trace produces an identical outcome.

### 5.1 Recorded Trace (Canonical)

```jsonc
{
  "trace_id": "replay-001",
  "steps": [
    { "step": 1, "region": "Ω", "event": "sim_init",           "idob_snapshot": { "iob-B": "solve(x)", "iob-C": "session_start" } },
    { "step": 2, "region": "Ω", "event": "AMBIGUITY_DETECTED", "count": 3 },
    { "step": 3, "region": "Δ", "event": "disambiguate_begin",  "targets": ["iob-C","iob-B","pronoun_it"] },
    { "step": 4, "region": "Δ", "event": "iob_mutate",          "id": "iob-C", "new_value": "session_42" },
    { "step": 5, "region": "Δ", "event": "iob_mutate",          "id": "iob-B", "new_value": "fix(bug_77)" },
    { "step": 6, "region": "Δ", "event": "DISAMBIGUATION_OK",   "resolved": 3 },
    { "step": 7, "region": "Σ", "event": "execute_begin",       "goal": "fix(bug_77)" },
    { "step": 8, "region": "Σ", "event": "task_complete",       "result": "PASS" }
  ]
}
```

### 5.2 Replay Execution Rules

1. Feed the trace to `TS.replay(trace_id="replay-001")`.
2. The engine must re-execute each step **in order**; no step may be skipped.
3. At each step, compare the live region and IdOB snapshot against the recorded values.
4. Any mismatch emits `REPLAY_DIVERGENCE(step=N, field=F)` and halts the replay.

### 5.3 Pass Criteria

| Check                          | Expected Value     |
|--------------------------------|--------------------|
| Steps executed                 | 8                  |
| `REPLAY_DIVERGENCE` events     | 0                  |
| Final region                   | `Σ`                |
| Final `iob-B` value            | `"fix(bug_77)"`    |
| Final `iob-C` value            | `"session_42"`     |
| `iob-A` unchanged throughout   | `"I"`              |
| `iob-E` unchanged throughout   | `"log_all=true"`   |

---

## 6. Expected System Simulation Flow

The diagram below shows the canonical happy-path through the TS for a single cognition cycle, incorporating all elements above.

```
sim_init()
    │
    ▼
[Load IdOBs iob-A … iob-E]
    │
    ▼
[Enter Manifold: Region Ω]
    │
    ▼
[Parse Instruction]────────► Unambiguous?
    │                              │ YES
    │ NO (ambiguous)               ▼
    ▼                       [Enter Region Σ]
[Enter Region Δ]                   │
    │                              ▼
[Disambiguator]             [Execute Steps]
    │                              │
    │ success                      ▼
    ▼                       [Task Complete?]
[DISAMBIGUATION_OK]                │ YES
    │                              ▼
    └──────────────────────► [Return to Ω / Emit Result]
                                   │
                                   ▼
                              [sim_end()]
```

### 6.1 Step-by-Step Narrative

| Step | Action                                                    | Active Region | IdOBs Involved                     |
|------|-----------------------------------------------------------|---------------|-------------------------------------|
| S1   | `sim_init()` — load all 5 IdOBs, set defaults             | Ω             | iob-A, iob-B, iob-C, iob-D, iob-E |
| S2   | Parse incoming instruction                                | Ω             | iob-B, iob-C                        |
| S3   | Detect ambiguity → `AMBIGUITY_DETECTED`                   | Ω → Δ         | iob-B, iob-C                        |
| S4   | Disambiguate `iob-C` (frame resolution)                   | Δ             | iob-C                               |
| S5   | Disambiguate `iob-B` (goal resolution)                    | Δ             | iob-B                               |
| S6   | Resolve pronoun reference                                 | Δ             | iob-B                               |
| S7   | `DISAMBIGUATION_OK` → transition to Σ                     | Δ → Σ         | iob-B, iob-C                        |
| S8   | Execute goal (`fix(bug_77)`) within `max_steps=10`        | Σ             | iob-B, iob-D                        |
| S9   | `task_complete` → transition back to Ω                    | Σ → Ω         | all                                 |
| S10  | `sim_end()` — snapshot final IdOB state, close monitor    | Ω             | iob-E                               |

### 6.2 Invariants That Must Hold Throughout

- `iob-A.value` is **always** `"I"` — any mutation raises `IdOB_WriteViolation`.
- `iob-E` is **always** read-only — any write raises `IdOB_WriteViolation`.
- `iob-D.max_steps` is the hard ceiling; exceeding it triggers `HALT`.
- Manifold must **never** be in two regions simultaneously.
- Every region transition must be **logged** by `iob-E`.

---

## 7. Quick-Reference Test Checklist

```
[ ] IdOB set loads with exactly 5 objects
[ ] iob-A and iob-E are immutable (write → exception)
[ ] Manifold initialises in Region Ω
[ ] Ambiguous instruction → Region Δ
[ ] Disambiguator resolves all 3 tokens → Region Σ
[ ] Disambiguation failure within max_steps → HALT
[ ] Replay trace-001 executes 8 steps with 0 divergences
[ ] Final IdOB state matches canonical replay snapshot
[ ] sim_end() captured by iob-E monitor log
```

---

*End of minimal_ts_cognition_tst.md*
```
