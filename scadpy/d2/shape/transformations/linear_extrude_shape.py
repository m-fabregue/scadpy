from __future__ import annotations

from typing import TYPE_CHECKING

from trimesh import Trimesh
from trimesh.creation import extrude_polygon
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape
    from scadpy.d3.solid import Solid


@typechecked
def linear_extrude_shape(shape: Shape, height: float) -> Solid:
    """
    Extrude a 2D shape along the Z axis into a 3D solid.

    Each part of the shape is extruded vertically by the given height,
    producing a solid with the same cross-section throughout.

    Parameters
    ----------
    shape : Shape
        The 2D shape to extrude.
    height : float
        The extrusion height along the Z axis.

    Returns
    -------
    Solid
        A 3D solid created by extruding the shape.

    Examples
    --------
    >>> from scadpy import linear_extrude_shape, square, circle

    >>> # simple box
    >>> linear_extrude_shape(square(10), height=5) # doctest: +SKIP

    .. render-example::
        :name: linear_extrude_shape_square
        :example: linear_extrude_shape(square(10), height=5)

    >>> # tube from a hollow circle
    >>> linear_extrude_shape(  # doctest: +SKIP
    ...     circle(5) - circle(3), height=10
    ... )

    .. render-example::
        :name: linear_extrude_shape_tube
        :example: linear_extrude_shape(circle(5) - circle(3), height=10)
    """
    from scadpy import Part, Solid

    solid_parts = [
        Part[Trimesh].from_geometry(extrude_polygon(p.geometry, height), p.color)
        for p in shape._parts
    ]
    return Solid.from_parts(solid_parts)
