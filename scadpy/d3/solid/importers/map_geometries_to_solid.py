from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from trimesh import Trimesh

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


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
    """
    from scadpy.core.part import Part
    from scadpy.d3.solid import Solid

    return Solid.from_parts([Part[Trimesh].from_geometry(g) for g in geometries])
