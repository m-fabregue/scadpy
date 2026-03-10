from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def rotate_vertex_coordinates(
    vertex_coordinates: NDArray[np.float64],
    rotation_matrix: NDArray[np.float64],
    pivot: float | Iterable[float] = 0,
    vertex_filter: NDArray[np.bool_] | None = None,
) -> NDArray[np.float64]:
    """
    Rotate vertex coordinates using a precomputed rotation matrix and a pivot point.

    Parameters
    ----------
    vertex_coordinates : NDArray[np.float64]
        2D array of shape (n_vertices, dimensions).
    rotation_matrix : NDArray[np.float64]
        Square rotation matrix of shape (dimensions, dimensions).
    pivot : float | Iterable[float], default=0
        The point around which rotation is applied. If a single float is provided,
        it will be broadcast to all coordinate dimensions. Defaults to the origin.
    vertex_filter : NDArray[np.bool_] | None, default=None
        Boolean array selecting which vertices are rotated. If ``None``, all vertices
        are rotated.

    Returns
    -------
    NDArray[np.float64]
        Array of shape (n_vertices, dimensions), one row per vertex.

    Examples
    --------
    >>> import numpy as np
    >>> from shapely.geometry import Polygon
    >>> from scadpy import rotate_vertex_coordinates, Shape

    >>> polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    >>> shape = Shape.from_geometries([polygon])
    >>> angle = np.deg2rad(90)
    >>> R = np.array([
    ...     [np.cos(angle), -np.sin(angle)],
    ...     [np.sin(angle), np.cos(angle)],
    ... ])
    >>> rotate_vertex_coordinates(
    ...     shape.vertex_coordinates,
    ...     R,
    ...     pivot=[1, 1],
    ... ).round(10) # doctest: +NORMALIZE_WHITESPACE
    array([[2., 0.],
           [2., 2.],
           [0., 2.],
           [0., 0.]])
    """
    from scadpy import resolve_vector

    dimensions: int = vertex_coordinates.shape[1]
    pivot_array = np.array(resolve_vector(pivot, 0, dimensions))

    if vertex_filter is None:
        return (vertex_coordinates - pivot_array) @ rotation_matrix.T + pivot_array

    result = np.array(vertex_coordinates)
    result[vertex_filter] = (
        (vertex_coordinates[vertex_filter] - pivot_array) @ rotation_matrix.T + pivot_array
    )
    return result
