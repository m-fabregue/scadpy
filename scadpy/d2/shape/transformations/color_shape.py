from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Color, Shape


def color_shape(shape: Shape, color: Color) -> Shape:
    """Set the color of all parts in a shape.

    Parameters
    ----------
    shape : Shape
        The shape whose parts will be recolored.
    color : Color
        The RGBA color to apply to all parts.

    Returns
    -------
    Shape
        A new shape with all parts set to the given color.
    """
    from scadpy import Shape, color_assembly

    return color_assembly(
        assembly=shape,
        color=color,
        get_assembly_parts=lambda assembly: assembly._parts,
        concat_parts=Shape.from_parts,
    )
