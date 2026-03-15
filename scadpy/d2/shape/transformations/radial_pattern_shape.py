from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Shape


def radial_pattern_shape(
    shape: Shape,
    count: int,
    angle: float = 360,
    pivot: float | Iterable[float] = 0,
) -> Shape:
    """Create a radial pattern of a shape around the origin.

    Parameters
    ----------
    shape : Shape
        The shape to repeat.
    count : int
        Number of copies.
    angle : float, default=360
        Total sweep angle in degrees.
    pivot : float | Iterable[float], default=0
        The point around which rotation is applied.

    Returns
    -------
    Shape
        The patterned shape containing ``count`` copies.
    """
    from scadpy import concat_shape, radial_pattern_assembly, rotate_shape

    return radial_pattern_assembly(
        assembly=shape,
        count=count,
        angle=angle,
        rotate=lambda s, a: rotate_shape(s, a, pivot=pivot),
        concat=concat_shape,
    )
