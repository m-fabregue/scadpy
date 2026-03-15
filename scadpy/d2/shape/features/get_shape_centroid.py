from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy import Shape


def get_shape_centroid(shape: Shape) -> NDArray[np.float64]:
    """Return the geometric centroid of the shape, weighted by part area.

    Parameters
    ----------
    shape : Shape
        The shape to compute the centroid for.

    Returns
    -------
    NDArray[np.float64]
        1D array ``[cx, cy]``.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import Shape

    >>> polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    >>> Shape.from_geometry(polygon).centroid
    array([1., 1.])
    """
    parts = shape._parts  # pyright: ignore[reportPrivateUsage]
    if not parts:
        return np.zeros(2, dtype=np.float64)

    total_area = sum(p.geometry.area for p in parts)
    if total_area == 0:
        return np.zeros(2, dtype=np.float64)

    cx = sum(p.geometry.centroid.x * p.geometry.area for p in parts) / total_area
    cy = sum(p.geometry.centroid.y * p.geometry.area for p in parts) / total_area
    return np.array([cx, cy], dtype=np.float64)
