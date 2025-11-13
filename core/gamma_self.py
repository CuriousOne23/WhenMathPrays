from __future__ import annotations
import numpy as np
import numpy.typing as npt
from typing import Union, Sequence


def gamma_self(
    t: Union[float, Sequence[float], npt.NDArray[np.float64]],
    reduce_ego_flux: float = 0.0,   # + = reduces ego (increase love), - = increases ego (reduce love)
    bond_flux: float = 0.0          # + = bond (increase love), - = enmity (reduce love)
) -> npt.NDArray[np.complex128]:
    t_arr = np.atleast_1d(t).astype(float)
    gamma = reduce_ego_flux + 1j * bond_flux
    return np.full_like(t_arr, gamma, dtype=complex)


def is_soul_present(gamma: npt.NDArray[np.complex128]) -> bool:
    arg = np.angle(gamma)
    return bool(np.mean(np.abs(arg - np.pi/2)) < 0.5)
