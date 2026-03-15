from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def get_component_bounds(vertex_coordinates: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Compute the axis-aligned bounding box from vertex coordinates.

    Parameters
    ----------
    vertex_coordinates : NDArray[np.float64]
        2D array of shape ``(n_vertices, n_dimensions)`` with vertex coordinates.

    Returns
    -------
    NDArray[np.float64]
        1D array ``[min_x, min_y, (min_z,) max_x, max_y, (max_z,)]``.
        Returns zeros if there are no vertices.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import get_component_bounds

    >>> get_component_bounds(np.array([[0., 0., 0.], [1., 2., 3.]]))
    array([0., 0., 0., 1., 2., 3.])

    >>> get_component_bounds(np.empty((0, 2)))
    array([0., 0., 0., 0.])
    """
    if len(vertex_coordinates) == 0:
        dimensions = vertex_coordinates.shape[1]
        return np.zeros(2 * dimensions, dtype=np.float64)
    return np.concatenate([vertex_coordinates.min(axis=0), vertex_coordinates.max(axis=0)])
