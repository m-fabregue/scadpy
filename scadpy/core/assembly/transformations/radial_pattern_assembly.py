from __future__ import annotations

from collections.abc import Callable, Sequence


def radial_pattern_assembly[A](
    assembly: A,
    count: int,
    angle: float,
    rotate: Callable[[A, float], A],
    concat: Callable[[Sequence[A]], A],
) -> A:
    """Create a radial pattern of an assembly around an axis.

    Uses dependency injection to remain type-agnostic and work with any
    assembly type (Shape, Solid, etc.).

    Parameters
    ----------
    assembly : A
        The assembly to repeat.
    count : int
        Number of copies.
    angle : float
        Total sweep angle in degrees.
    rotate : Callable[[A, float], A]
        Function that rotates an assembly by a given angle.
    concat : Callable[[Sequence[A]], A]
        Function that concatenates a sequence of assemblies into one.

    Returns
    -------
    A
        The patterned assembly containing ``count`` copies of the original.
    """
    step = angle / count
    return concat([rotate(assembly, step * i) for i in range(count)])
