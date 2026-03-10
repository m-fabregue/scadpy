from __future__ import annotations

from typing import TYPE_CHECKING

import trimesh
from shapely.geometry import MultiPolygon
from trimesh.path.exchange.dxf import export_dxf
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def map_shape_to_dxf(shape: Shape) -> str:
    """Export a shape to a DXF string.

    Each part of the shape is exported as a closed polyline. Polygon
    holes are exported as separate polylines.

    Parameters
    ----------
    shape : Shape
        The shape to export.

    Returns
    -------
    str
        A DXF document as a string.

    Examples
    --------
    >>> from scadpy import square, circle, map_shape_to_dxf

    >>> dxf = map_shape_to_dxf(square(4) - circle(1))
    >>> dxf.startswith("999")
    True
    """
    geometries = [part.geometry for part in shape._parts]
    if not geometries:
        return ""

    return export_dxf(trimesh.load_path(MultiPolygon(geometries)))
