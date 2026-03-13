from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def exclude_shape(shapes: Sequence[Shape]) -> Shape:
    """Compute the symmetric difference (XOR) of a sequence of shapes.

    Keeps only the regions that belong to exactly one of the input shapes.
    Regions shared by two or more shapes are removed.

    Parameters
    ----------
    shapes : Sequence[Shape]
        The shapes to compute the symmetric difference of.

    Returns
    -------
    Shape
        A new shape containing only the non-overlapping regions of the input shapes.
    """
    from scadpy import (
        Shape,
        are_shape_parts_intersecting,
        get_shape_part_bounds,
        intersect_shape_parts,
        subtract_shape_parts,
        unify_shape_parts,
    )
    from scadpy.core.assembly import exclude_assemblies

    return exclude_assemblies(
        assemblies=shapes,
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
