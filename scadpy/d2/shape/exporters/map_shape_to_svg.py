from __future__ import annotations

from typing import TYPE_CHECKING

import trimesh
from shapely.geometry import MultiPolygon
from trimesh.path.exchange.svg_io import export_svg
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def map_shape_to_svg(shape: Shape) -> str:
    """Export a shape to an SVG string.

    Parameters
    ----------
    shape : Shape
        The shape to export.

    Returns
    -------
    str
        A self-contained SVG document as a string.

    """
    geometries = [part.geometry for part in shape._parts]
    if not geometries:
        return '<svg xmlns="http://www.w3.org/2000/svg"/>'

    return export_svg(trimesh.load_path(MultiPolygon(geometries)))
