from __future__ import annotations

from typing import TYPE_CHECKING

from trimesh import Trimesh
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


@typechecked
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

    Examples
    --------
    >>> from scadpy import cuboid, map_geometry_to_solid

    >>> map_geometry_to_solid(  # doctest: +SKIP
    ...     cuboid(4)._parts[0].geometry
    ... )

    .. render-example::
        :name: map_geometry_to_solid
        :example: map_geometry_to_solid(cuboid(4)._parts[0].geometry)
    """
    from scadpy.d3.solid.importers import map_geometries_to_solid

    return map_geometries_to_solid([geometry])
