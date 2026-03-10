from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_corner_angles(
    shape: Shape,
) -> NDArray[np.float64]:
    """
    For each corner in the shape, return its interior angle in degrees.

    The angle is always positive, in the range (0°, 180°). It represents
    the turning angle at the corner, regardless of whether the corner is
    convex or concave. Use :func:`are_shape_corners_convex` to distinguish
    convex corners from concave ones.

    The angle is computed as the absolute value of the signed angle from the
    incoming edge to the outgoing edge at each corner, using the 2D cross
    product to determine orientation.

    Parameters
    ----------
    shape : Shape
        The shape to extract corner angles from.

    Returns
    -------
    NDArray[np.float64]
        1D array of shape (n_corners,), one angle per corner, in degrees.
        All values are in the range (0°, 180°).

    Examples
    --------
    >>> from scadpy import get_shape_corner_angles, polygon

    >>> # arrow: 5 convex corners + 2 concave corners,
    >>> # all with different angles
    >>> arrow = polygon(
    ...     [(0, 1), (3, 0), (5, 2), (3, 4),
    ...      (0, 3), (1, 2.5), (1, 1.5)]
    ... )
    >>> get_shape_corner_angles(arrow).round(2).tolist()
    [135.0, 63.43, 90.0, 63.43, 135.0, 63.43, 63.43]
    """
    from scadpy.core.assembly import get_assembly_face_corner_angles

    return get_assembly_face_corner_angles(
        corner_to_vertex=shape.corner_to_vertex,
        vertex_coordinates=shape.vertex_coordinates,
    )
