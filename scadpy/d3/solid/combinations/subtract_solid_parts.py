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
def subtract_solid_parts(
    to_be_subtracted: Part[Trimesh],
    to_subtract: Part[Trimesh],
    make_assembly_from_parts: Callable[[Sequence[Part[Trimesh]]], Solid],
) -> Solid:
    """Subtract one solid part from another and return the resulting solid.

    Shortcut for :func:`subtract_parts`.
    See :func:`subtract_parts` for full documentation.

    Parameters
    ----------
    to_be_subtracted : Part[Trimesh]
        The part to subtract from.
    to_subtract : Part[Trimesh]
        The part to subtract.
    make_assembly_from_parts : Callable[[list[Part[Trimesh]]], Solid]
        Factory function to build the resulting Solid from a sequence of parts.

    Returns
    -------
    Solid
        A new solid with the geometry of ``to_subtract`` removed from ``to_be_subtracted``.

    Examples
    --------
    >>> from scadpy import cuboid, sphere, subtract_solid_parts, Solid

    >>> subtract_solid_parts(  # doctest: +SKIP
    ...     to_be_subtracted=cuboid(4)._parts[0],
    ...     to_subtract=sphere(radius=2)._parts[0],
    ...     make_assembly_from_parts=Solid.from_parts,
    ... )

    .. render-example::
        :name: subtract_solid_parts_example
        :example: subtract_solid_parts(to_be_subtracted=cuboid(4)._parts[0], to_subtract=sphere(radius=2)._parts[0], make_assembly_from_parts=Solid.from_parts)
        :ghost: concat_solid(solids=[cuboid(4), sphere(radius=2)])
    """
    from scadpy import Part
    from scadpy.core.part import subtract_parts

    return subtract_parts(
        to_be_subtracted=to_be_subtracted,
        to_subtract=to_subtract,
        get_part_color=lambda p: p.color,
        get_part_geometry=lambda p: p.geometry,
        subtract_geometries=lambda g1, g2: boolean_manifold(
            [g1, g2], operation="difference", check_volume=False
        ).split(),  # pyright: ignore[reportUnknownMemberType]
        make_part_from_geometry=Part[Trimesh].from_geometry,
        make_assembly_from_parts=make_assembly_from_parts,
    )
