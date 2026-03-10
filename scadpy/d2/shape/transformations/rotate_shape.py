from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

import numpy as np
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape
    from scadpy import TopologyFilter


@typechecked
def rotate_shape(
    shape: Shape,
    angle: float,
    pivot: float | Iterable[float] = 0,
    vertex_filter: TopologyFilter[Shape] | None = None,
) -> Shape:
    """Rotate a shape by a given angle around a pivot point.

    Parameters
    ----------
    shape : Shape
        The shape to rotate.
    angle : float
        The rotation angle in degrees (counter-clockwise).
    pivot : float | Iterable[float], default=0
        The point around which rotation is applied. If a single float is provided,
        it is broadcast to all coordinate dimensions. Defaults to the origin.
    vertex_filter : TopologyFilter[Shape] | None, default=None
        Boolean array or callable selecting which vertices are rotated. If ``None``, all
        vertices are rotated.

    Returns
    -------
    Shape
        A new shape with the selected vertices rotated around the pivot.

    Examples
    --------
    >>> from scadpy import square, rotate_shape

    >>> rotate_shape(  # doctest: +SKIP
    ...     shape=square(4), angle=45, pivot=[2, 2]
    ... )

    .. render-example::
        :name: rotate_shape
        :example: rotate_shape(shape=square(4), angle=45, pivot=[2, 2])
        :ghost: square(4)
    """
    from scadpy import resolve_topology_filter, rotate_vertex_coordinates

    angle_rad = np.deg2rad(angle)
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    R = np.array([[c, -s], [s, c]])

    resolved_vertex_filter = resolve_topology_filter(shape, len(shape.vertex_coordinates), vertex_filter)
    return shape.recoordinate(
        rotate_vertex_coordinates(shape.vertex_coordinates, R, pivot, resolved_vertex_filter)
    )
