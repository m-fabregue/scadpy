from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def get_shape_bounds(shape: Shape) -> NDArray[np.float64]:
    """
    Return the axis-aligned bounding box of the shape.

    Parameters
    ----------
    shape : Shape
        The shape to compute bounds for.

    Returns
    -------
    NDArray[np.float64]
        1D array ``[min_x, min_y, max_x, max_y]``.
        Returns zeros if the shape is empty.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import Shape, get_shape_bounds

    >>> polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    >>> get_shape_bounds(Shape.from_geometry(polygon))
    array([0., 0., 2., 2.])
    """
    from scadpy import get_component_bounds

    return get_component_bounds(shape.vertex_coordinates)
