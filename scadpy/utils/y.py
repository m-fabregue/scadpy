import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def y(n: float) -> NDArray[np.float64]:
    """
    Creates a 3D vector along the Y-axis.

    Parameters
    ----------
    n : float
        The value of the Y component. The X and Z components are set to 0.

    Returns
    -------
    NDArray[np.float64]
        A NumPy array of shape (3,) representing the vector `[0, n, 0]`.

    Notes
    -----
    - The resulting array always has 3 elements.
    - The dtype of the array is `np.float64`.

    Examples
    --------
    >>> from scadpy import y
    >>> y(5)
    array([0., 5., 0.])

    >>> y(-2.3)
    array([ 0. , -2.3,  0. ])

    >>> y(0)
    array([0., 0., 0.])
    """
    return np.array([np.nan, n, np.nan], dtype=np.float64)
