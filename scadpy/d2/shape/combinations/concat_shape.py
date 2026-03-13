from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def concat_shape(shapes: Sequence[Shape]) -> Shape:
    """Concatenate a sequence of shapes into a single shape without any boolean operation.

    All parts from all input shapes are merged into a single shape. Parts that
    overlap are not merged geometrically — use :func:`unify_shape` for that.

    Parameters
    ----------
    shapes : Sequence[Shape]
        The shapes to concatenate.

    Returns
    -------
    Shape
        A new shape containing all parts from all input shapes.
    """
    from scadpy import Shape
    from scadpy.core.assembly import concat_assemblies

    return concat_assemblies(
        assemblies=shapes,
        get_assembly_parts=lambda a: a._parts,
        concat_parts=Shape.from_parts,
    )
