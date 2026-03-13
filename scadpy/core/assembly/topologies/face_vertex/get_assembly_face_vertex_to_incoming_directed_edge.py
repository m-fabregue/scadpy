from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def get_assembly_face_vertex_to_incoming_directed_edge(
    vertex_neighborhoods: NDArray[np.int64],
    directed_edge_to_vertex: NDArray[np.int64],
) -> NDArray[np.int64]:
    """
    For each vertex, return the index of its incoming directed edge.

    The incoming directed edge of vertex neighborhood ``(prev, curr, next)`` is
    ``prev → curr``.

    Parameters
    ----------
    vertex_neighborhoods : NDArray[np.int64]
        2D array of shape ``(n_vertices, 2)``. Each row is
        ``[prev_vertex, next_vertex]``.
    directed_edge_to_vertex : NDArray[np.int64]
        2D array of shape ``(n_directed_edges, 2)``. Each row is
        ``[start_vertex, end_vertex]``.

    Returns
    -------
    NDArray[np.int64]
        1D array of shape ``(n_vertices,)``. Each entry is the index of
        the incoming directed edge for that vertex.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import (
    ...     get_assembly_face_vertex_to_incoming_directed_edge,
    ... )

    >>> # triangle: directed edges
    >>> # [0→1]=0, [1→0]=1, [1→2]=2, [2→1]=3, [2→0]=4, [0→2]=5
    >>> directed_edge_to_vertex = np.array(
    ...     [[0, 1], [1, 0], [1, 2], [2, 1], [2, 0], [0, 2]],
    ...     dtype=np.int64,
    ... )
    >>> # vertices: (2,1), (0,2), (1,0)
    >>> # incoming: 2→0, 0→1, 1→2
    >>> vertex_neighborhoods = np.array(
    ...     [[2, 1], [0, 2], [1, 0]], dtype=np.int64
    ... )
    >>> get_assembly_face_vertex_to_incoming_directed_edge(
    ...     vertex_neighborhoods, directed_edge_to_vertex
    ... )
    array([4, 0, 2])
    """
    if len(vertex_neighborhoods) == 0:
        return np.empty(0, dtype=np.int64)

    from scadpy.core.assembly.utils import lookup_pairs

    n = len(vertex_neighborhoods)
    curr = np.arange(n, dtype=np.int64)
    return lookup_pairs(
        queries=np.stack([vertex_neighborhoods[:, 0], curr], axis=1),
        haystack=directed_edge_to_vertex,
    )
