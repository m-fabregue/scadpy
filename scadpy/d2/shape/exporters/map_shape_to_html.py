from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING

from scadpy.color.constants import BLACK, WHITE

if TYPE_CHECKING:
    from IPython.core.display import HTML

    from scadpy import Color, Shape


def map_shape_to_html(
    shape: Shape,
    background_color: Color = WHITE,
    foreground_color: Color = BLACK,
) -> HTML:
    """
    Render a shape assembly as an SVG HTML object using matplotlib and shapely.

    This function extracts all parts from the assembly, converts each to a Shapely
    polygon, and plots them with their associated colors. The resulting figure is
    exported as SVG and wrapped in an IPython HTML object for display in notebooks
    or web interfaces.

    Parameters
    ----------
    shape : Shape
        The shape to render.
    background_color : Color, default=WHITE
        The background color of the rendered output.
    foreground_color : Color, default=BLACK
        The foreground color (axes, grid) of the rendered output.

    Returns
    -------
    HTML
        An IPython HTML object containing the SVG rendering of the shape.
    """
    # Lazy imports: matplotlib (~1s) and IPython (~0.6s) are heavy at module level;
    # importing here defers the cost until the function is actually called.
    import matplotlib.pyplot as plt
    from IPython.core.display import HTML
    from shapely.plotting import plot_polygon

    foreground_color_hex = "#{:02X}{:02X}{:02X}".format(
        *(int(x * 255) for x in foreground_color[:-1])
    )
    background_color_hex = "#{:02X}{:02X}{:02X}".format(
        *(int(x * 255) for x in background_color[:-1])
    )
    x_min, y_min, x_max, y_max = shape.bounds

    width = x_max - x_min
    height = y_max - y_min

    if width > height:
        difference = width - height
        y_max = y_max + difference / 2
        y_min = y_min - difference / 2
        height = width
    else:
        difference = height - width
        x_max = x_max + difference / 2
        x_min = x_min - difference / 2
        width = height

    if width == 0 or height == 0:
        width = max(width, 1.0)
        height = max(height, 1.0)

    aspect_ratio = height / width
    fig_width = 5
    fig_height = fig_width * aspect_ratio
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    fig.patch.set_facecolor(background_color_hex)
    ax.set_facecolor(background_color_hex)
    ax.tick_params(axis="both", colors=foreground_color_hex)

    for spine in ax.spines.values():
        spine.set_edgecolor(foreground_color_hex)

    for part in shape._parts:
        color = part.color
        edge_color = [(c + b) / 2 for c, b in zip(color[:3], background_color[:3])]
        edge_color_rgba: tuple[float, float, float, float] = (
            edge_color[0], edge_color[1], edge_color[2], 1.0
        )
        plot_polygon(
            part.geometry,
            ax=ax,
            add_points=False,
            facecolor=(color[0], color[1], color[2], color[3]),
            edgecolor=edge_color_rgba,
            linewidth=2,
        )

    padding = 0.1 * width
    ax.set_xlim(x_min - padding, x_max + padding)
    ax.set_ylim(y_min - padding, y_max + padding)

    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.axhline(y=0, color=foreground_color_hex, linewidth=1, alpha=0.3)
    ax.axvline(x=0, color=foreground_color_hex, linewidth=1, alpha=0.3)

    svg_output = StringIO()
    plt.savefig(svg_output, format="svg", bbox_inches="tight", pad_inches=0)
    plt.close()

    return HTML(svg_output.getvalue())
