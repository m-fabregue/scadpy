from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy import Shape


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

    """
    from scadpy import get_component_bounds

    return get_component_bounds(shape.vertex_coordinates)
