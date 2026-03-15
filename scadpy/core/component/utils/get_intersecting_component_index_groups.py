from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from numpy.typing import NDArray
from rtree import index as rtree_index


def get_intersecting_component_index_groups[C](
    components: Sequence[C],
    get_component_bounds: Callable[[C], NDArray[np.float64]],
    are_components_intersecting: Callable[[C, C], bool],
) -> list[list[int]]:
    """
    Find groups of mutually intersecting components by their indices.

    This function uses an R-tree for efficient spatial indexing and a graph traversal
    to group components that are directly or indirectly intersecting. It is fully
    generic and uses dependency injection for all domain-specific operations.

    Parameters
    ----------
    components : Sequence[C]
        Sequence of components to group.
    get_component_bounds : Callable[[C], NDArray[np.float64]]
        Function to extract the bounding box of a component (as [minx, miny, maxx, maxy]).
    are_components_intersecting : Callable[[C, C], bool]
        Function to determine if two components intersect.

    Returns
    -------
    list[list[int]]
        A list of groups, each group being a list of indices into the original components
        sequence, where all components in a group are mutually intersecting (directly or indirectly).

    Examples
    --------
    >>> from scadpy import get_intersecting_component_index_groups

    >>> components = [
    ...     {'bounds': [0, 0, 2, 2]},
    ...     {'bounds': [1, 1, 3, 3]},
    ...     {'bounds': [5, 5, 6, 6]}
    ... ]
    ...
    >>> def are_intersecting(c1, c2):
    ...     b1, b2 = c1['bounds'], c2['bounds']
    ...     return not (b1[2] <= b2[0] or b2[2] <= b1[0] or
    ...                 b1[3] <= b2[1] or b2[3] <= b1[1])
    ...
    >>> get_intersecting_component_index_groups(
    ...     components,
    ...     get_component_bounds=lambda c: c['bounds'],
    ...     are_components_intersecting=are_intersecting
    ... )
    [[0, 1], [2]]

    >>> get_intersecting_component_index_groups(
    ...     [],
    ...     get_component_bounds=lambda c: c['bounds'],
    ...     are_components_intersecting=are_intersecting
    ... )
    []
    """
    if not components:
        return []

    first_bounding_box = len(get_component_bounds(components[0]))

    properties = rtree_index.Property()
    properties.dimension = int(first_bounding_box / 2)
    rtree = rtree_index.Index(properties=properties)
    for i, component in enumerate(components):
        rtree.insert(i, get_component_bounds(component))

    neighbors: list[set[int]] = [set() for _ in range(len(components))]

    for i, component_i in enumerate(components):
        component_i_bounds = get_component_bounds(component_i)
        candidate_indices = list(rtree.intersection(component_i_bounds))

        for j in candidate_indices:
            if j <= i:
                # avoid double counting
                continue
            component_j = components[j]
            if are_components_intersecting(component_i, component_j):
                neighbors[i].add(j)
                neighbors[j].add(i)

    groups: list[list[int]] = []
    visited: set[int] = set()
    for i in range(len(components)):
        if i not in visited:
            stack = [i]
            group: list[int] = []
            while stack:
                idx = stack.pop()
                if idx not in visited:
                    visited.add(idx)
                    group.append(idx)
                    stack.extend(neighbors[idx] - visited)
            groups.append(group)

    return groups
