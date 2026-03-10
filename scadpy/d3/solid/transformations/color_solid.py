from __future__ import annotations

from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Color, Solid


@typechecked
def color_solid(solid: Solid, color: Color) -> Solid:
    """Set the color of all parts in a solid.

    Parameters
    ----------
    solid : Solid
        The solid whose parts will be recolored.
    color : Color
        The RGBA color to apply to all parts.

    Returns
    -------
    Solid
        A new solid with all parts set to the given color.

    Examples
    --------
    >>> from scadpy import cuboid, color_solid
    >>> from scadpy.color.constants import RED

    >>> color_solid(solid=cuboid(4), color=RED) # doctest: +SKIP

    .. render-example::
        :name: color_solid
        :example: color_solid(solid=cuboid(4), color=RED)
        :keep-color:
    """
    from scadpy import Solid, color_assembly

    return color_assembly(
        assembly=solid,
        color=color,
        get_assembly_parts=lambda assembly: assembly._parts,
        concat_parts=Solid.from_parts,
    )
