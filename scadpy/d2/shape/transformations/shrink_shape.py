from __future__ import annotations

from typing import TYPE_CHECKING

from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
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

    Examples
    --------
    >>> from scadpy import shrink_shape, square
    >>> import numpy as np

    >>> shape = square(10)
    >>> shrink_shape(shape, 2) # doctest: +SKIP

    .. render-example::
        :name: shrink_shape
        :example: shrink_shape(shape, 2)
        :ghost: shape

    >>> # negative distance expands outward
    >>> shrink_shape(shape, -2) # doctest: +SKIP

    .. render-example::
        :name: shrink_shape_negative
        :example: shrink_shape(shape, -2)
        :ghost: shape

    >>> # partial shrink
    >>> a = square(6)
    >>> b = square(4).translate(10)
    >>> shrink_shape(  # doctest: +SKIP
    ...     a + b, 1, part_filter=np.array([True, False])
    ... )

    .. render-example::
        :name: shrink_shape_partial
        :example: shrink_shape(a + b, 1, part_filter=np.array([True, False]))
        :ghost: a + b
    """
    from scadpy import grow_shape

    return grow_shape(shape=shape, distance=-distance, part_filter=part_filter)
