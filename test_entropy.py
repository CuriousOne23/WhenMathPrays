"""Test entropy drift: compare delS=0 vs delS=0.05"""

from simulations.run_scenario import ScenarioRunner
import copy
from core.love import DEFAULT_WEIGHTS

# Test 1: No entropy (delS=0)
print("=" * 60)
print("TEST 1: No entropy (delS=0)")
print("=" * 60)
weights_no_entropy = copy.copy(DEFAULT_WEIGHTS)
weights_no_entropy['delS'] = 0.0

runner1 = ScenarioRunner(
    'data/single_dating_to_love_M1.csv',
    weights=weights_no_entropy
)
traj1 = runner1.run()
final1 = traj1.iloc[-1]
print(f"Final gamma_self: {final1['gamma_x']:.2f} + {final1['gamma_y']:.2f}i")
print(f"Final magnitude: {final1['gamma_magnitude']:.2f}")
print()

# Test 2: With entropy (delS=0.05)
print("=" * 60)
print("TEST 2: With entropy (delS=0.05)")
print("=" * 60)
weights_with_entropy = copy.copy(DEFAULT_WEIGHTS)
weights_with_entropy['delS'] = 0.05

runner2 = ScenarioRunner(
    'data/single_dating_to_love_M1.csv',
    weights=weights_with_entropy
)
traj2 = runner2.run()
final2 = traj2.iloc[-1]
print(f"Final gamma_self: {final2['gamma_x']:.2f} + {final2['gamma_y']:.2f}i")
print(f"Final magnitude: {final2['gamma_magnitude']:.2f}")
print()

# Compare
print("=" * 60)
print("COMPARISON")
print("=" * 60)
delta_x = final1['gamma_x'] - final2['gamma_x']
delta_y = final1['gamma_y'] - final2['gamma_y']
print(f"Delta_x (real axis): {delta_x:.2f}")
print(f"Delta_y (imag axis): {delta_y:.2f}")
print()
print("Expected: Entropy should pull LEFT (negative real)")
print(f"-> Delta_x should be POSITIVE (delS=0 ends more right than delS=0.05)")
print(f"-> Delta_y should be ~0 (no imaginary component in entropy)")
print()
if delta_x > 0 and abs(delta_y) < 0.5:
    print("✓ SIGNS CORRECT: Entropy pulls left as expected")
else:
    print("✗ SIGNS WRONG: Check the formula")
