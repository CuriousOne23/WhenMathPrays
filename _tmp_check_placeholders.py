import os
p40 = r'thought_simulator/40_thought_simulator_playground/40.165_dcb_stability_prototypes'
print('40.165 contents:', sorted(os.listdir(p40)))
p40a = os.path.join(p40, 'artifacts')
print('artifacts exists:', os.path.isdir(p40a))
print('artifacts contents:', os.listdir(p40a) if os.path.isdir(p40a) else 'N/A')
p30 = r'thought_simulator/30_verification/30.165_dcb_stability_prototypes'
print('30.165 contents:', sorted(os.listdir(p30)))
p50 = r'thought_simulator/50_thought_simulator_design/50.165_dcb_stability_design.md'
print('50.165 file exists:', os.path.isfile(p50))
p10 = r'thought_simulator/10_thought_simulator_req/50_design/10.50.165_dcb_stability_requirements.md'
print('10.50.165 file exists:', os.path.isfile(p10))
print('Done check.')
