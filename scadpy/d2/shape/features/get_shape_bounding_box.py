from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Shape


def get_shape_bounding_box(shape: Shape) -> Shape:
    """Return the axis-aligned bounding box of the shape as a rectangle.

    Parameters
    ----------
    shape : Shape
        The shape to compute the bounding box for.

    Returns
    -------
    Shape
        A rectangle Shape representing the bounding box.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import Shape

    >>> polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    >>> Shape.from_geometry(polygon).bounding_box.bounds
    array([0., 0., 2., 2.])
    """
    from scadpy import get_shape_bounds, rectangle, translate_shape

    bounds = get_shape_bounds(shape)
    size = [bounds[2] - bounds[0], bounds[3] - bounds[1]]
    center = (bounds[:2] + bounds[2:]) / 2
    return translate_shape(rectangle(size), center)
