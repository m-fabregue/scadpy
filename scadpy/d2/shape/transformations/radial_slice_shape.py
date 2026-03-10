from __future__ import annotations

from collections.abc import Iterable
from math import cos, radians, sin
from typing import TYPE_CHECKING

import numpy as np
from shapely.geometry.polygon import Polygon
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
def radial_slice_shape(
    shape: Shape,
    start: float = 0,
    end: float = 360,
    pivot: float | Iterable[float] = 0,
    part_filter: TopologyFilter[Shape] | None = None,
) -> Shape:
    """
    Slice a shape by keeping only the angular sector between two angles.

    Constructs a pie-shaped wedge from the pivot point spanning the angular range
    from start to end, and intersects it with the selected parts. Only the portion
    of the shape within the wedge remains.

    Parameters
    ----------
    shape : Shape
        The input shape to slice.
    start : float, optional
        The start angle of the sector in degrees. Defaults to 0.
    end : float, optional
        The end angle of the sector in degrees. Defaults to 360.
    pivot : float | Iterable[float], optional
        The center point of the angular sector. Defaults to the origin.
    part_filter : TopologyFilter[Shape] | None, optional
        A boolean mask selecting which parts to slice. If None, all parts are sliced.

    Returns
    -------
    Shape
        A new shape containing only the angular sector of the selected parts,
        plus the unselected parts unchanged. If start equals end, the shape
        is returned unchanged.

    Examples
    --------
    >>> from scadpy import radial_slice_shape, square, circle
    >>> import numpy as np

    >>> shape = square(10) - circle(3)

    >>> # quarter slice
    >>> radial_slice_shape(shape, start=0, end=90) # doctest: +SKIP

    .. render-example::
        :name: radial_slice_shape_quarter
        :example: radial_slice_shape(shape, start=0, end=90)
        :ghost: shape

    >>> # three quarter slice
    >>> radial_slice_shape(shape, start=45, end=315) # doctest: +SKIP

    .. render-example::
        :name: radial_slice_shape_three_quarter
        :example: radial_slice_shape(shape, start=45, end=315)
        :ghost: shape

    >>> # off-center pivot
    >>> radial_slice_shape(  # doctest: +SKIP
    ...     shape, start=0, end=180, pivot=[3, 3]
    ... )

    .. render-example::
        :name: radial_slice_shape_pivot
        :example: radial_slice_shape(shape, start=0, end=180, pivot=[3, 3])
        :ghost: shape

    >>> # partial slice on a composite shape
    >>> a = square(6) - circle(2)
    >>> b = circle(3).translate(10)

    >>> radial_slice_shape(  # doctest: +SKIP
    ...     a + b, start=0, end=120,
    ...     part_filter=np.array([True, False]),
    ... )

    .. render-example::
        :name: radial_slice_shape_partial
        :example: radial_slice_shape(a + b, start=0, end=120, part_filter=np.array([True, False]))
        :ghost: a + b
    """
    from scadpy import resolve_vector_2d, transform_filtered_parts, Shape

    pivot = resolve_vector_2d(pivot, 0)

    start = start % 360
    end = end % 360
    if start == end:
        return shape
    if end <= start:
        end += 360

    bounds = shape.bounds
    radius = max(bounds[2] - bounds[0], bounds[3] - bounds[1]) * 2

    n = max(2, int((end - start) / 5))
    if n == 2:
        theta = [radians(start), radians(end)]
    else:
        theta = np.linspace(radians(start), radians(end), n + 1)

    px, py = pivot
    points = (
        [(px, py)]
        + [(px + radius * cos(t), py + radius * sin(t)) for t in theta]
        + [(px, py)]
    )

    slice_mask = Shape.from_geometries([Polygon(points)])

    return transform_filtered_parts(
        assembly=shape,
        parts=shape._parts,
        part_filter=part_filter,
        transform=lambda parts: (Shape.from_parts(parts) & slice_mask)._parts,
        concat_parts=Shape.from_parts,
    )
