from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, cast
from urllib.request import Request, urlopen

from trimesh import load
from trimesh.path import Path2D
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


@typechecked
def map_svg_to_shape(source: str | Path) -> Shape:
    """Load a 2D shape from an SVG file or URL.

    Closed paths in the SVG are converted to filled polygons. Open paths
    and decorative elements (text, images, gradients) are ignored.
    ``source`` can be a local file path or an ``http``/``https`` URL.

    Parameters
    ----------
    source : str or Path
        Path to a local ``.svg`` file or an HTTP/HTTPS URL pointing to one.

    Returns
    -------
    Shape
        A new shape whose parts correspond to the closed filled regions
        found in the SVG.

    Examples
    --------
    >>> from scadpy import map_svg_to_shape

    >>> map_svg_to_shape("https://upload.wikimedia.org/wikipedia/commons/0/04/Pentagon.svg")  # doctest: +SKIP

    .. render-example::
        :name: map_svg_to_shape
        :example: map_svg_to_shape("https://upload.wikimedia.org/wikipedia/commons/0/04/Pentagon.svg")
    """
    from scadpy import map_geometries_to_shape

    if isinstance(source, str) and source.startswith(("http://", "https://")):
        req = Request(source, headers={"User-Agent": "ScadPy"})
        with urlopen(req) as response:
            data = BytesIO(response.read())
        path = cast(Path2D, load(data, file_type="svg"))
    else:
        path = cast(Path2D, load(source))

    return map_geometries_to_shape(list(path.polygons_full))
