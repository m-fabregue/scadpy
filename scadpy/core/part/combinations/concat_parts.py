from __future__ import annotations

from collections.abc import Callable, Sequence

from typeguard import typechecked


@typechecked
def concat_parts[A, P](
    parts: Sequence[P],
    make_assembly_from_parts: Callable[[Sequence[P]], A],
) -> A:
    """
    Combine multiple parts into a single assembly using a user-provided constructor.

    This function uses dependency injection to remain type-agnostic, allowing it
    to work with any part and assembly domain model by providing an appropriate
    assembly constructor function. No validation or modification of the parts is performed.

    Parameters
    ----------
    parts : Sequence[P]
        Sequence of part objects to be combined.
    make_assembly_from_parts : Callable[[Sequence[P]], A]
        Function that takes a sequence of parts and returns an assembly object.

    Returns
    -------
    A
        The assembly object created by combining the provided parts.

    Examples
    --------
    >>> from scadpy import concat_parts

    >>> parts = [1, 2, 3]
    >>> concat_parts(
    ...     parts, make_assembly_from_parts=lambda ps: sum(ps)
    ... )
    6

    >>> parts = ['a', 'b', 'c']
    >>> concat_parts(
    ...     parts, make_assembly_from_parts=lambda ps: ''.join(ps)
    ... )
    'abc'
    """
    return make_assembly_from_parts(parts)
