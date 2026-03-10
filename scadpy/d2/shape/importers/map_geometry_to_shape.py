from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.geometry import Polygon
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
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

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import map_geometry_to_shape

    >>> map_geometry_to_shape(  # doctest: +SKIP
    ...     Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])
    ... )

    .. render-example::
        :name: map_geometry_to_shape
        :example: map_geometry_to_shape(Polygon([(0, 0), (4, 0), (4, 4), (0, 4)]))
    """
    from scadpy.d2.shape.importers import map_geometries_to_shape

    return map_geometries_to_shape([geometry])
