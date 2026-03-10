from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_corner_to_vertex(
    shape: Shape,
) -> NDArray[np.int64]:
    """
    For each corner in the shape, return its three vertex indices (prev, curr, next).

    A corner is defined by three consecutive vertices on a ring. Each ring of ``n``
    vertices yields ``n`` corners (the ring is treated as cyclic).

    Parameters
    ----------
    shape : Shape
        The shape to extract corner vertex indices from.

    Returns
    -------
    NDArray[np.int64]
        2D array of shape (n_corners, 3). Each row contains the indices
        ``[prev, curr, next]`` into the shape's global vertex array.

    Examples
    --------
    >>> from scadpy import get_shape_corner_to_vertex, polygon

    >>> triangle = polygon([(0, 0), (1, 0), (0.5, 1)])
    >>> get_shape_corner_to_vertex(  # doctest: +NORMALIZE_WHITESPACE
    ...     triangle
    ... )
    array([[2, 0, 1],
           [0, 1, 2],
           [1, 2, 0]])
    """
    vertex_to_ring = shape.vertex_to_ring

    if len(vertex_to_ring) == 0:
        return np.empty((0, 3), dtype=np.int64)

    indices = np.arange(len(vertex_to_ring), dtype=np.int64)

    # for each vertex, prev and next are within the same ring (cyclic)
    # shift by +1 and -1 within each ring using modular arithmetic per ring
    ring_starts = np.searchsorted(vertex_to_ring, np.arange(vertex_to_ring[-1] + 1))
    ring_sizes = np.diff(np.append(ring_starts, len(vertex_to_ring)))

    # offset of each vertex within its ring
    offsets = indices - ring_starts[vertex_to_ring]
    ring_size_per_vertex = ring_sizes[vertex_to_ring]

    prev_indices = ring_starts[vertex_to_ring] + (offsets - 1) % ring_size_per_vertex
    next_indices = ring_starts[vertex_to_ring] + (offsets + 1) % ring_size_per_vertex

    return np.stack([prev_indices, indices, next_indices], axis=1)
