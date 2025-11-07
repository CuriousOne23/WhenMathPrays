from whenmathprays_core import WhenMathPraysCore
import numpy as np

def run_stress_test():
    core = WhenMathPraysCore(n_agents=1000)  # Fast test
    result = core.breath_cycle(steps=100)
    print(f"Mean Risk: {np.mean(result['risks']):.2f}")
    print(f"Max Risk: {np.max(result['risks']):.2f}")
    print(f"Passes: {result['passes']}")
    print(f"Escalations: {result.get('escalations', 0)}")
    assert result['passes'], "Stress test failed"

if __name__ == "__main__":
    run_stress_test()
