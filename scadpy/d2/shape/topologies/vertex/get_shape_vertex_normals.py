from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def get_shape_vertex_normals(
    shape: Shape,
    epsilon: float = 1e-10,
) -> NDArray[np.float64]:
    """
    For each vertex in the shape, return its outward unit normal.

    The normal is the bisector of the outward edge normals at the vertex,
    oriented to point away from the filled material. It points outward for
    convex vertices and inward for concave ones, consistently with
    :func:`are_shape_vertices_convex`.

    Each edge normal is the 90° CW rotation of the edge direction, which
    points outward for CCW (exterior) rings. The bisector is then the
    normalized average of the two adjacent edge normals. Its sign is
    corrected using :func:`are_shape_vertices_convex`, which already accounts
    for ring orientation (interior vs exterior), so no separate handling
    is needed here.

    For degenerate 180° vertices (straight edges) where the bisector
    vanishes, the normal falls back to the outward edge normal of the
    incoming edge (90° CW rotation).

    Parameters
    ----------
    shape : Shape
        The shape to extract vertex normals from.
    epsilon : float, optional
        Threshold below which the bisector norm is considered degenerate
        (straight 180° vertex). Defaults to ``1e-10``.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape (n_vertices, 2). Each row is a unit vector ``[nx, ny]``.

    """
    from scadpy.core.assembly import get_assembly_face_vertex_normals

    return get_assembly_face_vertex_normals(
        vertex_neighborhoods=shape.vertex_to_neighbor_vertex,
        vertex_coordinates=shape.vertex_coordinates,
        are_vertices_convex=shape.are_vertices_convex,
        epsilon=epsilon,
    )
