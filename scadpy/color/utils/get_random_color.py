from __future__ import annotations

import random
from typing import TYPE_CHECKING, cast

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.color import Color


@typechecked
def get_random_color() -> Color:
    from scadpy import color

    color_names: list[str] = getattr(color.constants, "__all__", [])
    color_names = [
        c for c in color_names if c != "DEFAULT_OPACITY" and c != "DEFAULT_COLOR"
    ]

    if not color_names:
        raise ValueError("No color constant found.")

    name = random.choice(color_names)
    color_value = cast(color.Color, getattr(color.constants, name))

    if not isinstance(color_value, (list, tuple)):
        raise TypeError(f"{name} is not a list or tuple.")

    if len(color_value) != 4:
        raise TypeError(f"{name} must be RGBA (4 values), got {len(color_value)}.")

    if not all(0.0 <= c <= 1.0 for c in color_value):
        raise ValueError(f"{name} has values outside [0.0, 1.0] range.")

    return color_value
