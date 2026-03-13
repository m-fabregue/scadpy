from __future__ import annotations

from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
def subtract_solid(to_be_subtracted: Solid, to_subtract: Solid) -> Solid:
    """Subtract one solid from another using boolean difference.

    The geometry of ``to_subtract`` is removed from ``to_be_subtracted``.

    Parameters
    ----------
    to_be_subtracted : Solid
        The solid to subtract from.
    to_subtract : Solid
        The solid to subtract.

    Returns
    -------
    Solid
        A new solid with the geometry of ``to_subtract`` removed from ``to_be_subtracted``.
    """
    from scadpy import (
        Solid,
        are_solid_parts_intersecting,
        get_solid_part_bounds,
        intersect_solid_parts,
        subtract_solid_parts,
        unify_solid_parts,
    )
    from scadpy.core.assembly import subtract_assemblies

    return subtract_assemblies(
        to_be_subtracted=to_be_subtracted,
        to_subtract=to_subtract,
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
