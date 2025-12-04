#!/usr/bin/env python3
"""
Scenario Generator for WhenMathPrays Framework
Generates CSV scenario files with various emotional arc patterns.

Usage:
    python tools/scenario_generator.py --name "Summer Romance" --duration 12 --time-unit weeks --arc slow_burn --output data/summer_romance.csv
"""

import sys
import csv
import argparse
from pathlib import Path
import numpy as np


# Arc type generators
def generate_slow_burn(num_events: int) -> list:
    """Gradual increase from low to moderate/high primitives."""
    events = []
    for i in range(num_events):
        progress = i / (num_events - 1)  # 0 to 1
        # Gentle exponential growth
        factor = progress ** 1.5
        
        v = 2 + 5 * factor
        r = 1 + 6 * factor
        f = 2 + 5 * factor
        a = 1 + 6 * factor
        S = 0 + 6 * factor
        
        events.append({'v': v, 'r': r, 'f': f, 'a': a, 'S': S})
    return events


def generate_hot_start_cold_finish(num_events: int) -> list:
    """High intensity declining to low/zero."""
    events = []
    for i in range(num_events):
        progress = i / (num_events - 1)
        # Decay curve
        factor = 1 - progress ** 0.8
        
        v = 8 * factor
        r = 9 * factor
        f = 9 * factor
        a = 8 * factor
        S = 8 * factor
        
        events.append({'v': v, 'r': r, 'f': f, 'a': a, 'S': S})
    return events


def generate_steady_growth(num_events: int) -> list:
    """Linear positive progression."""
    events = []
    for i in range(num_events):
        progress = i / (num_events - 1)
        
        v = 3 + 2 * progress
        r = 4 + 2 * progress
        f = 5 + 2 * progress
        a = 2 + 3 * progress
        S = 1 + 4 * progress
        
        events.append({'v': v, 'r': r, 'f': f, 'a': a, 'S': S})
    return events


def generate_rocky_but_committed(num_events: int) -> list:
    """Oscillating conflict/repair cycles with net positive trend."""
    events = []
    for i in range(num_events):
        progress = i / (num_events - 1)
        
        # Base positive trend
        base = 3 + 4 * progress
        
        # Add oscillation (conflict/repair cycles)
        cycle = 2 * np.sin(progress * 6 * np.pi)  # ~3 full cycles
        
        v = base + cycle * 0.5
        r = base + cycle * 0.8
        f = base + cycle * 0.6
        a = base + cycle * 0.4
        S = base + cycle * 0.3
        
        events.append({'v': v, 'r': r, 'f': f, 'a': a, 'S': S})
    return events


def generate_toxic_spiral(num_events: int) -> list:
    """Descending into Q3 (Ego + Hate) with sustained negatives."""
    events = []
    for i in range(num_events):
        progress = i / (num_events - 1)
        
        # Start neutral, end very negative
        v = 2 - 6 * progress
        r = 1 - 8 * progress
        f = 3 - 10 * progress
        a = 1 - 7 * progress
        S = 0 - 5 * progress
        
        events.append({'v': v, 'r': r, 'f': f, 'a': a, 'S': S})
    return events


def generate_u_shape_recovery(num_events: int) -> list:
    """Down then back up (crisis → repair)."""
    events = []
    for i in range(num_events):
        progress = i / (num_events - 1)
        
        # U-shape: high → low → high
        # Use parabola: (2*progress - 1)^2
        u_factor = 1 - (2 * progress - 1) ** 2  # 0 → 1 → 0 (inverted U)
        crisis_factor = 1 - u_factor  # 1 → 0 → 1 (U shape)
        
        # Start good, crisis mid, recover end
        v = 7 - 5 * crisis_factor
        r = 8 - 7 * crisis_factor
        f = 8 - 8 * crisis_factor
        a = 6 - 5 * crisis_factor
        S = 5 - 4 * crisis_factor
        
        events.append({'v': v, 'r': r, 'f': f, 'a': a, 'S': S})
    return events


