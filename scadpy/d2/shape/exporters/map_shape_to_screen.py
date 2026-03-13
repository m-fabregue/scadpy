from __future__ import annotations

from typing import TYPE_CHECKING

from scadpy.color.constants import BLACK, WHITE
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Color, Shape


@typechecked
def map_shape_to_screen(
    shape: Shape,
    background_color: Color = WHITE,
    foreground_color: Color = BLACK,
) -> None:
    """Display a shape in a Qt-based window.

    Shortcut for :func:`map_component_to_screen`.
    See :func:`map_component_to_screen` for full documentation.

    Parameters
    ----------
    shape : Shape
        The shape to display.
    background_color : Color, default=WHITE
        The background color of the rendered window.
    foreground_color : Color, default=BLACK
        The foreground color (axes, grid) of the rendered window.

    Returns
    -------
    None

    """
    from scadpy import map_component_to_screen, map_shape_to_html

    map_component_to_screen(
        component=shape,
        to_html=lambda component: map_shape_to_html(
            shape=component,
            background_color=background_color,
            foreground_color=foreground_color,
        ),
    )
