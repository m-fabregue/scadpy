from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape



def get_shape_directed_edge_to_vertex(
    shape: Shape,
) -> NDArray[np.int64]:
    """
    For each directed edge in the shape, return the indices of its start and end vertices.

    Each undirected edge ``i`` gives rise to two directed edges, interleaved:

    - ``directed_edge 2i``   : forward  → ``[start, end]`` (ring winding order)
    - ``directed_edge 2i+1`` : backward → ``[end, start]``

    Parameters
    ----------
    shape : Shape
        The shape to extract directed edge-to-vertex indices from.

    Returns
    -------
    NDArray[np.int64]
        2D array of shape ``(2 * n_edges, 2)``. Each row is
        ``[start_vertex, end_vertex]`` for the directed edge.

    """
    from scadpy.core.assembly import get_assembly_directed_edge_to_vertex

    return get_assembly_directed_edge_to_vertex(
        edge_to_vertex=shape.edge_to_vertex,
    )
