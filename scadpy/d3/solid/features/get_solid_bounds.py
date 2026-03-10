from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
def get_solid_bounds(solid: Solid) -> NDArray[np.float64]:
    """Return the axis-aligned bounding box of the solid.

    Parameters
    ----------
    solid : Solid
        The solid to compute bounds for.

    Returns
    -------
    NDArray[np.float64]
        1D array ``[min_x, min_y, min_z, max_x, max_y, max_z]``.
        Returns zeros if the solid is empty.

    Examples
    --------
    >>> from scadpy import cuboid, get_solid_bounds

    >>> get_solid_bounds(cuboid(2))
    array([-1., -1., -1.,  1.,  1.,  1.])
    """
    from scadpy import get_component_bounds

    return get_component_bounds(solid.vertex_coordinates)
