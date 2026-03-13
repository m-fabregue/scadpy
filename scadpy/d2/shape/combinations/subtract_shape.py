from __future__ import annotations

from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def subtract_shape(to_be_subtracted: Shape, to_subtract: Shape) -> Shape:
    """Subtract one shape from another using boolean difference.

    The geometry of ``to_subtract`` is removed from ``to_be_subtracted``.

    Parameters
    ----------
    to_be_subtracted : Shape
        The shape to subtract from.
    to_subtract : Shape
        The shape to subtract.

    Returns
    -------
    Shape
        A new shape with the geometry of ``to_subtract`` removed from ``to_be_subtracted``.
    """
    from scadpy import (
        Shape,
        are_shape_parts_intersecting,
        get_shape_part_bounds,
        intersect_shape_parts,
        subtract_shape_parts,
        unify_shape_parts,
    )
    from scadpy.core.assembly import subtract_assemblies

    return subtract_assemblies(
        to_be_subtracted=to_be_subtracted,
        to_subtract=to_subtract,
        get_assembly_parts=lambda assembly: assembly._parts,
        get_part_bounds=get_shape_part_bounds,
        are_parts_intersecting=are_shape_parts_intersecting,
        subtract_parts=lambda part_base, part_cutter: subtract_shape_parts(
            to_be_subtracted=part_base,
            to_subtract=part_cutter,
            make_assembly_from_parts=Shape.from_parts,
        ),
        intersect_parts=lambda parts: intersect_shape_parts(
            parts=parts,
            make_assembly_from_parts=Shape.from_parts,
        ),
        unify_parts=lambda parts: unify_shape_parts(
            parts=parts,
            make_assembly_from_parts=Shape.from_parts,
        ),
        concat_parts=Shape.from_parts,
    )
