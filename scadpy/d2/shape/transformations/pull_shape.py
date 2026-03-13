from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from typeguard import typechecked


if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
def pull_shape(
    shape: Shape,
    distance: float,
    pivot: float | Iterable[float] = 0,
    vertex_filter: TopologyFilter[Shape] | None = None,
) -> Shape:
    """Move a subset of shape vertices toward a pivot point by a given distance.

    Each selected vertex is translated toward the pivot by at most ``distance`` units.
    Vertices already closer than ``distance`` to the pivot are moved to the pivot.

    Parameters
    ----------
    shape : Shape
        The shape whose vertices will be pulled.
    distance : float
        The maximum distance each vertex is moved toward the pivot.
    pivot : float | Iterable[float], default=0
        The attraction point. If a single float is provided, it is broadcast
        to all coordinate dimensions. Defaults to the origin.
    vertex_filter : TopologyFilter[Shape] | None, default=None
        A boolean array or callable selecting which vertices are affected. If ``None``,
        all vertices are moved.

    Returns
    -------
    Shape
        A new shape with the selected vertices moved toward the pivot.

    See Also
    --------
    push_shape : Move shape vertices away from a pivot point.
    """
    from scadpy import resolve_topology_filter, pull_vertex_coordinates

    resolved_vertex_filter = resolve_topology_filter(shape, len(shape.vertex_coordinates), vertex_filter)
    return shape.recoordinate(
        pull_vertex_coordinates(shape.vertex_coordinates, distance, pivot, resolved_vertex_filter)
    )
