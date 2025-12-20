# Gamma_self Trajectory Reference (Diagnostic Marker Logic)

## Purpose
This document records the reference implementation and mapping logic for the gamma_self trajectory calculation and diagnostic marker placement in the interactive editor. It is intended to prevent loss of architectural knowledge and clarify the mapping between gamma_self trajectory indices and primitive/event indices.

## Location in Code
- **File:** tools/interactive_editor.py
- **Section:** Diagnostic marker handler (see `_on_diagnostic_marker`)

## Mapping Logic
- `gamma_trajectory[0]` = gamma_self_0 (initial state, before any event)
- `gamma_trajectory[i+1]` = gamma_self after event i's primitives are applied
- There are N events and N intervals; each interval applies the primitives at event i.
- For the last event, the marker reflects the final gamma_self value after all intervals.
- For other events, the marker reflects gamma_self after that event's primitives are applied.

## Reference Implementation (Summary)
```python
# --- Gamma_self trajectory calculation ---
# The gamma_self trajectory is mapped as follows:
#   gamma_trajectory[0] = gamma_self_0 (initial state, before any event)
#   gamma_trajectory[i+1] = gamma_self after event i's primitives are applied
# There are N events and N intervals; each interval applies the primitives at event i.
# For the last event, the marker should reflect the final gamma_self value after all intervals.

gamma_self = self.model.get_gamma_self_0(self.controller.perspective)
gamma_trajectory = [gamma_self]
n_events = len(events)
for i in range(n_events):
    # For the interval corresponding to the last event, use hypothetical value if applicable
    if i == event_index:
        # Apply hypothetical value for the selected primitive at this event
        v = hypothetical_value if primitive == 'v' else primitives_data['v'][i]
        r = hypothetical_value if primitive == 'r' else primitives_data['r'][i]
        f = hypothetical_value if primitive == 'f' else primitives_data['f'][i]
        a = hypothetical_value if primitive == 'a' else primitives_data['a'][i]
        S = hypothetical_value if primitive == 'S' else primitives_data['S'][i]
    else:
        v = primitives_data['v'][i]
        r = primitives_data['r'][i]
        f = primitives_data['f'][i]
        a = primitives_data['a'][i]
        S = primitives_data['S'][i]
    time_delta = times[i + 1] - times[i]
    gamma_self = update_gamma_self(
        gamma_self, v, r, f, a, S,
        weights=weights,
        time_delta=time_delta
    )
    gamma_trajectory.append(gamma_self)

# --- Marker placement logic ---
# For the last event, always use the final gamma_self value
# For other events, use gamma_self after that event's primitives are applied
if event_index == n_events - 1:
    gamma_val = gamma_trajectory[-1]
else:
    gamma_val = gamma_trajectory[event_index + 1]
```

## Documentation Placement Rationale
This logic is central to state management and diagnostic marker placement. It is referenced by both the controller and view logic, and is best placed in the state management documentation for future maintainers.

## See Also
- [STATE_MANAGEMENT_REFACTORING.md](STATE_MANAGEMENT_REFACTORING.md)
- [SOFTWARE_MODULES.md](architecture/SOFTWARE_MODULES.md)
- [02_INFORMATION_FLOW.md](architecture/02_INFORMATION_FLOW.md)

---
*Last updated: December 20, 2025*
