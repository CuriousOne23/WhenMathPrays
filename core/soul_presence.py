import numpy as np

def soul_presence(consistency, acceptance, coherence, resonance, utility_integral, clip=True):
    """
    SoulPresence: Persistent identity.
    Trust gate: both consistency AND acceptance ≥ 0.3
    """
    if clip:
        consistency = np.clip(consistency, 0.0, 1.0)
        acceptance = np.clip(acceptance, 0.0, 1.0)
        coherence = np.clip(coherence, 0.0, 1.0)
        resonance = np.clip(resonance, 0.01, 1.0)
        utility_integral = np.clip(utility_integral, -10, 10)

    # TRUST GATE: Both must be ≥ 0.3
    trust_gate = 1.0 if (consistency >= 0.3 and acceptance >= 0.3) else 0.0

    exponent = np.clip(0.1 * utility_integral, -10, 10)  # ← clamp exp input
    return trust_gate * coherence * resonance * np.exp(exponent)
