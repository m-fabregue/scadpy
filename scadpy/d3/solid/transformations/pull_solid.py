from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from typeguard import typechecked


if TYPE_CHECKING:
    from scadpy import Solid, TopologyFilter


@typechecked
def pull_solid(
    solid: Solid,
    distance: float,
    pivot: float | Iterable[float] = 0,
    vertex_filter: TopologyFilter[Solid] | None = None,
) -> Solid:
    """Move a subset of solid vertices toward a pivot point by a given distance.

    Each selected vertex is translated toward the pivot by at most ``distance`` units.
    Vertices already closer than ``distance`` to the pivot are moved to the pivot.

    Parameters
    ----------
    solid : Solid
        The solid whose vertices will be pulled.
    distance : float
        The maximum distance each vertex is moved toward the pivot.
    pivot : float | Iterable[float], default=0
        The attraction point. If a single float is provided, it is broadcast
        to all coordinate dimensions. Defaults to the origin.
    vertex_filter : TopologyFilter[Solid] | None, default=None
        A boolean array or callable selecting which vertices are affected. If ``None``,
        all vertices are moved.

    Returns
    -------
    Solid
        A new solid with the selected vertices moved toward the pivot.

    See Also
    --------
    push_solid : Move solid vertices away from a pivot point.

    Examples
    --------
    >>> from scadpy import cuboid, pull_solid
    >>> import numpy as np

    >>> pull_solid(  # doctest: +SKIP
    ...     solid=cuboid(4), distance=1.0, pivot=[2, 2, 2],
    ...     vertex_filter=np.ones(8, dtype=bool),
    ... )

    .. render-example::
        :name: pull_solid
        :example: pull_solid(solid=cuboid(4), distance=1.0, pivot=[2, 2, 2], vertex_filter=cuboid(4).vertex_coordinates[:, 0] < 1)
        :ghost: cuboid(4)
    """
    from scadpy import resolve_topology_filter, pull_vertex_coordinates

    resolved_vertex_filter = resolve_topology_filter(solid, len(solid.vertex_coordinates), vertex_filter)
    return solid.recoordinate(
        pull_vertex_coordinates(solid.vertex_coordinates, distance, pivot, resolved_vertex_filter)
    )
