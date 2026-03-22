import numpy as np
from numpy.typing import NDArray


def z(n: float = 1) -> NDArray[np.float64]:
    """Create a vector with ``n`` on the Z-axis and ``nan`` on X and Y.

    ``nan`` acts as a sentinel meaning "keep the current value" when this
    vector is passed to transforms such as :func:`~scadpy.translate_shape` or
    :func:`~scadpy.rotate_solid`.  Only the Z component is specified; the
    other axes are left untouched.

    Parameters
    ----------
    n : float
        The value of the Z component.  Default is ``1``.

    Returns
    -------
    NDArray[np.float64]
        A NumPy array of shape ``(3,)`` representing ``[nan, nan, n]``.

    Examples
    --------
    >>> from scadpy import z
    >>> z(5)
    array([nan, nan,  5.])

    >>> z(-2.3)
    array([ nan,  nan, -2.3])
    """
    return np.array([np.nan, np.nan, n], dtype=np.float64)
