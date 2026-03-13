from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from shapely.geometry import Polygon
from shapely.validation import make_valid
from typeguard import typechecked

from scadpy.d2.shape.types.utils import shapely_base_geometry_to_shapely_polygons

if TYPE_CHECKING:
    from scadpy import Part, Shape


@typechecked
def map_parts_to_shape(
    parts: Sequence[Part[Polygon]],
) -> Shape:
    """Map a sequence of parts to a shape, repairing and orienting each polygon.

    Each polygon is validated using :func:`shapely.validation.make_valid`. If a
    polygon is invalid, it is repaired and may be split into multiple valid polygons.
    All resulting polygons are oriented counter-clockwise (exterior) and clockwise
    (holes) using :func:`shapely.geometry.polygon.orient`.

    Parameters
    ----------
    parts : Sequence[Part[Polygon]]
        The parts to map. Each part holds a Shapely polygon and a color.

    Returns
    -------
    Shape
        A new shape containing all valid, oriented polygons from the input parts.

    """
    from scadpy.core.part import Part
    from scadpy.d2.shape import Shape

    validated: list[Part[Polygon]] = []
    for part in parts:
        geom = make_valid(part.geometry) if not part.geometry.is_valid else part.geometry
        for polygon in shapely_base_geometry_to_shapely_polygons(geom):
            validated.append(Part.from_geometry(polygon, part.color))

    shape = Shape()
    shape._parts = validated
    return shape
