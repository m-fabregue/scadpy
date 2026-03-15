from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def get_assembly_directed_edge_to_vertex(
    edge_to_vertex: NDArray[np.int64],
) -> NDArray[np.int64]:
    """
    For each directed edge, return the indices of its start and end vertices.

    Each undirected edge ``i`` gives rise to two directed edges, interleaved:

    - ``directed_edge 2i``   : forward  → ``[start, end]``
    - ``directed_edge 2i+1`` : backward → ``[end, start]``

    Parameters
    ----------
    edge_to_vertex : NDArray[np.int64]
        2D array of shape ``(n_edges, 2)`` mapping each edge to its
        ``[start_vertex, end_vertex]`` indices.

    Returns
    -------
    NDArray[np.int64]
        2D array of shape ``(2 * n_edges, 2)``. Each row is
        ``[start_vertex, end_vertex]`` for the directed edge.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import get_assembly_directed_edge_to_vertex

    >>> # triangle: 3 edges → 6 directed edges
    >>> edge_to_vertex = np.array(
    ...     [[0, 1], [1, 2], [2, 0]], dtype=np.int64
    ... )
    >>> get_assembly_directed_edge_to_vertex(edge_to_vertex)
    array([[0, 1],
           [1, 0],
           [1, 2],
           [2, 1],
           [2, 0],
           [0, 2]])
    """
    if len(edge_to_vertex) == 0:
        return np.empty((0, 2), dtype=np.int64)

    forward = edge_to_vertex
    backward = edge_to_vertex[:, ::-1]
    return np.stack([forward, backward], axis=1).reshape(-1, 2)
