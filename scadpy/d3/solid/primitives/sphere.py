from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from trimesh.creation import icosphere
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


@typechecked
def sphere(radius: float, subdivision_count: int = 4) -> Solid:
    """Create a sphere approximated by an icosphere mesh.

    Parameters
    ----------
    radius : float
        The radius of the sphere. Must be strictly positive.
    subdivision_count : int, optional
        The number of subdivision iterations applied to the base icosahedron.
        Higher values produce a smoother approximation. Default is 4.

    Returns
    -------
    Solid
        A :class:`~scadpy.d3.solid.types.solid.Solid` object representing the
        approximated sphere, centered at the origin.

    Notes
    -----
    - The sphere is always centered at the origin.
    - Subdivision count of 4 produces 2562 vertices.

    Examples
    --------
    >>> from scadpy import sphere

    >>> sphere(radius=2)  # doctest: +SKIP

    .. render-example::
        :name: sphere
        :example: sphere(radius=2)

    >>> sphere(radius=2, subdivision_count=1)  # doctest: +SKIP

    .. render-example::
        :name: low_resolution_sphere
        :example: sphere(radius=2, subdivision_count=1)
    """
    from scadpy.d3.solid.primitives.polyhedron import polyhedron

    mesh = icosphere(radius=radius, subdivisions=subdivision_count)
    return polyhedron(
        vertices=mesh.vertices.astype(np.float64),
        faces=mesh.faces.astype(np.int64),
    )
