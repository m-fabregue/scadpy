from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def get_assembly_face_corner_angles(
    corner_to_vertex: NDArray[np.int64],
    vertex_coordinates: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    For each corner, return its interior angle in degrees.

    The angle is always positive, in the range (0°, 180°). It represents
    the turning angle at the corner, regardless of whether the corner is
    convex or concave. Use convexity information separately to distinguish
    the two cases.

    The angle is computed as the absolute value of the signed angle from the
    incoming edge to the outgoing edge at each corner, using the 2D cross
    product to determine orientation.

    Parameters
    ----------
    corner_to_vertex : NDArray[np.int64]
        2D array of shape ``(n_corners, 3)``. Each row is
        ``[prev_vertex, curr_vertex, next_vertex]``.
    vertex_coordinates : NDArray[np.float64]
        2D array of shape ``(n_vertices, 2)`` with vertex coordinates.

    Returns
    -------
    NDArray[np.float64]
        1D array of shape ``(n_corners,)``, one angle per corner in degrees.
        All values are in the range (0°, 180°).

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import get_assembly_face_corner_angles

    >>> # square: 4 right-angle corners
    >>> corner_to_vertex = np.array(
    ...     [[3, 0, 1], [0, 1, 2], [1, 2, 3], [2, 3, 0]],
    ...     dtype=np.int64
    ... )
    >>> vertex_coordinates = np.array(
    ...     [[-1., -1.], [1., -1.], [1., 1.], [-1., 1.]]
    ... )
    >>> get_assembly_face_corner_angles(
    ...     corner_to_vertex, vertex_coordinates
    ... )
    array([90., 90., 90., 90.])
    """
    if len(corner_to_vertex) == 0:
        return np.empty(0, dtype=np.float64)

    prev_coords = vertex_coordinates[corner_to_vertex[:, 0]]
    curr_coords = vertex_coordinates[corner_to_vertex[:, 1]]
    next_coords = vertex_coordinates[corner_to_vertex[:, 2]]

    v_in = curr_coords - prev_coords
    v_out = next_coords - curr_coords

    cross = v_in[:, 0] * v_out[:, 1] - v_in[:, 1] * v_out[:, 0]
    dot = v_in[:, 0] * v_out[:, 0] + v_in[:, 1] * v_out[:, 1]

    angles_rad = np.arctan2(cross, dot)

    return np.abs(np.degrees(angles_rad))
