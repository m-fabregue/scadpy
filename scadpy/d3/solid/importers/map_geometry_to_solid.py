from __future__ import annotations

from typing import TYPE_CHECKING

from trimesh import Trimesh

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


def map_geometry_to_solid(geometry: Trimesh) -> Solid:
    """Map a single Trimesh geometry to a solid.

    Shortcut for :func:`map_geometries_to_solid` with a single geometry.

    Parameters
    ----------
    geometry : Trimesh
        The geometry to map.

    Returns
    -------
    Solid
        A new solid containing the single geometry as a part.
    """
    from scadpy.d3.solid.importers import map_geometries_to_solid

    return map_geometries_to_solid([geometry])
