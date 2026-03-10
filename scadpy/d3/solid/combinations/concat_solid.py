from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
def concat_solid(solids: Sequence[Solid]) -> Solid:
    """Concatenate a sequence of solids into a single solid without any boolean operation.

    All parts from all input solids are merged into a single solid. Parts that
    overlap are not merged geometrically — use :func:`unify_solid` for that.

    Parameters
    ----------
    solids : Sequence[Solid]
        The solids to concatenate.

    Returns
    -------
    Solid
        A new solid containing all parts from all input solids.

    Examples
    --------
    >>> from scadpy import cuboid, sphere, concat_solid

    >>> concat_solid(  # doctest: +SKIP
    ...     solids=[cuboid(4), sphere(radius=2).translate([3, 2, 0])]
    ... )

    .. render-example::
        :name: concat_solid
        :example: concat_solid(solids=[cuboid(4), sphere(radius=2).translate([3, 2, 0])])
    """
    from scadpy import Solid
    from scadpy.core.assembly import concat_assemblies

    return concat_assemblies(
        assemblies=solids,
        get_assembly_parts=lambda assembly: assembly._parts,
        concat_parts=Solid.from_parts,
    )
