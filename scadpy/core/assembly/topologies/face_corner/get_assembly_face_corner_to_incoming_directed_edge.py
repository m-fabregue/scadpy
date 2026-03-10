from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def get_assembly_face_corner_to_incoming_directed_edge(
    corner_to_vertex: NDArray[np.int64],
    directed_edge_to_vertex: NDArray[np.int64],
) -> NDArray[np.int64]:
    """
    For each corner, return the index of its incoming directed edge.

    The incoming directed edge of corner ``(prev, curr, next)`` is
    ``prev → curr``.

    Parameters
    ----------
    corner_to_vertex : NDArray[np.int64]
        2D array of shape ``(n_corners, 3)``. Each row is
        ``[prev_vertex, curr_vertex, next_vertex]``.
    directed_edge_to_vertex : NDArray[np.int64]
        2D array of shape ``(n_directed_edges, 2)``. Each row is
        ``[start_vertex, end_vertex]``.

    Returns
    -------
    NDArray[np.int64]
        1D array of shape ``(n_corners,)``. Each entry is the index of
        the incoming directed edge for that corner.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import (
    ...     get_assembly_face_corner_to_incoming_directed_edge,
    ... )

    >>> # triangle: directed edges
    >>> # [0→1]=0, [1→0]=1, [1→2]=2, [2→1]=3, [2→0]=4, [0→2]=5
    >>> directed_edge_to_vertex = np.array(
    ...     [[0, 1], [1, 0], [1, 2], [2, 1], [2, 0], [0, 2]],
    ...     dtype=np.int64,
    ... )
    >>> # corners: (2,0,1), (0,1,2), (1,2,0)
    >>> # incoming: 2→0, 0→1, 1→2
    >>> corner_to_vertex = np.array(
    ...     [[2, 0, 1], [0, 1, 2], [1, 2, 0]], dtype=np.int64
    ... )
    >>> get_assembly_face_corner_to_incoming_directed_edge(
    ...     corner_to_vertex, directed_edge_to_vertex
    ... )
    array([4, 0, 2])
    """
    if len(corner_to_vertex) == 0:
        return np.empty(0, dtype=np.int64)

    from scadpy.core.assembly.utils import lookup_pairs

    return lookup_pairs(
        queries=corner_to_vertex[:, 0:2],
        haystack=directed_edge_to_vertex,
    )
