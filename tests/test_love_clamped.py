# tests/test_love_clamped.py
import numpy as np
from core.love import love
from core.gamma_self import gamma_self

def test_no_negative_love():
    t = np.linspace(0, 10, 11)
    dt = 1.0
    gamma_t = gamma_self(t, reduce_ego_flux=-0.1, bond_flux=-0.1)

    # Negative resonance → should be clamped
    res_t = np.full(11, -5.0)
    L = love(
        vis_t=np.ones(11), res_t=res_t,
        fidelity=1.0, altruism=1.0,
        shared_growth_t=np.ones(11),
        gamma_t=gamma_t, delta_S_t=np.zeros(11), dt=dt
    )
    assert L.real >= 0  # No anti-love