from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def get_assembly_edge_lengths(
    edge_to_vertex: NDArray[np.int64],
    vertex_coordinates: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    For each edge, return the Euclidean distance between its two vertices.

    Parameters
    ----------
    edge_to_vertex : NDArray[np.int64]
        2D array of shape ``(n_edges, 2)`` mapping each edge to its
        ``[start_vertex, end_vertex]`` indices.
    vertex_coordinates : NDArray[np.float64]
        2D array of shape ``(n_vertices, d)`` with vertex coordinates.

    Returns
    -------
    NDArray[np.float64]
        1D array of shape ``(n_edges,)``, one length per edge.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy.core.assembly import get_assembly_edge_lengths

    >>> edge_to_vertex = np.array(
    ...     [[0, 1], [1, 2], [2, 0]], dtype=np.int64
    ... )
    >>> vertex_coordinates = np.array([[0., 0.], [3., 0.], [0., 4.]])
    >>> get_assembly_edge_lengths(edge_to_vertex, vertex_coordinates)
    array([3., 5., 4.])
    """
    if len(edge_to_vertex) == 0:
        return np.empty(0, dtype=np.float64)

    starts = vertex_coordinates[edge_to_vertex[:, 0]]
    ends = vertex_coordinates[edge_to_vertex[:, 1]]
    return np.linalg.norm(ends - starts, axis=1)
