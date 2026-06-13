from __future__ import annotations

from typing import TYPE_CHECKING

from trimesh import Trimesh

if TYPE_CHECKING:
    from scadpy.core.part import Part


def are_solid_part_bounding_boxes_intersecting(
    part1: Part[Trimesh],
    part2: Part[Trimesh],
) -> bool:
    """Return whether two solid parts' bounding boxes overlap.

    Fast, conservative broad-phase: it never misses a real overlap, but may
    report a false positive for parts whose bounding boxes overlap without their
    geometry touching. Used as the intersection criterion for boolean operations
    where false positives are harmless (the boolean simply becomes a no-op). For
    the exact test, see :func:`are_solid_parts_intersecting`.

    Parameters
    ----------
    part1 : Part[Trimesh]
        The first solid part.
    part2 : Part[Trimesh]
        The second solid part.

    Returns
    -------
    bool
        True if the two parts' bounding boxes overlap, False otherwise.

    Examples
    --------
    >>> from scadpy import cuboid, are_solid_part_bounding_boxes_intersecting

    >>> are_solid_part_bounding_boxes_intersecting(
    ...     part1=cuboid(2)._parts[0],
    ...     part2=cuboid(2)._parts[0],
    ... )
    True
    >>> are_solid_part_bounding_boxes_intersecting(
    ...     part1=cuboid(1)._parts[0],
    ...     part2=cuboid(1).translate(10)._parts[0],
    ... )
    False
    """
    from scadpy import are_bounds_overlapping, get_solid_part_bounds

    return are_bounds_overlapping(
        get_solid_part_bounds(part1), get_solid_part_bounds(part2)
    )
