from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np

from scadpy.color import Color


def blend_component_colors[C](
    components: Sequence[C],
    get_component_color: Callable[[C], Color],
    get_component_magnitude: Callable[[C], float],
) -> Color:
    """
    Compute the weighted average (blend) of component colors, using each component's magnitude as the weight.

    This function is fully generic and uses dependency injection for all domain-specific
    operations, making it suitable for a wide range of applications (2D, 3D, CAD, etc.).
    Colors are expected to be RGBA sequences (length 4). If the total magnitude is zero,
    a default color is returned.

    Parameters
    ----------
    components : Sequence[C]
        List of components whose colors will be blended.
    get_component_color : Callable[[C], Color]
        Function to extract the color from a component (as a list or tuple of 4 floats: RGBA).
    get_component_magnitude : Callable[[C], float]
        Function to extract a magnitude (e.g., area, volume) from a component for weighting.

    Returns
    -------
    Color
        The blended color as a list of 4 floats (RGBA).

    Examples
    --------
    >>> from scadpy import blend_component_colors, DEFAULT_COLOR

    >>> components = [
    ...     {'color': [1, 0, 0, 1], 'magnitude': 1},
    ...     {'color': [0, 1, 0, 1], 'magnitude': 2}
    ... ]
    ...
    >>> blend_component_colors(
    ...     components,
    ...     get_component_color=lambda c: c['color'],
    ...     get_component_magnitude=lambda c: c['magnitude']
    ... )
    [0.3333333333333333, 0.6666666666666666, 0.0, 1.0]

    >>> blend_component_colors(
    ...     [],
    ...     get_component_color=lambda c: c['color'],
    ...     get_component_magnitude=lambda c: c['magnitude']
    ... ) == DEFAULT_COLOR
    True
    """
    from scadpy.color import DEFAULT_COLOR

    total_magnitude = 0.0
    weighted_color = np.zeros(4, dtype=np.float64)

    for component in components:
        color = np.array(get_component_color(component))
        magnitude = get_component_magnitude(component)
        weighted_color += color * magnitude
        total_magnitude += magnitude

    if total_magnitude == 0:
        return DEFAULT_COLOR

    blended = weighted_color / total_magnitude
    return [float(x) for x in blended]  # pyright: ignore[reportAny]
