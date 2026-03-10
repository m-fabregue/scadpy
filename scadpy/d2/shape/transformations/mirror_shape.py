from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def mirror_shape(
    shape: Shape,
    normal: float | Iterable[float],
    pivot: float | Iterable[float] = 0,
) -> Shape:
    """Mirror a shape across a line defined by a normal vector and a pivot point.

    Parameters
    ----------
    shape : Shape
        The shape to mirror.
    normal : float | Iterable[float]
        The normal vector of the mirror line. Does not need to be normalized.
        If a single float is provided, it is broadcast to all coordinate dimensions.
    pivot : float | Iterable[float], default=0
        The point through which the mirror line passes. If a single float is
        provided, it is broadcast to all coordinate dimensions. Defaults to the origin.

    Returns
    -------
    Shape
        A new shape with all vertices mirrored across the specified line.

    Examples
    --------
    >>> from scadpy import square, mirror_shape

    >>> mirror_shape(  # doctest: +SKIP
    ...     shape=square(4), normal=[1, 0], pivot=[2, 0]
    ... )

    .. render-example::
        :name: mirror_shape
        :example: mirror_shape(shape=square(4), normal=[1, 0], pivot=[2, 0])
        :ghost: square(4)
    """
    from scadpy import mirror_vertex_coordinates

    return shape.recoordinate(
        mirror_vertex_coordinates(shape.vertex_coordinates, normal, pivot)
    )
