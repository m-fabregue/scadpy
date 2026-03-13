from __future__ import annotations

from typing import TYPE_CHECKING

from scadpy.color.constants import BLACK, WHITE
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Color, Solid


@typechecked
def map_solid_to_screen(
    solid: Solid,
    background_color: Color = WHITE,
    foreground_color: Color = BLACK,
) -> None:
    """Display a solid in a Qt-based window.

    Shortcut for :func:`map_component_to_screen`.
    See :func:`map_component_to_screen` for full documentation.

    Parameters
    ----------
    solid : Solid
        The solid to display.
    background_color : Color, default=WHITE
        The background color of the rendered window.
    foreground_color : Color, default=BLACK
        The foreground color (axes, grid) of the rendered window.

    Returns
    -------
    None
    """
    from scadpy import map_component_to_screen, map_solid_to_html

    map_component_to_screen(
        component=solid,
        to_html=lambda component: map_solid_to_html(
            solid=component,
            background_color=background_color,
            foreground_color=foreground_color,
        ),
    )
