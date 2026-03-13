from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from trimesh import Trimesh
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


@typechecked
def recoordinate_solid(
    solid: Solid, vertex_coordinates: NDArray[np.float64]
) -> Solid:
    """Rebuild a solid with new vertex coordinates, preserving topology and colors.

    Parameters
    ----------
    solid : Solid
        The source solid providing topology (part/face structure) and colors.
    vertex_coordinates : NDArray[np.float64]
        New vertex coordinates of shape ``(n_vertices, 3)``, in the same order
        as :func:`get_assembly_vertex_coordinates`.

    Returns
    -------
    Solid
        A new solid with the same topology as *solid* but at the new positions.
    """
    from scadpy import Part, map_parts_to_solid

    vertex_to_part = solid.vertex_to_part
    part_colors = solid.part_colors

    parts = []
    for part_index in np.unique(vertex_to_part):
        part_mask = vertex_to_part == part_index
        part_vertex_coordinates = vertex_coordinates[part_mask]
        color = list(part_colors[part_index])

        parts.append(
            Part[Trimesh].from_geometry(
                Trimesh(
                    vertices=part_vertex_coordinates,
                    faces=solid._parts[part_index].geometry.faces,
                ),
                color,
            )
        )

    return map_parts_to_solid(parts)
