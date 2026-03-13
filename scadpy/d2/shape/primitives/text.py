from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from matplotlib import font_manager as fm
from matplotlib.path import Path
from matplotlib.textpath import TextPath
from numpy.typing import NDArray
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d2.shape import Shape


def _quadratic_bezier(
    p0: NDArray[np.float64],
    p1: NDArray[np.float64],
    p2: NDArray[np.float64],
    n: int,
) -> NDArray[np.float64]:
    """Sample a quadratic Bézier curve at n equally-spaced parameter values.

    The start point p0 is not included in the output (it is assumed to already
    be in the caller's point list).

    Parameters
    ----------
    p0 : NDArray[np.float64]
        Start point (shape (2,)).
    p1 : NDArray[np.float64]
        Control point (shape (2,)).
    p2 : NDArray[np.float64]
        End point (shape (2,)).
    n : int
        Number of output samples (not counting p0).

    Returns
    -------
    NDArray[np.float64]
        Sampled points of shape (n, 2).
    """
    t = np.linspace(0, 1, n + 1)[1:]
    return np.outer((1 - t) ** 2, p0) + np.outer(2 * (1 - t) * t, p1) + np.outer(t**2, p2)


def _cubic_bezier(
    p0: NDArray[np.float64],
    p1: NDArray[np.float64],
    p2: NDArray[np.float64],
    p3: NDArray[np.float64],
    n: int,
) -> NDArray[np.float64]:
    """Sample a cubic Bézier curve at n equally-spaced parameter values.

    The start point p0 is not included in the output.

    Parameters
    ----------
    p0 : NDArray[np.float64]
        Start point (shape (2,)).
    p1 : NDArray[np.float64]
        First control point (shape (2,)).
    p2 : NDArray[np.float64]
        Second control point (shape (2,)).
    p3 : NDArray[np.float64]
        End point (shape (2,)).
    n : int
        Number of output samples (not counting p0).

    Returns
    -------
    NDArray[np.float64]
        Sampled points of shape (n, 2).
    """
    t = np.linspace(0, 1, n + 1)[1:]
    return (
        np.outer((1 - t) ** 3, p0)
        + np.outer(3 * (1 - t) ** 2 * t, p1)
        + np.outer(3 * (1 - t) * t**2, p2)
        + np.outer(t**3, p3)
    )


def _path_to_contours(
    path: Path,
    curve_segments: int,
) -> list[NDArray[np.float64]]:
    """Convert a matplotlib Path into a list of closed 2D contours.

    Each MOVETO/CLOSEPOLY pair produces one contour. Bézier segments
    (CURVE3, CURVE4) are approximated by straight-line sequences.

    Parameters
    ----------
    path : Path
        Matplotlib path, typically from TextPath.
    curve_segments : int
        Number of line segments used to approximate each Bézier curve.

    Returns
    -------
    list[NDArray[np.float64]]
        List of contours, each of shape (n_points, 2).
    """
    contours: list[NDArray[np.float64]] = []
    current: list[NDArray[np.float64]] = []

    for verts, code in path.iter_segments(simplify=False):
        if code == Path.MOVETO:
            if len(current) >= 3:
                contours.append(np.array(current))
            current = [verts]
        elif code == Path.LINETO:
            current.append(verts)
        elif code == Path.CURVE3:
            p0 = np.array(current[-1])
            pts = _quadratic_bezier(p0, verts[:2], verts[2:], curve_segments)
            current.extend(pts)
        elif code == Path.CURVE4:
            p0 = np.array(current[-1])
            pts = _cubic_bezier(p0, verts[:2], verts[2:4], verts[4:], curve_segments)
            current.extend(pts)
        elif code == Path.CLOSEPOLY:
            if len(current) >= 3:
                contours.append(np.array(current))
            current = []

    if len(current) >= 3:
        contours.append(np.array(current))

    return contours


@typechecked
def text(
    content: str,
    font: str | None = None,
    size: float = 10,
    curve_segments: int = 12,
) -> Shape:
    """Create a 2D shape from a text string.

    Each glyph is traced from the font outlines and converted to a polygon.
    Holes (e.g. inside ``o``, ``e``, ``a``) are handled via symmetric
    difference (XOR) across all contours.

    Parameters
    ----------
    content : str
        The text to render.
    font : str or None
        Font family name (e.g. ``"DejaVu Serif"``). Use :func:`available_fonts`
        to list fonts available on the current system. If ``None``, matplotlib's
        default font (DejaVu Sans, bundled with matplotlib) is used — this is
        guaranteed to work cross-platform.
    size : float
        Font size in units. Default is 10.
    curve_segments : int
        Number of line segments used to approximate each Bézier curve in the
        font outlines. Higher values produce smoother curves. Default is 12.

    Returns
    -------
    Shape
        A :class:`~scadpy.d2.shape.types.Shape` representing the text outlines.

    Examples
    --------
    >>> from scadpy import text

    >>> text("ScadPy", font="DejaVu Sans", size=20) # doctest: +SKIP

    .. render-example::
        :name: text_example
        :example: text("ScadPy", font="DejaVu Sans", size=20)
    """
    from functools import reduce

    from scadpy.d2.shape.primitives import polygon

    props = fm.FontProperties()
    if font is not None:
        props.set_family(font)
    path = TextPath((0, 0), content, size=size, prop=props)
    contours = _path_to_contours(path, curve_segments)
    polygons = [polygon(c) for c in contours]
    result = reduce(lambda a, b: a ^ b, polygons)
    bounds = result.bounds
    cx = (bounds[0] + bounds[2]) / 2
    cy = (bounds[1] + bounds[3]) / 2
    return result.translate([-cx, -cy])
