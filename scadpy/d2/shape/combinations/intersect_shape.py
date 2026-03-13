from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def intersect_shape(shapes: Sequence[Shape]) -> Shape:
    """Compute the intersection of a sequence of shapes.

    Only the regions shared by all input shapes are kept.

    Parameters
    ----------
    shapes : Sequence[Shape]
        The shapes to intersect.

    Returns
    -------
    Shape
        A new shape containing only the regions present in all input shapes.
    """
    from scadpy import (
        Shape,
        are_shape_parts_intersecting,
        get_shape_part_bounds,
        intersect_shape_parts,
        unify_shape_parts,
    )
    from scadpy.core.assembly import intersect_assemblies

    return intersect_assemblies(
        assemblies=shapes,
        get_assembly_parts=lambda assembly: assembly._parts,
        get_part_bounds=get_shape_part_bounds,
        are_parts_intersecting=are_shape_parts_intersecting,
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
