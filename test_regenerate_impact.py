from scripts.scenario_generator import ScenarioGenerator

# Test regenerating Test1_Linear with new parameters
gen = ScenarioGenerator('Test1_Linear_Regen')
result = gen.generate_scenario(
    M1_trajectory=[(0,-2.5,0.5,0),(6,-1.5,1.5,0.3),(12,-0.7,2.75,0.2)],
    M2_trajectory=[(0,-2.0,1.0,0),(6,-1.5,1.5,0.3),(12,-1.0,2.0,0.2)],
    duration_days=84,
    event_sampling='weekly'
)

print(f"Test1_Linear regenerated with new parameters:")
print(f"  M1 final S={result['M1_data'][-1]['S']}")
print(f"  M2 final S={result['M2_data'][-1]['S']}")
print(f"  Original Test1_Linear had: M1 S=0, M2 S=0")
