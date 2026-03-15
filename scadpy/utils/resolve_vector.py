from numbers import Real
from typing import Iterable

import numpy as np
from numpy.typing import NDArray
from typing_extensions import cast


def resolve_vector(
    values: float | Iterable[float], default_value: float, length: int
) -> NDArray[np.float64]:
    """
    Resolves a given input into a NumPy array of a specified length.

    Parameters
    ----------
    values : float or Iterable[float]
        The input values to be resolved. This can be:

        - A single numeric value, which will be repeated to fill the array.
        - An iterable of numeric values, which will be extended or truncated to match the desired length.
    default_value : float
        The value to use for padding if the input `values` is shorter than
        the required length.
    length : int
        The desired length of the output array.

    Returns
    -------
    NDArray[np.float64]
        A NumPy array of the specified length containing the resolved values.
        If `values` is shorter than `length`, it is padded with `default_value`.
        If it is longer, it is truncated.

    Notes
    -----
    - The resulting array always has exactly `length` elements.

    Examples
    --------
    >>> from scadpy import resolve_vector
    >>> resolve_vector(5, 0, 3)
    array([5., 5., 5.])

    >>> resolve_vector([1, 2], 0, 5)
    array([1., 2., 0., 0., 0.])

    >>> resolve_vector([1, 2, 3, 4, 5, 6], 0, 4)
    array([1., 2., 3., 4.])
    """
    result = np.full(length, default_value, dtype=float)

    if isinstance(values, Real):
        result[:] = float(values)
    else:
        vals = np.fromiter(cast(Iterable[float], values), dtype=float)
        n = min(len(vals), length)
        result[:n] = vals[:n]

    # replace np.nan with default_value
    result = np.where(np.isnan(result), default_value, result)
    return result
