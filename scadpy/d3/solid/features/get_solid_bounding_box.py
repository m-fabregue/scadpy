from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Solid


def get_solid_bounding_box(solid: Solid) -> Solid:
    """Return the axis-aligned bounding box of the solid as a cuboid.

    Parameters
    ----------
    solid : Solid
        The solid to compute the bounding box for.

    Returns
    -------
    Solid
        A cuboid Solid representing the bounding box.

    Examples
    --------
    >>> from scadpy import cuboid

    >>> cuboid(2).bounding_box.bounds
    array([-1., -1., -1.,  1.,  1.,  1.])
    """
    from scadpy import cuboid, get_solid_bounds, translate_solid

    bounds = get_solid_bounds(solid)
    size = bounds[3:] - bounds[:3]
    center = (bounds[:3] + bounds[3:]) / 2
    return translate_solid(cuboid(size), center)
