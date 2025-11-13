import numpy as np
from core.love import love
from core.gamma_self import gamma_self

def test_decay_with_magnitude():
    t = np.linspace(0, 10, 11)
    dt = 1.0

    gamma_low = gamma_self(t, reduce_ego_flux=-0.1, bond_flux=-0.1)
    L_low = love(
        vis_t=np.ones(11), res_t=np.ones(11),
        fidelity=1.0, altruism=1.0,
        shared_growth_t=np.full(11, 10),
        gamma_t=gamma_low, delta_S_t=np.zeros(11), dt=dt
    )

    gamma_high = gamma_self(t, reduce_ego_flux=0.5, bond_flux=0.5)
    L_high = love(
        vis_t=np.ones(11), res_t=np.ones(11),
        fidelity=1.0, altruism=1.0,
        shared_growth_t=np.full(11, 10),
        gamma_t=gamma_high, delta_S_t=np.zeros(11), dt=dt
    )

    assert L_low.real > 500
    assert L_high.real < 50
