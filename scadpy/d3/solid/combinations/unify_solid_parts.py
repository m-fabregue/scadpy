from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from trimesh import Trimesh
from trimesh.boolean import boolean_manifold  # pyright: ignore[reportUnknownVariableType]

if TYPE_CHECKING:
    from scadpy.core.part import Part
    from scadpy.d3.solid import Solid


def unify_solid_parts(
    parts: Sequence[Part[Trimesh]],
    make_assembly_from_parts: Callable[[Sequence[Part[Trimesh]]], Solid],
) -> Solid:
    """Unite a sequence of solid parts and return the resulting solid.

    Shortcut for :func:`unify_parts`.
    See :func:`unify_parts` for full documentation.

    Parameters
    ----------
    parts : Sequence[Part[Trimesh]]
        The solid parts to unite.
    make_assembly_from_parts : Callable[[Sequence[Part[Trimesh]]], Solid]
        Factory function to build the resulting Solid from a sequence of parts.

    Returns
    -------
    Solid
        A new solid containing the geometric union of the input parts.

    Examples
    --------
    >>> from scadpy import cuboid, sphere, unify_solid_parts, concat_solid, Solid

    >>> unify_solid_parts(  # doctest: +SKIP
    ...     parts=(
    ...         list(cuboid(4)._parts)
    ...         + list(sphere(radius=2).translate(2)._parts)
    ...     ),
    ...     make_assembly_from_parts=Solid.from_parts,
    ... )

    .. render-example::
        :name: unify_solid_parts_example
        :example: unify_solid_parts(parts=list(cuboid(4)._parts) + list(sphere(radius=2).translate([2, 2, 2])._parts), make_assembly_from_parts=Solid.from_parts)
        :ghost: concat_solid(solids=[cuboid(4), sphere(radius=2).translate(2)])
    """
    from scadpy import (
        Part,
        are_solid_parts_intersecting,
        get_solid_part_bounds,
    )
    from scadpy.core.part import unify_parts

    return unify_parts(
        parts=parts,
        get_part_color=lambda p: p.color,
        get_part_magnitude=lambda p: p.geometry.volume,  # pyright: ignore[reportAny]
        get_part_bounds=get_solid_part_bounds,
        are_parts_intersecting=are_solid_parts_intersecting,
        get_part_geometry=lambda p: p.geometry,
        unify_geometries=lambda g: boolean_manifold(
            g, operation="union", check_volume=False
        ).split(),  # pyright: ignore[reportUnknownMemberType]
        make_part_from_geometry=Part[Trimesh].from_geometry,
        make_assembly_from_parts=make_assembly_from_parts,
    )
