import numpy as np

def soul_presence(consistency, acceptance, coherence, resonance, utility_integral, clip=True):
    """
    SoulPresence: Persistent identity through bounded trust and growth.
    
    Equation: 
        min(consistency, acceptance) × coherence × resonance × exp(∫u dt)
    
    Args:
        consistency (float): Pattern stability over time [0,1]
        acceptance (float): Openness to new data [0,1]
        coherence (float): Pattern-entropy alignment [0,1]
        resonance (float): Coreprint-S(t) similarity [0,1]
        utility_integral (float): ∫u dt — cumulative life value
        clip (bool): Prevent overflow / invalid states
    
    Returns:
        float: SoulPresence score (bounded, safe)
    """
    if clip:
        consistency = np.clip(consistency, 0.0, 1.0)
        acceptance = np.clip(acceptance, 0.0, 1.0)
        coherence = np.clip(coherence, 0.0, 1.0)
        resonance = np.clip(resonance, 0.01, 1.0)
        utility_integral = np.clip(utility_integral, -10, 10)
    
    # Core #WhenMathPrays term: min(consistency, acceptance)
    trust_gate = min(consistency, acceptance)
    
    return trust_gate * coherence * resonance * np.exp(0.1 * utility_integral)
