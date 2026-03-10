from collections.abc import Iterable

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def resolve_vector_2d(
    values: float | Iterable[float],
    default_value: float,
) -> NDArray[np.float64]:
    """
    Resolves input into a 2D vector (NumPy array of length 2).

    Parameters
    ----------
    values : float or Iterable[float]
        The input values to resolve into a 2D vector. It can be:
        - A single numeric value, repeated to fill the vector.
        - An iterable of numeric values, extended or truncated to length 2.
    default_value : float
        The value used to pad the vector if `values` has fewer than 2 elements.

    Returns
    -------
    NDArray[np.float64]
        A NumPy array of shape (2,) containing the resolved 2D vector.

    Notes
    -----
    - If `values` is a single number, the result will be `[values, values]`.
    - If `values` has one element, the result will be `[values[0], default_value]`.
    - If `values` has more than 2 elements, only the first two will be kept.

    Examples
    --------
    >>> from scadpy import resolve_vector_2d
    >>> resolve_vector_2d(5, 0)
    array([5., 5.])

    >>> resolve_vector_2d([1], 0)
    array([1., 0.])

    >>> resolve_vector_2d([3, 4, 5], 0)
    array([3., 4.])
    """
    from scadpy.utils.resolve_vector import resolve_vector

    return resolve_vector(values, default_value, 2)
