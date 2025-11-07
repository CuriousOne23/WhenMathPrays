import numpy as np
from core.soul_presence import soul_presence

def test_soul_presence_trust_gate():
    # Trust gate: min(consistency, acceptance)
    assert soul_presence(0.2, 0.8, 1.0, 1.0, 0.0) == 0.0  # low consistency
    assert soul_presence(0.8, 0.2, 1.0, 1.0, 0.0) == 0.0  # low acceptance
    assert soul_presence(0.6, 0.7, 1.0, 1.0, 0.0) > 0.0  # both above threshold

def test_soul_presence_historical_growth():
    # utility_integral drives growth
    sp1 = soul_presence(0.8, 0.8, 1.0, 1.0, 0.0)
    sp2 = soul_presence(0.8, 0.8, 1.0, 1.0, 10.0)
    assert sp2 > sp1 * 2  # exp(1.0) ≈ 2.7

def test_soul_presence_present_reality():
    # coherence and resonance
    sp_low = soul_presence(0.8, 0.8, 0.1, 0.1, 0.0)
    sp_high = soul_presence(0.8, 0.8, 0.9, 0.9, 0.0)
    assert sp_high > sp_low * 5

def test_soul_presence_clipping():
    # No blowup
    sp = soul_presence(10.0, 10.0, 10.0, 10.0, 100.0)
    assert np.isfinite(sp)
    assert sp < 25_000  # exp(10) ≈ 22K

def test_soul_presence_thresholds():
    # Claim: SP > 0.1 = alive, SP < 0.1 = fading
    alive = soul_presence(0.6, 0.6, 0.7, 0.7, 1.0)
    fading = soul_presence(0.3, 0.3, 0.5, 0.5, -5.0)
    assert alive > 0.1
    assert fading < 0.1
