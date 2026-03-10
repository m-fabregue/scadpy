from __future__ import annotations

from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
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

    Examples
    --------
    >>> from scadpy import Solid, is_solid_empty

    >>> is_solid_empty(Solid.from_parts([]))
    True

    >>> from scadpy import cuboid
    >>> is_solid_empty(cuboid(2))
    False
    """
    return len(solid.vertex_coordinates) == 0
