from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_edge_to_vertex(
    shape: Shape,
) -> NDArray[np.int64]:
    """
    For each edge in the shape, return the indices of its start and end vertices.

    An edge connects two consecutive vertices within a ring. Edges are directed
    implicitly by the ring winding order (CCW for exterior rings, CW for interior
    rings in Shapely convention).

    Parameters
    ----------
    shape : Shape
        The shape to extract edge-to-vertex indices from.

    Returns
    -------
    NDArray[np.int64]
        2D array of shape ``(n_edges, 2)``. Each row is ``[start_vertex, end_vertex]``.
        The number of edges equals the number of vertices (one edge per vertex,
        since each ring is closed).

    """
    rings = [
        ring
        for g in map(lambda p: p.geometry, shape._parts)  # pyright: ignore[reportPrivateUsage]
        for ring in (g.exterior, *g.interiors)
    ]
    if not rings:
        return np.empty((0, 2), dtype=np.int64)

    # Build edge_to_vertex: for each ring, consecutive vertex pairs (wrapping around)
    edge_rows: list[NDArray[np.int64]] = []
    offset = 0
    for ring in rings:
        n = len(ring.coords) - 1  # exclude closing duplicate
        local_indices = np.arange(n, dtype=np.int64)
        starts = offset + local_indices
        ends = offset + (local_indices + 1) % n
        edge_rows.append(np.stack([starts, ends], axis=1))
        offset += n

    return np.concatenate(edge_rows, axis=0)
