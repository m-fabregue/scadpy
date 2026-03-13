from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from typeguard import typechecked


if TYPE_CHECKING:
    from scadpy import Solid, TopologyFilter


@typechecked
def push_solid(
    solid: Solid,
    distance: float,
    pivot: float | Iterable[float] = 0,
    vertex_filter: TopologyFilter[Solid] | None = None,
) -> Solid:
    """Move a subset of solid vertices away from a pivot point by a given distance.

    Each selected vertex is translated away from the pivot by exactly ``distance`` units.
    Vertices located exactly at the pivot are not moved (undefined direction).

    Parameters
    ----------
    solid : Solid
        The solid whose vertices will be pushed.
    distance : float
        The distance each vertex is moved away from the pivot.
    pivot : float | Iterable[float], default=0
        The repulsion point. If a single float is provided, it is broadcast
        to all coordinate dimensions. Defaults to the origin.
    vertex_filter : TopologyFilter[Solid] | None, default=None
        A boolean array or callable selecting which vertices are affected. If ``None``,
        all vertices are moved.

    Returns
    -------
    Solid
        A new solid with the selected vertices moved away from the pivot.

    See Also
    --------
    pull_solid : Move solid vertices toward a pivot point.
    """
    from scadpy import resolve_topology_filter, push_vertex_coordinates

    resolved_vertex_filter = resolve_topology_filter(solid, len(solid.vertex_coordinates), vertex_filter)
    return solid.recoordinate(
        push_vertex_coordinates(solid.vertex_coordinates, distance, pivot, resolved_vertex_filter)
    )
