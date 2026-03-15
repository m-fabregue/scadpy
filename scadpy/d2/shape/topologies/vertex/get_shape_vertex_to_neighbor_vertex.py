from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def get_shape_vertex_to_neighbor_vertex(
    shape: Shape,
) -> NDArray[np.int64]:
    """
    For each vertex in the shape, return its two neighbor vertex indices (prev, next).

    A vertex neighborhood is defined by three consecutive vertices on a ring. Each ring
    of ``n`` vertices yields ``n`` neighborhoods (the ring is treated as cyclic).
    The current vertex index equals the row index, so it is not included.

    Parameters
    ----------
    shape : Shape
        The shape to extract vertex neighbor indices from.

    Returns
    -------
    NDArray[np.int64]
        2D array of shape (n_vertices, 2). Each row contains the indices
        ``[prev, next]`` into the shape's global vertex array.

    """
    vertex_to_ring = shape.vertex_to_ring

    if len(vertex_to_ring) == 0:
        return np.empty((0, 2), dtype=np.int64)

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

    return np.stack([prev_indices, next_indices], axis=1)
