from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def get_assembly_face_directed_edge_to_corner(
    corner_to_outgoing_directed_edge: NDArray[np.int64],
    corner_to_incoming_directed_edge: NDArray[np.int64],
) -> NDArray[np.int64]:
    """
    For each directed edge, return the indices of its source and target corners.

    The source corner of a directed edge ``curr → next`` is the corner
    ``(prev, curr, next)`` — the one that *emits* the directed edge as outgoing.
    The target corner is the corner ``(curr, next, next_next)`` — the one that
    *receives* it as incoming.

    Parameters
    ----------
    corner_to_outgoing_directed_edge : NDArray[np.int64]
        1D array of shape ``(n_corners,)``. Each entry is the index of the
        outgoing directed edge for that corner.
    corner_to_incoming_directed_edge : NDArray[np.int64]
        1D array of shape ``(n_corners,)``. Each entry is the index of the
        incoming directed edge for that corner.

    Returns
    -------
    NDArray[np.int64]
        2D array of shape ``(n_directed_edges, 2)``. Each row is
        ``[source_corner, target_corner]``. Column 0 is the corner that emits
        the directed edge (outgoing), column 1 is the corner that receives it
        (incoming).

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import get_assembly_face_directed_edge_to_corner

    >>> # triangle: 3 corners, 3 edges → 6 directed edges
    >>> # corners: (2,0,1)=0, (0,1,2)=1, (1,2,0)=2
    >>> # outgoing: corner 0 → de 0 (0→1),
    >>> #           corner 1 → de 2 (1→2), corner 2 → de 4 (2→0)
    >>> # incoming: corner 0 → de 4 (2→0),
    >>> #           corner 1 → de 0 (0→1), corner 2 → de 2 (1→2)
    >>> corner_to_outgoing = np.array([0, 2, 4], dtype=np.int64)
    >>> corner_to_incoming = np.array([4, 0, 2], dtype=np.int64)
    >>> get_assembly_face_directed_edge_to_corner(
    ...     corner_to_outgoing, corner_to_incoming
    ... )
    array([[0, 1],
           [1, 0],
           [1, 2],
           [2, 1],
           [2, 0],
           [0, 2]])
    """
    if len(corner_to_outgoing_directed_edge) == 0:
        return np.empty((0, 2), dtype=np.int64)

    n_corners = len(corner_to_outgoing_directed_edge)
    n_directed_edges = n_corners * 2
    source_corner = np.empty(n_directed_edges, dtype=np.int64)
    target_corner = np.empty(n_directed_edges, dtype=np.int64)

    corner_indices = np.arange(n_corners, dtype=np.int64)

    # Forward directed edges: source = corner that emits (outgoing), target = corner that receives (incoming)
    source_corner[corner_to_outgoing_directed_edge] = corner_indices
    target_corner[corner_to_incoming_directed_edge] = corner_indices

    # Backward directed edges (index ^ 1): source/target are swapped vs forward
    source_corner[corner_to_outgoing_directed_edge ^ 1] = target_corner[corner_to_outgoing_directed_edge]
    target_corner[corner_to_outgoing_directed_edge ^ 1] = corner_indices

    return np.stack([source_corner, target_corner], axis=1)
