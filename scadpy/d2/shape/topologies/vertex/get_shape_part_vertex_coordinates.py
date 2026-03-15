from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from shapely.coords import CoordinateSequence
from shapely.geometry import Polygon

if TYPE_CHECKING:
    from scadpy.core.part import Part


def get_shape_part_vertex_coordinates(part: Part[Polygon]) -> NDArray[np.float64]:
    """
    For each vertex in the part, return its coordinates

    Parameters
    ----------
    part : Part[Polygon]
        The shape part to extract vertex coordinates from.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape (n_vertices, 2), one row per vertex.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import Part, get_shape_part_vertex_coordinates
    ...
    >>> polygon = Polygon(
    ...     shell=[(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)],
    ...     holes=[[(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)]]
    ... )
    >>> get_shape_part_vertex_coordinates(
    ...     Part.from_geometry(polygon)
    ... ) # doctest: +NORMALIZE_WHITESPACE
    array([[0., 0.],
           [4., 0.],
           [4., 4.],
           ...
           [3., 1.],
           [3., 3.],
           [1., 3.]])
    """

    def remove_closing_point(coordinates: CoordinateSequence) -> NDArray[np.float64]:
        array = np.array(coordinates)
        if len(array) > 1 and np.allclose(array[0], array[-1]):  # pyright: ignore[reportAny]
            return array[:-1]
        return array

    geometry = part.geometry
    exterior = remove_closing_point(geometry.exterior.coords)
    interiors = [remove_closing_point(interior.coords) for interior in geometry.interiors]
    if not interiors:
        return exterior
    return np.vstack([exterior] + interiors)
