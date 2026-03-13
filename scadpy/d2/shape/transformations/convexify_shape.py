from __future__ import annotations

from typing import TYPE_CHECKING, cast

from shapely.geometry import MultiPolygon, Polygon
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
def convexify_shape(
    shape: Shape, part_filter: TopologyFilter[Shape] | None = None
) -> Shape:
    """
    Create a new shape whose single part is the convex hull of all parts in the input shape.

    This function computes the convex hull that encloses all parts of the input shape,
    resulting in a single convex polygon. The color of the resulting part is determined
    by blending the colors of the original parts, weighted by their area.

    Parameters
    ----------
    shape : Shape
        The input shape whose parts will be merged and convexified.
    part_filter : TopologyFilter[Shape] | None, optional
        A boolean mask selecting which parts to convexify. Parts not selected are left
        unchanged. If None, all parts are convexified.

    Returns
    -------
    Shape
        A new shape consisting of the convex hull of the selected parts, plus the
        unselected parts unchanged.
    """
    from scadpy import Part, Shape, blend_part_colors, transform_filtered_parts

    return transform_filtered_parts(
        assembly=shape,
        parts=shape._parts,
        part_filter=part_filter,
        transform=lambda parts: [
            Part[Polygon].from_geometry(
                cast(Polygon, MultiPolygon([p.geometry for p in parts]).convex_hull),
                blend_part_colors(
                    parts=parts,
                    get_part_magnitude=lambda p: p.geometry.area,
                ),
            )
        ],
        concat_parts=Shape.from_parts,
    )