def generate_plateau(num_events: int) -> list:
    """Quick rise then steady maintenance."""
    events = []
    for i in range(num_events):
        progress = i / (num_events - 1)
        
        # Quick rise (logarithmic)
        if progress < 0.2:
            # First 20%: rapid rise
            factor = progress / 0.2
            v = 2 + 5 * factor
            r = 2 + 6 * factor
            f = 3 + 5 * factor
            a = 2 + 5 * factor
            S = 1 + 6 * factor
        else:
            # Remaining 80%: plateau
            v = 7
            r = 8
            f = 8
            a = 7
            S = 7
        
        events.append({'v': v, 'r': r, 'f': f, 'a': a, 'S': S})
    return events


def generate_oscillatory(num_events: int) -> list:
    """Sustained cycling (up/down patterns)."""
    events = []
    for i in range(num_events):
        progress = i / (num_events - 1)
        
        # Multiple cycles
        cycle = np.sin(progress * 8 * np.pi)  # ~4 full cycles
        
        v = 4 + 3 * cycle
        r = 5 + 4 * cycle
        f = 4 + 3 * cycle
        a = 3 + 2 * cycle
        S = 3 + 3 * cycle
        
        events.append({'v': v, 'r': r, 'f': f, 'a': a, 'S': S})
    return events


# Arc type registry
ARC_GENERATORS = {
    'slow_burn': generate_slow_burn,
    'hot_start_cold_finish': generate_hot_start_cold_finish,
    'steady_growth': generate_steady_growth,
    'rocky_but_committed': generate_rocky_but_committed,
    'toxic_spiral': generate_toxic_spiral,
    'u_shape_recovery': generate_u_shape_recovery,
    'plateau': generate_plateau,
    'oscillatory': generate_oscillatory,
}


# Dual perspective asymmetry patterns
def apply_pursuer_withdrawer(events_m1: list, events_m2: list):
    """M1 increases while M2 decreases (pursuit-withdraw)."""
    for i in range(len(events_m1)):
        progress = i / (len(events_m1) - 1)
        
        # M1 pursues (increase)
        boost = 2 * progress
        events_m1[i]['v'] += boost
        events_m1[i]['r'] += boost
        
        # M2 withdraws (decrease)
        events_m2[i]['v'] -= boost
        events_m2[i]['r'] -= boost


def apply_convergent(events_m1: list, events_m2: list):
    """Both move toward each other at different rates."""
    for i in range(len(events_m1)):
        progress = i / (len(events_m1) - 1)
        
        # M1 faster convergence
        boost_m1 = 3 * progress
        events_m1[i]['v'] += boost_m1
        events_m1[i]['f'] += boost_m1
        
        # M2 slower convergence
        boost_m2 = 1.5 * progress
        events_m2[i]['v'] += boost_m2
        events_m2[i]['f'] += boost_m2


def apply_leader_follower(events_m1: list, events_m2: list):
    """M1 changes first, M2 follows with delay."""
    # Shift M2's trajectory to lag behind M1
    for i in range(1, len(events_m2)):
        # M2 adopts M1's previous state (with damping)
        for prim in ['v', 'r', 'f', 'a', 'S']:
            events_m2[i][prim] = 0.7 * events_m1[i-1][prim] + 0.3 * events_m2[i][prim]


ASYMMETRY_PATTERNS = {
    'symmetric': lambda m1, m2: None,  # No change
    'pursuer_withdrawer': apply_pursuer_withdrawer,
    'convergent': apply_convergent,
    'leader_follower': apply_leader_follower,
}


def calculate_num_events(duration: float, time_unit: str, num_events: int = None) -> int:
    """Calculate appropriate number of events if not specified."""
    if num_events is not None:
        return num_events
    
    # Auto-calculate based on time unit
    if time_unit == 'days':
        return max(10, int(duration / 7))  # Weekly snapshots
    elif time_unit == 'weeks':
        return max(10, int(duration / 4))  # Monthly snapshots
    elif time_unit == 'months':
        return max(12, int(duration))  # Monthly
    elif time_unit == 'years':
        return max(12, int(duration * 4))  # Quarterly
    else:
        return 20  # Default


