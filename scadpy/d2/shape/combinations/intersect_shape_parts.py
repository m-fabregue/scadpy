from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from shapely import intersection_all  # pyright: ignore[reportUnknownVariableType]
from shapely.geometry.polygon import Polygon
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.core.part import Part
    from scadpy.d2.shape import Shape


@typechecked
def intersect_shape_parts(
    parts: Sequence[Part[Polygon]],
    make_assembly_from_parts: Callable[[Sequence[Part[Polygon]]], Shape],
) -> Shape:
    """Intersect a sequence of shape parts and return the resulting shape.

    Shortcut for :func:`intersect_parts`.
    See :func:`intersect_parts` for full documentation.

    Parameters
    ----------
    parts : Sequence[Part[Polygon]]
        The shape parts to intersect.
    make_assembly_from_parts : Callable[[Sequence[Part[Polygon]]], Shape]
        Factory function to build the resulting Shape from a sequence of parts.

    Returns
    -------
    Shape
        A new shape containing the geometric intersection of the input parts.

    Examples
    --------
    >>> from scadpy import (
    ...     square, circle, intersect_shape_parts, concat_shape, Shape
    ... )

    >>> intersect_shape_parts(  # doctest: +SKIP
    ...     parts=(
    ...         list(square(3)._parts)
    ...         + list(circle(radius=1.5).translate([2, 2])._parts)
    ...     ),
    ...     make_assembly_from_parts=Shape.from_parts,
    ... )

    .. render-example::
        :name: intersect_shape_parts_example
        :example: intersect_shape_parts(parts=list(square(3)._parts) + list(circle(radius=1.5).translate([2, 2])._parts), make_assembly_from_parts=Shape.from_parts)
        :ghost: concat_shape(shapes=[square(3), circle(radius=1.5).translate([2, 2])])
    """
    from scadpy import Part, are_shape_parts_intersecting, get_shape_part_bounds
    from scadpy import intersect_parts, shapely_base_geometry_to_shapely_polygons

    return intersect_parts(
        parts=parts,
        get_part_color=lambda p: p.color,
        get_part_magnitude=lambda p: p.geometry.area,
        get_part_bounds=get_shape_part_bounds,
        are_parts_intersecting=are_shape_parts_intersecting,
        get_part_geometry=lambda p: p.geometry,
        intersect_geometries=lambda g: shapely_base_geometry_to_shapely_polygons(
            intersection_all(g)
        ),
        make_part_from_geometry=Part[Polygon].from_geometry,
        make_assembly_from_parts=make_assembly_from_parts,
    )
