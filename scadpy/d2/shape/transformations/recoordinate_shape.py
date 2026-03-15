from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from shapely.geometry import Polygon

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def recoordinate_shape(
    shape: Shape, vertex_coordinates: NDArray[np.float64]
) -> Shape:
    """Rebuild a shape with new vertex coordinates, preserving topology and colors.

    Parameters
    ----------
    shape : Shape
        The source shape providing topology (part/ring structure) and colors.
    vertex_coordinates : NDArray[np.float64]
        New vertex coordinates of shape ``(n_vertices, 2)``, in the same order
        as :func:`get_shape_vertex_coordinates`.

    Returns
    -------
    Shape
        A new shape with the same topology as *shape* but at the new positions.
    """
    from scadpy.core.part import Part

    vertex_to_part = shape.vertex_to_part
    vertex_to_ring = shape.vertex_to_ring
    part_colors = shape.part_colors
    ring_types = shape.ring_types

    parts = []
    for part_index in np.unique(vertex_to_part):
        part_mask = vertex_to_part == part_index
        part_coords = vertex_coordinates[part_mask]
        part_ring_indices = vertex_to_ring[part_mask]
        color = list(part_colors[part_index])

        exterior = None
        interiors = []
        for ring_index in np.unique(part_ring_indices):
            ring_mask = part_ring_indices == ring_index
            coordinates = part_coords[ring_mask]
            if ring_types[ring_index] == "exterior":
                exterior = coordinates
            else:
                interiors.append(coordinates)

        parts.append(
            Part[Polygon].from_geometry(
                Polygon(shell=exterior, holes=interiors),
                color,
            )
        )

    return shape.from_parts(parts)
