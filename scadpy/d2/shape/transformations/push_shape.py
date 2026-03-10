from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from typeguard import typechecked


if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
def push_shape(
    shape: Shape,
    distance: float,
    pivot: float | Iterable[float] = 0,
    vertex_filter: TopologyFilter[Shape] | None = None,
) -> Shape:
    """Move a subset of shape vertices away from a pivot point by a given distance.

    Each selected vertex is translated away from the pivot by exactly ``distance`` units.
    Vertices located exactly at the pivot are not moved (undefined direction).

    Parameters
    ----------
    shape : Shape
        The shape whose vertices will be pushed.
    distance : float
        The distance each vertex is moved away from the pivot.
    pivot : float | Iterable[float], default=0
        The repulsion point. If a single float is provided, it is broadcast
        to all coordinate dimensions. Defaults to the origin.
    vertex_filter : TopologyFilter[Shape] | None, default=None
        A boolean array or callable selecting which vertices are affected. If ``None``,
        all vertices are moved.

    Returns
    -------
    Shape
        A new shape with the selected vertices moved away from the pivot.

    See Also
    --------
    pull_shape : Move shape vertices toward a pivot point.

    Examples
    --------
    >>> from scadpy import square, push_shape

    >>> shape = square(4)
    >>> push_shape(  # doctest: +SKIP
    ...     shape=shape, distance=1.0, pivot=[2, 2],
    ...     vertex_filter=shape.vertex_coordinates[:, 0] < 1,
    ... )

    .. render-example::
        :name: push_shape
        :example: push_shape(shape=square(4), distance=1.0, pivot=[2, 2], vertex_filter=square(4).vertex_coordinates[:, 0] < 1)
        :ghost: square(4)
    """
    from scadpy import resolve_topology_filter, push_vertex_coordinates

    resolved_vertex_filter = resolve_topology_filter(shape, len(shape.vertex_coordinates), vertex_filter)
    return shape.recoordinate(
        push_vertex_coordinates(shape.vertex_coordinates, distance, pivot, resolved_vertex_filter)
    )
