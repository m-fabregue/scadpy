from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from numpy.typing import NDArray


def pull_vertex_coordinates(
    vertex_coordinates: NDArray[np.float64],
    distance: float,
    pivot: float | Iterable[float] = 0,
    vertex_filter: NDArray[np.bool_] | None = None,
) -> NDArray[np.float64]:
    """
    Move selected vertices toward a pivot point by at most ``distance`` units.

    Each selected vertex is translated in the direction of the pivot by at most
    ``distance``. Vertices already closer than ``distance`` to the pivot are moved
    exactly to the pivot.

    Parameters
    ----------
    vertex_coordinates : NDArray[np.float64]
        2D array of shape (n_vertices, dimensions).
    distance : float
        The maximum distance each vertex is moved toward the pivot.
    pivot : float | Iterable[float], default=0
        The point vertices are pulled toward. If a single float is provided,
        it is broadcast to all coordinate dimensions. Defaults to the origin.
    vertex_filter : NDArray[np.bool_] | None, default=None
        Boolean array selecting which vertices are moved. If ``None``, all
        vertices are moved.

    Returns
    -------
    NDArray[np.float64]
        Array of shape (n_vertices, dimensions), one row per vertex.

    See Also
    --------
    push_vertex_coordinates : Move vertices away from a pivot point.
    """
    from scadpy import resolve_vector

    dimensions: int = vertex_coordinates.shape[1]
    pivot_array = resolve_vector(pivot, 0, dimensions)

    coords = vertex_coordinates if vertex_filter is None else vertex_coordinates[vertex_filter]
    vectors = pivot_array - coords
    lengths = np.linalg.norm(vectors, axis=1, keepdims=True)
    directions = np.divide(
        vectors, lengths, out=np.zeros_like(vectors), where=lengths != 0
    )
    translations = directions * np.minimum(distance, lengths)

    if vertex_filter is None:
        return vertex_coordinates + translations

    result = np.array(vertex_coordinates)
    result[vertex_filter] += translations
    return result
