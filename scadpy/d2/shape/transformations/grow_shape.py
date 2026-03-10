from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.geometry import Polygon
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
def grow_shape(
    shape: Shape, distance: float, part_filter: TopologyFilter[Shape] | None = None
) -> Shape:
    """
    Grow or shrink each selected part by offsetting its boundary by a given distance.

    A positive distance expands the shape outward, a negative distance shrinks it
    inward. The offset uses mitre joins to preserve sharp corners.

    Parameters
    ----------
    shape : Shape
        The input shape whose parts will be grown.
    distance : float
        The offset distance. Positive values expand, negative values shrink.
    part_filter : TopologyFilter[Shape] | None, optional
        A boolean mask selecting which parts to grow. If None, all parts are grown.

    Returns
    -------
    Shape
        A new shape with the selected parts grown and the unselected parts unchanged.

    Examples
    --------
    >>> from scadpy import grow_shape, square
    >>> import numpy as np

    >>> shape = square(10)
    >>> grow_shape(shape, 2) # doctest: +SKIP

    .. render-example::
        :name: grow_shape
        :example: grow_shape(shape, 2)
        :ghost: shape

    >>> # shrink with negative distance
    >>> grow_shape(shape, -2) # doctest: +SKIP

    .. render-example::
        :name: grow_shape_shrink
        :example: grow_shape(shape, -2)
        :ghost: shape

    >>> # partial grow
    >>> a = square(4)
    >>> b = square(2).translate(10)
    >>> grow_shape(  # doctest: +SKIP
    ...     a + b, 1, part_filter=np.array([True, False])
    ... )

    .. render-example::
        :name: grow_shape_partial
        :example: grow_shape(a + b, 1, part_filter=np.array([True, False]))
        :ghost: a + b
    """
    from scadpy import Part, Shape, transform_filtered_parts

    return transform_filtered_parts(
        assembly=shape,
        parts=shape._parts,
        part_filter=part_filter,
        transform=lambda parts: [
            Part[Polygon].from_geometry(
                p.geometry.buffer(distance, join_style="mitre"), p.color
            )
            for p in parts
        ],
        concat_parts=Shape.from_parts,
    )
