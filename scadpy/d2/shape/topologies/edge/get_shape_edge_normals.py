from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_edge_normals(
    shape: Shape,
) -> NDArray[np.float64]:
    """
    For each edge in the shape, return its outward unit normal.

    See :func:`get_assembly_edge_normals` for full documentation.

    """
    from scadpy.core.assembly import get_assembly_edge_normals

    return get_assembly_edge_normals(
        edge_to_vertex=shape.edge_to_vertex,
        vertex_coordinates=shape.vertex_coordinates,
    )
