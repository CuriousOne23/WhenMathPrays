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

try:
    from bond_calibration_map import get_bond_parameters, get_initial_bond, classify_slope
except ImportError:
    # Fallback if bond_calibration_map not available
    def get_bond_parameters(duration_days, avg_slope):
        return {"beta_S": (2.0, 4.0), "s_S": (15, 30)}
    def get_initial_bond(relationship_type):
        return 0.0
    def classify_slope(avg_slope):
        return "mild"


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
        decline_score: float = 0.0,
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
            decline_score: Human-entry score for declining scenarios (0 to -10).
                          0 = neutral decline (natural entropy)
                          -3 to -5 = moderate toxicity (conflict, disappointment)
                          -7 to -10 = extreme toxicity (betrayal, abuse, destruction)
        
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
            days_per_event, shared_breath_prob, decline_score, "M1"
        )
        M2_data = self._generate_trajectory(
            M2_trajectory, num_events, max_delta_y, max_delta_x,
            days_per_event, shared_breath_prob, decline_score, "M2"
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
        decline_score: float,
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
        
        # Calculate trajectory slopes for each segment
        # Slope = delta_y / delta_events (love axis movement per event)
        segment_slopes = []
        for i in range(len(waypoints) - 1):
            event_start, x_start, y_start, tol_start = waypoints[i]
            event_end, x_end, y_end, tol_end = waypoints[i + 1]
            
            delta_y = y_end - y_start
            delta_events = event_end - event_start
            slope = delta_y / delta_events if delta_events > 0 else 0
            segment_slopes.append((event_start, event_end, slope))
        
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
            
            # Determine current segment slope
            current_slope = 0
            for seg_start, seg_end, slope in segment_slopes:
                if seg_start <= event <= seg_end:
                    current_slope = slope
                    break
            
            # Base primitive from slope (trajectory dynamics)
            # Growing trajectories (positive slope) need high primitives to overcome entropy
            # Stable trajectories (near-zero slope) need moderate primitives
            # Declining trajectories (negative slope) need low/negative primitives
            # Calibrated via empirical tests: slope +0.05 needs primitives ~0.75+ to overcome entropy
            
            if current_slope > 0.15:  # Strong growth (slope > 0.15)
                base_primitive = np.clip(0.85 + current_slope * 0.8, 0.85, 0.98)
            elif current_slope > 0.10:  # Moderate-strong growth (0.10 < slope ≤ 0.15)
                base_primitive = np.clip(0.80 + current_slope * 1.5, 0.80, 0.90)
            elif current_slope > 0.03:  # Mild growth (0.03 < slope ≤ 0.10) - CRITICAL threshold
                base_primitive = np.clip(0.75 + current_slope * 2.5, 0.75, 0.85)
            elif current_slope > -0.03:  # Stable (near zero slope)
                base_primitive = np.clip(0.65 + current_slope * 3.0, 0.60, 0.75)
            elif current_slope > -0.10:  # Mild decline
                base_primitive = np.clip(0.55 + current_slope * 2.0, 0.50, 0.65)
            elif current_slope > -0.15:  # Moderate decline
                base_primitive = np.clip(0.45 + current_slope * 1.5, 0.40, 0.55)
            else:  # Strong decline (slope < -0.15)
                base_primitive = np.clip(0.35 + current_slope * 1.0, 0.20, 0.45)
            
            # Apply decline_score modulation (0 to -10 scale)
            # decline_score dampens primitives and can make them negative for toxic scenarios
            if decline_score < 0:
                # Map decline_score to dampening factor:
                # 0 → 1.0 (no effect)
                # -3 → 0.70 (30% reduction)
                # -5 → 0.50 (50% reduction)
                # -7 → 0.30 (70% reduction)
                # -10 → 0.0 (complete suppression, can go negative)
                decline_factor = np.clip(1.0 + (decline_score / 10.0), 0.0, 1.0)
                
                # For extreme toxicity (-8 to -10), allow negative primitives
                if decline_score <= -8:
                    # Shift base_primitive into negative range
                    base_primitive = base_primitive * decline_factor - (abs(decline_score) - 7) * 0.1
                else:
                    # Dampen but keep non-negative
                    base_primitive = base_primitive * decline_factor
            
            # Generate primitives with independent random variation (±10% for good saturation)
            v_raw = np.clip(base_primitive + random.uniform(-0.10, 0.10), -1, 1)
            r_raw = np.clip(base_primitive + random.uniform(-0.10, 0.10), -1, 1)
            f_raw = np.clip(base_primitive + random.uniform(-0.10, 0.10), -1, 1)
            a_raw = np.clip(base_primitive + random.uniform(-0.10, 0.10), -1, 1)
            
            # Apply 7-tap FIR filter independently per primitive
            v_history.append(v_raw)
            r_history.append(r_raw)
            f_history.append(f_raw)
            a_history.append(a_raw)
            
            v_filtered = self._apply_fir(v_history)
            r_filtered = self._apply_fir(r_history)
            f_filtered = self._apply_fir(f_history)
            a_filtered = self._apply_fir(a_history)
            
            # Adjust shared breath probability based on slope and decline_score
            # Growing trajectories need more shared breath to sustain growth
            # Declining trajectories have reduced connection moments
            
            # Base adjustment from slope - calibrated to ensure S accumulation for mild growth
            if current_slope > 0.10:  # Strong growth
                slope_breath_factor = 1.5  # Strong boost for growth
            elif current_slope > 0.03:  # Mild growth (CRITICAL: needs boost to accumulate S)
                slope_breath_factor = 1.4  # Strong boost even for mild growth
            elif current_slope > -0.03:  # Stable
                slope_breath_factor = 1.0  # Normal probability
            elif current_slope > -0.10:  # Mild decline
                slope_breath_factor = 0.7  # Reduced probability
            else:  # Moderate/strong decline
                slope_breath_factor = 0.5  # Very low probability
            
            adjusted_breath_prob = shared_breath_prob * slope_breath_factor
            
            # Apply decline_score modulation on top of slope adjustment
            if decline_score < 0:
                # Linear reduction: -10 → 0% probability, 0 → normal probability
                adjusted_breath_prob = adjusted_breath_prob * (1.0 + decline_score / 10.0)
            
            adjusted_breath_prob = np.clip(adjusted_breath_prob, 0.0, 0.95)
            
            # Check for shared breath trigger (adaptive threshold based on slope)
            # Growing trajectories: lower threshold to ensure S accumulation
            # Stable/declining: normal threshold
            primitives = [v_filtered, r_filtered, f_filtered, a_filtered]
            
            if current_slope > 0.05:  # Growing: use relaxed threshold
                count_75 = sum(1 for p in primitives if p >= 0.75)
                count_78 = sum(1 for p in primitives if p >= 0.78)
                saturated_count = count_75 if count_75 >= 3 else (count_78 if count_78 >= 3 else 0)
            else:  # Stable/declining: use standard threshold
                count_80 = sum(1 for p in primitives if p >= 0.80)
                count_78 = sum(1 for p in primitives if p >= 0.78)
                saturated_count = count_80 if count_80 >= 3 else (count_78 if count_78 >= 4 else 0)
            
            note = ""
            if saturated_count >= 3:
                # Roll for shared breath vs internal fire
                if random.uniform(0, 1) < adjusted_breath_prob:
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
        
        # Allow negative values for toxic scenarios
        return np.clip(filtered, -1, 1)
    
    def _auto_select_breath_params(
        self, 
        M1_data: List[Dict], 
        M2_data: List[Dict],
        duration_days: int
    ) -> Tuple[float, float]:
        """
        Auto-select beta_S and s_S based on scenario characteristics using calibration map.
        
        Uses empirically validated bond parameter calibration map based on:
        - Duration (very_short/short/medium/long/very_long)
        - Average trajectory slope (declining/stable/mild/moderate/strong)
        """
        
        # Calculate average trajectory slope from gamma_self data
        # Slope = average delta_y across all events
        M1_slopes = []
        for i in range(1, len(M1_data)):
            delta_y = M1_data[i]["y"] - M1_data[i-1]["y"]
            M1_slopes.append(delta_y)
        
        M2_slopes = []
        for i in range(1, len(M2_data)):
            delta_y = M2_data[i]["y"] - M2_data[i-1]["y"]
            M2_slopes.append(delta_y)
        
        # Average slope across both entities and all events
        all_slopes = M1_slopes + M2_slopes
        avg_slope = np.mean(all_slopes) if all_slopes else 0.0
        
        # Lookup calibrated parameters from map
        params = get_bond_parameters(duration_days, avg_slope)
        
        # Select random values within calibrated ranges
        beta_S = random.uniform(params["beta_S"][0], params["beta_S"][1])
        s_S = random.uniform(params["s_S"][0], params["s_S"][1])
        
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
