from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.core.part import Part


# @typechecked is intentionally omitted: typeguard v4 cannot validate Callable types
# that contain generic type variables (e.g. Part[G]) at runtime.
def get_assembly_vertex_coordinates[G](
    parts: Sequence[Part[G]],
    get_part_vertex_coordinates: Callable[[Part[G]], NDArray[np.float64]],
    dimensions: int,
) -> NDArray[np.float64]:
    """
    For each vertex in the assembly, return its coordinates.

    Parameters
    ----------
    parts : Sequence[Part[G]]
        The parts of the assembly.
    get_part_vertex_coordinates : Callable[[Part[G]], NDArray[np.float64]]
        Function that extracts vertex coordinates from a single part.
    dimensions : int
        Number of spatial dimensions (used when ``parts`` is empty).

    Returns
    -------
    NDArray[np.float64]
        2D array of shape (n_vertices, dimensions), one row per vertex.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import (
    ...     get_assembly_vertex_coordinates,
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
    >>> get_assembly_vertex_coordinates(
    ...     shape._parts,
    ...     get_shape_part_vertex_coordinates,
    ...     2,
    ... ) # doctest: +NORMALIZE_WHITESPACE
    array([[ 0. ,  0. ],
           [ 2. ,  0. ],
           [ 2. ,  2. ],
           ...
           [12. , 10. ],
           [12. , 12. ],
           [10. , 12. ]])
    """
    if not parts:
        return np.empty((0, dimensions), dtype=np.float64)

    return np.vstack([get_part_vertex_coordinates(p) for p in parts])
