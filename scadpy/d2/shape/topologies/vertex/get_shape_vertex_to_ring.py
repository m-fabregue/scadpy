from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_vertex_to_ring(
    shape: Shape,
) -> NDArray[np.int64]:
    """
    For each vertex in the shape, return the index of the ring (exterior or interior) it belongs to.

    Parameters
    ----------
    shape : Shape
        The shape to extract vertex ring indices from.

    Returns
    -------
    NDArray[np.float64]
        1D array of shape (n_vertices,), one element per vertex.

    """
    # extract and flatmap polygon rings
    rings = [
        ring
        for g in map(lambda p: p.geometry, shape._parts)  # pyright: ignore[reportPrivateUsage]
        for ring in (g.exterior, *g.interiors)
    ]
    # no ring found
    if not rings:
        return np.array([], dtype=np.int64)

    ring_indices = np.concatenate(
        [np.full(len(ring.coords) - 1, i, dtype=np.int64) for i, ring in enumerate(rings)]
    )
    return np.array(ring_indices, dtype=np.int64)
