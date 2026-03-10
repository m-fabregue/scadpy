from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from scadpy import Color, Part


# @typechecked
def blend_part_colors[G](
    parts: Sequence[Part[G]],
    get_part_magnitude: Callable[[Part[G]], float],
) -> Color:
    from scadpy.color import DEFAULT_COLOR

    total_magnitude = 0.0
    weighted_color = np.zeros(4, dtype=np.float64)

    for part in parts:
        color = np.array(part.color)
        magnitude = get_part_magnitude(part)
        weighted_color += color * magnitude
        total_magnitude += magnitude

    if total_magnitude == 0:
        return DEFAULT_COLOR

    blended = weighted_color / total_magnitude
    return [float(x) for x in blended]  # pyright: ignore[reportAny]
