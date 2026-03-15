from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def _make_half_plane(
    size: float,
    axis_x: float,
    axis_y: float,
    pivot_x: float,
    pivot_y: float,
    positive: bool,
) -> Shape:
    """Large polygon covering one half-plane relative to an axis line."""
    from scadpy.d2.shape.primitives.polygon import polygon

    radial_x, radial_y = (axis_y, -axis_x) if positive else (-axis_y, axis_x)
    return polygon(
        [
            [pivot_x - size * axis_x, pivot_y - size * axis_y],
            [pivot_x + size * axis_x, pivot_y + size * axis_y],
            [
                pivot_x + size * axis_x + size * radial_x,
                pivot_y + size * axis_y + size * radial_y,
            ],
            [
                pivot_x - size * axis_x + size * radial_x,
                pivot_y - size * axis_y + size * radial_y,
            ],
        ]
    )


def linear_cut_shape(
    shape: Shape,
    axis: float | Iterable[float],
    pivot: float | Iterable[float] = 0,
) -> Shape:
    """Cut a shape along an axis line through a pivot point.

    The axis line divides the plane into two half-planes and the shape
    is split accordingly. Both halves are returned as a single
    :class:`Shape` whose parts are the individual cut pieces.

    The *positive* side is 90° clockwise from the axis direction. For
    ``axis=[0, 1]`` (Y-axis) this means points with ``x >= 0``; for
    ``axis=[1, 0]`` (X-axis) this means points with ``y <= 0``.

    Parameters
    ----------
    shape : Shape
        The shape to cut.
    axis : float or Iterable[float]
        Direction of the cut line (2D vector).
    pivot : float or Iterable[float], optional
        A point on the cut line. Default is the origin ``0``.

    Returns
    -------
    Shape
        A new shape whose parts are the two halves of the original shape
        concatenated together.
    """
    from scadpy import resolve_vector_2d

    axis = resolve_vector_2d(axis, 0)
    axis = axis / np.linalg.norm(axis)
    pivot = resolve_vector_2d(pivot, 0)

    bounds = shape.bounds
    size = float(np.max(np.abs(bounds))) * 10 + 100

    axis_x, axis_y = float(axis[0]), float(axis[1])
    pivot_x, pivot_y = float(pivot[0]), float(pivot[1])

    positive_half_plane = _make_half_plane(
        size, axis_x, axis_y, pivot_x, pivot_y, positive=True
    )
    negative_half_plane = _make_half_plane(
        size, axis_x, axis_y, pivot_x, pivot_y, positive=False
    )

    positive_side = shape - negative_half_plane
    negative_side = shape - positive_half_plane

    return positive_side + negative_side
