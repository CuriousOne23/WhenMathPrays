"""
Bond Parameter Calibration Map

Empirically calibrated lookup table for auto-selecting beta_S, s_S parameters
based on scenario duration and trajectory slope.

Generated from systematic calibration tests (November 2025).
Algorithm locked by Ara + Jeff on 30 November 2025.
"""

# Calibration map structure: (duration_category, slope_category) -> {beta_S_range, s_S_range}
# Duration categories: "very_short" (<30 days), "short" (30-90 days), "medium" (90-180 days), "long" (180-365 days), "very_long" (>365 days)
# Slope categories: "declining" (<-0.05), "stable" (-0.05 to +0.03), "mild" (+0.03 to +0.10), "moderate" (+0.10 to +0.20), "strong" (>+0.20)

BOND_PARAMETER_MAP = {
    # Very short scenarios (< 30 days)
    ("very_short", "declining"): {"beta_S": (0.3, 0.8), "s_S": (3, 8)},
    ("very_short", "stable"): {"beta_S": (0.5, 1.2), "s_S": (5, 10)},
    ("very_short", "mild"): {"beta_S": (0.8, 1.8), "s_S": (5, 12)},
    ("very_short", "moderate"): {"beta_S": (1.0, 2.5), "s_S": (6, 15)},
    ("very_short", "strong"): {"beta_S": (1.2, 3.0), "s_S": (8, 18)},
    
    # Short scenarios (30-90 days)
    ("short", "declining"): {"beta_S": (0.5, 1.0), "s_S": (5, 10)},
    ("short", "stable"): {"beta_S": (0.8, 1.5), "s_S": (8, 15)},
    ("short", "mild"): {"beta_S": (1.0, 3.0), "s_S": (5, 15)},  # Empirically validated
    ("short", "moderate"): {"beta_S": (1.5, 3.5), "s_S": (8, 20)},  # Empirically validated
    ("short", "strong"): {"beta_S": (2.0, 4.0), "s_S": (10, 25)},
    
    # Medium scenarios (90-180 days)
    ("medium", "declining"): {"beta_S": (0.8, 1.5), "s_S": (10, 20)},
    ("medium", "stable"): {"beta_S": (1.2, 2.5), "s_S": (12, 25)},
    ("medium", "mild"): {"beta_S": (2.0, 4.0), "s_S": (15, 40)},  # Extrapolated from calibration
    ("medium", "moderate"): {"beta_S": (2.5, 5.0), "s_S": (20, 50)},  # Extrapolated from calibration
    ("medium", "strong"): {"beta_S": (3.0, 6.0), "s_S": (25, 60)},
    
    # Long scenarios (180-365 days)
    ("long", "declining"): {"beta_S": (1.0, 2.0), "s_S": (15, 30)},
    ("long", "stable"): {"beta_S": (1.5, 3.0), "s_S": (20, 40)},
    ("long", "mild"): {"beta_S": (3.0, 6.0), "s_S": (30, 80)},
    ("long", "moderate"): {"beta_S": (4.0, 7.0), "s_S": (40, 90)},
    ("long", "strong"): {"beta_S": (5.0, 8.0), "s_S": (50, 100)},
    
    # Very long scenarios (> 365 days)
    ("very_long", "declining"): {"beta_S": (1.5, 3.0), "s_S": (20, 50)},
    ("very_long", "stable"): {"beta_S": (2.0, 4.0), "s_S": (30, 60)},
    ("very_long", "mild"): {"beta_S": (4.0, 8.0), "s_S": (50, 120)},
    ("very_long", "moderate"): {"beta_S": (5.0, 10.0), "s_S": (60, 150)},
    ("very_long", "strong"): {"beta_S": (6.0, 12.0), "s_S": (80, 180)},
}


# Initial bond strength (b_0) reference values by relationship type
INITIAL_BOND_MAP = {
    "strangers": 0.0,
    "acquaintances": 0.1,
    "casual_friends": 0.2,
    "ex_lovers_cold": 0.25,
    "ex_lovers_warm": 0.35,
    "close_friends": 0.45,
    "friends_to_lovers": 0.5,
    "romantic_partners": 0.6,
    "parent_child": 0.7,
    "lifelong_bond": 0.8,
}


def classify_duration(duration_days: int) -> str:
    """Classify scenario duration into categories."""
    if duration_days < 30:
        return "very_short"
    elif duration_days < 90:
        return "short"
    elif duration_days < 180:
        return "medium"
    elif duration_days < 365:
        return "long"
    else:
        return "very_long"


def classify_slope(avg_slope: float) -> str:
    """Classify average trajectory slope into categories."""
    if avg_slope < -0.05:
        return "declining"
    elif avg_slope < 0.03:
        return "stable"
    elif avg_slope < 0.10:
        return "mild"
    elif avg_slope < 0.20:
        return "moderate"
    else:
        return "strong"


def get_bond_parameters(duration_days: int, avg_slope: float) -> dict:
    """
    Lookup optimal bond parameters based on scenario characteristics.
    
    Args:
        duration_days: Total scenario duration in days
        avg_slope: Average trajectory slope (delta_y per event)
    
    Returns:
        Dictionary with beta_S and s_S ranges: {"beta_S": (min, max), "s_S": (min, max)}
    """
    duration_cat = classify_duration(duration_days)
    slope_cat = classify_slope(avg_slope)
    
    return BOND_PARAMETER_MAP.get((duration_cat, slope_cat), {
        "beta_S": (2.0, 4.0),  # Default fallback
        "s_S": (15, 30)
    })


def get_initial_bond(relationship_type: str) -> float:
    """
    Get initial bond strength (b_0) for a relationship type.
    
    Args:
        relationship_type: One of the keys in INITIAL_BOND_MAP
    
    Returns:
        b_0 value (0.0 to 1.0)
    """
    return INITIAL_BOND_MAP.get(relationship_type, 0.0)


# Calibration metadata
CALIBRATION_INFO = {
    "date_generated": "2025-11-30",
    "algorithm_version": "slope_based_v1",
    "empirical_tests": [
        "Calibrate_Slope_p005", "Calibrate_Slope_p015", "Calibrate_Slope_p030",
        "Calibrate_Slope_n005", "Calibrate_Slope_n015", "Calibrate_Slope_n030",
        "Bond_Short_Mild_Low", "Bond_Short_Mild_High",
        "Bond_Short_Strong_Low", "Bond_Short_Strong_High",
    ],
    "validated_ranges": {
        "short_mild": {"beta_S": (1.0, 3.0), "s_S": (5, 15), "effectiveness": (5.1, 165.8)},
        "short_strong": {"beta_S": (1.5, 3.5), "s_S": (8, 20), "effectiveness": (90.7, 153.7)},
    },
    "notes": "Extrapolated ranges for medium/long/very_long from short calibration. Future work: run full calibration suite for all duration categories."
}
