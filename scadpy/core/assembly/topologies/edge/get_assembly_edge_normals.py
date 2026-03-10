from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def get_assembly_edge_normals(
    edge_to_vertex: NDArray[np.int64],
    vertex_coordinates: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    For each edge, return its outward unit normal.

    The outward normal is the 90° clockwise rotation of the edge direction
    vector ``(dx, dy) → (dy, -dx)``. For exterior rings (CCW winding), this
    points away from the filled area. For interior rings (CW winding, i.e.
    holes), this also points away from the filled area (outward into the hole).

    Parameters
    ----------
    edge_to_vertex : NDArray[np.int64]
        2D array of shape ``(n_edges, 2)`` mapping each edge to its
        ``[start_vertex, end_vertex]`` indices.
    vertex_coordinates : NDArray[np.float64]
        2D array of shape ``(n_vertices, 2)`` with vertex coordinates.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape ``(n_edges, 2)``. Each row is a unit vector
        ``[nx, ny]`` perpendicular to the edge and pointing outward.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import get_assembly_edge_normals

    >>> # square centered at origin: 4 edges, normals point outward
    >>> edge_to_vertex = np.array(
    ...     [[0, 1], [1, 2], [2, 3], [3, 0]], dtype=np.int64
    ... )
    >>> vertex_coordinates = np.array(
    ...     [[-1., -1.], [1., -1.], [1., 1.], [-1., 1.]]
    ... )
    >>> get_assembly_edge_normals(
    ...     edge_to_vertex, vertex_coordinates
    ... ).round(4)
    array([[ 0., -1.],
           [ 1., -0.],
           [ 0.,  1.],
           [-1., -0.]])
    """
    if len(edge_to_vertex) == 0:
        d = vertex_coordinates.shape[1] if vertex_coordinates.ndim == 2 else 0
        return np.empty((0, d), dtype=np.float64)

    starts = vertex_coordinates[edge_to_vertex[:, 0]]
    ends = vertex_coordinates[edge_to_vertex[:, 1]]

    directions = ends - starts
    lengths = np.linalg.norm(directions, axis=1, keepdims=True)
    directions_normalized = directions / lengths

    # 90° CW rotation: (dx, dy) → (dy, -dx)
    return np.stack([directions_normalized[:, 1], -directions_normalized[:, 0]], axis=1)
