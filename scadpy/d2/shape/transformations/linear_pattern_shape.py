from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy import Shape


def linear_pattern_shape(
    shape: Shape,
    counts: int | Sequence[int],
    steps: NDArray[np.float64] | Sequence[NDArray[np.float64]],
) -> Shape:
    """Create a linear (grid) pattern of a shape along one or more axes.

    Parameters
    ----------
    shape : Shape
        The shape to repeat.
    counts : int | Sequence[int]
        Number of copies along each axis. A single int creates a 1D pattern.
        A sequence of ints creates a 2D or 3D grid pattern.
    steps : NDArray[np.float64] | Sequence[NDArray[np.float64]]
        Translation vector between consecutive copies along each axis.
        Must be a single vector when ``counts`` is an int, or a sequence of
        vectors matching the length of ``counts``.

    Returns
    -------
    Shape
        The patterned shape containing ``prod(counts)`` copies.
    """
    from scadpy import concat_shape, linear_pattern_assembly, translate_shape

    return linear_pattern_assembly(
        assembly=shape,
        counts=counts,
        steps=steps,
        translate=lambda shape, translation: translate_shape(shape, translation),
        concat=concat_shape,
        dimensions=2,
    )
