import os
base = 'thought_simulator/40_thought_simulator_playground/40.165_dcb_stability_prototypes/artifacts'
os.makedirs(base, exist_ok=True)
with open(os.path.join(base, '.gitkeep'), 'w', encoding='utf-8') as f:
    f.write('Scaffold placeholder for future 40.165 run artifacts (e.g. stability observation logs).\n')
print('Created:', base)
print('Exists now:', os.path.isdir(base))
print('Contents:', os.listdir(base))
