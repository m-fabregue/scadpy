from __future__ import annotations

from typing import TYPE_CHECKING

from scadpy.color.constants import BLACK, WHITE

if TYPE_CHECKING:
    from scadpy import Color, Shape


def map_shape_to_html_file(
    shape: Shape,
    path: str,
    background_color: Color = WHITE,
    foreground_color: Color = BLACK,
) -> int:
    """Save a shape as an HTML file.

    Shortcut for :func:`map_component_to_html_file`.
    See :func:`map_component_to_html_file` for full documentation.

    Parameters
    ----------
    shape : Shape
        The shape to save.
    path : str
        The file path where the HTML will be written.
    background_color : Color, default=WHITE
        The background color of the rendered output.
    foreground_color : Color, default=BLACK
        The foreground color (axes, grid) of the rendered output.

    Returns
    -------
    int
        The number of characters written to the file.

    """
    from scadpy import map_component_to_html_file, map_shape_to_html

    return map_component_to_html_file(
        component=shape,
        path=path,
        to_html=lambda component: map_shape_to_html(
            shape=component,
            background_color=background_color,
            foreground_color=foreground_color,
        ),
    )
