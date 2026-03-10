from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.geometry import Polygon
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
def fill_shape(shape: Shape, part_filter: TopologyFilter[Shape] | None = None) -> Shape:
    """
    Fill the interior holes of each selected part, keeping only the exterior ring.

    Each selected part's interior rings (holes) are removed, producing a solid
    polygon from its exterior boundary. Unselected parts are left unchanged.

    Parameters
    ----------
    shape : Shape
        The input shape whose parts will be filled.
    part_filter : TopologyFilter[Shape] | None, optional
        A boolean mask selecting which parts to fill. If None, all parts are filled.

    Returns
    -------
    Shape
        A new shape with the selected parts filled and the unselected parts unchanged.

    Examples
    --------
    >>> from scadpy import fill_shape, square, circle
    >>> import numpy as np

    >>> shape = square(10) - circle(3)
    >>> fill_shape(shape) # doctest: +SKIP

    .. render-example::
        :name: fill_shape
        :example: fill_shape(shape)
        :ghost: shape

    >>> # partial fill
    >>> a = square(5) - circle(1)
    >>> b = (square(3) - circle(0.5)).translate(10)
    >>> fill_shape(  # doctest: +SKIP
    ...     a + b, part_filter=np.array([True, False])
    ... )

    .. render-example::
        :name: fill_shape_partial
        :example: fill_shape(a + b, part_filter=np.array([True, False]))
        :ghost: a + b
    """
    from scadpy import Part, Shape, transform_filtered_parts

    return transform_filtered_parts(
        assembly=shape,
        parts=shape._parts,
        part_filter=part_filter,
        transform=lambda parts: [
            Part[Polygon].from_geometry(Polygon(p.geometry.exterior), p.color)
            for p in parts
        ],
        concat_parts=Shape.from_parts,
    )
