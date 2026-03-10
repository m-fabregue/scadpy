from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def get_shape_ring_types(
    shape: Shape,
) -> NDArray[np.object_]:
    """
    For each ring in the shape, return its type ('exterior' or 'interior').

    Parameters
    ----------
    shape : Shape
        The shape to extract ring types from.

    Returns
    -------
    NDArray[np.object_]
        1D array of shape (n_rings,), one element per ring.

    Examples
    --------
    >>> from scadpy import get_shape_ring_types, square

    >>> # square with a hole (exterior + interior)
    >>> # unioned with a separate square (exterior only)
    >>> shape = (square(2) - square(1)) | square(1).translate([5, 0])
    >>> get_shape_ring_types(shape)  # doctest: +NORMALIZE_WHITESPACE
    array(['exterior', 'interior', 'exterior'], dtype=object)
    """
    # extract and flatmap polygon ring types
    ring_types = [
        ring_type
        for g in [p.geometry for p in shape._parts]  # pyright: ignore[reportPrivateUsage]
        for ring_type in ["exterior"] + ["interior"] * len(g.interiors)
    ]
    return np.array(ring_types, dtype=np.object_)
