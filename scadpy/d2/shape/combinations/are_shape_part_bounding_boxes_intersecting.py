from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.geometry.polygon import Polygon

if TYPE_CHECKING:
    from scadpy.core.part import Part


def are_shape_part_bounding_boxes_intersecting(
    part1: Part[Polygon],
    part2: Part[Polygon],
) -> bool:
    """Return whether two shape parts' bounding boxes overlap.

    Fast, conservative broad-phase: it never misses a real overlap, but may
    report a false positive for parts whose bounding boxes overlap without their
    geometry touching. Used as the intersection criterion for boolean operations
    where false positives are harmless (the boolean simply becomes a no-op). For
    the exact test, see :func:`are_shape_parts_intersecting`.

    Parameters
    ----------
    part1 : Part[Polygon]
        The first shape part.
    part2 : Part[Polygon]
        The second shape part.

    Returns
    -------
    bool
        True if the two parts' bounding boxes overlap, False otherwise.

    Examples
    --------
    >>> from scadpy import square, are_shape_part_bounding_boxes_intersecting

    >>> are_shape_part_bounding_boxes_intersecting(
    ...     part1=square(2)._parts[0],
    ...     part2=square(2)._parts[0],
    ... )
    True
    >>> are_shape_part_bounding_boxes_intersecting(
    ...     part1=square(1)._parts[0],
    ...     part2=square(1).translate(10)._parts[0],
    ... )
    False
    """
    from scadpy import are_bounds_overlapping, get_shape_part_bounds

    return are_bounds_overlapping(
        get_shape_part_bounds(part1), get_shape_part_bounds(part2)
    )
