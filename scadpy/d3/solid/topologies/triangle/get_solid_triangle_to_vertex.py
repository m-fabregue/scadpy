from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


@typechecked
def get_solid_triangle_to_vertex(
    solid: Solid,
) -> NDArray[np.int64]:
    """For each triangle in the solid, return the indices of its three vertices.

    Parameters
    ----------
    solid : Solid
        The solid to extract triangle-to-vertex mapping from.

    Returns
    -------
    NDArray[np.int64]
        2D array of shape (n_triangles, 3), one row per triangle containing
        the global vertex indices of its three corners.

    Examples
    --------
    >>> from scadpy import cuboid, get_solid_triangle_to_vertex

    >>> triangle_to_vertex = get_solid_triangle_to_vertex(cuboid(2))
    >>> triangle_to_vertex.shape[1]
    3
    """
    if not solid._parts:
        return np.empty((0, 3), dtype=np.int64)

    part_vertex_counts = [len(part.geometry.vertices) for part in solid._parts]
    offsets = np.concatenate([[0], np.cumsum(part_vertex_counts[:-1])])

    return np.concatenate(
        [
            (part.geometry.faces + offset).astype(np.int64)
            for part, offset in zip(solid._parts, offsets)
        ]
    )
