from shapely.geometry import MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry
from typeguard import typechecked


@typechecked
def shapely_base_geometry_to_shapely_polygons(
    base_geometry: BaseGeometry,
) -> list[Polygon]:
    """Recursively extract all polygons from a Shapely geometry.

    Handles :class:`~shapely.geometry.Polygon` and
    :class:`~shapely.geometry.MultiPolygon`; returns an empty list for empty
    or unsupported geometry types.

    Parameters
    ----------
    base_geometry : BaseGeometry
        Any Shapely geometry.

    Returns
    -------
    list[Polygon]
        Flat list of all non-empty polygons found in *base_geometry*.

    Examples
    --------
    >>> from shapely.geometry import MultiPolygon, Polygon
    >>> from scadpy.d2.shape.utils import (
    ...     shapely_base_geometry_to_shapely_polygons,
    ... )

    >>> polygons = shapely_base_geometry_to_shapely_polygons(
    ...     MultiPolygon([
    ...         Polygon([(0, 0), (1, 0), (1, 1)]),
    ...         Polygon([(2, 0), (3, 0), (3, 1)]),
    ...     ])
    ... )
    >>> len(polygons)
    2
    """
    if base_geometry.is_empty:
        return []

    if isinstance(base_geometry, Polygon):
        return [base_geometry]

    if isinstance(base_geometry, MultiPolygon):
        return [
            polygon
            for geom in base_geometry.geoms
            for polygon in shapely_base_geometry_to_shapely_polygons(geom)
        ]

    return []
