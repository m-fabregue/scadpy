from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray


def reverse_sweep(
    strategy: Callable[[NDArray[np.float64], float], NDArray[np.float64]],
) -> Callable[[NDArray[np.float64], float], NDArray[np.float64]]:
    """Wrap a strategy so it runs in reverse (``t=0`` becomes ``t=1``).

    Parameters
    ----------
    strategy:
        Any extrusion strategy callable.
    """

    def _strategy(points: NDArray[np.float64], t: float) -> NDArray[np.float64]:
        return strategy(points, 1.0 - t)

    return _strategy
