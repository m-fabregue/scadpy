from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_corner_normals(
    shape: Shape,
    epsilon: float = 1e-10,
) -> NDArray[np.float64]:
    """
    For each corner in the shape, return its outward unit normal.

    The normal is the bisector of the outward edge normals at the corner,
    oriented to point away from the filled material. It points outward for
    convex corners and inward for concave ones, consistently with
    :func:`are_shape_corners_convex`.

    Each edge normal is the 90° CW rotation of the edge direction, which
    points outward for CCW (exterior) rings. The bisector is then the
    normalized average of the two adjacent edge normals. Its sign is
    corrected using :func:`are_shape_corners_convex`, which already accounts
    for ring orientation (interior vs exterior), so no separate handling
    is needed here.

    For degenerate 180° corners (straight edges) where the bisector
    vanishes, the normal falls back to the outward edge normal of the
    incoming edge (90° CW rotation).

    Parameters
    ----------
    shape : Shape
        The shape to extract corner normals from.
    epsilon : float, optional
        Threshold below which the bisector norm is considered degenerate
        (straight 180° corner). Defaults to ``1e-10``.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape (n_corners, 2). Each row is a unit vector ``[nx, ny]``.

    Examples
    --------
    >>> from scadpy import (
    ...     get_shape_corner_normals,
    ...     are_shape_corners_convex,
    ...     polygon,
    ... )

    >>> # arrow: 5 convex corners (normals point outward)
    >>> # + 2 concave corners (normals point inward,
    >>> # into the tail notch — x component is positive)
    >>> arrow = polygon(
    ...     [(0, 1), (3, 0), (5, 2), (3, 4),
    ...      (0, 3), (1, 2.5), (1, 1.5)]
    ... )
    >>> normals = get_shape_corner_normals(arrow)
    >>> normals.round(4)  # doctest: +NORMALIZE_WHITESPACE
    array([[-0.9975, -0.0709],
           [ 0.2298, -0.9732],
           [ 1.    ,  0.    ],
           [ 0.2298,  0.9732],
           [-0.9975,  0.0709],
           [ 0.8507,  0.5257],
           [ 0.8507, -0.5257]])
    """
    from scadpy.core.assembly import get_assembly_face_corner_normals

    return get_assembly_face_corner_normals(
        corner_to_vertex=shape.corner_to_vertex,
        vertex_coordinates=shape.vertex_coordinates,
        are_corners_convex=shape.are_corners_convex,
        epsilon=epsilon,
    )
