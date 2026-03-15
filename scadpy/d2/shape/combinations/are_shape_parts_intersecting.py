from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.geometry.polygon import Polygon

if TYPE_CHECKING:
    from scadpy.core.part import Part


def are_shape_parts_intersecting(
    part1: Part[Polygon],
    part2: Part[Polygon],
) -> bool:
    """Return whether two shape parts intersect geometrically.

    Parameters
    ----------
    part1 : Part[Polygon]
        The first shape part.
    part2 : Part[Polygon]
        The second shape part.

    Returns
    -------
    bool
        True if the two parts intersect, False otherwise.

    Examples
    --------
    >>> from scadpy import (
    ...     square, circle, are_shape_parts_intersecting
    ... )
    >>> are_shape_parts_intersecting(
    ...     part1=square(2)._parts[0],
    ...     part2=square(2)._parts[0],
    ... )
    True
    >>> are_shape_parts_intersecting(
    ...     part1=square(1)._parts[0],
    ...     part2=square(1).rotate(
    ...         angle=0
    ...     ).grow(distance=5)._parts[0],
    ... )
    True
    """
    return part1.geometry.intersects(part2.geometry)
