from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_corner_to_incoming_directed_edge(
    shape: Shape,
) -> NDArray[np.int64]:
    """
    For each corner in the shape, return the index of its incoming directed edge.

    See :func:`get_assembly_face_corner_to_incoming_directed_edge` for full documentation.

    Examples
    --------
    >>> from scadpy import (
    ...     get_shape_corner_to_incoming_directed_edge, polygon
    ... )

    >>> # triangle: corners (2,0,1), (0,1,2), (1,2,0)
    >>> # incoming: 2→0, 0→1, 1→2
    >>> triangle = polygon([(0, 0), (1, 0), (0.5, 1)])
    >>> get_shape_corner_to_incoming_directed_edge(triangle)
    array([4, 0, 2])
    """
    from scadpy.core.assembly import get_assembly_face_corner_to_incoming_directed_edge

    return get_assembly_face_corner_to_incoming_directed_edge(
        corner_to_vertex=shape.corner_to_vertex,
        directed_edge_to_vertex=shape.directed_edge_to_vertex,
    )
