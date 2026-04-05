"""Vertex/topology filter type used by transforms such as translate, rotate, chamfer, etc.

A TopologyFilter restricts a transform to a subset of vertices. Pass either:
- A boolean NumPy array of shape (n_vertices,) — True = apply transform to that vertex.
- A callable that receives the assembly and returns such a boolean array.

Examples: s.translate(x(3), vertex_filter=s.are_vertices_convex)
          s.chamfer(1.0, vertex_filter=lambda s: s.vertex_angles > 90)
"""
from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

type TopologyFilter[A] = NDArray[np.bool_] | Callable[[A], NDArray[np.bool_]]
