from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


def translate_shape(
    shape: Shape,
    translation: float | Iterable[float],
    vertex_filter: TopologyFilter[Shape] | None = None,
) -> Shape:
    """Translate a shape by a given vector.

    Parameters
    ----------
    shape : Shape
        The shape to translate.
    translation : float | Iterable[float]
        The translation vector. If a single float is provided, it is broadcast
        to all coordinate dimensions.
    vertex_filter : TopologyFilter[Shape] | None, default=None
        Boolean array or callable selecting which vertices are translated. If ``None``, all
        vertices are translated.

    Returns
    -------
    Shape
        A new shape with the selected vertices shifted by the translation vector.
    """
    from scadpy import resolve_topology_filter, translate_vertex_coordinates

    resolved_vertex_filter = resolve_topology_filter(shape, len(shape.vertex_coordinates), vertex_filter)
    return shape.recoordinate(
        translate_vertex_coordinates(shape.vertex_coordinates, translation, resolved_vertex_filter)
    )
