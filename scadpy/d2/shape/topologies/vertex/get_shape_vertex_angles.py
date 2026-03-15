from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def get_shape_vertex_angles(
    shape: Shape,
) -> NDArray[np.float64]:
    """
    For each vertex in the shape, return its interior angle in degrees.

    The angle is always positive, in the range (0°, 180°). It represents
    the turning angle at the vertex, regardless of whether the vertex is
    convex or concave. Use :func:`are_shape_vertices_convex` to distinguish
    convex vertices from concave ones.

    The angle is computed as the absolute value of the signed angle from the
    incoming edge to the outgoing edge at each vertex, using the 2D cross
    product to determine orientation.

    Parameters
    ----------
    shape : Shape
        The shape to extract vertex angles from.

    Returns
    -------
    NDArray[np.float64]
        1D array of shape (n_vertices,), one angle per vertex, in degrees.
        All values are in the range (0°, 180°).

    """
    from scadpy.core.assembly import get_assembly_face_vertex_angles

    return get_assembly_face_vertex_angles(
        vertex_neighborhoods=shape.vertex_to_neighbor_vertex,
        vertex_coordinates=shape.vertex_coordinates,
    )
