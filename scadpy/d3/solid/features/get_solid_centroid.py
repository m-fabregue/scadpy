from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy import Solid


def get_solid_centroid(solid: Solid) -> NDArray[np.float64]:
    """Return the geometric centroid of the solid, weighted by part volume.

    Parameters
    ----------
    solid : Solid
        The solid to compute the centroid for.

    Returns
    -------
    NDArray[np.float64]
        1D array ``[cx, cy, cz]``.

    Examples
    --------
    >>> from scadpy import cuboid, Solid

    >>> cuboid(2).centroid
    array([0., 0., 0.])

    >>> Solid.from_parts([]).centroid
    array([0., 0., 0.])
    """
    parts = solid._parts  # pyright: ignore[reportPrivateUsage]
    if not parts:
        return np.zeros(3, dtype=np.float64)

    total_volume = sum(p.geometry.volume for p in parts)
    if total_volume == 0:
        return np.zeros(3, dtype=np.float64)

    centroid = sum(p.geometry.centroid * p.geometry.volume for p in parts) / total_volume  # pyright: ignore[reportAny]
    return np.array(centroid, dtype=np.float64)
