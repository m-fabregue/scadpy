from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray


def scale_sweep(
    end: float | list[float],
    start: float | list[float] = 1.0,
) -> Callable[[NDArray[np.float64], float], NDArray[np.float64]]:
    """Return a strategy that linearly scales the cross-section along the path.

    Parameters
    ----------
    end:
        Scale factor at ``t=1``.  A scalar applies uniformly on both axes;
        a 2-element list applies ``[sx, sy]`` independently.
    start:
        Scale factor at ``t=0``.  Defaults to ``1.0`` (no scale at start).
    """
    from scadpy import scale_vertex_coordinates

    end_arr = np.asarray(end, dtype=np.float64)
    start_arr = np.asarray(start, dtype=np.float64)

    def _strategy(points: NDArray[np.float64], t: float) -> NDArray[np.float64]:
        factor = start_arr + (end_arr - start_arr) * t
        return scale_vertex_coordinates(points, factor)

    return _strategy
