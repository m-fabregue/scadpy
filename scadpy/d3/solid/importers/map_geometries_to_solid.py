from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from trimesh import Trimesh
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


@typechecked
def map_geometries_to_solid(geometries: Sequence[Trimesh]) -> Solid:
    """Map a sequence of Trimesh geometries to a solid.

    Parameters
    ----------
    geometries : Sequence[Trimesh]
        The geometries to map.

    Returns
    -------
    Solid
        A new solid containing all input geometries as parts.

    Examples
    --------
    >>> from scadpy import cuboid, map_geometries_to_solid

    >>> map_geometries_to_solid(  # doctest: +SKIP
    ...     [cuboid(4)._parts[0].geometry]
    ... )

    .. render-example::
        :name: map_geometries_to_solid
        :example: map_geometries_to_solid([cuboid(4)._parts[0].geometry])
    """
    from scadpy.core.part import Part
    from scadpy.d3.solid import Solid

    return Solid.from_parts([Part[Trimesh].from_geometry(g) for g in geometries])
