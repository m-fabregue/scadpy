from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def are_bounds_overlapping(
    bounds_a: NDArray[np.float64],
    bounds_b: NDArray[np.float64],
) -> bool:
    """
    Return whether two axis-aligned bounding boxes overlap.

    Dimension-agnostic and conservative: it never misses a real overlap. Bounds
    use the flat ``[min..., max...]`` format produced by
    :func:`get_component_bounds`, so the same function serves 2D and 3D parts.
    Touching boxes are not considered overlapping.

    Parameters
    ----------
    bounds_a : NDArray[np.float64]
        First bounding box as ``[min_x, min_y, (min_z,) max_x, max_y, (max_z,)]``.
    bounds_b : NDArray[np.float64]
        Second bounding box, same format.

    Returns
    -------
    bool
        True if the two boxes overlap, False otherwise.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import are_bounds_overlapping

    >>> are_bounds_overlapping(
    ...     np.array([0.0, 0.0, 2.0, 2.0]), np.array([1.0, 1.0, 3.0, 3.0])
    ... )
    True
    >>> are_bounds_overlapping(
    ...     np.array([0.0, 0.0, 2.0, 2.0]), np.array([2.0, 2.0, 3.0, 3.0])
    ... )
    False
    >>> are_bounds_overlapping(
    ...     np.array([0.0, 0.0, 0.0, 1.0, 1.0, 1.0]),
    ...     np.array([0.5, 0.5, 0.5, 2.0, 2.0, 2.0]),
    ... )
    True
    """
    dimensions = len(bounds_a) // 2
    mins_a, maxs_a = bounds_a[:dimensions], bounds_a[dimensions:]
    mins_b, maxs_b = bounds_b[:dimensions], bounds_b[dimensions:]
    return bool(np.all(maxs_a > mins_b) and np.all(maxs_b > mins_a))
