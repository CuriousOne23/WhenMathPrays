# core/gamma_self.py
import numpy as np
from typing import Union, Sequence
import numpy.typing as npt


# core/gamma_self.py
def gamma_self(
    t: Union[Sequence[float], npt.NDArray[np.float64]],
    b: float = 0.5,
    A: float = 0.5,
    omega: float = 2 * np.pi / 100.0,  # ← ONE CYCLE IN 100 STEPS
    C: float | None = None
) -> npt.NDArray[np.complex128]:
    t_arr = np.asarray(t, dtype=np.float64)
    if t_arr.ndim not in (0, 1):
        raise ValueError("t must be scalar or 1D array")

    if C is None:
        C = A

    ego = -b + A * np.sin(omega * t_arr)
    resonance = C * np.cos(omega * t_arr)
    gamma = ego + 1j * resonance

    return gamma