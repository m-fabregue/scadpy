from __future__ import annotations

from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Color, Shape


@typechecked
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

    Examples
    --------
    >>> from scadpy import square, color_shape
    >>> from scadpy.color.constants import RED

    >>> color_shape(shape=square(4), color=RED) # doctest: +SKIP

    .. render-example::
        :name: color_shape
        :example: color_shape(shape=square(4), color=RED)
        :keep-color:
    """
    from scadpy import Shape, color_assembly

    return color_assembly(
        assembly=shape,
        color=color,
        get_assembly_parts=lambda assembly: assembly._parts,
        concat_parts=Shape.from_parts,
    )
