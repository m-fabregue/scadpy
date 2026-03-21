from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape
    from scadpy.d3.solid import Solid


def linear_extrude_shape(
    shape: Shape,
    height: float,
    intermediate_sections: int | None = None,
    strategy: list[Callable[[NDArray[np.float64], float], NDArray[np.float64]]]
    | Callable[[NDArray[np.float64], float], NDArray[np.float64]]
    | None = None,
) -> Solid:
    """
    Extrude a 2D shape along the Z axis into a 3D solid.

    Implemented as a :func:`path_extrude_shape` sweep along a straight vertical
    path, which makes all sweep features (strategies, intermediate sections)
    available on plain linear extrusions.

    Parameters
    ----------
    shape : Shape
        The 2D shape to extrude.
    height : float
        The extrusion height along the Z axis.
    intermediate_sections : int or None, optional
        Number of intermediate cross-section planes to insert uniformly along
        the path. Useful when a ``strategy`` deforms the cross-section
        continuously. ``None`` uses only the two end planes.
    strategy : Callable[[NDArray[np.float64], float], NDArray[np.float64]] or list[Callable[[NDArray[np.float64], float], NDArray[np.float64]]], optional
        A function or list of functions with signature ``(points, t) -> points``.
        ``points`` is an ``(N, 2)`` array of cross-section vertices and ``t`` is
        a scalar in ``[0, 1]`` representing position along the path (0 = bottom,
        1 = top).  See :mod:`scadpy.d2.shape.transformations.extrusion_strategies`
        for ready-made factories such as :func:`scale_sweep` and
        :func:`rotate_sweep`.

    Returns
    -------
    Solid
        A 3D solid created by extruding the shape.
    """
    from scadpy import path_extrude_shape

    path = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, height]], dtype=np.float64)
    return path_extrude_shape(
        shape=shape,
        path=path,
        intermediate_sections=intermediate_sections,
        strategy=strategy,
    )
