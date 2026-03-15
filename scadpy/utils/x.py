import numpy as np
from numpy.typing import NDArray


def x(n: float = 1) -> NDArray[np.float64]:
    """
    Creates a 3D vector along the X-axis.

    Parameters
    ----------
    n : float
        The value of the X component. The Y and Z components are set to 0.

    Returns
    -------
    NDArray[np.float64]
        A NumPy array of shape (3,) representing the vector `[n, 0, 0]`.

    Notes
    -----
    - The resulting array always has 3 elements.
    - The dtype of the array is `np.float64`.

    Examples
    --------
    >>> from scadpy import x
    >>> x(5)
    array([5., 0., 0.])

    >>> x(-2.3)
    array([-2.3,  0. ,  0. ])

    >>> x(0)
    array([0., 0., 0.])
    """
    return np.array([n, np.nan, np.nan], dtype=np.float64)
