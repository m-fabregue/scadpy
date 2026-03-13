from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_ring_to_part(
    shape: Shape,
) -> NDArray[np.int64]:
    """
    For each ring in the shape, return its part index

    Parameters
    ----------
    shape : Shape
        The shape to extract ring part indices from.

    Returns
    -------
    NDArray[np.float64]
        1D array of shape (n_rings,), one element per ring.

    """
    part_indices = [
        i
        for i, p in enumerate(shape._parts)  # pyright: ignore[reportPrivateUsage]
        for _ in range(1 + len(p.geometry.interiors))
    ]
    return np.array(part_indices, dtype=np.int64)
