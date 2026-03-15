from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


def cuboid(size: float | Iterable[float]) -> Solid:
    """Create a box (rectangular cuboid) centered at the origin.

    Parameters
    ----------
    size : float | Iterable[float]
        The dimensions of the cuboid as ``[width, depth, height]``.
        If a single float is provided, it is broadcast to all three dimensions,
        producing a cube. Missing values default to 0.

    Returns
    -------
    Solid
        A :class:`~scadpy.d3.solid.types.solid.Solid` object representing the cuboid,
        centered at the origin.

    Examples
    --------
    >>> from scadpy import cuboid

    >>> cuboid(4)  # doctest: +SKIP

    .. render-example::
        :name: cube
        :example: cuboid(4)

    >>> cuboid([4, 2, 1])  # doctest: +SKIP

    .. render-example::
        :name: cuboid
        :example: cuboid([4, 2, 1])
    """
    from scadpy.d3 import resolve_vector_3d
    from scadpy.d3.solid.primitives.polyhedron import polyhedron

    w, d, h = resolve_vector_3d(size, 0) / 2

    vertices = np.array(
        [
            [-w, -d, -h],  # 0
            [+w, -d, -h],  # 1
            [+w, +d, -h],  # 2
            [-w, +d, -h],  # 3
            [-w, -d, +h],  # 4
            [+w, -d, +h],  # 5
            [+w, +d, +h],  # 6
            [-w, +d, +h],  # 7
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 3, 2], [0, 2, 1],  # bottom  (normal -z)
            [4, 5, 6], [4, 6, 7],  # top     (normal +z)
            [0, 1, 5], [0, 5, 4],  # front   (normal -y)
            [3, 7, 6], [3, 6, 2],  # back    (normal +y)
            [0, 4, 7], [0, 7, 3],  # left    (normal -x)
            [1, 2, 6], [1, 6, 5],  # right   (normal +x)
        ],
        dtype=np.int64,
    )
    return polyhedron(vertices=vertices, faces=faces)
