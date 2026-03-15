from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from numpy.typing import NDArray


def scale_vertex_coordinates(
    vertex_coordinates: NDArray[np.float64],
    scale: float | Iterable[float],
    pivot: float | Iterable[float] = 0,
    vertex_filter: NDArray[np.bool_] | None = None,
) -> NDArray[np.float64]:
    """
    Scale vertex coordinates by a given factor or vector, relative to a pivot.

    Parameters
    ----------
    vertex_coordinates : NDArray[np.float64]
        2D array of shape (n_vertices, dimensions).
    scale : float | Iterable[float]
        The scaling factor(s) to apply. Its length should match the number of coordinate dimensions.
        If a single float is provided, it will be broadcast to all coordinate dimensions.
    pivot : float | Iterable[float], default=0
        The point relative to which scaling is performed. If a single float is provided, it will be broadcast to all coordinate dimensions.
        Defaults to 0 (the origin).
    vertex_filter : NDArray[np.bool_] | None, default=None
        Boolean array selecting which vertices are scaled. If ``None``, all vertices are scaled.

    Returns
    -------
    NDArray[np.float64]
        Array of shape (n_vertices, dimensions), one row per vertex.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import scale_vertex_coordinates, Shape

    >>> polygon1 = Polygon(
    ...     shell=[(0, 0), (2, 0), (2, 2), (0, 2)],
    ...     holes=[[(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)]]
    ... )
    >>> polygon2 = Polygon(
    ...     shell=[(10, 10), (12, 10), (12, 12), (10, 12)]
    ... )
    >>> shape = Shape.from_geometries([polygon1, polygon2])
    >>> scale_vertex_coordinates(
    ...     shape.vertex_coordinates,
    ...     scale=[10, 0.5],
    ...     pivot=[1, 2]
    ... ) # doctest: +NORMALIZE_WHITESPACE
    array([[ -9.  ,   1.  ],
           [ 11.  ,   1.  ],
           [ 11.  ,   2.  ],
           ...
           [111.  ,   6.  ],
           [111.  ,   7.  ],
           [ 91.  ,   7.  ]])
    """
    from scadpy import resolve_vector

    dimensions: int = vertex_coordinates.shape[1]

    pivot_array = np.array(resolve_vector(pivot, 0, dimensions))
    scale_array = np.array(resolve_vector(scale, 1, dimensions))

    if vertex_filter is None:
        return pivot_array + (vertex_coordinates - pivot_array) * scale_array

    result = np.array(vertex_coordinates)
    result[vertex_filter] = pivot_array + (vertex_coordinates[vertex_filter] - pivot_array) * scale_array
    return result
