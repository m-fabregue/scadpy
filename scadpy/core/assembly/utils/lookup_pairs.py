from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def lookup_pairs(
    queries: NDArray[np.int64],
    haystack: NDArray[np.int64],
) -> NDArray[np.int64]:
    """
    For each queried pair, return its index in the haystack.

    Each pair ``(a, b)`` is encoded as ``a * n + b`` where ``n`` is
    ``max(haystack) + 1``, then looked up via binary search. This is
    fully vectorized with no Python loops.

    Parameters
    ----------
    queries : NDArray[np.int64]
        2D array of shape ``(n_queries, 2)``. Pairs to look up.
    haystack : NDArray[np.int64]
        2D array of shape ``(n_items, 2)``. The reference pairs.
        Each pair must appear exactly once.

    Returns
    -------
    NDArray[np.int64]
        1D array of shape ``(n_queries,)``. Each entry is the index
        in ``haystack`` of the corresponding query pair.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import lookup_pairs

    >>> haystack = np.array(
    ...     [[0, 1], [1, 0], [1, 2], [2, 1], [2, 0], [0, 2]],
    ...     dtype=np.int64,
    ... )
    >>> queries = np.array([[2, 0], [0, 1], [1, 2]], dtype=np.int64)
    >>> lookup_pairs(queries, haystack)
    array([4, 0, 2])
    """
    if len(queries) == 0:
        return np.empty(0, dtype=np.int64)

    n = int(haystack.max()) + 1
    haystack_keys = haystack[:, 0] * n + haystack[:, 1]
    sort_order = np.argsort(haystack_keys)
    haystack_keys_sorted = haystack_keys[sort_order]

    query_keys = queries[:, 0] * n + queries[:, 1]
    return sort_order[np.searchsorted(haystack_keys_sorted, query_keys)]
