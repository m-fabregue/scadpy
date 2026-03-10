import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def z(n: float) -> NDArray[np.float64]:
    """
    Creates a 3D vector along the Z-axis.

    Parameters
    ----------
    n : float
        The value of the Z component. The X and Y components are set to 0.

    Returns
    -------
    NDArray[np.float64]
        A NumPy array of shape (3,) representing the vector `[0, 0, n]`.

    Notes
    -----
    - The resulting array always has 3 elements.
    - The dtype of the array is `np.float64`.

    Examples
    --------
    >>> from scadpy import z
    >>> z(5)
    array([0., 0., 5.])

    >>> z(-2.3)
    array([ 0. ,  0. , -2.3])

    >>> z(0)
    array([0., 0., 0.])
    """
    return np.array([np.nan, np.nan, n], dtype=np.float64)
