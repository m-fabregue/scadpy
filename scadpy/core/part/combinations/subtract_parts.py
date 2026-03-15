from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scadpy.color import Color


# @typechecked
def subtract_parts[A, P, G](
    to_be_subtracted: P,
    to_subtract: Sequence[P],
    get_part_color: Callable[[P], Color],
    get_part_geometry: Callable[[P], G],
    subtract_geometries: Callable[[G, Sequence[G]], Iterable[G]],
    make_part_from_geometry: Callable[[G, Color], P],
    make_assembly_from_parts: Callable[[Sequence[P]], A],
) -> A:
    """
    Subtract the geometries of multiple parts from one part and return a new assembly.

    This function is fully generic and uses dependency injection for all domain-specific
    operations, making it suitable for a wide range of applications (2D, 3D, CAD, etc.).
    The color of the resulting part(s) is inherited from the part being subtracted from.

    Parameters
    ----------
    to_be_subtracted : P
        The part whose geometry will be subtracted from.
    to_subtract : Sequence[P]
        The parts whose geometries will be subtracted.
    get_part_color : Callable[[P], Color]
        Function to extract the color from a part (as a list or tuple of 4 floats: RGBA).
    get_part_geometry : Callable[[P], G]
        Function to extract the geometry from a part.
    subtract_geometries : Callable[[G, Sequence[G]], Iterable[G]]
        Function to compute the subtraction of multiple geometries from one geometry.
    make_part_from_geometry : Callable[[G, Color], P]
        Function to create a part from a geometry and a color.
    make_assembly_from_parts : Callable[[Sequence[P]], A]
        Function to create an assembly from a sequence of parts.

    Returns
    -------
    A
        The assembly object containing all subtracted parts.

    Examples
    --------
    >>> from scadpy import subtract_parts

    >>> part1 = {'bounds': [0, 0, 3, 3], 'color': [1, 0, 0, 1]}
    >>> part2 = {'bounds': [1, 1, 2, 2], 'color': [0, 1, 0, 1]}
    ...
    >>> def subtract_geoms(g1, g2_list):
    ...     g2 = g2_list[0]
    ...     if (g2[0] > g1[0] and g2[2] < g1[2]
    ...             and g2[1] > g1[1] and g2[3] < g1[3]):
    ...         return [
    ...             [g1[0], g1[1], g2[0], g1[3]],  # left
    ...             [g2[2], g1[1], g1[2], g1[3]],  # right
    ...             [g2[0], g1[1], g2[2], g2[1]],  # bottom
    ...             [g2[0], g2[3], g2[2], g1[3]],  # top
    ...         ]
    ...     return [g1]
    ...
    >>> result = subtract_parts(
    ...     part1, [part2],
    ...     get_part_color=lambda p: p['color'],
    ...     get_part_geometry=lambda p: p['bounds'],
    ...     subtract_geometries=subtract_geoms,
    ...     make_part_from_geometry=lambda geometry, color: {
    ...         'bounds': geometry,
    ...         'color': [float(v) for v in color]
    ...     },
    ...     make_assembly_from_parts=lambda parts: parts
    ... )
    ...
    >>> result == [
    ...     {'bounds': [0, 0, 1, 3], 'color': [1.0, 0.0, 0.0, 1.0]},
    ...     {'bounds': [2, 0, 3, 3], 'color': [1.0, 0.0, 0.0, 1.0]},
    ...     {'bounds': [1, 0, 2, 1], 'color': [1.0, 0.0, 0.0, 1.0]},
    ...     {'bounds': [1, 2, 2, 3], 'color': [1.0, 0.0, 0.0, 1.0]}
    ... ]
    True
    """
    subtracted_geometries = subtract_geometries(
        get_part_geometry(to_be_subtracted),
        [get_part_geometry(p) for p in to_subtract],
    )
    subtracted_parts = [
        make_part_from_geometry(s, get_part_color(to_be_subtracted))
        for s in subtracted_geometries
    ]
    return make_assembly_from_parts(subtracted_parts)
