from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence



def concat_assemblies[A, P](
    assemblies: Iterable[A],
    get_assembly_parts: Callable[[A], Iterable[P]],
    concat_parts: Callable[[Sequence[P]], A],
) -> A:
    """
    Combine multiple assemblies into a single assembly by concatenating all their parts.

    This function uses dependency injection to remain type-agnostic, allowing it
    to work with any assembly/part domain model by providing appropriate accessor
    and concatenation functions.

    Parameters
    ----------
    assemblies : Iterable[A]
        Iterable of assembly objects to be combined.
    get_assembly_parts : Callable[[A], Iterable[P]]
        Function that extracts parts from an assembly.
    concat_parts : Callable[[Sequence[P]], A]
        Function that combines a sequence of parts into a new assembly.

    Returns
    -------
    A
        The assembly object created by combining all parts from all input assemblies.

    Examples
    --------
    >>> from scadpy import concat_assemblies
    >>> assemblies = [
    ...     ['a', 'b'],
    ...     ['c'],
    ...     []
    ... ]
    >>> concat_assemblies(
    ...     assemblies,
    ...     get_assembly_parts=lambda a: a,
    ...     concat_parts=lambda parts: ''.join(parts)
    ... )
    'abc'
    """
    return concat_parts([p for a in assemblies for p in get_assembly_parts(a)])
