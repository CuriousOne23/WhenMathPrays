"""Test new default delS=0.02"""
from simulations.run_scenario import ScenarioRunner

runner = ScenarioRunner('data/single_dating_to_love_M1.csv')
traj = runner.run()
final = traj.iloc[-1]

print(f"With delS=0.02 (new default):")
print(f"  gamma_self = {final['gamma_x']:.2f} + {final['gamma_y']:.2f}i")
print(f"  Magnitude: {final['gamma_magnitude']:.2f}")
print(f"  Entropy drift over 60 days: ~{0.02 * 60:.2f} units leftward")
