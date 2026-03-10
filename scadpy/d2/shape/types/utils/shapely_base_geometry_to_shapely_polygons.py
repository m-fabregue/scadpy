from shapely.geometry import MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient
from typeguard import typechecked


@typechecked
def shapely_base_geometry_to_shapely_polygons(
    base_geometry: BaseGeometry,
) -> list[Polygon]:
    if base_geometry.is_empty:
        return []

    if isinstance(base_geometry, Polygon):
        # normalize orientation: exterior CCW, interiors CW (shapely convention)
        return [orient(base_geometry, sign=1.0)]

    if isinstance(base_geometry, MultiPolygon):
        return [
            polygon
            for geom in base_geometry.geoms
            for polygon in shapely_base_geometry_to_shapely_polygons(geom)
        ]

    return []
