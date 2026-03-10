from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

type TopologyFilter[A] = NDArray[np.bool_] | Callable[[A], NDArray[np.bool_]]
