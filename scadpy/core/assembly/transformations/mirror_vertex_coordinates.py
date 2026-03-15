from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from numpy.typing import NDArray


def mirror_vertex_coordinates(
    vertex_coordinates: NDArray[np.float64],
    normal: float | Iterable[float],
    pivot: float | Iterable[float] = 0,
) -> NDArray[np.float64]:
    """
    Mirror vertex coordinates across a line (2D) or plane (3D) defined by a normal vector and a pivot point.

    Parameters
    ----------
    vertex_coordinates : NDArray[np.float64]
        2D array of shape (n_vertices, dimensions).
    normal : float | Iterable[float]
        The normal vector of the mirror line (2D) or plane (3D). Does not need to be normalized.
        If a single float is provided, it will be broadcast to all coordinate dimensions.
    pivot : float | Iterable[float], default=0
        The point through which the mirror line/plane passes. If a single float is provided, it will be broadcast to all coordinate dimensions.
        Defaults to 0 (the origin).

    Returns
    -------
    NDArray[np.float64]
        Array of shape (n_vertices, dimensions), one row per vertex.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import mirror_vertex_coordinates, Shape

    >>> polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    >>> shape = Shape.from_geometries([polygon])
    >>> mirror_vertex_coordinates(
    ...     shape.vertex_coordinates,
    ...     normal=[1, 0],  # Mirror across y-axis
    ...     pivot=[1, 0]
    ... ) # doctest: +NORMALIZE_WHITESPACE
    array([[2., 0.],
           [0., 0.],
           [0., 2.],
           [2., 2.]])
    """
    from scadpy import resolve_vector

    dimensions: int = vertex_coordinates.shape[1]

    normal = resolve_vector(normal, 0, dimensions)
    pivot = resolve_vector(pivot, 0, dimensions)

    normal = normal / np.linalg.norm(normal)

    # vector from pivot to each vertex
    v = vertex_coordinates - pivot
    # project v onto normal
    projection = np.dot(v, normal)
    # reflection formula
    mirrored = vertex_coordinates - 2 * projection[:, np.newaxis] * normal

    return mirrored
