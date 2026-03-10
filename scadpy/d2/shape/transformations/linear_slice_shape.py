from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

import numpy as np
from shapely.geometry.polygon import Polygon
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
def linear_slice_shape(
    shape: Shape,
    thickness: float,
    direction: float | Iterable[float],
    pivot: float | Iterable[float] = 0,
    part_filter: TopologyFilter[Shape] | None = None,
) -> Shape:
    """
    Slice a shape along a directed line, keeping only a strip of given thickness.

    Constructs an oriented rectangle along the specified direction, centered on the
    pivot point, and intersects it with the selected parts. The rectangle is wide
    enough to cover the entire shape, so only the strip of the given thickness remains.

    Parameters
    ----------
    shape : Shape
        The input shape to slice.
    thickness : float
        The width of the slice strip.
    direction : float | Iterable[float]
        The direction vector along which the slice is oriented.
    pivot : float | Iterable[float], optional
        The center point of the slice strip. Defaults to the origin.
    part_filter : TopologyFilter[Shape] | None, optional
        A boolean mask selecting which parts to slice. If None, all parts are sliced.

    Returns
    -------
    Shape
        A new shape containing only the sliced strip of the selected parts,
        plus the unselected parts unchanged.

    Examples
    --------
    >>> from scadpy import linear_slice_shape, square, circle
    >>> import numpy as np

    >>> shape = square(10) - circle(3)

    >>> # horizontal slice through center
    >>> linear_slice_shape(  # doctest: +SKIP
    ...     shape, thickness=3, direction=[1, 0]
    ... )

    .. render-example::
        :name: linear_slice_shape_horizontal
        :example: linear_slice_shape(shape, thickness=3, direction=[1, 0])
        :ghost: shape

    >>> # diagonal slice
    >>> linear_slice_shape(  # doctest: +SKIP
    ...     shape, thickness=2, direction=[1, 1]
    ... )

    .. render-example::
        :name: linear_slice_shape_diagonal
        :example: linear_slice_shape(shape, thickness=2, direction=[1, 1])
        :ghost: shape

    >>> # off-center slice with pivot
    >>> linear_slice_shape(  # doctest: +SKIP
    ...     shape, thickness=2, direction=[0, 1], pivot=[3, 0]
    ... )

    .. render-example::
        :name: linear_slice_shape_pivot
        :example: linear_slice_shape(shape, thickness=2, direction=[0, 1], pivot=[3, 0])
        :ghost: shape

    >>> # partial slice on a composite shape
    >>> a = square(6)
    >>> b = circle(3).translate(10)

    >>> linear_slice_shape(  # doctest: +SKIP
    ...     a + b, thickness=2, direction=[1, 0],
    ...     part_filter=np.array([True, False]),
    ... )

    .. render-example::
        :name: linear_slice_shape_partial
        :example: linear_slice_shape(a + b, thickness=2, direction=[1, 0], part_filter=np.array([True, False]))
        :ghost: a + b
    """
    from scadpy import resolve_vector_2d, transform_filtered_parts, Shape

    direction = resolve_vector_2d(direction, 0)
    pivot = resolve_vector_2d(pivot, 0)

    bounds = shape.bounds
    size = max(bounds[2] - bounds[0], bounds[3] - bounds[1]) * 2

    direction = direction / np.linalg.norm(direction)
    direction_x, direction_y = direction[0], direction[1]

    normal_x = -direction_y
    normal_y = direction_x

    half_thickness = thickness / 2
    px, py = pivot[0], pivot[1]

    half_size = size / 2
    points = [
        (
            px - direction_x * half_size - normal_x * half_thickness,
            py - direction_y * half_size - normal_y * half_thickness,
        ),
        (
            px + direction_x * half_size - normal_x * half_thickness,
            py + direction_y * half_size - normal_y * half_thickness,
        ),
        (
            px + direction_x * half_size + normal_x * half_thickness,
            py + direction_y * half_size + normal_y * half_thickness,
        ),
        (
            px - direction_x * half_size + normal_x * half_thickness,
            py - direction_y * half_size + normal_y * half_thickness,
        ),
    ]

    slice_mask = Shape.from_geometries([Polygon(points)])

    return transform_filtered_parts(
        assembly=shape,
        parts=shape._parts,
        part_filter=part_filter,
        transform=lambda parts: (Shape.from_parts(parts) & slice_mask)._parts,
        concat_parts=Shape.from_parts,
    )
