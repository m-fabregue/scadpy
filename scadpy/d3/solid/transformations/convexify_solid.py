from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from trimesh import Trimesh
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid, TopologyFilter


@typechecked
def convexify_solid(
    solid: Solid, part_filter: TopologyFilter[Solid] | None = None
) -> Solid:
    """Create a new solid whose selected parts are replaced by their convex hull.

    Parameters
    ----------
    solid : Solid
        The input solid whose parts will be convexified.
    part_filter : TopologyFilter[Solid] | None, optional
        A boolean mask selecting which parts to convexify. Parts not selected are
        left unchanged. If None, all parts are convexified together.

    Returns
    -------
    Solid
        A new solid consisting of the convex hull of the selected parts, plus the
        unselected parts unchanged.

    Examples
    --------
    >>> from scadpy import cuboid, sphere, convexify_solid

    >>> convexify_solid(  # doctest: +SKIP
    ...     cuboid(4) + sphere(radius=2).translate([3, 3, 3])
    ... )

    .. render-example::
        :name: convexify_solid
        :example: convexify_solid(cuboid(4) + sphere(radius=2).translate([3, 3, 3]))
        :ghost: cuboid(4) + sphere(radius=2).translate([3, 3, 3])
    """
    from scadpy import Part, Solid, blend_part_colors, transform_filtered_parts

    return transform_filtered_parts(
        assembly=solid,
        parts=solid._parts,
        part_filter=part_filter,
        transform=lambda parts: [
            Part[Trimesh].from_geometry(
                Trimesh(
                    vertices=np.vstack([p.geometry.vertices for p in parts])
                ).convex_hull,
                blend_part_colors(
                    parts=parts,
                    get_part_magnitude=lambda p: p.geometry.volume,
                ),
            )
        ],
        concat_parts=Solid.from_parts,
    )
