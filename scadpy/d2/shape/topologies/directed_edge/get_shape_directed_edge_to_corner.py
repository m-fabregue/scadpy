from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_directed_edge_to_corner(
    shape: Shape,
) -> NDArray[np.int64]:
    """
    For each directed edge in the shape, return its source and target corner indices.

    See :func:`get_assembly_face_directed_edge_to_corner` for full documentation.

    Examples
    --------
    >>> from scadpy import get_shape_directed_edge_to_corner, polygon

    >>> # triangle: corners (2,0,1)=0, (0,1,2)=1, (1,2,0)=2
    >>> triangle = polygon([(0, 0), (1, 0), (0.5, 1)])
    >>> get_shape_directed_edge_to_corner(triangle)
    array([[0, 1],
           [1, 0],
           [1, 2],
           [2, 1],
           [2, 0],
           [0, 2]])
    """
    from scadpy.core.assembly import get_assembly_face_directed_edge_to_corner

    return get_assembly_face_directed_edge_to_corner(
        corner_to_outgoing_directed_edge=shape.corner_to_outgoing_directed_edge,
        corner_to_incoming_directed_edge=shape.corner_to_incoming_directed_edge,
    )
