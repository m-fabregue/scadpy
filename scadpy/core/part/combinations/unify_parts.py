from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from scadpy.color import Color


# @typechecked
def unify_parts[A, P, G](
    parts: Sequence[P],
    get_part_color: Callable[[P], Color],
    get_part_magnitude: Callable[[P], float],
    get_part_bounds: Callable[[P], NDArray[np.float64]],
    are_parts_intersecting: Callable[[P, P], bool],
    get_part_geometry: Callable[[P], G],
    unify_geometries: Callable[[list[G]], Iterable[G]],
    make_part_from_geometry: Callable[[G, Color], P],
    make_assembly_from_parts: Callable[[Sequence[P]], A],
) -> A:
    """
    Unite (union) groups of intersecting parts, blend their colors (weighted by magnitude), and return a new assembly.

    This function is fully generic and uses dependency injection for all domain-specific
    operations, making it suitable for a wide range of applications (2D, 3D, CAD, etc.).
    Colors are blended using a weighted average, where each part's color is weighted by its magnitude.

    Parameters
    ----------
    parts : Sequence[Part]
        Sequence of part objects to process.
    get_part_color : Callable[[P], Color]
        Function to extract the color from a part (as a list or tuple of 4 floats: RGBA).
    get_part_magnitude : Callable[[P], float]
        Function to extract a magnitude (e.g., area, volume) from a part for color blending.
    get_part_bounds : Callable[[P], NDArray[np.float64]]
        Function to extract the bounding box of a part.
    are_parts_intersecting : Callable[[P, P], bool]
        Function to determine if two parts intersect.
    get_part_geometry : Callable[[P], G]
        Function to extract the geometry from a part.
    unify_geometries : Callable[[list[G]], Iterable[G]]
        Function to compute the union of a list of geometries.
    make_part_from_geometry : Callable[[G, Color], P]
        Function to create a part from a geometry and a color.
    make_assembly_from_parts : Callable[[Sequence[P]], A]
        Function to create an assembly from a sequence of parts.

    Returns
    -------
    A
        The assembly object containing all unified parts with blended colors.

    Examples
    --------
    >>> from scadpy import unify_parts

    >>> parts = [
    ...     {
    ...         'bounds': [0, 0, 2, 2],
    ...         'color': [1, 0, 0, 1],
    ...         'magnitude': 1,
    ...     },
    ...     {
    ...         'bounds': [1, 1, 3, 3],
    ...         'color': [0, 1, 0, 1],
    ...         'magnitude': 2,
    ...     },
    ...     {
    ...         'bounds': [5, 5, 6, 6],
    ...         'color': [0, 0, 1, 1],
    ...         'magnitude': 1,
    ...     },
    ... ]
    ...
    >>> def are_intersecting(p1, p2):
    ...     b1, b2 = p1['bounds'], p2['bounds']
    ...     return not (b1[2] <= b2[0] or b2[2] <= b1[0] or
    ...                 b1[3] <= b2[1] or b2[3] <= b1[1])
    ...
    >>> def unify_geometries(geometries):
    ...     minx = min(g[0] for g in geometries)
    ...     miny = min(g[1] for g in geometries)
    ...     maxx = max(g[2] for g in geometries)
    ...     maxy = max(g[3] for g in geometries)
    ...     return [[minx, miny, maxx, maxy]]
    ...
    >>> result = unify_parts(
    ...     parts,
    ...     get_part_color=lambda p: p['color'],
    ...     get_part_magnitude=lambda p: p['magnitude'],
    ...     get_part_bounds=lambda p: p['bounds'],
    ...     are_parts_intersecting=are_intersecting,
    ...     get_part_geometry=lambda p: p['bounds'],
    ...     unify_geometries=unify_geometries,
    ...     make_part_from_geometry=lambda geometry, color: {
    ...         'bounds': geometry,
    ...         'color': [round(float(v), 2) for v in color]
    ...     },
    ...     make_assembly_from_parts=lambda parts: parts
    ... )
    ...
    >>> result == [
    ...     {'bounds': [0, 0, 3, 3], 'color': [0.33, 0.67, 0.0, 1.0]},
    ...     {'bounds': [5, 5, 6, 6], 'color': [0.0, 0.0, 1.0, 1.0]}
    ... ]
    True
    """

    from scadpy.core.component.utils import (
        blend_component_colors,
        get_intersecting_component_index_groups,
    )

    intersecting_part_index_groups: list[list[int]] = (
        get_intersecting_component_index_groups(
            parts,
            get_component_bounds=get_part_bounds,
            are_components_intersecting=are_parts_intersecting,
        )
    )
    intersecting_part_groups: list[list[P]] = [
        [parts[i] for i in group] for group in intersecting_part_index_groups
    ]

    unified_parts: list[P] = []
    for parts in intersecting_part_groups:
        blended_color = blend_component_colors(
            components=parts,
            get_component_color=get_part_color,
            get_component_magnitude=get_part_magnitude,
        )
        geometries = [get_part_geometry(p) for p in parts]
        unified_geometries = unify_geometries(geometries)
        unified_parts += [
            make_part_from_geometry(u, blended_color) for u in unified_geometries
        ]

    return make_assembly_from_parts(unified_parts)
