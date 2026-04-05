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

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import circle
    >>> path = np.column_stack([np.zeros(10), np.zeros(10), np.linspace(0, 20, 10)])
    >>> circle(5).path_extrude(path, strategy=reverse_sweep(scale_sweep(end=0.2)))  # taper from tip # doctest: +SKIP
    """

    def _strategy(points: NDArray[np.float64], t: float) -> NDArray[np.float64]:
        return strategy(points, 1.0 - t)

    return _strategy
