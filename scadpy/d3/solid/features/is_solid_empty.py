from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Solid


def is_solid_empty(solid: Solid) -> bool:
    """Return whether the solid has no vertices.

    Parameters
    ----------
    solid : Solid
        The solid to check.

    Returns
    -------
    bool
        True if the solid has no vertices, False otherwise.
    """
    return len(solid.vertex_coordinates) == 0
