from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.core.part import Part


def get_assembly_vertex_to_part[G](
    parts: Sequence[Part[G]],
    get_part_vertex_coordinates: Callable[[Part[G]], NDArray[np.float64]],
) -> NDArray[np.int64]:
    """
    For each vertex in the assembly, return its part index.

    Parameters
    ----------
    parts : Sequence[Part[G]]
        The parts of the assembly.
    get_part_vertex_coordinates : Callable[[Part[G]], NDArray[np.float64]]
        Function that extracts vertex coordinates from a single part.

    Returns
    -------
    NDArray[np.int64]
        1D array of shape (n_vertices,), one element per vertex.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import (
    ...     get_assembly_vertex_to_part,
    ...     get_shape_part_vertex_coordinates,
    ...     Shape,
    ... )

    >>> polygon1 = Polygon(
    ...     shell=[(0, 0), (2, 0), (2, 2), (0, 2)],
    ...     holes=[[(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)]]
    ... )
    >>> polygon2 = Polygon(
    ...     shell=[(10, 10), (12, 10), (12, 12), (10, 12)]
    ... )
    >>> shape = Shape.from_geometries([polygon1, polygon2])
    >>> get_assembly_vertex_to_part(
    ...     shape._parts,
    ...     get_shape_part_vertex_coordinates,
    ... ) # doctest: +NORMALIZE_WHITESPACE
    array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
    """
    if not parts:
        return np.array([], dtype=np.int64)
    return np.concatenate([
        np.full(len(get_part_vertex_coordinates(p)), i, dtype=np.int64)
        for i, p in enumerate(parts)
    ])
