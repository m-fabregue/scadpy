from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def get_assembly_face_vertex_normals(
    vertex_neighborhoods: NDArray[np.int64],
    vertex_coordinates: NDArray[np.float64],
    are_vertices_convex: NDArray[np.bool_],
    epsilon: float = 1e-10,
) -> NDArray[np.float64]:
    """
    For each vertex, return its outward unit normal.

    The normal is the bisector of the two adjacent edge normals (90° CW
    rotation of each edge direction), oriented outward for convex vertices
    and inward for concave ones. For degenerate 180° vertices where the
    bisector vanishes, falls back to the incoming edge normal.

    The term *face* distinguishes this from a purely topological vertex:
    the computation relies on face geometry (vertex coordinates) and face
    orientation (convexity), making it applicable to both 2D shape rings
    and 3D solid faces.

    Parameters
    ----------
    vertex_neighborhoods : NDArray[np.int64]
        2D array of shape ``(n_vertices, 2)``. Each row is
        ``[prev_vertex, next_vertex]``.
    vertex_coordinates : NDArray[np.float64]
        2D array of shape ``(n_vertices, d)`` with vertex coordinates.
    are_vertices_convex : NDArray[np.bool_]
        1D boolean array of shape ``(n_vertices,)``. True if the vertex
        is convex (normal points outward), False if concave (normal points
        inward).
    epsilon : float, optional
        Threshold below which the bisector norm is considered degenerate
        (straight 180° vertex). Defaults to ``1e-10``.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape ``(n_vertices, 2)``. Each row is a unit vector
        ``[nx, ny]``.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import get_assembly_face_vertex_normals

    >>> # square: 4 convex vertices, normals point outward
    >>> # (diagonal directions)
    >>> vertex_neighborhoods = np.array(
    ...     [[3, 1], [0, 2], [1, 3], [2, 0]],
    ...     dtype=np.int64
    ... )
    >>> vertex_coordinates = np.array(
    ...     [[-1., -1.], [1., -1.], [1., 1.], [-1., 1.]]
    ... )
    >>> are_vertices_convex = np.array([True, True, True, True])
    >>> get_assembly_face_vertex_normals(
    ...     vertex_neighborhoods,
    ...     vertex_coordinates,
    ...     are_vertices_convex,
    ... ).round(4)
    array([[-0.7071, -0.7071],
           [ 0.7071, -0.7071],
           [ 0.7071,  0.7071],
           [-0.7071,  0.7071]])
    """
    if len(vertex_neighborhoods) == 0:
        d = vertex_coordinates.shape[1] if vertex_coordinates.ndim == 2 else 0
        return np.empty((0, d), dtype=np.float64)

    prev_coords = vertex_coordinates[vertex_neighborhoods[:, 0]]
    curr_coords = vertex_coordinates
    next_coords = vertex_coordinates[vertex_neighborhoods[:, 1]]

    v_in = curr_coords - prev_coords
    v_out = next_coords - curr_coords

    v_in_norm = v_in / np.linalg.norm(v_in, axis=1, keepdims=True)
    v_out_norm = v_out / np.linalg.norm(v_out, axis=1, keepdims=True)

    # outward edge normals: 90° CW rotation (dx, dy) → (dy, -dx)
    n_in = np.stack([v_in_norm[:, 1], -v_in_norm[:, 0]], axis=1)
    n_out = np.stack([v_out_norm[:, 1], -v_out_norm[:, 0]], axis=1)

    bisector = n_in + n_out

    # degenerate case: 180° corner — bisector vanishes, fall back to incoming edge normal
    zero_mask = np.linalg.norm(bisector, axis=1) < epsilon
    if np.any(zero_mask):
        bisector[zero_mask] = n_in[zero_mask]

    bisector_norm = bisector / np.linalg.norm(bisector, axis=1, keepdims=True)

    sign = np.where(are_vertices_convex, 1.0, -1.0)[:, np.newaxis]

    return bisector_norm * sign
