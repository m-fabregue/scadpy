from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy import Solid


def get_solid_vertex_coordinates(solid: Solid) -> NDArray[np.float64]:
    """For each vertex in the solid, return its coordinates.

    Parameters
    ----------
    solid : Solid
        The solid to extract vertex coordinates from.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape (n_vertices, 3), one row per vertex.
    """
    from scadpy import get_assembly_vertex_coordinates

    return get_assembly_vertex_coordinates(
        solid._parts, lambda p: p.geometry.vertices, 3
    )
