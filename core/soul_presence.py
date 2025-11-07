import numpy as np

def soul_presence(coherence, resonance, utility_integral, clip=True):
    """
    SoulPresence: Persistent identity through coherence, resonance, and utility growth.
    
    Equation: coherence × resonance × exp(∫u dt)
    
    Args:
        coherence (float): Pattern-entropy alignment [0,1]
        resonance (float): Coreprint-S(t) similarity [0,1]
        utility_integral (float): ∫u dt — cumulative life value
        clip (bool): Prevent overflow
    
    Returns:
        float: SoulPresence score (bounded)
    """
    if clip:
        coherence = np.clip(coherence, 0.0, 1.0)
        resonance = np.clip(resonance, 0.01, 1.0)
        utility_integral = np.clip(utility_integral, -10, 10)  # exp safety
    
    return coherence * resonance * np.exp(0.1 * utility_integral)
