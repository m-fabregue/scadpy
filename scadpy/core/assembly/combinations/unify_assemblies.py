from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence



def unify_assemblies[A, P](
    assemblies: Sequence[A],
    get_assembly_parts: Callable[[A], Iterable[P]],
    unify_parts: Callable[[Sequence[P]], A],
) -> A:
    """
    Unite (union) multiple assemblies into a single assembly by unifying all their parts.

    This function uses dependency injection to remain type-agnostic, allowing it
    to work with any assembly/part domain model by providing appropriate accessor
    and unification functions.

    Parameters
    ----------
    assemblies : Sequence[A]
        Sequence of assembly objects to be unified.
    get_assembly_parts : Callable[[A], Iterable[P]]
        Function that extracts parts from an assembly.
    unify_parts : Callable[[Sequence[P]], Assembly]
        Function that unifies a sequence of parts into a new assembly.

    Returns
    -------
    A
        The assembly object created by unifying all parts from all input assemblies.

    Examples
    --------
    >>> from scadpy import unify_assemblies

    >>> assemblies = [
    ...     [[0, 0, 2, 2], [1, 1, 3, 3]],
    ...     [[5, 5, 6, 6]]
    ... ]
    ...
    >>> def unify_parts(parts):
    ...     minx = min(p[0] for p in parts)
    ...     miny = min(p[1] for p in parts)
    ...     maxx = max(p[2] for p in parts)
    ...     maxy = max(p[3] for p in parts)
    ...     return [[minx, miny, maxx, maxy]]
    ...
    >>> result = unify_assemblies(
    ...     assemblies,
    ...     get_assembly_parts=lambda a: a,
    ...     unify_parts=unify_parts
    ... )
    >>> result == [[0, 0, 6, 6]]
    True
    """
    return unify_parts([p for a in assemblies for p in get_assembly_parts(a)])
