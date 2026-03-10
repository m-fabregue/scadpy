from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def subtract_assemblies[A, P](
    to_be_subtracted: A,
    to_subtract: A,
    get_assembly_parts: Callable[[A], Iterable[P]],
    get_part_bounds: Callable[[P], NDArray[np.float64]],
    are_parts_intersecting: Callable[[P, P], bool],
    subtract_parts: Callable[[P, P], A],
    intersect_parts: Callable[[Sequence[P]], A],
    unify_parts: Callable[[Sequence[P]], A],
    concat_parts: Callable[[Sequence[P]], A],
) -> A:
    """
    Subtract the geometry of all parts in one assembly from all parts in another assembly.

    This function is fully generic and uses dependency injection for all domain-specific
    operations, making it suitable for a wide range of applications (2D, 3D, CAD, etc.).
    For each part in the first assembly, all intersecting parts from the second assembly are subtracted.

    Parameters
    ----------
    to_be_subtracted : A
        The assembly whose parts will be subtracted from.
    to_subtract : A
        The assembly whose parts will be subtracted.
    get_assembly_parts : Callable[[A], Iterable[P]]
        Function that extracts parts from an assembly.
    get_part_bounds : Callable[[P], NDArray[np.float64]]
        Function to extract the bounding box of a part.
    are_parts_intersecting : Callable[[P, P], bool]
        Function to determine if two parts intersect.
    subtract_parts : Callable[[P, P], A]
        Function to subtract one part from another, returning an assembly.
    intersect_parts : Callable[[Sequence[P]], A]
        Function to compute the intersection of a group of parts.
    unify_parts : Callable[[Sequence[P]], A]
        Function to unify (union) overlapping parts within an assembly.
    concat_parts : Callable[[Sequence[P]], A]
        Function to concatenate a sequence of parts into a new assembly.

    Returns
    -------
    A
        The assembly object containing all subtracted parts.

    Examples
    --------
    >>> from scadpy import subtract_assemblies

    >>> assembly1 = [{'bounds': [0, 0, 3, 3]}]
    >>> assembly2 = [{'bounds': [1, 1, 2, 2]}]
    ...
    >>> def are_intersecting(p1, p2):
    ...     b1, b2 = p1['bounds'], p2['bounds']
    ...     return not (b1[2] <= b2[0] or b2[2] <= b1[0] or
    ...                 b1[3] <= b2[1] or b2[3] <= b1[1])
    ...
    >>> def subtract_geometries(g1, g2):
    ...     if (g2[0] > g1[0] and g2[2] < g1[2]
    ...             and g2[1] > g1[1] and g2[3] < g1[3]):
    ...         return [
    ...             [g1[0], g1[1], g2[0], g1[3]],  # left
    ...             [g2[2], g1[1], g1[2], g1[3]],  # right
    ...             [g2[0], g1[1], g2[2], g2[1]],  # bottom
    ...             [g2[0], g2[3], g2[2], g1[3]],  # top
    ...         ]
    ...     return [g1]
    ...
    >>> def subtract_parts(p1, p2):
    ...     geometries = subtract_geometries(
    ...         p1['bounds'], p2['bounds']
    ...     )
    ...     return [{'bounds': g} for g in geometries]
    ...
    >>> result = subtract_assemblies(
    ...     assembly1, assembly2,
    ...     get_assembly_parts=lambda a: a,
    ...     get_part_bounds=lambda p: p['bounds'],
    ...     are_parts_intersecting=are_intersecting,
    ...     subtract_parts=subtract_parts,
    ...     intersect_parts=lambda p: p,
    ...     unify_parts=lambda p: p,
    ...     concat_parts=lambda p: p
    ... )
    >>> result == [
    ...     {'bounds': [0, 0, 1, 3]},
    ...     {'bounds': [2, 0, 3, 3]},
    ...     {'bounds': [1, 0, 2, 1]},
    ...     {'bounds': [1, 2, 2, 3]}
    ... ]
    True
    """

    from scadpy.core.assembly import (
        concat_assemblies,
        intersect_assemblies,
        unify_assemblies,
    )

    unified_to_subtract = unify_assemblies(
        [to_subtract],
        get_assembly_parts=get_assembly_parts,
        unify_parts=unify_parts,
    )

    parts_to_be_subtracted = get_assembly_parts(to_be_subtracted)
    parts_to_subtract = get_assembly_parts(unified_to_subtract)

    subtracted_assemblies: list[A] = []
    for part_to_be_subtracted in parts_to_be_subtracted:
        intersecting_parts_to_subtract = [
            part
            for part in parts_to_subtract
            if are_parts_intersecting(part_to_be_subtracted, part)
        ]
        if not intersecting_parts_to_subtract:
            subtracted_assemblies.append(concat_parts([part_to_be_subtracted]))
            continue

        partially_subtracted_assemblies: list[A] = []
        for part_to_subtract in intersecting_parts_to_subtract:
            partially_subtracted_assemblies.append(
                subtract_parts(part_to_be_subtracted, part_to_subtract)
            )

        subtracted_assemblies += [
            intersect_assemblies(
                assemblies=partially_subtracted_assemblies,
                get_assembly_parts=get_assembly_parts,
                get_part_bounds=get_part_bounds,
                are_parts_intersecting=are_parts_intersecting,
                intersect_parts=intersect_parts,
                unify_parts=unify_parts,
                concat_parts=concat_parts,
            )
        ]

    return concat_assemblies(
        assemblies=subtracted_assemblies,
        get_assembly_parts=get_assembly_parts,
        concat_parts=concat_parts,
    )
