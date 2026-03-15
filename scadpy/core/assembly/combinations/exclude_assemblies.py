from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence



def exclude_assemblies[A, P](
    assemblies: Sequence[A],
    get_assembly_parts: Callable[[A], Iterable[P]],
    are_parts_intersecting: Callable[[P, P], bool],
    subtract_parts: Callable[[P, Sequence[P]], A],
    unify_parts: Callable[[Sequence[P]], A],
    concat_parts: Callable[[Sequence[P]], A],
) -> A:
    """
    Compute the symmetric difference (exclusive-or) of multiple assemblies.

    This function is fully generic and uses dependency injection for all domain-specific
    operations, making it suitable for a wide range of applications (2D, 3D, CAD, etc.).
    The result contains all parts that are present in exactly one assembly, i.e., the union minus all intersections.

    Parameters
    ----------
    assemblies : Sequence[A]
        Sequence of assembly objects to process.
    get_assembly_parts : Callable[[A], Iterable[P]]
        Function that extracts parts from an assembly.
    are_parts_intersecting : Callable[[P, P], bool]
        Function to determine if two parts intersect.
    subtract_parts : Callable[[P, Sequence[P]], A]
        Function to subtract multiple parts from one part, returning an assembly.
    unify_parts : Callable[[Sequence[P]], A]
        Function to unify (union) overlapping parts within an assembly.
    concat_parts : Callable[[Sequence[P]], A]
        Function to concatenate a sequence of parts into a new assembly.

    Returns
    -------
    A
        The assembly object containing the symmetric difference of all input assemblies.

    Examples
    --------
    >>> from scadpy import exclude_assemblies

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
    >>> def subtract_parts(p1, p2_list):
    ...     geometries = subtract_geometries(
    ...         p1['bounds'], p2_list[0]['bounds']
    ...     )
    ...     return [{'bounds': g} for g in geometries]
    ...
    >>> result = exclude_assemblies(
    ...     assemblies,
    ...     get_assembly_parts=lambda a: a,
    ...     are_parts_intersecting=are_intersecting,
    ...     subtract_parts=subtract_parts,
    ...     unify_parts=lambda parts: parts,
    ...     concat_parts=lambda parts: parts
    ... )
    >>> result == [
    ...     {'bounds': [0, 0, 2, 2]},
    ...     {'bounds': [1, 1, 3, 3]},
    ...     {'bounds': [5, 5, 6, 6]}
    ... ]
    True
    """
    from scadpy.core.assembly import subtract_assemblies, unify_assemblies

    if len(assemblies) == 0:
        return concat_parts([])

    result = assemblies[0]
    for assembly in assemblies[1:]:
        result = unify_assemblies(
            assemblies=[
                subtract_assemblies(
                    to_be_subtracted=result,
                    to_subtract=assembly,
                    get_assembly_parts=get_assembly_parts,
                    are_parts_intersecting=are_parts_intersecting,
                    subtract_parts=subtract_parts,
                    concat_parts=concat_parts,
                ),
                subtract_assemblies(
                    to_be_subtracted=assembly,
                    to_subtract=result,
                    get_assembly_parts=get_assembly_parts,
                    are_parts_intersecting=are_parts_intersecting,
                    subtract_parts=subtract_parts,
                    concat_parts=concat_parts,
                ),
            ],
            get_assembly_parts=get_assembly_parts,
            unify_parts=unify_parts,
        )
    return result
