from typing import Iterable

import numpy as np
from numpy.typing import NDArray


def resolve_vector_3d(
    values: float | Iterable[float],
    default_value: float,
) -> NDArray[np.float64]:
    """
    Resolves input into a 3D vector (NumPy array of length 3).

    Parameters
    ----------
    values : float or Iterable[float]
        The input values to resolve into a 3D vector. It can be:
        - A single numeric value, repeated to fill the vector.
        - An iterable of numeric values, extended or truncated to length 3.
    default_value : float
        The value used to pad the vector if `values` has fewer than 3 elements.

    Returns
    -------
    NDArray[np.float64]
        A NumPy array of shape (3,) containing the resolved 3D vector.

    Notes
    -----
    - If `values` is a single number, the result will be `[values, values, values]`.
    - If `values` has fewer than 3 elements, it is padded with `default_value`.
    - If `values` has more than 3 elements, only the first three will be kept.

    Examples
    --------
    >>> from scadpy import resolve_vector_3d
    >>> resolve_vector_3d(5, 0)
    array([5., 5., 5.])

    >>> resolve_vector_3d([1, 2], 0)
    array([1., 2., 0.])

    >>> resolve_vector_3d([3, 4, 5, 6], 0)
    array([3., 4., 5.])
    """
    from scadpy import resolve_vector

    return resolve_vector(values, default_value, 3)
