import numpy as np
from core.soul_presence import soul_presence

def run_stress_test(agents=10000, steps=1000, noise_level=0.3):
    np.random.seed(42)
    
    # Base inputs for 3 agent types
    bases = [
        {"c": 0.6, "a": 0.6, "coh": 0.7, "res": 0.7, "u_step": 0.01},  # Growing
        {"c": 0.2, "a": 0.8, "coh": 0.5, "res": 0.5, "u_step": 0.00},  # Fading
        {"c": 0.8, "a": 0.8, "coh": 0.9, "res": 0.9, "u_step": 0.02},  # Thriving
    ]
    
    sp_history = {i: [] for i in range(3)}
    utility = [0.0] * 3
    
    for step in range(steps):
        for i, base in enumerate(bases):
            # Add 30% noise
            c = max(0.0, base["c"] + np.random.normal(0, noise_level * base["c"]))
            a = max(0.0, base["a"] + np.random.normal(0, noise_level * base["a"]))
            coh = max(0.0, base["coh"] + np.random.normal(0, noise_level * base["coh"]))
            res = max(0.01, base["res"] + np.random.normal(0, noise_level * base["res"]))
            
            utility[i] += base["u_step"] + np.random.normal(0, 0.005)
            
            sp = soul_presence(c, a, coh, res, utility[i])
            sp_history[i].append(sp)
    
    return sp_history

# Run and print summary
if __name__ == "__main__":
    history = run_stress_test()
    for i, name in enumerate(["Growing", "Fading", "Thriving"]):
        sp = history[i]
        print(f"{name}: min={min(sp):.3f}, max={max(sp):.3f}, final={sp[-1]:.3f}")