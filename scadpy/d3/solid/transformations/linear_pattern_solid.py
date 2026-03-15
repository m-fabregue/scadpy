from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy import Solid


def linear_pattern_solid(
    solid: Solid,
    counts: int | Sequence[int],
    steps: NDArray[np.float64] | Sequence[NDArray[np.float64]],
) -> Solid:
    """Create a linear (grid) pattern of a solid along one or more axes.

    Parameters
    ----------
    solid : Solid
        The solid to repeat.
    counts : int | Sequence[int]
        Number of copies along each axis. A single int creates a 1D pattern.
        A sequence of ints creates a 2D or 3D grid pattern.
    steps : NDArray[np.float64] | Sequence[NDArray[np.float64]]
        Translation vector between consecutive copies along each axis.
        Must be a single vector when ``counts`` is an int, or a sequence of
        vectors matching the length of ``counts``.

    Returns
    -------
    Solid
        The patterned solid containing ``prod(counts)`` copies.
    """
    from scadpy import concat_solid, linear_pattern_assembly, translate_solid

    return linear_pattern_assembly(
        assembly=solid,
        counts=counts,
        steps=steps,
        translate=lambda solid, translation: translate_solid(solid, translation),
        concat=concat_solid,
        dimensions=3,
    )
