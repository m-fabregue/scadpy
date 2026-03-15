from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def get_assembly_directed_edge_to_edge(
    n_edges: int,
) -> NDArray[np.int64]:
    """
    For each directed edge, return the index of its parent undirected edge.

    Since directed edges are interleaved (``directed_edge 2i`` and
    ``directed_edge 2i+1`` both belong to ``edge i``), the mapping is:

    .. code-block:: text

        edge index = directed_edge index // 2

    Parameters
    ----------
    n_edges : int
        Number of undirected edges.

    Returns
    -------
    NDArray[np.int64]
        1D array of shape ``(2 * n_edges,)``. Each entry is the index of
        the parent undirected edge.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import get_assembly_directed_edge_to_edge

    >>> # triangle: 3 edges → 6 directed edges
    >>> get_assembly_directed_edge_to_edge(3)
    array([0, 0, 1, 1, 2, 2])

    >>> # square: 4 edges → 8 directed edges
    >>> get_assembly_directed_edge_to_edge(4)
    array([0, 0, 1, 1, 2, 2, 3, 3])
    """
    if n_edges == 0:
        return np.empty(0, dtype=np.int64)

    return np.arange(n_edges, dtype=np.int64).repeat(2)
