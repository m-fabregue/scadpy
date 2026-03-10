from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.core.assembly import Assembly


@typechecked
def get_assembly_part_colors[G](
    assembly: Assembly[G],
) -> NDArray[np.float64]:
    """
    For each part in the assembly, return its color (r, g, b, a).

    Parameters
    ----------
    assembly : VertexableAssembly[G]
        The assembly object to extract part colors from.

    Returns
    -------
    NDArray[np.float64]
        2D array of shape (n_parts, 4), one row per part.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import (
    ...     BLUE, RED, get_assembly_part_colors, Part, Shape
    ... )
    ...
    >>> polygon1 = Polygon(
    ...     shell=[(0, 0), (2, 0), (2, 2), (0, 2)],
    ...     holes=[[(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)]]
    ... )
    >>> polygon2 = Polygon(
    ...     shell=[(10, 10), (12, 10), (12, 12), (10, 12)]
    ... )
    >>> get_assembly_part_colors(
    ...     Shape.from_parts([
    ...         Part[Polygon].from_geometry(polygon1, BLUE),
    ...         Part[Polygon].from_geometry(polygon2, RED)
    ...     ]),
    ... ) # doctest: +NORMALIZE_WHITESPACE
    array([[0.1, 0.3, 0.9, 1. ],
           [0.9, 0.1, 0.1, 1. ]])
    """
    if not assembly._parts:
        return np.empty((0, 4), dtype=np.float64)
    return np.array([p.color for p in assembly._parts])
