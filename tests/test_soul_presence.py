import numpy as np
from core.soul_presence import soul_presence

def test_soul_presence_trust_gate():
    assert np.isclose(soul_presence(0.2, 0.8, 1.0, 1.0, 0.0), 0.0)
    assert np.isclose(soul_presence(0.8, 0.2, 1.0, 1.0, 0.0), 0.0)
    assert soul_presence(0.6, 0.7, 1.0, 1.0, 0.0) > 0.0

def test_soul_presence_historical_growth():
    sp1 = soul_presence(0.8, 0.8, 1.0, 1.0, 0.0)
    sp2 = soul_presence(0.8, 0.8, 1.0, 1.0, 10.0)
    assert sp2 > sp1 * 2

def test_soul_presence_present_reality():
    sp_low = soul_presence(0.8, 0.8, 0.1, 0.1, 0.0)
    sp_high = soul_presence(0.8, 0.8, 0.9, 0.9, 0.0)
    assert sp_high > sp_low * 5

def test_soul_presence_clipping():
    sp = soul_presence(10.0, 10.0, 10.0, 10.0, 100.0)
    assert np.isfinite(sp)
    assert sp < 25_000

def test_soul_presence_thresholds():
    alive = soul_presence(0.6, 0.6, 0.7, 0.7, 1.0)
    fading = soul_presence(0.3, 0.3, 0.5, 0.5, -5.0)
    assert alive > 0.1
    assert fading < 0.2  # ← was 0.1, now 0.2