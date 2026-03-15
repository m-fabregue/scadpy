from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from shapely.geometry.polygon import Polygon
from shapely.ops import unary_union

if TYPE_CHECKING:
    from scadpy.core.part import Part
    from scadpy.d2.shape import Shape


def subtract_shape_parts(
    to_be_subtracted: Part[Polygon],
    to_subtract: Sequence[Part[Polygon]],
    make_assembly_from_parts: Callable[[Sequence[Part[Polygon]]], Shape],
) -> Shape:
    """Subtract shape parts from a shape part and return the resulting shape.

    Shortcut for :func:`subtract_parts`.
    See :func:`subtract_parts` for full documentation.

    Parameters
    ----------
    to_be_subtracted : Part[Polygon]
        The part to subtract from.
    to_subtract : Sequence[Part[Polygon]]
        The parts to subtract.
    make_assembly_from_parts : Callable[[list[Part[Polygon]]], Shape]
        Factory function to build the resulting Shape from a sequence of parts.

    Returns
    -------
    Shape
        A new shape with the geometries of ``to_subtract`` removed from ``to_be_subtracted``.

    Examples
    --------
    >>> from scadpy import square, circle, subtract_shape_parts, Shape

    >>> subtract_shape_parts(
    ...     to_be_subtracted=square(4)._parts[0],
    ...     to_subtract=[circle(radius=1)._parts[0]],
    ...     make_assembly_from_parts=Shape.from_parts,
    ... ) # doctest: +SKIP

    .. render-example::
        :name: subtract_shape_parts_example
        :example: subtract_shape_parts(to_be_subtracted=square(4)._parts[0], to_subtract=[circle(radius=1)._parts[0]], make_assembly_from_parts=Shape.from_parts)
        :ghost: square(4)
    """
    from scadpy import Part, shapely_base_geometry_to_shapely_polygons, subtract_parts

    return subtract_parts(
        to_be_subtracted=to_be_subtracted,
        to_subtract=to_subtract,
        get_part_color=lambda p: p.color,
        get_part_geometry=lambda p: p.geometry,
        subtract_geometries=lambda g1, g2_list: (
            shapely_base_geometry_to_shapely_polygons(g1 - unary_union(g2_list))
        ),
        make_part_from_geometry=Part[Polygon].from_geometry,
        make_assembly_from_parts=make_assembly_from_parts,
    )
