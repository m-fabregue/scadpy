from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def are_shape_corners_convex(
    shape: Shape,
) -> NDArray[np.bool_]:
    """
    For each corner in the shape, return whether it is convex.

    A corner is convex if the shape turns left at that vertex on an exterior
    ring (counter-clockwise winding). Concave corners turn right. Interior
    rings have their orientation inverted accordingly.

    Use :func:`get_shape_corner_angles` to get the magnitude of the turning
    angle independently of convexity.

    Parameters
    ----------
    shape : Shape
        The shape to extract corner convexity from.

    Returns
    -------
    NDArray[np.bool_]
        1D boolean array of shape (n_corners,). True if convex, False if concave.

    Examples
    --------
    >>> from scadpy import are_shape_corners_convex, polygon

    >>> # arrow: 5 convex corners (tip and sides)
    >>> # + 2 concave corners (the tail notch)
    >>> arrow = polygon(
    ...     [(0, 1), (3, 0), (5, 2), (3, 4),
    ...      (0, 3), (1, 2.5), (1, 1.5)]
    ... )
    >>> are_shape_corners_convex(arrow).tolist()
    [True, True, True, True, True, False, False]
    """
    corner_to_vertex = shape.corner_to_vertex
    coords = shape.vertex_coordinates

    if len(corner_to_vertex) == 0:
        return np.empty(0, dtype=np.bool_)

    prev_coords = coords[corner_to_vertex[:, 0]]
    curr_coords = coords[corner_to_vertex[:, 1]]
    next_coords = coords[corner_to_vertex[:, 2]]

    v_in = curr_coords - prev_coords
    v_out = next_coords - curr_coords

    # 2D cross product: positive = left turn (convex on CCW ring)
    cross = v_in[:, 0] * v_out[:, 1] - v_in[:, 1] * v_out[:, 0]

    is_convex = cross > 0

    # interior rings (CW in shapely) have inverted orientation — flip convexity
    ring_types = shape.ring_types
    vertex_to_ring = shape.vertex_to_ring
    corner_ring_indices = vertex_to_ring[corner_to_vertex[:, 1]]
    is_interior = ring_types[corner_ring_indices] == "interior"
    is_convex = np.where(is_interior, ~is_convex, is_convex)

    return is_convex
