from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Solid


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
        subtract_solid_parts,
        unify_solid_parts,
    )
    from scadpy.core.assembly import exclude_assemblies

    return exclude_assemblies(
        assemblies=solids,
        get_assembly_parts=lambda assembly: assembly._parts,
        are_parts_intersecting=are_solid_parts_intersecting,
        subtract_parts=lambda part_base, parts_cutter: subtract_solid_parts(
            to_be_subtracted=part_base,
            to_subtract=parts_cutter,
            make_assembly_from_parts=Solid.from_parts,
        ),
        unify_parts=lambda parts: unify_solid_parts(
            parts=parts,
            make_assembly_from_parts=Solid.from_parts,
        ),
        concat_parts=Solid.from_parts,
    )
