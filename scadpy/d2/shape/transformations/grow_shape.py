from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.geometry import Polygon

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter

# Mitre joins can overshoot at concave/thin features when the buffer is
# eroding (negative distance), producing self-intersections. GEOS resolves
# these internally so the result stays topologically valid, but it can do so
# by splitting the output into a real polygon plus a handful of numerically
# degenerate sliver fragments (areas many orders of magnitude below any real
# geometry) right around the distance where a thin bridge collapses. Left in,
# these slivers triangulate into degenerate 3D geometry with no validation
# anywhere downstream (Solid.from_parts and to_stl_file are unchecked), so
# broken solids can slip through silently until some unrelated later
# operation (translate, rotate, ...) happens to trigger a manifold check.
#
# The threshold is scaled by distance**2 rather than a fixed epsilon so it
# adapts to both the requested offset and the model's own unit scale, instead
# of assuming millimetres. In practice degenerate slivers measure ~1e-13 to
# ~1e-17 of distance**2 (essentially floating-point noise); 1e-3 leaves many
# orders of magnitude of headroom before a real, intentionally tiny detail
# would ever be at risk of being dropped.
_DEGENERATE_AREA_RATIO = 1e-3


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

    min_area = (distance**2) * _DEGENERATE_AREA_RATIO

    def _grow_part(p):
        grown = p.geometry.buffer(distance, join_style="mitre")
        return [
            Part[Polygon].from_geometry(polygon, p.color)
            for polygon in shapely_base_geometry_to_shapely_polygons(grown)
            if polygon.area >= min_area
        ]

    return transform_filtered_parts(
        assembly=shape,
        parts=shape._parts,
        part_filter=part_filter,
        transform=lambda parts: [part for p in parts for part in _grow_part(p)],
        concat_parts=Shape.from_parts,
    )
