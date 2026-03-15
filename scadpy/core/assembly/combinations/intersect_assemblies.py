from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence

import numpy as np
from numpy.typing import NDArray


def intersect_assemblies[A, P](
    assemblies: Sequence[A],
    get_assembly_parts: Callable[[A], Iterable[P]],
    get_part_bounds: Callable[[P], NDArray[np.float64]],
    are_parts_intersecting: Callable[[P, P], bool],
    intersect_parts: Callable[[Sequence[P]], A],
    unify_parts: Callable[[Sequence[P]], A],
    concat_parts: Callable[[Sequence[P]], A],
) -> A:
    """
    Compute the intersection of multiple assemblies, keeping only intersections that involve at least one part from each assembly.

    This function is fully generic and uses dependency injection for all domain-specific
    operations, making it suitable for a wide range of applications (2D, 3D, CAD, etc.).
    Only groups of parts that include at least one part from each input assembly are intersected and included in the result.

    Parameters
    ----------
    assemblies : Sequence[A]
        Sequence of assembly objects to intersect.
    get_assembly_parts : Callable[[A], Iterable[P]]
        Function that extracts parts from an assembly.
    get_part_bounds : Callable[[P], NDArray[np.float64]]
        Function to extract the bounding box of a part.
    are_parts_intersecting : Callable[[P, P], bool]
        Function to determine if two parts intersect.
    intersect_parts : Callable[[Sequence[P]], A]
        Function to compute the intersection of a group of parts.
    unify_parts : Callable[[Sequence[P]], A]
        Function to unify (union) overlapping parts within an assembly.
    concat_parts : Callable[[Sequence[P]], A]
        Function to concatenate a sequence of parts into a new assembly.

    Returns
    -------
    A
        The assembly object containing all intersections involving at least one part from each input assembly.

    Examples
    --------
    >>> from scadpy import intersect_assemblies

    >>> assemblies = [
    ...     [{'bounds': [0, 0, 2, 2]}],
    ...     [{'bounds': [1, 1, 3, 3]}, {'bounds': [5, 5, 6, 6]}]
    ... ]
    ...
    >>> def are_intersecting(p1, p2):
    ...     b1, b2 = p1['bounds'], p2['bounds']
    ...     return not (b1[2] <= b2[0] or b2[2] <= b1[0] or
    ...                 b1[3] <= b2[1] or b2[3] <= b1[1])
    ...
    >>> def intersect_geometries(geometries):
    ...     if len(geometries) == 1:
    ...         return [geometries[0]]
    ...     minx = max(g[0] for g in geometries)
    ...     miny = max(g[1] for g in geometries)
    ...     maxx = min(g[2] for g in geometries)
    ...     maxy = min(g[3] for g in geometries)
    ...     if minx < maxx and miny < maxy:
    ...         return [[minx, miny, maxx, maxy]]
    ...     return []
    ...
    >>> def intersect_parts(parts):
    ...     geometries = [p['bounds'] for p in parts]
    ...     for g in intersect_geometries(geometries):
    ...         return [{'bounds': g}]
    ...
    >>> intersect_assemblies(
    ...     assemblies,
    ...     get_assembly_parts=lambda a: a,
    ...     get_part_bounds=lambda p: p['bounds'],
    ...     are_parts_intersecting=are_intersecting,
    ...     intersect_parts=intersect_parts,
    ...     unify_parts=lambda p: p,
    ...     concat_parts=lambda p: p
    ... )
    [{'bounds': [1, 1, 2, 2]}]
    """
    from scadpy.core.assembly import concat_assemblies, unify_assemblies
    from scadpy.core.component import get_intersecting_component_index_groups

    unified_assemblies = [
        unify_assemblies(
            [a],
            get_assembly_parts=get_assembly_parts,
            unify_parts=unify_parts,
        )
        for a in assemblies
    ]
    part_with_assembly_index: list[tuple[P, int]] = [
        (p, i) for i, a in enumerate(unified_assemblies) for p in get_assembly_parts(a)
    ]
    parts = [p for p, _ in part_with_assembly_index]
    assembly_indices = [i for _, i in part_with_assembly_index]

    intersecting_part_index_groups: list[list[int]] = (
        get_intersecting_component_index_groups(
            parts,
            get_component_bounds=get_part_bounds,
            are_components_intersecting=are_parts_intersecting,
        )
    )

    # keep only groups that have at least one part from each assembly
    num_assemblies = len(assemblies)
    intersected_assemblies: list[A] = []
    for group in intersecting_part_index_groups:
        assembly_ids_in_group = {assembly_indices[idx] for idx in group}
        if len(assembly_ids_in_group) == num_assemblies:
            group_parts = [parts[idx] for idx in group]
            intersected_assemblies.append(intersect_parts(group_parts))

    return concat_assemblies(
        assemblies=intersected_assemblies,
        get_assembly_parts=get_assembly_parts,
        concat_parts=concat_parts,
    )
