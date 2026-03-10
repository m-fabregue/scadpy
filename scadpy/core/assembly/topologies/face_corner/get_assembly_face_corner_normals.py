from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def get_assembly_face_corner_normals(
    corner_to_vertex: NDArray[np.int64],
    vertex_coordinates: NDArray[np.float64],
    are_corners_convex: NDArray[np.bool_],
    epsilon: float = 1e-10,
) -> NDArray[np.float64]:
    """
    For each corner, return its outward unit normal.

    The normal is the bisector of the two adjacent edge normals (90° CW
    rotation of each edge direction), oriented outward for convex corners
    and inward for concave ones. For degenerate 180° corners where the
    bisector vanishes, falls back to the incoming edge normal.

    The term *face* distinguishes this from a purely topological corner:
    the computation relies on face geometry (vertex coordinates) and face
    orientation (convexity), making it applicable to both 2D shape rings
    and 3D solid faces.

    Parameters
    ----------
    corner_to_vertex : NDArray[np.int64]
        2D array of shape ``(n_corners, 3)``. Each row is
        ``[prev_vertex, curr_vertex, next_vertex]``.
    vertex_coordinates : NDArray[np.float64]
        2D array of shape ``(n_vertices, d)`` with vertex coordinates.
    are_corners_convex : NDArray[np.bool_]
        1D boolean array of shape ``(n_corners,)``. True if the corner
        is convex (normal points outward), False if concave (normal points
        inward).
    epsilon : float, optional
        Threshold below which the bisector norm is considered degenerate
        (straight 180° corner). Defaults to ``1e-10``.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape ``(n_corners, 2)``. Each row is a unit vector
        ``[nx, ny]``.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import get_assembly_face_corner_normals

    >>> # square: 4 convex corners, normals point outward
    >>> # (diagonal directions)
    >>> corner_to_vertex = np.array(
    ...     [[3, 0, 1], [0, 1, 2], [1, 2, 3], [2, 3, 0]],
    ...     dtype=np.int64
    ... )
    >>> vertex_coordinates = np.array(
    ...     [[-1., -1.], [1., -1.], [1., 1.], [-1., 1.]]
    ... )
    >>> are_corners_convex = np.array([True, True, True, True])
    >>> get_assembly_face_corner_normals(
    ...     corner_to_vertex,
    ...     vertex_coordinates,
    ...     are_corners_convex,
    ... ).round(4)
    array([[-0.7071, -0.7071],
           [ 0.7071, -0.7071],
           [ 0.7071,  0.7071],
           [-0.7071,  0.7071]])
    """
    if len(corner_to_vertex) == 0:
        d = vertex_coordinates.shape[1] if vertex_coordinates.ndim == 2 else 0
        return np.empty((0, d), dtype=np.float64)

    prev_coords = vertex_coordinates[corner_to_vertex[:, 0]]
    curr_coords = vertex_coordinates[corner_to_vertex[:, 1]]
    next_coords = vertex_coordinates[corner_to_vertex[:, 2]]

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

    sign = np.where(are_corners_convex, 1.0, -1.0)[:, np.newaxis]

    return bisector_norm * sign