def generate_time_points(duration: float, num_events: int) -> list:
    """Generate evenly spaced time points from 0 to duration."""
    if num_events == 1:
        return [duration]
    return [duration * i / (num_events - 1) for i in range(num_events)]


def clamp_primitives(events: list) -> list:
    """Clamp primitive values to [-10, +10] range."""
    for event in events:
        for prim in ['v', 'r', 'f', 'a', 'S']:
            event[prim] = max(-10, min(10, event[prim]))
    return events


def add_markers(events: list, time_points: list) -> list:
    """Add markers at key trajectory points."""
    # First and last always get markers
    events[0]['marker'] = 'star'
    events[-1]['marker'] = 'star'
    
    # Add marker at midpoint if enough events
    if len(events) >= 5:
        mid = len(events) // 2
        events[mid]['marker'] = 'circle'
    
    # Add markers at quarter points for longer scenarios
    if len(events) >= 10:
        q1 = len(events) // 4
        q3 = 3 * len(events) // 4
        events[q1]['marker'] = 'triangle'
        events[q3]['marker'] = 'diamond'
    
    return events


def add_locked(events: list) -> list:
    """Mark first and last events as locked."""
    events[0]['locked'] = '*'
    events[-1]['locked'] = '*'
    return events


def generate_scenario(name: str, duration: float, time_unit: str, arc_type: str,
                     num_events: int = None, perspective: str = 'single',
                     asymmetry: str = 'symmetric', output_path: str = None) -> str:
    """
    Generate scenario CSV file(s).
    
    Args:
        name: Scenario name
        duration: Duration in specified time unit
        time_unit: 'days', 'weeks', 'months', or 'years'
        arc_type: Arc template type
        num_events: Number of time points (auto if None)
        perspective: 'single' or 'dual'
        asymmetry: Asymmetry pattern for dual ('symmetric', 'pursuer_withdrawer', etc.)
        output_path: Output file path (or base path for dual)
    
    Returns:
        Path(s) to created file(s)
    """
    # Validate inputs
    if arc_type not in ARC_GENERATORS:
        raise ValueError(f"Unknown arc type '{arc_type}'. Available: {list(ARC_GENERATORS.keys())}")
    
    if time_unit not in ['days', 'weeks', 'months', 'years']:
        raise ValueError(f"Invalid time_unit '{time_unit}'. Must be: days, weeks, months, years")
    
    if perspective not in ['single', 'dual']:
        raise ValueError(f"Invalid perspective '{perspective}'. Must be: single, dual")
    
    # Calculate number of events
    num_events = calculate_num_events(duration, time_unit, num_events)
    
    # Generate time points
    time_points = generate_time_points(duration, num_events)
    
    # Generate arc
    arc_func = ARC_GENERATORS[arc_type]
    events = arc_func(num_events)
    events = clamp_primitives(events)
    
    # Add notes
    for i, event in enumerate(events):
        if i == 0:
            event['notes'] = f"Start: {arc_type.replace('_', ' ')}"
        elif i == num_events - 1:
            event['notes'] = f"End: {arc_type.replace('_', ' ')}"
        else:
            event['notes'] = f"Progress: {int(100 * i / (num_events-1))}%"
    
    # Add markers and locked
    events = add_markers(events, time_points)
    events = add_locked(events)
    
    # Handle perspective
    if perspective == 'single':
        # Single perspective
        output_file = Path(output_path) if output_path else Path(f"data/{name.replace(' ', '_')}.csv")
        write_csv(output_file, name, time_unit, time_points, events)
        print(f"Generated: {output_file}")
        return str(output_file)
    
    else:
        # Dual perspective
        events_m2 = arc_func(num_events)
        events_m2 = clamp_primitives(events_m2)
        
        # Apply asymmetry
        if asymmetry in ASYMMETRY_PATTERNS:
            ASYMMETRY_PATTERNS[asymmetry](events, events_m2)
            events = clamp_primitives(events)
            events_m2 = clamp_primitives(events_m2)
        
        # Add notes, markers, locked to M2
        for i, event in enumerate(events_m2):
            if i == 0:
                event['notes'] = f"Start: {arc_type.replace('_', ' ')} (M2)"
            elif i == num_events - 1:
                event['notes'] = f"End: {arc_type.replace('_', ' ')} (M2)"
            else:
                event['notes'] = f"Progress: {int(100 * i / (num_events-1))}% (M2)"
        events_m2 = add_markers(events_m2, time_points)
        events_m2 = add_locked(events_m2)
        
        # Write both files
        base_path = Path(output_path) if output_path else Path(f"data/{name.replace(' ', '_')}")
        m1_file = base_path.parent / f"{base_path.stem}_M1.csv"
        m2_file = base_path.parent / f"{base_path.stem}_M2.csv"
        
        write_csv(m1_file, f"{name} - M1", time_unit, time_points, events)
        write_csv(m2_file, f"{name} - M2", time_unit, time_points, events_m2)
        
        print(f"Generated: {m1_file}")
        print(f"Generated: {m2_file}")
        return f"{m1_file}, {m2_file}"


