from __future__ import annotations
import numpy as np
import numpy.typing as npt
from core.gamma_self import is_soul_present


def love(
    vis_t: npt.NDArray[np.float64],
    res_t: npt.NDArray[np.float64],
    fidelity: float,
    altruism: float,
    shared_growth_t: npt.NDArray[np.float64],
    gamma_t: npt.NDArray[np.complex128],
    delta_S_t: npt.NDArray[np.float64],
    dt: float,
    soul_required: bool = False
) -> complex:
    if soul_required and not is_soul_present(gamma_t):
        return 0.0 + 0.0j

    t = np.arange(len(vis_t)) * dt
    decay_delta = np.exp(-np.mean(delta_S_t) * t)

    term = (
        np.maximum(vis_t, 0) *
        np.maximum(res_t, 0) *
        fidelity *
        altruism *
        shared_growth_t *
        gamma_t *
        decay_delta
    )

    return complex(np.sum(term) * dt)
