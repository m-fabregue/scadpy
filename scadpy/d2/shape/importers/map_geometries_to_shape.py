from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from shapely.geometry import Polygon
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def map_geometries_to_shape(geometries: Sequence[Polygon]) -> Shape:
    """Map a sequence of polygons to a shape.

    Each polygon is validated and oriented via :func:`map_parts_to_shape`.

    Parameters
    ----------
    geometries : Sequence[Polygon]
        The polygons to map.

    Returns
    -------
    Shape
        A new shape containing all valid, oriented polygons.

    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> from scadpy import map_geometries_to_shape

    >>> map_geometries_to_shape(  # doctest: +SKIP
    ...     [Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])]
    ... )

    .. render-example::
        :name: map_geometries_to_shape
        :example: map_geometries_to_shape([Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])])
    """
    from scadpy.core.part import Part
    from scadpy.d2.shape import Shape

    return Shape.from_parts([Part[Polygon].from_geometry(g) for g in geometries])
