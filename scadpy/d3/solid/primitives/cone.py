from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


def cone(radius: float, height: float, section_count: int = 32) -> Solid:
    """Create a cone centered at the origin, apex pointing along +z.

    Parameters
    ----------
    radius : float
        The radius of the base circle.
    height : float
        The total height of the cone.
    section_count : int, optional
        The number of sides of the polygonal base approximation. Default is 32.

    Returns
    -------
    Solid
        A :class:`~scadpy.d3.solid.types.solid.Solid` object representing the
        cone, centered at the origin.

    Examples
    --------
    >>> from scadpy import cone

    >>> cone(radius=2, height=4)  # doctest: +SKIP

    .. render-example::
        :name: cone
        :example: cone(radius=2, height=4)

    >>> cone(radius=2, height=4, section_count=6)  # doctest: +SKIP

    .. render-example::
        :name: hexagonal_cone
        :example: cone(radius=2, height=4, section_count=6)
    """
    from scadpy.d3.solid.primitives.polyhedron import polyhedron

    n = section_count
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    cos_a = np.cos(angles)
    sin_a = np.sin(angles)

    # Vertex layout:
    #   0 .. n-1    base circle at z = -height/2
    #   n           apex at z = +height/2
    #   n+1         base center at z = -height/2
    base = np.column_stack([radius * cos_a, radius * sin_a, np.full(n, -height / 2)])
    apex = np.array([[0.0, 0.0, height / 2]])
    base_center = np.array([[0.0, 0.0, -height / 2]])
    vertices = np.vstack([base, apex, base_center]).astype(np.float64)

    i = np.arange(n, dtype=np.int64)
    j = (i + 1) % n

    side = np.column_stack([i, j, np.full(n, n, dtype=np.int64)])               # normal outward+up
    base_cap = np.column_stack([np.full(n, n + 1, dtype=np.int64), j, i])       # normal -z

    faces = np.vstack([side, base_cap]).astype(np.int64)
    return polyhedron(vertices=vertices, faces=faces)
