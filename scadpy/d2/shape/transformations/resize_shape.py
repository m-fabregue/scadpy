from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
def resize_shape(
    shape: Shape,
    size: Iterable[float | None],
    auto: bool = False,
    pivot: float | Iterable[float] | None = None,
    vertex_filter: TopologyFilter[Shape] | None = None,
) -> Shape:
    """Resize a shape to fit target dimensions.

    Scales the shape so that each non-``None`` axis matches the given target
    size. The scaling pivot defaults to the center of the bounding box so the
    shape stays in place.

    Shortcut delegating to :func:`resize_vertex_coordinates`.

    Parameters
    ----------
    shape : Shape
        The shape to resize.
    size : Iterable[float | None]
        Target dimensions ``[width, height]``. Pass ``None`` for an axis to
        leave it unchanged (or scale it proportionally when ``auto=True``).
    auto : bool, default=False
        If ``True``, axes with ``None`` are scaled proportionally to the
        average ratio of the defined axes. If ``False``, ``None`` axes are
        left unchanged.
    pivot : float | Iterable[float] | None, default=None
        The point relative to which scaling is performed. Defaults to the
        center of the bounding box.
    vertex_filter : TopologyFilter[Shape] | None, default=None
        Boolean array or callable selecting which vertices are resized. If ``None``, all
        vertices are resized.

    Returns
    -------
    Shape
        A new shape resized to the target dimensions.

    Examples
    --------
    >>> from scadpy import rectangle, resize_shape

    >>> # resize to an exact size on both axes:
    >>> resize_shape(shape=rectangle([4, 2]), size=[6, 6]) # doctest: +SKIP

    .. render-example::
       :name: resize_shape_exact
       :example: resize_shape(shape=rectangle([4, 2]), size=[6, 6])
       :ghost: rectangle([4, 2])

    >>> # freeze one axis (``None``) to leave it unchanged:
    >>> resize_shape(shape=rectangle([4, 2]), size=[6, None]) # doctest: +SKIP

    .. render-example::
       :name: resize_shape_freeze
       :example: resize_shape(shape=rectangle([4, 2]), size=[6, None])
       :ghost: rectangle([4, 2])

    >>> # scale frozen axes proportionally with ``auto=True``:
    >>> resize_shape(shape=rectangle([4, 2]), size=[6, None], auto=True) # doctest: +SKIP

    .. render-example::
       :name: resize_shape_auto
       :example: resize_shape(shape=rectangle([4, 2]), size=[6, None], auto=True)
       :ghost: rectangle([4, 2])
    """
    from scadpy import resolve_topology_filter, resize_vertex_coordinates

    resolved_vertex_filter = resolve_topology_filter(shape, len(shape.vertex_coordinates), vertex_filter)
    return shape.recoordinate(
        resize_vertex_coordinates(
            shape.vertex_coordinates,
            size=size,
            n_dims=2,
            auto=auto,
            pivot=pivot,
            vertex_filter=resolved_vertex_filter,
        )
    )
