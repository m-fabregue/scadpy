from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Shape


def unify_shape(shapes: Sequence[Shape]) -> Shape:
    """Unite a sequence of shapes into a single shape using boolean union.

    All overlapping parts across the input shapes are merged geometrically.
    Use :func:`concat_shape` if you want to combine shapes without merging overlaps.

    Parameters
    ----------
    shapes : Sequence[Shape]
        The shapes to unite.

    Returns
    -------
    Shape
        A new shape containing the geometric union of all input shapes.
    """
    from scadpy import Shape, unify_shape_parts
    from scadpy.core.assembly import unify_assemblies

    return unify_assemblies(
        assemblies=shapes,
        get_assembly_parts=lambda assembly: assembly._parts,
        unify_parts=lambda parts: unify_shape_parts(
            parts=parts,
            make_assembly_from_parts=Shape.from_parts,
        ),
    )
