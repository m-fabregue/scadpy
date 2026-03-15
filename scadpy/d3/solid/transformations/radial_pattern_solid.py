from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Solid


def radial_pattern_solid(
    solid: Solid,
    count: int,
    axis: float | Iterable[float],
    angle: float = 360,
    pivot: float | Iterable[float] = 0,
) -> Solid:
    """Create a radial pattern of a solid around an axis.

    Parameters
    ----------
    solid : Solid
        The solid to repeat.
    count : int
        Number of copies.
    angle : float, default=360
        Total sweep angle in degrees.
    axis : float | Iterable[float]
        The rotation axis vector.
    pivot : float | Iterable[float], default=0
        The point around which rotation is applied.

    Returns
    -------
    Solid
        The patterned solid containing ``count`` copies.
    """
    from scadpy import concat_solid, radial_pattern_assembly, rotate_solid

    return radial_pattern_assembly(
        assembly=solid,
        count=count,
        angle=angle,
        rotate=lambda s, a: rotate_solid(s, a, axis=axis, pivot=pivot),
        concat=concat_solid,
    )
