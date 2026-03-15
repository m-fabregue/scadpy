from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Solid, TopologyFilter


def translate_solid(
    solid: Solid,
    translation: float | Iterable[float],
    vertex_filter: TopologyFilter[Solid] | None = None,
) -> Solid:
    """Translate a solid by a given vector.

    Parameters
    ----------
    solid : Solid
        The solid to translate.
    translation : float | Iterable[float]
        The translation vector. If a single float is provided, it is broadcast
        to all coordinate dimensions.
    vertex_filter : TopologyFilter[Solid] | None, default=None
        Boolean array or callable selecting which vertices are translated. If ``None``, all
        vertices are translated.

    Returns
    -------
    Solid
        A new solid with the selected vertices shifted by the translation vector.
    """
    from scadpy import resolve_topology_filter, translate_vertex_coordinates

    resolved_vertex_filter = resolve_topology_filter(solid, len(solid.vertex_coordinates), vertex_filter)
    return solid.recoordinate(
        translate_vertex_coordinates(solid.vertex_coordinates, translation, resolved_vertex_filter)
    )
