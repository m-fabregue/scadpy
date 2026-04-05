from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray


def resize_sweep(
    end_size: list[float | None],
    start_size: list[float | None] | None = None,
) -> Callable[[NDArray[np.float64], float], NDArray[np.float64]]:
    """Return a strategy that linearly resizes the cross-section along the path.

    Parameters
    ----------
    end_size:
        Target ``[width, height]`` at ``t=1``.  ``None`` on an axis means
        "keep proportional to the other axis" (forwarded to
        :func:`resize_vertex_coordinates`).
    start_size:
        Target ``[width, height]`` at ``t=0``.  When ``None`` (default) the
        bounding box of the cross-section is captured on the first call and
        used as the starting size.

    Examples
    --------
    >>> import numpy as np
    >>> from scadpy import circle
    >>> path = np.column_stack([np.zeros(10), np.zeros(10), np.linspace(0, 20, 10)])
    >>> circle(5).path_extrude(path, strategy=resize_sweep(end_size=[2, 8]))  # squish to 2×8 # doctest: +SKIP
    >>> circle(5).path_extrude(path, strategy=resize_sweep(end_size=[None, 2]))  # proportional height # doctest: +SKIP
    """
    from scadpy import resize_vertex_coordinates

    end_arr = np.array(
        [float("nan") if s is None else float(s) for s in end_size],
        dtype=np.float64,
    )

    state: dict[str, NDArray[np.float64]] = {}

    def _get_start(points: NDArray[np.float64]) -> NDArray[np.float64]:
        if "start" not in state:
            if start_size is None:
                bbox: NDArray[np.float64] = points.max(axis=0) - points.min(axis=0)
                state["start"] = bbox
            else:
                state["start"] = np.array(
                    [float("nan") if s is None else float(s) for s in start_size],
                    dtype=np.float64,
                )
        return state["start"]

    def _strategy(points: NDArray[np.float64], t: float) -> NDArray[np.float64]:
        start_arr = _get_start(points)
        size = np.where(
            np.isnan(start_arr) | np.isnan(end_arr),
            np.nan,
            start_arr + (end_arr - start_arr) * t,
        )
        size_list: list[float | None] = [
            None if bool(np.isnan(float(v))) else float(v) for v in size
        ]
        return resize_vertex_coordinates(points, size_list, n_dims=2)

    return _strategy
