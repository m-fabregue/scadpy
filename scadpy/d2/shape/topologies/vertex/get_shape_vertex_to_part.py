from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def get_shape_vertex_to_part(shape: Shape) -> NDArray[np.int64]:
    """
    For each vertex in the shape, return its part index.

    Parameters
    ----------
    shape : Shape
        The shape to extract part indices from.

    Returns
    -------
    NDArray[np.int64]
        1D array of shape (n_vertices,), one element per vertex.

    """
    from scadpy import get_assembly_vertex_to_part, get_shape_part_vertex_coordinates

    return get_assembly_vertex_to_part(shape._parts, get_shape_part_vertex_coordinates)
