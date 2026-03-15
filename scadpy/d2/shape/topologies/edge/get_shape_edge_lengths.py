from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def get_shape_edge_lengths(
    shape: Shape,
) -> NDArray[np.float64]:
    """
    For each edge in the shape, return its length.

    Parameters
    ----------
    shape : Shape
        The shape to extract edge lengths from.

    Returns
    -------
    NDArray[np.float64]
        1D array of shape ``(n_edges,)``, one length per edge.

    """
    from scadpy.core.assembly import get_assembly_edge_lengths

    return get_assembly_edge_lengths(
        edge_to_vertex=shape.edge_to_vertex,
        vertex_coordinates=shape.vertex_coordinates,
    )
