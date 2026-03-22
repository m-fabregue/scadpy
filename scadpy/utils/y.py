import numpy as np
from numpy.typing import NDArray


def y(n: float = 1) -> NDArray[np.float64]:
    """Create a vector with ``n`` on the Y-axis and ``nan`` on X and Z.

    ``nan`` acts as a sentinel meaning "keep the current value" when this
    vector is passed to transforms such as :func:`~scadpy.translate_shape` or
    :func:`~scadpy.rotate_solid`.  Only the Y component is specified; the
    other axes are left untouched.

    Parameters
    ----------
    n : float
        The value of the Y component.  Default is ``1``.

    Returns
    -------
    NDArray[np.float64]
        A NumPy array of shape ``(3,)`` representing ``[nan, n, nan]``.

    Examples
    --------
    >>> from scadpy import y
    >>> y(5)
    array([nan,  5., nan])

    >>> y(-2.3)
    array([ nan, -2.3,  nan])
    """
    return np.array([np.nan, n, np.nan], dtype=np.float64)
