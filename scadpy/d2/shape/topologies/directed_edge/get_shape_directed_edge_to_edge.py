from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_directed_edge_to_edge(
    shape: Shape,
) -> NDArray[np.int64]:
    """
    For each directed edge in the shape, return the index of its parent undirected edge.

    Since directed edges are interleaved (``directed_edge 2i`` and
    ``directed_edge 2i+1`` both belong to ``edge i``), the mapping is:
    ``edge index = directed_edge index // 2``.

    Parameters
    ----------
    shape : Shape
        The shape to extract directed edge-to-edge indices from.

    Returns
    -------
    NDArray[np.int64]
        1D array of shape ``(2 * n_edges,)``. Each entry is the index of
        the parent undirected edge.

    """
    from scadpy.core.assembly import get_assembly_directed_edge_to_edge

    return get_assembly_directed_edge_to_edge(n_edges=len(shape.edge_to_vertex))
