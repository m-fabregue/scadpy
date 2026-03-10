from __future__ import annotations

from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def is_shape_empty(shape: Shape) -> bool:
    """
    Return whether the shape has no vertices.

    Parameters
    ----------
    shape : Shape
        The shape to check.

    Returns
    -------
    bool
        True if the shape has no vertices, False otherwise.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import Shape, is_shape_empty

    >>> is_shape_empty(Shape.from_parts([]))
    True

    >>> polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    >>> is_shape_empty(Shape.from_geometry(polygon))
    False
    """
    return len(shape.vertex_coordinates) == 0
