from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from trimesh import Trimesh

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


def polyhedron(
    vertices: NDArray[np.float64],
    faces: NDArray[np.int64],
) -> Solid:
    """Create a solid from raw vertex coordinates and triangular face indices.

    This is the base primitive constructor. All other solid primitives ultimately
    call this function with numpy-computed geometry.

    Parameters
    ----------
    vertices : NDArray[np.float64]
        Vertex coordinates of shape ``(n, 3)``.
    faces : NDArray[np.int64]
        Triangle face indices of shape ``(m, 3)``. Each row contains the indices
        of three vertices forming a triangle. Winding order follows the
        right-hand rule: outward-pointing normals require counter-clockwise
        vertex ordering when viewed from outside.

    Returns
    -------
    Solid
        A new solid built from the given geometry.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import polyhedron

    >>> polyhedron(  # doctest: +SKIP
    ...     vertices=np.array([
    ...         [ 1.0,  1.0,  1.0],
    ...         [ 1.0, -1.0, -1.0],
    ...         [-1.0,  1.0, -1.0],
    ...         [-1.0, -1.0,  1.0],
    ...     ]),
    ...     faces=np.array([[0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2]], dtype=np.int64),
    ... )

    .. render-example::
        :name: polyhedron
        :example: polyhedron(vertices=np.array([[1.0,1.0,1.0],[1.0,-1.0,-1.0],[-1.0,1.0,-1.0],[-1.0,-1.0,1.0]]), faces=np.array([[0,1,2],[0,2,3],[0,3,1],[1,3,2]], dtype=np.int64))
    """
    from scadpy.d3.solid import Solid

    return Solid.from_geometry(Trimesh(vertices=vertices, faces=faces))
