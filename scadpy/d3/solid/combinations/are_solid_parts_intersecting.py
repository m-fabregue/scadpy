from __future__ import annotations

import numpy as np
from typing import TYPE_CHECKING

from trimesh import Trimesh
from trimesh.collision import CollisionManager

if TYPE_CHECKING:
    from scadpy.core.part import Part


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
    # AABB broad-phase: reject non-overlapping pairs without building FCL objects.
    b1 = part1.geometry.bounds  # [[min_x, min_y, min_z], [max_x, max_y, max_z]]
    b2 = part2.geometry.bounds
    if np.any(b1[1] <= b2[0]) or np.any(b2[1] <= b1[0]):
        return False

    manager = CollisionManager()
    manager.add_object("a", part1.geometry)  # pyright: ignore[reportUnknownMemberType]
    return bool(manager.in_collision_single(part2.geometry))  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
