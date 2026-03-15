from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from numpy.typing import NDArray


def linear_pattern_assembly[A](
    assembly: A,
    counts: int | Sequence[int],
    steps: NDArray[np.float64] | Sequence[NDArray[np.float64]],
    translate: Callable[[A, NDArray[np.float64]], A],
    concat: Callable[[Sequence[A]], A],
    dimensions: int,
) -> A:
    """Create a linear (grid) pattern of an assembly along one or more axes.

    Uses dependency injection to remain type-agnostic and work with any
    assembly type (Shape, Solid, etc.).

    Parameters
    ----------
    assembly : A
        The assembly to repeat.
    counts : int | Sequence[int]
        Number of copies along each axis. A single int creates a 1D pattern.
        A sequence of ints creates a 2D or 3D grid pattern.
    steps : NDArray[np.float64] | Sequence[NDArray[np.float64]]
        Translation vector between consecutive copies along each axis.
        Must be a single vector when ``counts`` is an int, or a sequence of
        vectors matching the length of ``counts``.
    translate : Callable[[A, NDArray[np.float64]], A]
        Function that translates an assembly by a displacement vector.
    concat : Callable[[Sequence[A]], A]
        Function that concatenates a sequence of assemblies into one.
    dimensions : int
        Number of spatial dimensions

    Returns
    -------
    A
        The patterned assembly containing ``prod(counts)`` copies of the
        original, including the copy at the origin.
    """
    from scadpy import resolve_vector

    if isinstance(counts, int) and isinstance(steps, np.ndarray):
        counts = [counts]
        steps = [steps]
    if isinstance(counts, int) or isinstance(steps, np.ndarray):
        raise ValueError("counts and steps must be homogeneous")
    if len(counts) == 0 or len(steps) == 0:
        raise ValueError("counts and steps cannot be an empty sequence")
    if len(counts) != len(steps):
        raise ValueError("counts and steps should have the same size")

    steps = [resolve_vector(step, 0, dimensions) for step in steps]

    step = steps[0]
    count = counts[0]

    result = concat([translate(assembly, step * i) for i in range(0, count)])
    if len(counts) > 1:
        return linear_pattern_assembly(
            result, counts[1:], steps[1:], translate, concat, dimensions
        )
    return result
