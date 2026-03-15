from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def get_assembly_directed_edge_directions(
    directed_edge_to_vertex: NDArray[np.int64],
    vertex_coordinates: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    For each directed edge, return its unit direction vector.

    The direction vector points from the start vertex to the end vertex,
    normalized to unit length.

    Parameters
    ----------
    directed_edge_to_vertex : NDArray[np.int64]
        2D array of shape ``(n_directed_edges, 2)`` mapping each directed edge
        to its ``[start_vertex, end_vertex]`` indices.
    vertex_coordinates : NDArray[np.float64]
        2D array of shape ``(n_vertices, 2)`` with vertex coordinates.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape ``(n_directed_edges, 2)``. Each row is a unit vector
        ``[dx, dy]`` pointing from start to end vertex.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import get_assembly_directed_edge_directions

    >>> # square: forward edges go right, up, left, down;
    >>> # backward edges are reversed
    >>> directed_edge_to_vertex = np.array([
    ...     [0, 1], [1, 0],
    ...     [1, 2], [2, 1],
    ...     [2, 3], [3, 2],
    ...     [3, 0], [0, 3],
    ... ], dtype=np.int64)
    >>> vertex_coordinates = np.array(
    ...     [[0., 0.], [1., 0.], [1., 1.], [0., 1.]]
    ... )
    >>> get_assembly_directed_edge_directions(
    ...     directed_edge_to_vertex, vertex_coordinates
    ... ).round(4)
    array([[ 1.,  0.],
           [-1.,  0.],
           [ 0.,  1.],
           [ 0., -1.],
           [-1.,  0.],
           [ 1.,  0.],
           [ 0., -1.],
           [ 0.,  1.]])
    """
    if len(directed_edge_to_vertex) == 0:
        d = vertex_coordinates.shape[1] if vertex_coordinates.ndim == 2 else 0
        return np.empty((0, d), dtype=np.float64)

    starts = vertex_coordinates[directed_edge_to_vertex[:, 0]]
    ends = vertex_coordinates[directed_edge_to_vertex[:, 1]]

    directions = ends - starts
    lengths = np.linalg.norm(directions, axis=1, keepdims=True)
    return directions / lengths
