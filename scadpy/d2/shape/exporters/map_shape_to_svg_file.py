from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape


@typechecked
def map_shape_to_svg_file(shape: Shape, path: str | Path) -> int:
    """Save a shape as an SVG file.

    Parameters
    ----------
    shape : Shape
        The shape to export.
    path : str or Path
        Destination file path.

    Returns
    -------
    int
        Number of characters written.

    Examples
    --------
    >>> from scadpy import square, circle, map_shape_to_svg_file

    >>> map_shape_to_svg_file(  # doctest: +SKIP
    ...     shape=square(4) - circle(1), path="output.svg"
    ... )
    """
    from scadpy import map_shape_to_svg

    return Path(path).write_text(map_shape_to_svg(shape), encoding="utf-8")
