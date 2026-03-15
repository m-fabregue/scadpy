from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


def shrink_shape(
    shape: Shape, distance: float, part_filter: TopologyFilter[Shape] | None = None
) -> Shape:
    """
    Shrink each selected part by offsetting its boundary inward by a given distance.

    This is a convenience wrapper around :func:`grow_shape` with a negated distance.

    Parameters
    ----------
    shape : Shape
        The input shape whose parts will be shrunk.
    distance : float
        The offset distance. Positive values shrink inward, negative values expand outward.
    part_filter : TopologyFilter[Shape] | None, optional
        A boolean mask selecting which parts to shrink. If None, all parts are shrunk.

    Returns
    -------
    Shape
        A new shape with the selected parts shrunk and the unselected parts unchanged.
    """
    from scadpy import grow_shape

    return grow_shape(shape=shape, distance=-distance, part_filter=part_filter)
