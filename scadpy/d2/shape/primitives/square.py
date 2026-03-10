from __future__ import annotations

from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def square(size: float) -> Shape:
    """
    Creates a square centered at the origin.

    This function is a convenience wrapper around
    :func:`~scadpy.d2.shape.primitives.rectangle`, with equal width and height.

    Parameters
    ----------
    size : float
        The length of each side of the square.

    Returns
    -------
    Shape
        A :class:`~scadpy.d2.shape.types.Shape` object representing the square.

    Notes
    -----
    - The square is centered at the origin `(0, 0)`.
    - The square is equivalent to calling ``rectangle([size, size])``.

    Examples
    --------
    >>> from scadpy import square

    >>> # square of size 1x1
    >>> x = square(1)
    >>> x.vertex_coordinates # doctest: +NORMALIZE_WHITESPACE
    array([[-0.5, -0.5],
           [ 0.5, -0.5],
           [ 0.5,  0.5],
           [-0.5,  0.5]])

    >>> # square of size 5x5
    >>> x = square(5)
    >>> x.vertex_coordinates # doctest: +NORMALIZE_WHITESPACE
    array([[-2.5, -2.5],
           [ 2.5, -2.5],
           [ 2.5,  2.5],
           [-2.5,  2.5]])
    """

    from scadpy.d2.shape import rectangle

    return rectangle(size=[size, size])
