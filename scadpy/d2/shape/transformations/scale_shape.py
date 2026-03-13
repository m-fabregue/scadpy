from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
def scale_shape(
    shape: Shape,
    scale: float | Iterable[float],
    pivot: float | Iterable[float] = 0,
    vertex_filter: TopologyFilter[Shape] | None = None,
) -> Shape:
    """Scale a shape by a given factor, relative to a pivot point.

    Parameters
    ----------
    shape : Shape
        The shape to scale.
    scale : float | Iterable[float]
        The scaling factor(s). If a single float is provided, it is broadcast
        to all coordinate dimensions.
    pivot : float | Iterable[float], default=0
        The point relative to which scaling is performed. If a single float is
        provided, it is broadcast to all coordinate dimensions. Defaults to the origin.
    vertex_filter : TopologyFilter[Shape] | None, default=None
        Boolean array or callable selecting which vertices are scaled. If ``None``, all
        vertices are scaled.

    Returns
    -------
    Shape
        A new shape with the selected vertices scaled relative to the pivot.
    """
    from scadpy import resolve_topology_filter, scale_vertex_coordinates

    resolved_vertex_filter = resolve_topology_filter(shape, len(shape.vertex_coordinates), vertex_filter)
    return shape.recoordinate(
        scale_vertex_coordinates(shape.vertex_coordinates, scale, pivot, resolved_vertex_filter)
    )
