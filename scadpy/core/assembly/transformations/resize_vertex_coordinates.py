from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from numpy.typing import NDArray
from typeguard import typechecked


@typechecked
def resize_vertex_coordinates(
    vertex_coordinates: NDArray[np.float64],
    size: Iterable[float | None],
    n_dims: int,
    auto: bool = False,
    pivot: float | Iterable[float] | None = None,
    vertex_filter: NDArray[np.bool_] | None = None,
) -> NDArray[np.float64]:
    """
    Resize vertex coordinates to fit target dimensions.

    Computes per-axis scale factors from the bounding box of
    ``vertex_coordinates`` and ``size``, then delegates to
    :func:`scale_vertex_coordinates`.

    ``None`` entries in ``size`` mark axes to leave unchanged. When
    ``auto=True``, those axes are scaled proportionally to the average
    ratio of the defined axes instead.

    Parameters
    ----------
    vertex_coordinates : NDArray[np.float64]
        2D array of shape ``(n_vertices, n_dims)``.
    size : Iterable[float | None]
        Target dimensions. ``None`` for an axis means "leave unchanged"
        (or "scale proportionally" when ``auto=True``). Broadcast rules
        from :func:`resolve_vector` apply: a shorter iterable is padded
        with ``None`` (no resize on missing axes).
    n_dims : int
        Number of coordinate dimensions. Used to broadcast ``size`` and
        ``pivot`` to the correct length via :func:`resolve_vector`.
    auto : bool, default=False
        If ``True``, axes with ``None`` are scaled proportionally to the
        average ratio of the defined axes.
    pivot : float | Iterable[float] | None, default=None
        The point relative to which scaling is applied. Defaults to the
        center of the bounding box of ``vertex_coordinates``.
    vertex_filter : NDArray[np.bool_] | None, default=None
        Boolean array selecting which vertices are resized. If ``None``,
        all vertices are resized.

    Returns
    -------
    NDArray[np.float64]
        Array of shape ``(n_vertices, n_dims)``, one row per vertex.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import resize_vertex_coordinates

    Resize a 4×2 rectangle to 6×6:

    >>> coordinates = np.array(
    ...     [[0., 0.], [4., 0.], [4., 2.], [0., 2.]], dtype=np.float64
    ... )
    >>> result = resize_vertex_coordinates(coordinates, size=[6, 6], n_dims=2)
    >>> (result.max(axis=0) - result.min(axis=0)).tolist()
    [6.0, 6.0]

    Freeze the Y axis (``None``):

    >>> result = resize_vertex_coordinates(coordinates, size=[6, None], n_dims=2)
    >>> (result.max(axis=0) - result.min(axis=0)).tolist()
    [6.0, 2.0]

    Scale the Y axis proportionally with ``auto=True``:

    >>> result = resize_vertex_coordinates(
    ...     coordinates, size=[6, None], n_dims=2, auto=True
    ... )
    >>> (result.max(axis=0) - result.min(axis=0)).tolist()
    [6.0, 3.0]
    """
    from scadpy import resolve_vector, scale_vertex_coordinates

    # Convert None → nan so resolve_vector can broadcast to n_dims.
    # resolve_vector replaces nan with its default_value; using nan as
    # default_value preserves the sentinel for frozen axes.
    size_as_floats = [float("nan") if s is None else float(s) for s in size]
    size_array = resolve_vector(size_as_floats, float("nan"), n_dims)

    if len(vertex_coordinates) == 0:
        return vertex_coordinates

    bounds_min = vertex_coordinates.min(axis=0)
    bounds_max = vertex_coordinates.max(axis=0)
    current_size = bounds_max - bounds_min

    if pivot is None:
        effective_pivot = (bounds_min + bounds_max) / 2
    else:
        effective_pivot = np.array(resolve_vector(pivot, 0, n_dims))

    defined_scales = [
        s / c
        for s, c in zip(size_array, current_size)
        if not np.isnan(s) and c != 0
    ]
    auto_scale = sum(defined_scales) / len(defined_scales) if defined_scales else 1.0

    scale_array = np.ones(n_dims, dtype=np.float64)
    for i, (s, c) in enumerate(zip(size_array, current_size)):
        if not np.isnan(s):
            scale_array[i] = s / c if c != 0 else 1.0
        elif auto:
            scale_array[i] = auto_scale

    return scale_vertex_coordinates(
        vertex_coordinates, scale_array, effective_pivot, vertex_filter
    )
