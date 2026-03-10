from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
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

    Examples
    --------
    >>> from scadpy import cuboid, get_solid_vertex_coordinates

    >>> vertex_coordinates = get_solid_vertex_coordinates(cuboid(2))
    >>> vertex_coordinates.shape
    (8, 3)
    """
    from scadpy import get_assembly_vertex_coordinates

    return get_assembly_vertex_coordinates(
        solid._parts, lambda p: p.geometry.vertices, 3
    )
