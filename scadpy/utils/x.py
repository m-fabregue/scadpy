import numpy as np
from numpy.typing import NDArray


def x(n: float = 1) -> NDArray[np.float64]:
    """Create a vector with ``n`` on the X-axis and ``nan`` on Y and Z.

    ``nan`` acts as a sentinel meaning "keep the current value" when this
    vector is passed to transforms such as :func:`~scadpy.translate_shape` or
    :func:`~scadpy.rotate_solid`.  Only the X component is specified; the
    other axes are left untouched.

    Parameters
    ----------
    n : float
        The value of the X component.  Default is ``1``.

    Returns
    -------
    NDArray[np.float64]
        A NumPy array of shape ``(3,)`` representing ``[n, nan, nan]``.

    Examples
    --------
    >>> from scadpy import x
    >>> x(5)
    array([ 5., nan, nan])

    >>> x(-2.3)
    array([-2.3,  nan,  nan])
    """
    return np.array([n, np.nan, np.nan], dtype=np.float64)
