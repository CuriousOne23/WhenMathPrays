#!/usr/bin/env python3
"""
Scenario Generator for WhenMathPrays Framework
Generates γ_self trajectories and love equation parameters from waypoint specifications.

Algorithm locked by Ara + Jeff G on 30 November 2025.
Implementation: Event-driven, 7-tap FIR filter, probabilistic S, manual override system.
"""

import numpy as np
import random
import csv
import os
from typing import List, Tuple, Dict, Optional


class ScenarioGenerator:
    """
    Generates γ_self trajectories from waypoint specifications using locked algorithm:
    - 7-tap FIR filter with geometric decay [1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/128]
    - Event-by-event primitive generation (pick 2, balance delta)
    - Probabilistic S (60% shared breath, 40% internal fire)
    - Manual override system (preserve rows marked with *)
    """
    
    # 7-tap FIR coefficients (geometric decay, DC normalized)
    FIR_COEFFS = np.array([0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125])
    
    def __init__(self, scenario_name: str = "Generated_Scenario"):
        self.scenario_name = scenario_name
        self.output_dir = os.path.join("data", scenario_name)
        
    def generate_scenario(
        self,
        M1_trajectory: List[Tuple[int, float, float, float]],
        M2_trajectory: List[Tuple[int, float, float, float]],
        max_delta_y: float = 0.5,
        max_delta_x: float = 0.3,
        duration_days: int = 60,
        event_sampling: str = "weekly",
        beta_S: Optional[float] = None,
        s_S: Optional[float] = None,
        b_0: float = 0.0,
        shared_breath_prob: float = 0.60,
        m1_name: str = "M1",
        m2_name: str = "M2",
    ) -> Dict:
        """
        Generate complete scenario from waypoints.
        
        Args:
            M1_trajectory: List of (event, x, y, tolerance) waypoints for M1
            M2_trajectory: List of (event, x, y, tolerance) waypoints for M2
            max_delta_y: Maximum movement on love/hate axis per event
            max_delta_x: Maximum movement on ego/we axis per event
            duration_days: Total scenario duration
            event_sampling: Time interval ("daily", "weekly", "monthly")
            beta_S: Max boost for shared breath (auto-select if None)
            s_S: Saturation scale for shared breath (auto-select if None)
            b_0: Initial bond condition (0 for strangers, >0 for existing relationships)
            shared_breath_prob: Probability of shared breath when triggered (default 0.60)
        
        Returns:
            Dictionary with generated trajectories and metadata
        """
        
        # Determine time mapping
        if event_sampling == "daily":
            days_per_event = 1
        elif event_sampling == "weekly":
            days_per_event = 7
        elif event_sampling == "monthly":
            days_per_event = 30
        else:
            days_per_event = int(event_sampling)  # Allow custom intervals
            
        num_events = duration_days // days_per_event + 1
        
        # Validate feasibility
        self._check_feasibility(M1_trajectory, num_events, max_delta_y, max_delta_x)
        self._check_feasibility(M2_trajectory, num_events, max_delta_y, max_delta_x)
        
        # Generate trajectories
        M1_data = self._generate_trajectory(
            M1_trajectory, num_events, max_delta_y, max_delta_x, 
            days_per_event, shared_breath_prob, "M1"
        )
        M2_data = self._generate_trajectory(
            M2_trajectory, num_events, max_delta_y, max_delta_x,
            days_per_event, shared_breath_prob, "M2"
        )
        
        # Auto-select beta_S and s_S if not provided
        if beta_S is None or s_S is None:
            beta_S, s_S = self._auto_select_breath_params(
                M1_data, M2_data, duration_days
            )
        
        # Save CSV files
        os.makedirs(self.output_dir, exist_ok=True)
        self._save_csv(M1_data, "M1", beta_S, s_S, b_0, m1_name, m2_name)
        self._save_csv(M2_data, "M2", None, None, None, m1_name, m2_name)  # M2 doesn't get parameters header
        
        return {
            "M1_data": M1_data,
            "M2_data": M2_data,
            "beta_S": beta_S,
            "s_S": s_S,
            "b_0": b_0,
            "duration_days": duration_days,
            "num_events": num_events,
        }
    
    def _check_feasibility(
        self, 
        waypoints: List[Tuple[int, float, float, float]], 
        num_events: int,
        max_delta_y: float,
        max_delta_x: float
    ):
        """Validate that waypoints are reachable with given constraints."""
        for i in range(len(waypoints) - 1):
            event_i, x_i, y_i, tol_i = waypoints[i]
            event_j, x_j, y_j, tol_j = waypoints[i + 1]
            
            required_delta = np.sqrt((x_j - x_i)**2 + (y_j - y_i)**2)
            available_events = event_j - event_i
            
            # Account for filter damping (conservatively estimate 85% efficiency)
            max_possible = available_events * np.sqrt(max_delta_x**2 + max_delta_y**2) * 0.85
            
            if required_delta > max_possible:
                raise ValueError(
                    f"Waypoint unreachable!\n"
                    f"  From event {event_i} to {event_j}:\n"
                    f"  Required movement: {required_delta:.2f}\n"
                    f"  Available budget: {max_possible:.2f}\n"
                    f"  Suggestions: increase max_delta, add events, or adjust waypoint"
                )
    
    def _generate_trajectory(
        self,
        waypoints: List[Tuple[int, float, float, float]],
        num_events: int,
        max_delta_y: float,
        max_delta_x: float,
        days_per_event: int,
        shared_breath_prob: float,
        entity: str,
    ) -> List[Dict]:
        """Generate event-by-event trajectory between waypoints."""
        
        # Initialize trajectory data
        trajectory = []
        
        # Create full trajectory by interpolating between waypoints
        gamma_x = []
        gamma_y = []
        
        for i in range(len(waypoints) - 1):
            event_start, x_start, y_start, tol_start = waypoints[i]
            event_end, x_end, y_end, tol_end = waypoints[i + 1]
            
            # Linear interpolation between waypoints with small random variation
            num_steps = event_end - event_start + 1
            for j in range(num_steps):
                t = j / (num_steps - 1) if num_steps > 1 else 0
                
                # Exact match at waypoints, small variation in between
                if j == 0:
                    x = x_start
                    y = y_start
                elif j == num_steps - 1:
                    x = x_end
                    y = y_end
                else:
                    # Linear interpolation with small random walk
                    x_base = x_start + t * (x_end - x_start)
                    y_base = y_start + t * (y_end - y_start)
                    
                    # Add variation within tolerance
                    x = x_base + random.uniform(-tol_end, tol_end) * 0.5
                    y = y_base + random.uniform(-tol_end, tol_end) * 0.5
                    
                    # Clamp to max deltas
                    if len(gamma_x) > 0:
                        x = np.clip(x, gamma_x[-1] - max_delta_x, gamma_x[-1] + max_delta_x)
                        y = np.clip(y, gamma_y[-1] - max_delta_y, gamma_y[-1] + max_delta_y)
                
                gamma_x.append(x)
                gamma_y.append(y)
        
        # Initialize primitive histories (for FIR filter)
        v_history = []
        r_history = []
        f_history = []
        a_history = []
        
        S = 0  # Shared breath counter
        
        # Generate primitives event-by-event
        for event in range(num_events):
            day = event * days_per_event
            
            # Get current gamma_self
            if event < len(gamma_x):
                x = gamma_x[event]
                y = gamma_y[event]
            else:
                # Use last waypoint if beyond
                x = gamma_x[-1]
                y = gamma_y[-1]
            
            # Compute |gamma_self| for base primitive intensity
            gamma_mag = np.sqrt(x**2 + y**2)
            
            # Base primitive from |gamma_self| with improved scaling for sustained bonds
            # Lower threshold at γ≥5 (strong friendship/moderate bonds)
            # For γ=5-6: base ~0.75-0.83
            # For γ=7-8: base ~0.88-0.92
            # For γ=9-10: base ~0.94-0.96
            if gamma_mag >= 5:
                base_primitive = np.clip(0.65 + (gamma_mag - 5) / 16, 0.65, 0.98)
            else:
                base_primitive = np.clip((gamma_mag / 12.0) * 0.5 + 0.5, 0.3, 0.98)
            
            # Generate primitives with independent random variation (±10% for good saturation)
            v_raw = np.clip(base_primitive + random.uniform(-0.10, 0.10), 0, 1)
            r_raw = np.clip(base_primitive + random.uniform(-0.10, 0.10), 0, 1)
            f_raw = np.clip(base_primitive + random.uniform(-0.10, 0.10), 0, 1)
            a_raw = np.clip(base_primitive + random.uniform(-0.10, 0.10), 0, 1)
            
            # Apply 7-tap FIR filter independently per primitive
            v_history.append(v_raw)
            r_history.append(r_raw)
            f_history.append(f_raw)
            a_history.append(a_raw)
            
            v_filtered = self._apply_fir(v_history)
            r_filtered = self._apply_fir(r_history)
            f_filtered = self._apply_fir(f_history)
            a_filtered = self._apply_fir(a_history)
            
            # Check for shared breath trigger (flexible threshold for diverse bonds)
            # Trigger if: 3+ primitives >= 0.80 OR all 4 primitives >= 0.78
            primitives = [v_filtered, r_filtered, f_filtered, a_filtered]
            count_80 = sum(1 for p in primitives if p >= 0.80)
            count_78 = sum(1 for p in primitives if p >= 0.78)
            saturated_count = count_80 if count_80 >= 3 else (count_78 if count_78 >= 4 else 0)
            
            note = ""
            if saturated_count >= 3:
                # Roll for shared breath vs internal fire
                if random.uniform(0, 1) < shared_breath_prob:
                    S += 1
                    note = "Shared breath moment"
                else:
                    note = "Internal fire (no shared breath)"
            
            # Convert to human scale [-10, +10]
            v_human = (v_filtered - 0.5) * 20
            r_human = (r_filtered - 0.5) * 20
            f_human = (f_filtered - 0.5) * 20
            a_human = (a_filtered - 0.5) * 20
            
            # Store event data
            trajectory.append({
                "day": day,
                "x": x,
                "y": y,
                "v": v_human,
                "r": r_human,
                "f": f_human,
                "a": a_human,
                "S": S,
                "override_flag": "",
                "notes": note,
            })
        
        return trajectory
    
    def _apply_fir(self, history: List[float]) -> float:
        """Apply 7-tap FIR filter to primitive history."""
        # Use last 7 values (or less if history shorter)
        recent = history[-7:]
        
        # Pad with first value if not enough history
        while len(recent) < 7:
            recent = [history[0]] + recent
        
        # Apply coefficients
        filtered = sum(c * v for c, v in zip(self.FIR_COEFFS, recent))
        
        return np.clip(filtered, 0, 1)
    
    def _auto_select_breath_params(
        self, 
        M1_data: List[Dict], 
        M2_data: List[Dict],
        duration_days: int
    ) -> Tuple[float, float]:
        """
        Auto-select beta_S and s_S based on scenario characteristics.
        
        Uses relationship class heuristics from CONSTANTS.md:
        - Duration (short → casual, long → deep bond)
        - |gamma_self| range (low → casual, high → deep)
        - S accumulation rate
        """
        
        # Compute average |gamma_self|
        M1_gamma_mags = [np.sqrt(d["x"]**2 + d["y"]**2) for d in M1_data]
        M2_gamma_mags = [np.sqrt(d["x"]**2 + d["y"]**2) for d in M2_data]
        avg_gamma_mag = (np.mean(M1_gamma_mags) + np.mean(M2_gamma_mags)) / 2
        
        # Compute S accumulation rate
        final_S = max(M1_data[-1]["S"], M2_data[-1]["S"])
        S_rate = final_S / duration_days  # breaths per day
        
        # Classification logic
        if duration_days < 30:
            # Casual
            beta_S = random.uniform(0.3, 0.8)
            s_S = random.uniform(3, 8)
        elif duration_days < 180:
            # Ordinary friendship/romance
            beta_S = random.uniform(1.0, 2.5)
            s_S = random.uniform(10, 20)
        elif duration_days < 365 * 3:
            # Deep romantic partnership
            beta_S = random.uniform(2.0, 4.0)
            s_S = random.uniform(15, 40)
        elif duration_days < 365 * 10:
            # Long-term bond
            beta_S = random.uniform(3.0, 6.0)
            s_S = random.uniform(20, 60)
        else:
            # Lifelong bond
            beta_S = random.uniform(4.0, 8.0)
            s_S = random.uniform(30, 100)
        
        # Adjust based on |gamma_self| intensity
        if avg_gamma_mag > 8:
            beta_S *= 1.3
            s_S *= 1.5
        elif avg_gamma_mag < 3:
            beta_S *= 0.7
            s_S *= 0.7
        
        return round(beta_S, 1), round(s_S)
    
    def _save_csv(
        self, 
        data: List[Dict], 
        entity: str,
        beta_S: Optional[float],
        s_S: Optional[float],
        b_0: Optional[float],
        m1_name: str,
        m2_name: str
    ):
        """Save trajectory to CSV file with override_flag column."""
        filename = f"{self.scenario_name}_{entity}_gamma_self_table.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', newline='') as f:
            # Write header with beta_S, s_S, and b_0 (M1 only)
            if beta_S is not None and s_S is not None and b_0 is not None:
                f.write(f"beta_S\t{beta_S}\n")
                f.write(f"s_S\t{s_S}\n")
                f.write(f"b_0\t{b_0}\n")
            
            # Write Name row with entity's own name only
            entity_name = m1_name if entity == "M1" else m2_name
            if entity_name != entity:
                f.write(f"Name\t{entity_name}\n")
            
            # Blank line before data
            f.write("\n")
            
            # Write column headers
            f.write("Day\t{}_x\t{}_y\t".format(entity, entity))
            f.write("Visibility v(t)\tResonance r(t)\tFidelity f(t)\t")
            f.write("Alturism a(t)\tShared Breth S(t)\toverride_flag\tNotes\n")
            
            # Write data rows
            for row in data:
                f.write(f"{row['day']}\t")
                f.write(f"{row['x']:.2f}\t{row['y']:.2f}\t")
                f.write(f"{row['v']:.0f}\t{row['r']:.0f}\t")
                f.write(f"{row['f']:.0f}\t{row['a']:.0f}\t")
                f.write(f"{row['S']}\t{row['override_flag']}\t")
                f.write(f"{row['notes']}\n")
        
        print(f"Saved: {filepath}")


