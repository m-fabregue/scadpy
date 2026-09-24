from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.geometry import Polygon

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


def grow_shape(
    shape: Shape, distance: float, part_filter: TopologyFilter[Shape] | None = None
) -> Shape:
    """
    Grow or shrink each selected part by offsetting its boundary by a given distance.

    A positive distance expands the shape outward, a negative distance shrinks it
    inward. The offset uses mitre joins to preserve sharp corners.

    Parameters
    ----------
    shape : Shape
        The input shape whose parts will be grown.
    distance : float
        The offset distance. Positive values expand, negative values shrink.
    part_filter : TopologyFilter[Shape] | None, optional
        A boolean mask selecting which parts to grow. If None, all parts are grown.

    Returns
    -------
    Shape
        A new shape with the selected parts grown and the unselected parts unchanged.
    """
    from scadpy import Part, Shape, transform_filtered_parts
    from scadpy.d2.shape.types.utils import shapely_base_geometry_to_shapely_polygons

    def _grow_part(p):
        grown = p.geometry.buffer(distance, join_style="mitre")
        return [
            Part[Polygon].from_geometry(polygon, p.color)
            for polygon in shapely_base_geometry_to_shapely_polygons(grown)
        ]

    return transform_filtered_parts(
        assembly=shape,
        parts=shape._parts,
        part_filter=part_filter,
        transform=lambda parts: [part for p in parts for part in _grow_part(p)],
        concat_parts=Shape.from_parts,
    )
