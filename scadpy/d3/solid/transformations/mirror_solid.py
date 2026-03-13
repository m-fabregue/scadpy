from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
def mirror_solid(
    solid: Solid,
    normal: float | Iterable[float],
    pivot: float | Iterable[float] = 0,
) -> Solid:
    """Mirror a solid across a plane defined by a normal vector and a pivot point.

    Parameters
    ----------
    solid : Solid
        The solid to mirror.
    normal : float | Iterable[float]
        The normal vector of the mirror plane. Does not need to be normalized.
        If a single float is provided, it is broadcast to all coordinate dimensions.
    pivot : float | Iterable[float], default=0
        The point through which the mirror plane passes. If a single float is
        provided, it is broadcast to all coordinate dimensions. Defaults to the origin.

    Returns
    -------
    Solid
        A new solid with all vertices mirrored across the specified plane.
    """
    from scadpy import mirror_vertex_coordinates

    return solid.recoordinate(
        mirror_vertex_coordinates(solid.vertex_coordinates, normal, pivot)
    )
