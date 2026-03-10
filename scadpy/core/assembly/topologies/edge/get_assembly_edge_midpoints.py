from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def get_assembly_edge_midpoints(
    edge_to_vertex: NDArray[np.int64],
    vertex_coordinates: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    For each edge, return the midpoint between its two vertices.

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
        2D array of shape ``(n_edges, d)``, one midpoint per edge.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy.core.assembly import get_assembly_edge_midpoints

    >>> edge_to_vertex = np.array(
    ...     [[0, 1], [1, 2], [2, 0]], dtype=np.int64
    ... )
    >>> vertex_coordinates = np.array([[0., 0.], [2., 0.], [1., 2.]])
    >>> get_assembly_edge_midpoints(
    ...     edge_to_vertex, vertex_coordinates
    ... )
    array([[1. , 0. ],
           [1.5, 1. ],
           [0.5, 1. ]])
    """
    if len(edge_to_vertex) == 0:
        d = vertex_coordinates.shape[1] if vertex_coordinates.ndim == 2 else 0
        return np.empty((0, d), dtype=np.float64)

    starts = vertex_coordinates[edge_to_vertex[:, 0]]
    ends = vertex_coordinates[edge_to_vertex[:, 1]]
    return (starts + ends) / 2
