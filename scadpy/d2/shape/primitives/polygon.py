from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from shapely.geometry import Polygon

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def polygon(points: Iterable[Iterable[float]]) -> Shape:
    """
    Create a 2D polygon shape from a sequence of points.

    This function constructs a :class:`~scadpy.d2.shape.types.Shape` from the given 2D points.
    The polygon is automatically closed by connecting the last point to the first.
    If the polygon is self-intersecting, it may be split into multiple parts.

    Parameters
    ----------
    points : Iterable[Iterable[float]]
        A sequence of coordinate pairs ``[x, y]`` defining the vertices
        of the polygon. At least three points are required.

    Returns
    -------
    Shape
        A :class:`~scadpy.d2.shape.types.Shape` object representing the polygon.

    Notes
    -----
    - The polygon is automatically closed by connecting the last point to the first.
    - The input points are converted into 2D coordinates; extra dimensions are ignored.
    - If the polygon is self-intersecting, it may be split into multiple parts.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import polygon

    >>> # simple triangle
    >>> p = polygon([[0, 0], [1, 0], [0, 1]])
    >>> p.vertex_coordinates # doctest: +NORMALIZE_WHITESPACE
    array([[0., 0.],
           [1., 0.],
           [0., 1.]])

    >>> # square defined manually
    >>> # equivalent to square(2)
    >>> p = polygon([[-1, -1], [1, -1], [1, 1], [-1, 1]])
    >>> p.vertex_coordinates # doctest: +NORMALIZE_WHITESPACE
    array([[-1., -1.],
           [ 1., -1.],
           [ 1.,  1.],
           [-1.,  1.]])

    >>> # self-intersecting polygon generate multiple parts
    >>> p = polygon([[0, 0], [2, 2], [0, 2], [2, 0]])
    >>> vtop = p.vertex_to_part[:, np.newaxis]
    >>> stacked = np.hstack([vtop, p.vertex_coordinates])
    >>> stacked  # doctest: +NORMALIZE_WHITESPACE
    array([[0., 2., 0.],
           [0., 1., 1.],
           [0., 0., 0.],
           [1., 2., 2.],
           [1., 0., 2.],
           [1., 1., 1.]])

    >>> # invalid polygon (less than 3 points)
    >>> polygon([[0, 0], [1, 1]])
    Traceback (most recent call last):
        ...
    ValueError: A polygon must have at least 3 points
    """
    from scadpy.d2 import resolve_vector_2d
    from scadpy.d2.shape import Shape

    coords = [tuple(resolve_vector_2d(p, 0)) for p in points]
    if len(coords) < 3:
        raise ValueError("A polygon must have at least 3 points")

    polygon = Polygon(coords)
    return Shape.from_geometry(polygon)
