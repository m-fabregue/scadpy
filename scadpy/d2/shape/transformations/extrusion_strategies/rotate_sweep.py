from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray


def rotate_sweep(
    angle: float,
    start_angle: float = 0.0,
) -> Callable[[NDArray[np.float64], float], NDArray[np.float64]]:
    """Return a strategy that linearly rotates the cross-section along the path.

    Parameters
    ----------
    angle:
        Total rotation angle in degrees at ``t=1``.
    start_angle:
        Rotation angle in degrees at ``t=0``.  Defaults to ``0.0``.
    """
    from scadpy import rotate_vertex_coordinates

    def _strategy(points: NDArray[np.float64], t: float) -> NDArray[np.float64]:
        a: float = float(np.radians(start_angle + (angle - start_angle) * t))
        cos_a: float = float(np.cos(a))
        sin_a: float = float(np.sin(a))
        rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
        return rotate_vertex_coordinates(points, rotation_matrix)

    return _strategy
