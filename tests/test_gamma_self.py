# tests/test_gamma_self.py
import numpy as np
from core.gamma_self import gamma_self

def test_gamma_sign_convention():
    t = [0]
    # +Re = ego
    g = gamma_self(t, reduce_ego_flux=0.5, bond_flux=0.0)
    assert g.real > 0 and g.imag == 0

    # -Re = union
    g = gamma_self(t, reduce_ego_flux=-0.5, bond_flux=0.0)
    assert g.real < 0 and g.imag == 0

    # +Im = enmity
    g = gamma_self(t, reduce_ego_flux=0.0, bond_flux=0.5)
    assert g.real == 0 and g.imag > 0

    # -Im = union
    g = gamma_self(t, reduce_ego_flux=0.0, bond_flux=-0.5)
    assert g.real == 0 and g.imag < 0