from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy import Shape


def get_shape_vertex_coordinates(shape: Shape) -> NDArray[np.float64]:
    """
    For each vertex in the shape, return its coordinates.

    Parameters
    ----------
    shape : Shape
        The shape to extract vertex coordinates from.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape (n_vertices, 2), one row per vertex.

    """
    from scadpy import get_assembly_vertex_coordinates, get_shape_part_vertex_coordinates

    return get_assembly_vertex_coordinates(shape._parts, get_shape_part_vertex_coordinates, 2)
