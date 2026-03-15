from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def get_shape_directed_edge_directions(
    shape: Shape,
) -> NDArray[np.float64]:
    """
    For each directed edge in the shape, return its unit direction vector.

    See :func:`get_assembly_directed_edge_directions` for full documentation.

    """
    from scadpy.core.assembly import get_assembly_directed_edge_directions

    return get_assembly_directed_edge_directions(
        directed_edge_to_vertex=shape.directed_edge_to_vertex,
        vertex_coordinates=shape.vertex_coordinates,
    )
