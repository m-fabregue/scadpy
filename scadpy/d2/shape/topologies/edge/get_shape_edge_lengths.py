from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
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

    Examples
    --------
    >>> from scadpy import get_shape_edge_lengths, square

    >>> square_shape = square(2)
    >>> get_shape_edge_lengths(square_shape)
    array([2., 2., 2., 2.])
    """
    from scadpy.core.assembly import get_assembly_edge_lengths

    return get_assembly_edge_lengths(
        edge_to_vertex=shape.edge_to_vertex,
        vertex_coordinates=shape.vertex_coordinates,
    )
