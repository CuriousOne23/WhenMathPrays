from scripts.scenario_generator import ScenarioGenerator

gen = ScenarioGenerator('Test2_Parent_Child')

# Balanced waypoints for normal parent-child bond (both should sustain/grow over 5 years)
# Increase Child's targets to match Parent's trajectory more closely
M1_wp = [(0, 2, 8, 0), (20, 2, 9, 0.5), (40, 2, 9, 0.5), (60, 2, 9, 0.5)]
M2_wp = [(0, 2, 7.5, 0), (20, 2, 8.5, 0.5), (40, 2, 8.5, 0.5), (60, 2, 8.5, 0.5)]

result = gen.generate_scenario(
    M1_trajectory=M1_wp,
    M2_trajectory=M2_wp,
    duration_days=1825,
    event_sampling='monthly',
    m1_name='Parent',
    m2_name='Child',
    shared_breath_prob=0.85  # Higher for stable long-term bonds (increased from 0.80)
)

print(f'Regenerated: {result["num_events"]} events, beta_S={result["beta_S"]}, s_S={result["s_S"]}')
print(f'M1 final S={result["M1_data"][-1]["S"]}, M2 final S={result["M2_data"][-1]["S"]}')
print(f'M1 Day 0 S={result["M1_data"][0]["S"]}, M1 Day 30 S={result["M1_data"][1]["S"]}')
