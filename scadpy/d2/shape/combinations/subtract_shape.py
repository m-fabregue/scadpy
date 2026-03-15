from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Shape


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
        subtract_shape_parts,
    )
    from scadpy.core.assembly import subtract_assemblies

    return subtract_assemblies(
        to_be_subtracted=to_be_subtracted,
        to_subtract=to_subtract,
        get_assembly_parts=lambda assembly: assembly._parts,
        are_parts_intersecting=are_shape_parts_intersecting,
        subtract_parts=lambda part_base, parts_cutter: subtract_shape_parts(
            to_be_subtracted=part_base,
            to_subtract=parts_cutter,
            make_assembly_from_parts=Shape.from_parts,
        ),
        concat_parts=Shape.from_parts,
    )
