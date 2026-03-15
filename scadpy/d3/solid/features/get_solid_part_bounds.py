from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from trimesh import Trimesh

if TYPE_CHECKING:
    from scadpy.core.part import Part


def get_solid_part_bounds(part: Part[Trimesh]) -> NDArray[np.float64]:
    """Return the 3D bounding box of a solid part as [minx, miny, minz, maxx, maxy, maxz].

    Parameters
    ----------
    part : Part[Trimesh]
        The solid part to compute the bounding box of.

    Returns
    -------
    NDArray[np.float64]
        Array of shape (6,) containing [minx, miny, minz, maxx, maxy, maxz].

    Examples
    --------
    >>> from scadpy import cuboid, get_solid_part_bounds
    >>> bounds = get_solid_part_bounds(part=cuboid(2)._parts[0])
    >>> bounds.shape
    (6,)
    """
    from scadpy import get_component_bounds

    return get_component_bounds(part.geometry.vertices)
