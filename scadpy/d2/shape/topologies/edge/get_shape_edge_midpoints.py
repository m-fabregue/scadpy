from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def get_shape_edge_midpoints(
    shape: Shape,
) -> NDArray[np.float64]:
    """
    For each edge in the shape, return the midpoint between its two vertices.

    Parameters
    ----------
    shape : Shape
        The shape to extract edge midpoints from.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape ``(n_edges, 2)``, one midpoint per edge.

    """
    from scadpy.core.assembly import get_assembly_edge_midpoints

    return get_assembly_edge_midpoints(
        edge_to_vertex=shape.edge_to_vertex,
        vertex_coordinates=shape.vertex_coordinates,
    )
