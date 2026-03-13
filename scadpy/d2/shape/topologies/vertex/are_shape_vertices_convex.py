from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def are_shape_vertices_convex(
    shape: Shape,
) -> NDArray[np.bool_]:
    """
    For each vertex in the shape, return whether it is convex.

    A vertex is convex if the shape turns left at that vertex on an exterior
    ring (counter-clockwise winding). Concave vertices turn right. Interior
    rings have their orientation inverted accordingly.

    Use :func:`get_shape_vertex_angles` to get the magnitude of the turning
    angle independently of convexity.

    Parameters
    ----------
    shape : Shape
        The shape to extract vertex convexity from.

    Returns
    -------
    NDArray[np.bool_]
        1D boolean array of shape (n_vertices,). True if convex, False if concave.

    """
    vertex_neighborhoods = shape.vertex_to_neighbor_vertex
    coords = shape.vertex_coordinates

    if len(vertex_neighborhoods) == 0:
        return np.empty(0, dtype=np.bool_)

    prev_coords = coords[vertex_neighborhoods[:, 0]]
    curr_coords = coords
    next_coords = coords[vertex_neighborhoods[:, 1]]

    v_in = curr_coords - prev_coords
    v_out = next_coords - curr_coords

    # 2D cross product: positive = left turn (convex on CCW ring)
    cross = v_in[:, 0] * v_out[:, 1] - v_in[:, 1] * v_out[:, 0]

    is_convex = cross > 0

    # interior rings (CW in shapely) have inverted orientation — flip convexity
    ring_types = shape.ring_types
    vertex_to_ring = shape.vertex_to_ring
    vertex_ring_indices = vertex_to_ring
    is_interior = ring_types[vertex_ring_indices] == "interior"
    is_convex = np.where(is_interior, ~is_convex, is_convex)

    return is_convex
