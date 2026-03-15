from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy import TopologyFilter


def resolve_topology_filter[A](
    assembly: A,
    count: int,
    topology_filter: TopologyFilter[A] | None,
) -> NDArray[np.bool_] | None:
    """
    Resolve a topology filter into a boolean mask.

    A topology filter can be either a precomputed boolean mask or a callable
    that derives one from the assembly. This function normalizes both forms
    into a concrete mask and validates its length against the expected
    topology count (vertices, edges, parts, etc.).

    Parameters
    ----------
    assembly : A
        The assembly to pass to the filter if it is a callable.
    topology_filter : TopologyFilter[A] | None
        A boolean mask, a callable that produces one from the assembly,
        or None. If None, the function returns None immediately.
    count : int
        The expected length of the resulting mask. Should match the number
        of topological elements being filtered (e.g. vertex_count, edge_count,
        part count).

    Returns
    -------
    NDArray[np.bool_] | None
        The resolved boolean mask, or None if topology_filter is None.

    Raises
    ------
    ValueError
        If the resolved mask length does not match the expected count.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import resolve_topology_filter

    >>> # none passthrough
    >>> resolve_topology_filter("any", 4, None) is None
    True

    >>> # direct mask
    >>> mask = np.array([True, False, True, False])
    >>> resolve_topology_filter("any", 4, mask)
    array([ True, False,  True, False])

    >>> # callable filter
    >>> resolve_topology_filter(
    ...     "hello", 1, lambda s: np.array([len(s) > 3])
    ... )
    array([ True])

    >>> # mismatched count
    >>> resolve_topology_filter(
    ...     "any", 5, np.array([True, False])
    ... )  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: Topology filter length (2) does not match...
    """
    if topology_filter is None:
        return None
    mask = topology_filter(assembly) if callable(topology_filter) else topology_filter
    if len(mask) != count:
        raise ValueError(
            f"Topology filter length ({len(mask)}) does not match expected count ({count})."
        )
    return mask
