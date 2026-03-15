from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


def cylinder(radius: float, height: float, section_count: int = 32) -> Solid:
    """Create a cylinder centered at the origin, aligned along the z-axis.

    Parameters
    ----------
    radius : float
        The radius of the cylinder.
    height : float
        The total height of the cylinder.
    section_count : int, optional
        The number of sides of the polygonal approximation. Default is 32.

    Returns
    -------
    Solid
        A :class:`~scadpy.d3.solid.types.solid.Solid` object representing the
        cylinder, centered at the origin.

    Examples
    --------
    >>> from scadpy import cylinder

    >>> cylinder(radius=2, height=4)  # doctest: +SKIP

    .. render-example::
        :name: cylinder
        :example: cylinder(radius=2, height=4)

    >>> cylinder(radius=2, height=4, section_count=6)  # doctest: +SKIP

    .. render-example::
        :name: hexagonal_cylinder
        :example: cylinder(radius=2, height=4, section_count=6)
    """
    from scadpy.d3.solid.primitives.polyhedron import polyhedron

    n = section_count
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    cos_a = np.cos(angles)
    sin_a = np.sin(angles)

    # Vertex layout:
    #   0 .. n-1        bottom circle
    #   n .. 2n-1       top circle
    #   2n              bottom center
    #   2n+1            top center
    bottom = np.column_stack([radius * cos_a, radius * sin_a, np.full(n, -height / 2)])
    top = np.column_stack([radius * cos_a, radius * sin_a, np.full(n, height / 2)])
    centers = np.array([[0.0, 0.0, -height / 2], [0.0, 0.0, height / 2]])
    vertices = np.vstack([bottom, top, centers]).astype(np.float64)

    i = np.arange(n, dtype=np.int64)
    j = (i + 1) % n

    side1 = np.column_stack([i, j, n + j])          # side triangle A
    side2 = np.column_stack([i, n + j, n + i])      # side triangle B
    bot_cap = np.column_stack([np.full(n, 2 * n, dtype=np.int64), j, i])   # normal -z
    top_cap = np.column_stack([np.full(n, 2 * n + 1, dtype=np.int64), n + i, n + j])  # normal +z

    faces = np.vstack([side1, side2, bot_cap, top_cap]).astype(np.int64)
    return polyhedron(vertices=vertices, faces=faces)
