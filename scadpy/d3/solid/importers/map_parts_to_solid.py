from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from trimesh import Trimesh
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Part, Solid


@typechecked
def map_parts_to_solid(
    parts: Sequence[Part[Trimesh]],
) -> Solid:
    """Map a sequence of parts to a solid, repairing geometry where needed.

    For each part, two repairs are applied if needed:

    - **Locally inconsistent winding**: if adjacent faces have inconsistent winding
      order (e.g. after some boolean operations), :func:`trimesh.Trimesh.fix_normals`
      is called to make them consistent.
    - **Globally inverted normals**: if the mesh has negative volume (e.g. after
      a mirror transform), the face winding order is reversed to restore
      outward-pointing normals.

    A mesh copy is only made when a repair is actually needed.

    Parameters
    ----------
    parts : Sequence[Part[Trimesh]]
        The parts to map. Each part holds a Trimesh mesh and a color.

    Returns
    -------
    Solid
        A new solid containing all parts with corrected geometry.

    Examples
    --------
    >>> from scadpy import cuboid, map_parts_to_solid

    >>> map_parts_to_solid(  # doctest: +SKIP
    ...     cuboid(4)._parts
    ... )

    .. render-example::
        :name: map_parts_to_solid
        :example: map_parts_to_solid(cuboid(4)._parts)
    """
    from scadpy.core.part import Part
    from scadpy.d3.solid.types.solid import Solid

    fixed_parts: list[Part[Trimesh]] = []
    for part in parts:
        mesh = part.geometry
        needs_fix = (not mesh.is_winding_consistent) or (mesh.volume < 0)
        if needs_fix:
            mesh = mesh.copy()
            mesh.fix_normals()
        fixed_parts.append(Part[Trimesh].from_geometry(mesh, part.color))

    solid = Solid()
    solid._parts = fixed_parts
    return solid
