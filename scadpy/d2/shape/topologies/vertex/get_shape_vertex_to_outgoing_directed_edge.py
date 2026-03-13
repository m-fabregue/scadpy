from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_vertex_to_outgoing_directed_edge(
    shape: Shape,
) -> NDArray[np.int64]:
    """
    For each vertex in the shape, return the index of its outgoing directed edge.

    See :func:`get_assembly_face_vertex_to_outgoing_directed_edge` for full documentation.

    """
    from scadpy.core.assembly import get_assembly_face_vertex_to_outgoing_directed_edge

    return get_assembly_face_vertex_to_outgoing_directed_edge(
        vertex_neighborhoods=shape.vertex_to_neighbor_vertex,
        directed_edge_to_vertex=shape.directed_edge_to_vertex,
    )
