from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Solid, TopologyFilter


def scale_solid(
    solid: Solid,
    scale: float | Iterable[float],
    pivot: float | Iterable[float] = 0,
    vertex_filter: TopologyFilter[Solid] | None = None,
) -> Solid:
    """Scale a solid by a given factor, relative to a pivot point.

    Parameters
    ----------
    solid : Solid
        The solid to scale.
    scale : float | Iterable[float]
        The scaling factor(s). If a single float is provided, it is broadcast
        to all coordinate dimensions.
    pivot : float | Iterable[float], default=0
        The point relative to which scaling is performed. If a single float is
        provided, it is broadcast to all coordinate dimensions. Defaults to the origin.
    vertex_filter : TopologyFilter[Solid] | None, default=None
        Boolean array or callable selecting which vertices are scaled. If ``None``, all
        vertices are scaled.

    Returns
    -------
    Solid
        A new solid with the selected vertices scaled relative to the pivot.
    """
    from scadpy import resolve_topology_filter, scale_vertex_coordinates

    resolved_vertex_filter = resolve_topology_filter(solid, len(solid.vertex_coordinates), vertex_filter)
    return solid.recoordinate(
        scale_vertex_coordinates(solid.vertex_coordinates, scale, pivot, resolved_vertex_filter)
    )