def write_csv(output_path: Path, name: str, time_unit: str, time_points: list, events: list):
    """Write CSV file with metadata and events."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        # Write metadata
        f.write(f"name,{name}\n")
        f.write(f"time_unit,{time_unit}\n")
        
        # Write data
        fieldnames = ['day', 'v', 'r', 'f', 'a', 'S', 'notes', 'marker', 'locked']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, (time, event) in enumerate(zip(time_points, events)):
            row = {
                'day': f"{time:.1f}" if time_unit != 'days' else str(int(time)),
                'v': f"{event['v']:.1f}",
                'r': f"{event['r']:.1f}",
                'f': f"{event['f']:.1f}",
                'a': f"{event['a']:.1f}",
                'S': f"{event['S']:.1f}",
                'notes': event.get('notes', ''),
                'marker': event.get('marker', ''),
                'locked': event.get('locked', '')
            }
            writer.writerow(row)


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Generate WhenMathPrays scenario CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Arc types:
  slow_burn              - Gradual increase from low to high
  hot_start_cold_finish  - High intensity declining to low
  steady_growth          - Linear positive progression
  rocky_but_committed    - Oscillating with net positive trend
  toxic_spiral           - Descending into negativity
  u_shape_recovery       - Crisis then recovery
  plateau                - Quick rise then steady maintenance
  oscillatory            - Sustained up/down cycles

Examples:
  python tools/scenario_generator.py --name "Summer Romance" --duration 12 --time-unit weeks --arc slow_burn
  python tools/scenario_generator.py --name "Long Distance" --duration 6 --time-unit months --arc rocky_but_committed --perspective dual --asymmetry pursuer_withdrawer
        """
    )
    
    parser.add_argument('--name', required=True, help='Scenario name')
    parser.add_argument('--duration', type=float, required=True, help='Duration in time units')
    parser.add_argument('--time-unit', choices=['days', 'weeks', 'months', 'years'], default='days',
                       help='Time unit (default: days)')
    parser.add_argument('--arc', required=True, choices=list(ARC_GENERATORS.keys()),
                       help='Arc type template')
    parser.add_argument('--num-events', type=int, help='Number of events (auto-calculated if omitted)')
    parser.add_argument('--perspective', choices=['single', 'dual'], default='single',
                       help='Single or dual perspective (default: single)')
    parser.add_argument('--asymmetry', choices=list(ASYMMETRY_PATTERNS.keys()), default='symmetric',
                       help='Asymmetry pattern for dual perspective (default: symmetric)')
    parser.add_argument('--output', help='Output file path (or base for dual)')
    
    args = parser.parse_args()
    
    try:
        generate_scenario(
            name=args.name,
            duration=args.duration,
            time_unit=args.time_unit,
            arc_type=args.arc,
            num_events=args.num_events,
            perspective=args.perspective,
            asymmetry=args.asymmetry,
            output_path=args.output
        )
        print("\nScenario generation complete!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
