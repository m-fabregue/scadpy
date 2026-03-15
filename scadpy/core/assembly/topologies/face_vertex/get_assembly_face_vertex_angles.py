from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def get_assembly_face_vertex_angles(
    vertex_neighborhoods: NDArray[np.int64],
    vertex_coordinates: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    For each vertex, return its interior angle in degrees.

    The angle is always positive, in the range (0°, 180°). It represents
    the turning angle at the vertex, regardless of whether the vertex is
    convex or concave. Use convexity information separately to distinguish
    the two cases.

    The angle is computed as the absolute value of the signed angle from the
    incoming edge to the outgoing edge at each vertex, using the 2D cross
    product to determine orientation.

    Parameters
    ----------
    vertex_neighborhoods : NDArray[np.int64]
        2D array of shape ``(n_vertices, 2)``. Each row is
        ``[prev_vertex, next_vertex]``.
    vertex_coordinates : NDArray[np.float64]
        2D array of shape ``(n_vertices, 2)`` with vertex coordinates.

    Returns
    -------
    NDArray[np.float64]
        1D array of shape ``(n_vertices,)``, one angle per vertex in degrees.
        All values are in the range (0°, 180°).

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import get_assembly_face_vertex_angles

    >>> # square: 4 right-angle vertices
    >>> vertex_neighborhoods = np.array(
    ...     [[3, 1], [0, 2], [1, 3], [2, 0]],
    ...     dtype=np.int64
    ... )
    >>> vertex_coordinates = np.array(
    ...     [[-1., -1.], [1., -1.], [1., 1.], [-1., 1.]]
    ... )
    >>> get_assembly_face_vertex_angles(
    ...     vertex_neighborhoods, vertex_coordinates
    ... )
    array([90., 90., 90., 90.])
    """
    if len(vertex_neighborhoods) == 0:
        return np.empty(0, dtype=np.float64)

    prev_coords = vertex_coordinates[vertex_neighborhoods[:, 0]]
    curr_coords = vertex_coordinates
    next_coords = vertex_coordinates[vertex_neighborhoods[:, 1]]

    v_in = curr_coords - prev_coords
    v_out = next_coords - curr_coords

    cross = v_in[:, 0] * v_out[:, 1] - v_in[:, 1] * v_out[:, 0]
    dot = v_in[:, 0] * v_out[:, 0] + v_in[:, 1] * v_out[:, 1]

    angles_rad = np.arctan2(cross, dot)

    return np.abs(np.degrees(angles_rad))
