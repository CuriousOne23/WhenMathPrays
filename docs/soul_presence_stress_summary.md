# SoulPresence: Stress Test Summary

**Simulation:** `simulations/stress_soul.py`  
**Agents:** 10,000  
**Steps:** 1,000  
**Noise:** 30% Gaussian on all inputs  
**Seed:** 42

---

## Simulation Output

```text
Growing: min=0.000, max=2.613, final=2.192
Fading: min=0.000, max=0.468, final=0.000
Thriving: min=0.000, max=2.718, final=1.798

## Interpretation
Agent,Final SP,Status,Cause
Growing,2.192,Alive & Growing,Trust gate ON + positive utility/step
Fading,0.000,Dead,consistency = 0.2 < 0.3 → trust gate OFF
Thriving,1.798,Strong,High trust + high utility/step

30% real-world noise did not kill any agent.
Only lack of trust did.

## Key Insight
"Noise is survivable. Distrust is fatal."
— @PursueTruth123

The soul does not die from chaos.
It dies from distrust.