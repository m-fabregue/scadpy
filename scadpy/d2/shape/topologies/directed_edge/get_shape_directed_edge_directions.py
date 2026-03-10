from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_directed_edge_directions(
    shape: Shape,
) -> NDArray[np.float64]:
    """
    For each directed edge in the shape, return its unit direction vector.

    See :func:`get_assembly_directed_edge_directions` for full documentation.

    Examples
    --------
    >>> from scadpy import get_shape_directed_edge_directions, square

    >>> # unit square: 4 edges → 8 directed edges,
    >>> # forward then backward interleaved
    >>> square_shape = square(1)
    >>> get_shape_directed_edge_directions(square_shape).round(4)
    array([[ 1.,  0.],
           [-1.,  0.],
           [ 0.,  1.],
           [ 0., -1.],
           [-1.,  0.],
           [ 1.,  0.],
           [ 0., -1.],
           [ 0.,  1.]])
    """
    from scadpy.core.assembly import get_assembly_directed_edge_directions

    return get_assembly_directed_edge_directions(
        directed_edge_to_vertex=shape.directed_edge_to_vertex,
        vertex_coordinates=shape.vertex_coordinates,
    )
