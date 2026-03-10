from __future__ import annotations

from typing import TYPE_CHECKING

from trimesh import Trimesh
from trimesh.boolean import boolean_manifold  # pyright: ignore[reportUnknownVariableType]
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.core.part import Part


@typechecked
def are_solid_parts_intersecting(part1: Part[Trimesh], part2: Part[Trimesh]) -> bool:
    """Return whether two solid parts intersect geometrically.

    Parameters
    ----------
    part1 : Part[Trimesh]
        The first solid part.
    part2 : Part[Trimesh]
        The second solid part.

    Returns
    -------
    bool
        True if the two parts intersect (shared volume > 0), False otherwise.

    Examples
    --------
    >>> from scadpy import cuboid, are_solid_parts_intersecting

    >>> are_solid_parts_intersecting(
    ...     part1=cuboid(2)._parts[0],
    ...     part2=cuboid(2)._parts[0],
    ... )
    True
    >>> are_solid_parts_intersecting(
    ...     part1=cuboid(1)._parts[0],
    ...     part2=cuboid(1).translate(10)._parts[0],
    ... )
    False
    """
    return bool(
        boolean_manifold(  # pyright: ignore[reportAny]
            [part1.geometry, part2.geometry],
            operation="intersection",
            check_volume=False,
        ).volume
        != 0
    )
