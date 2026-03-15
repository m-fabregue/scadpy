from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def rectangle(size: Iterable[float]) -> Shape:
    """
    Create a rectangle centered at the origin.

    Parameters
    ----------
    size : Iterable[float]
        The dimensions of the rectangle as ``[width, height]``.
        Both values must be strictly positive numbers.

    Returns
    -------
    Shape
        A :class:`~scadpy.d2.shape.types.Shape` object representing the rectangle.

    Notes
    -----
    - The rectangle is always centered at the origin (0, 0).
    - The edges of the rectangle are aligned with the X and Y axes.

    Examples
    --------
    >>> from scadpy import rectangle

    >>> # rectangle 4 units wide and 2 units tall
    >>> x = rectangle([4, 2])
    >>> x.vertex_coordinates # doctest: +NORMALIZE_WHITESPACE
    array([[-2., -1.],
           [ 2., -1.],
           [ 2.,  1.],
           [-2.,  1.]])

    >>> # equivalent to square(10)
    >>> x = rectangle([10, 10])
    >>> x.vertex_coordinates # doctest: +NORMALIZE_WHITESPACE
    array([[-5., -5.],
           [ 5., -5.],
           [ 5.,  5.],
           [-5.,  5.]])

    >>> # if one or no dimension is provided,
    >>> # the missing value defaults to 1.0
    >>> x = rectangle([5])
    >>> x.vertex_coordinates # doctest: +NORMALIZE_WHITESPACE
    array([[-2.5, -0.5],
           [ 2.5, -0.5],
           [ 2.5,  0.5],
           [-2.5,  0.5]])

    >>> # invalid rectangle
    >>> rectangle([0, 5])
    Traceback (most recent call last):
        ...
    ValueError: Rectangle dimensions must be strictly positive.
    """

    from scadpy.d2 import resolve_vector_2d
    from scadpy.d2.shape import polygon

    width, height = resolve_vector_2d(size, 1.0)  # pyright: ignore[reportAny]

    if width <= 0 or height <= 0:
        raise ValueError("Rectangle dimensions must be strictly positive.")

    half_width, half_height = width / 2.0, height / 2.0  # pyright: ignore[reportAny]

    points = [
        (-half_width, -half_height),
        (half_width, -half_height),
        (half_width, half_height),
        (-half_width, half_height),
    ]
    return polygon(points=points)
