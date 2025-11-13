import numpy as np
from core.love import love
from core.gamma_self import gamma_self

def test_complex_output():
    t = np.linspace(0, 10, 11)
    dt = 1.0
    gamma_t = gamma_self(t, reduce_ego_flux=-0.5, bond_flux=0.0)
    L = love(
        vis_t=np.ones(11), res_t=np.ones(11),
        fidelity=1.0, altruism=1.0,
        shared_growth_t=np.full(11, 10),
        gamma_t=gamma_t, delta_S_t=np.zeros(11), dt=dt
    )
    assert isinstance(L, complex)
    assert L.imag == 0
    assert L.real > 100
