from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from trimesh import Trimesh
from trimesh.boolean import boolean_manifold  # pyright: ignore[reportUnknownVariableType]
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.core.part import Part
    from scadpy.d3.solid import Solid


@typechecked
def intersect_solid_parts(
    parts: Sequence[Part[Trimesh]],
    make_assembly_from_parts: Callable[[Sequence[Part[Trimesh]]], Solid],
) -> Solid:
    """Intersect a sequence of solid parts and return the resulting solid.

    Shortcut for :func:`intersect_parts`.
    See :func:`intersect_parts` for full documentation.

    Parameters
    ----------
    parts : Sequence[Part[Trimesh]]
        The solid parts to intersect.
    make_assembly_from_parts : Callable[[Sequence[Part[Trimesh]]], Solid]
        Factory function to build the resulting Solid from a sequence of parts.

    Returns
    -------
    Solid
        A new solid containing the geometric intersection of the input parts.

    Examples
    --------
    >>> from scadpy import cuboid, sphere, intersect_solid_parts, Solid

    >>> intersect_solid_parts(  # doctest: +SKIP
    ...     parts=(
    ...         list(cuboid(4)._parts)
    ...         + list(sphere(radius=2).translate([2, 2, 2])._parts)
    ...     ),
    ...     make_assembly_from_parts=Solid.from_parts,
    ... )

    .. render-example::
        :name: intersect_solid_parts_example
        :example: intersect_solid_parts(parts=list(cuboid(4)._parts) + list(sphere(radius=2).translate([2, 2, 2])._parts), make_assembly_from_parts=Solid.from_parts)
        :ghost: concat_solid(solids=[cuboid(4), sphere(radius=2).translate([2, 2, 2])])
    """
    from scadpy import (
        Part,
        are_solid_parts_intersecting,
        get_solid_part_bounds,
    )
    from scadpy.core.part import intersect_parts

    return intersect_parts(
        parts=parts,
        get_part_color=lambda p: p.color,
        get_part_magnitude=lambda p: p.geometry.volume,  # pyright: ignore[reportAny]
        get_part_bounds=get_solid_part_bounds,
        are_parts_intersecting=are_solid_parts_intersecting,
        get_part_geometry=lambda p: p.geometry,
        intersect_geometries=lambda g: boolean_manifold(
            g, operation="intersection", check_volume=False
        ).split(),  # pyright: ignore[reportUnknownMemberType]
        make_part_from_geometry=Part[Trimesh].from_geometry,
        make_assembly_from_parts=make_assembly_from_parts,
    )
