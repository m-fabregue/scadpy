from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Solid, TopologyFilter


def resize_solid(
    solid: Solid,
    size: Iterable[float | None],
    auto: bool = False,
    pivot: float | Iterable[float] | None = None,
    vertex_filter: TopologyFilter[Solid] | None = None,
) -> Solid:
    """Resize a solid to fit target dimensions.

    Scales the solid so that each non-``None`` axis matches the given target
    size. The scaling pivot defaults to the center of the bounding box so the
    solid stays in place.

    Shortcut delegating to :func:`resize_vertex_coordinates`.

    Parameters
    ----------
    solid : Solid
        The solid to resize.
    size : Iterable[float | None]
        Target dimensions ``[width, height, depth]``. Pass ``None`` for an
        axis to leave it unchanged (or scale it proportionally when
        ``auto=True``).
    auto : bool, default=False
        If ``True``, axes with ``None`` are scaled proportionally to the
        average ratio of the defined axes. If ``False``, ``None`` axes are
        left unchanged.
    pivot : float | Iterable[float] | None, default=None
        The point relative to which scaling is performed. Defaults to the
        center of the bounding box.
    vertex_filter : TopologyFilter[Solid] | None, default=None
        Boolean array or callable selecting which vertices are resized. If ``None``, all
        vertices are resized.

    Returns
    -------
    Solid
        A new solid resized to the target dimensions.
    """
    from scadpy import resolve_topology_filter, resize_vertex_coordinates

    resolved_vertex_filter = resolve_topology_filter(solid, len(solid.vertex_coordinates), vertex_filter)
    return solid.recoordinate(
        resize_vertex_coordinates(
            solid.vertex_coordinates,
            size=size,
            n_dims=3,
            auto=auto,
            pivot=pivot,
            vertex_filter=resolved_vertex_filter,
        )
    )
