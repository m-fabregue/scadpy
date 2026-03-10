from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def circle(radius: float, segment_count: int = 64) -> Shape:
    """
    Create a circle approximated by a polygon.

    Parameters
    ----------
    radius : float
        The radius of the circle. Must be strictly positive.
    segment_count : int, optional
        The number of segments used to approximate the circle.
        Higher values produce a smoother shape. Default is 64.

    Returns
    -------
    Shape
        A :class:`~scadpy.d2.shape.types.Shape` object representing the approximated circle.

    Notes
    -----
    - The circle is centered at the origin (0, 0).
    - The more segments, the smoother the approximation.

    Examples
    --------
    >>> from scadpy import circle

    >>> # circle of radius 5 with default resolution (64 vertices)
    >>> x = circle(5)
    >>> len(x.vertex_coordinates)
    64

    >>> # circle of radius 3 with low resolution
    >>> x = circle(3, segment_count=8)
    >>> coords = x.vertex_coordinates[:4]
    >>> coords.round(2)  # doctest: +NORMALIZE_WHITESPACE
    array([[ 3.  ,  0.  ],
           [ 2.12,  2.12],
           [ 0.  ,  3.  ],
           [-2.12,  2.12]])

    >>> # invalid circle (radius <= 0)
    >>> circle(0)
    Traceback (most recent call last):
        ...
    ValueError: Circle radius must be strictly positive.
    """
    from scadpy.d2.shape import polygon

    if radius <= 0:
        raise ValueError("Circle radius must be strictly positive.")
    if segment_count < 3:
        raise ValueError("Circle vertex segment_count must be at least 3.")

    angles = np.linspace(0, 2 * np.pi, segment_count, endpoint=False)
    points = np.column_stack((radius * np.cos(angles), radius * np.sin(angles)))
    return polygon(points=points)
