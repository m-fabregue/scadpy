from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
def intersect_solid(solids: Sequence[Solid]) -> Solid:
    """Compute the intersection of a sequence of solids.

    Only the regions shared by all input solids are kept.

    Parameters
    ----------
    solids : Sequence[Solid]
        The solids to intersect.

    Returns
    -------
    Solid
        A new solid containing only the regions present in all input solids.

    Examples
    --------
    >>> from scadpy import cuboid, sphere, intersect_solid

    >>> intersect_solid(  # doctest: +SKIP
    ...     solids=[cuboid(4), sphere(radius=2).translate(1)]
    ... )

    .. render-example::
        :name: intersect_solid
        :example: intersect_solid(solids=[cuboid(4), sphere(radius=2).translate(1)])
        :ghost: cuboid(4) + sphere(radius=2).translate(1)
    """
    from scadpy import (
        Solid,
        are_solid_parts_intersecting,
        get_solid_part_bounds,
        intersect_solid_parts,
        unify_solid_parts,
    )
    from scadpy.core.assembly import intersect_assemblies

    return intersect_assemblies(
        assemblies=solids,
        get_assembly_parts=lambda assembly: assembly._parts,
        get_part_bounds=get_solid_part_bounds,
        are_parts_intersecting=are_solid_parts_intersecting,
        intersect_parts=lambda parts: intersect_solid_parts(
            parts=parts,
            make_assembly_from_parts=Solid.from_parts,
        ),
        unify_parts=lambda parts: unify_solid_parts(
            parts=parts,
            make_assembly_from_parts=Solid.from_parts,
        ),
        concat_parts=Solid.from_parts,
    )