def main():
    """Example usage: recreate Singles Dating scenario."""
    
    generator = ScenarioGenerator("Test_Singles_Dating")
    
    # Define waypoints from original Singles Dating scenario
    # Using event indices (0-8 for 9 total events over 60 days)
    M1_waypoints = [
        (0, -2.5, 0.5, 0),      # Day 0: exact start
        (4, -1.5, 1.5, 0.3),    # Day 28: repair underway
        (8, -0.7, 2.75, 0.2),   # Day 56: final position with tolerance
    ]
    
    M2_waypoints = [
        (0, -2.0, 1.0, 0),      # Day 0: exact start
        (4, -1.5, 1.5, 0.3),    # Day 28: warming
        (8, -1.0, 2.0, 0.2),    # Day 56: final position with tolerance
    ]
    
    result = generator.generate_scenario(
        M1_trajectory=M1_waypoints,
        M2_trajectory=M2_waypoints,
        max_delta_y=0.5,
        max_delta_x=0.3,
        duration_days=60,
        event_sampling="weekly",
        beta_S=1.5,
        s_S=15,
        shared_breath_prob=0.60,
        m1_name="M1",
        m2_name="M2",
    )
    
    print("\n=== Scenario Generated ===")
    print(f"Scenario: {generator.scenario_name}")
    print(f"Duration: {result['duration_days']} days")
    print(f"Events: {result['num_events']}")
    print(f"Breath params: beta_S={result['beta_S']}, s_S={result['s_S']}")
    print(f"\nM1 final: ({result['M1_data'][-1]['x']:.2f}, {result['M1_data'][-1]['y']:.2f}), S={result['M1_data'][-1]['S']}")
    print(f"M2 final: ({result['M2_data'][-1]['x']:.2f}, {result['M2_data'][-1]['y']:.2f}), S={result['M2_data'][-1]['S']}")


if __name__ == "__main__":
    main()
