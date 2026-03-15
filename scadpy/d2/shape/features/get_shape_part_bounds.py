from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from shapely.geometry.polygon import Polygon

if TYPE_CHECKING:
    from scadpy.core.part import Part


def get_shape_part_bounds(part: Part[Polygon]) -> NDArray[np.float64]:
    """Return the 2D bounding box of a shape part as [minx, miny, maxx, maxy].

    Parameters
    ----------
    part : Part[Polygon]
        The shape part to compute the bounding box of.

    Returns
    -------
    NDArray[np.float64]
        Array of shape (4,) containing [minx, miny, maxx, maxy].

    Examples
    --------
    >>> from scadpy import square, get_shape_part_bounds
    >>> bounds = get_shape_part_bounds(part=square(2)._parts[0])
    >>> bounds.shape
    (4,)
    """
    from scadpy import get_component_bounds, get_shape_part_vertex_coordinates

    return get_component_bounds(get_shape_part_vertex_coordinates(part))
