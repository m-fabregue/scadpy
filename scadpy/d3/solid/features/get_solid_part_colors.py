from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
def get_solid_part_colors(solid: Solid) -> NDArray[np.float64]:
    """For each part in the solid, return its RGBA color.

    Parameters
    ----------
    solid : Solid
        The solid to extract part colors from.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape (n_parts, 4), one RGBA row per part.
    """
    from scadpy import get_assembly_part_colors

    return get_assembly_part_colors(solid)
