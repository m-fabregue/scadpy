from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
def get_solid_vertex_to_part(solid: Solid) -> NDArray[np.int64]:
    """For each vertex in the solid, return its part index.

    Parameters
    ----------
    solid : Solid
        The solid to extract part indices from.

    Returns
    -------
    NDArray[np.int64]
        1D array of shape (n_vertices,), one element per vertex.

    Examples
    --------
    >>> from scadpy import cuboid, get_solid_vertex_to_part

    >>> solid = cuboid(2) + cuboid(2).translate(5)
    >>> get_solid_vertex_to_part(solid)
    array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])
    """
    from scadpy import get_assembly_vertex_to_part

    return get_assembly_vertex_to_part(solid._parts, lambda p: p.geometry.vertices)
