from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
def exclude_solid(solids: Sequence[Solid]) -> Solid:
    """Compute the symmetric difference (XOR) of a sequence of solids.

    Keeps only the regions that belong to exactly one of the input solids.
    Regions shared by two or more solids are removed.

    Parameters
    ----------
    solids : Sequence[Solid]
        The solids to compute the symmetric difference of.

    Returns
    -------
    Solid
        A new solid containing only the non-overlapping regions of the input solids.
    """
    from scadpy import (
        Solid,
        are_solid_parts_intersecting,
        get_solid_part_bounds,
        intersect_solid_parts,
        subtract_solid_parts,
        unify_solid_parts,
    )
    from scadpy.core.assembly import exclude_assemblies

    return exclude_assemblies(
        assemblies=solids,
        get_assembly_parts=lambda assembly: assembly._parts,
        get_part_bounds=get_solid_part_bounds,
        are_parts_intersecting=are_solid_parts_intersecting,
        subtract_parts=lambda part_base, part_cutter: subtract_solid_parts(
            to_be_subtracted=part_base,
            to_subtract=part_cutter,
            make_assembly_from_parts=Solid.from_parts,
        ),
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
