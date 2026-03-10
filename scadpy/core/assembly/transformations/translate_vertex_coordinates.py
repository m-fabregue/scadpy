from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def translate_vertex_coordinates(
    vertex_coordinates: NDArray[np.float64],
    translation: float | Iterable[float],
    vertex_filter: NDArray[np.bool_] | None = None,
) -> NDArray[np.float64]:
    """
    Translate vertex coordinates by a given vector.

    Parameters
    ----------
    vertex_coordinates : NDArray[np.float64]
        2D array of shape (n_vertices, dimensions).
    translation : float | Iterable[float]
        The translation vector to apply. Its length should match the number of coordinate dimensions.
        If a single float is provided, it will be broadcast to all coordinate dimensions.
    vertex_filter : NDArray[np.bool_] | None, default=None
        Boolean array selecting which vertices are translated. If ``None``, all vertices
        are translated.

    Returns
    -------
    NDArray[np.float64]
        Array of shape (n_vertices, dimensions), one row per vertex.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import translate_vertex_coordinates, Shape

    >>> polygon1 = Polygon(
    ...     shell=[(0, 0), (2, 0), (2, 2), (0, 2)],
    ...     holes=[[(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)]]
    ... )
    >>> polygon2 = Polygon(
    ...     shell=[(10, 10), (12, 10), (12, 12), (10, 12)]
    ... )
    >>> shape = Shape.from_geometries([polygon1, polygon2])
    >>> translate_vertex_coordinates(
    ...     shape.vertex_coordinates,
    ...     translation=[10, 20]
    ... ) # doctest: +NORMALIZE_WHITESPACE
    array([[10. , 20. ],
           [12. , 20. ],
           [12. , 22. ],
           ...
           [22. , 30. ],
           [22. , 32. ],
           [20. , 32. ]])
    """
    from scadpy import resolve_vector

    dimensions: int = vertex_coordinates.shape[1]
    translation_array = np.array(resolve_vector(translation, 0, dimensions))

    if vertex_filter is None:
        return vertex_coordinates + translation_array

    result = np.array(vertex_coordinates)
    result[vertex_filter] += translation_array
    return result
