from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.geometry import Polygon

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def map_geometry_to_shape(geometry: Polygon) -> Shape:
    """Map a single polygon to a shape.

    Shortcut for :func:`map_geometries_to_shape` with a single polygon.

    Parameters
    ----------
    geometry : Polygon
        The polygon to map.

    Returns
    -------
    Shape
        A new shape containing the single valid, oriented polygon.

    """
    from scadpy.d2.shape.importers import map_geometries_to_shape

    return map_geometries_to_shape([geometry])
