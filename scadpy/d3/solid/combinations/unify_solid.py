from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
def unify_solid(solids: Sequence[Solid]) -> Solid:
    """Unite a sequence of solids into a single solid using boolean union.

    All overlapping parts across the input solids are merged geometrically.
    Use :func:`concat_solid` if you want to combine solids without merging overlaps.

    Parameters
    ----------
    solids : Sequence[Solid]
        The solids to unite.

    Returns
    -------
    Solid
        A new solid containing the geometric union of all input solids.
    """
    from scadpy import Solid, unify_solid_parts
    from scadpy.core.assembly import unify_assemblies

    return unify_assemblies(
        assemblies=solids,
        get_assembly_parts=lambda assembly: assembly._parts,
        unify_parts=lambda parts: unify_solid_parts(
            parts=parts,
            make_assembly_from_parts=Solid.from_parts,
        ),
    )
