from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid
    from scadpy import TopologyFilter


def rotate_solid(
    solid: Solid,
    angle: float,
    axis: float | Iterable[float],
    pivot: float | Iterable[float] = 0,
    vertex_filter: TopologyFilter[Solid] | None = None,
) -> Solid:
    """Rotate a solid by a given angle around an axis passing through a pivot point.

    Parameters
    ----------
    solid : Solid
        The solid to rotate.
    angle : float
        The rotation angle in degrees.
    axis : float | Iterable[float]
        The rotation axis vector. If a single float is provided, it is broadcast
        to all coordinate dimensions.
    pivot : float | Iterable[float], default=0
        The point around which rotation is applied. If a single float is provided,
        it is broadcast to all coordinate dimensions. Defaults to the origin.
    vertex_filter : TopologyFilter[Solid] | None, default=None
        Boolean array or callable selecting which vertices are rotated. If ``None``, all
        vertices are rotated.

    Returns
    -------
    Solid
        A new solid with the selected vertices rotated around the axis and pivot.
    """
    from scadpy import resolve_topology_filter, rotate_vertex_coordinates, resolve_vector_3d

    angle_rad = np.deg2rad(angle)
    cosinus = np.cos(angle_rad)
    sinus = np.sin(angle_rad)
    one_minus_cosinus = 1 - cosinus

    axis_array = resolve_vector_3d(axis, 0)
    axis_array = axis_array / np.linalg.norm(axis_array)
    x, y, z = axis_array

    R = np.array(
        [
            [
                cosinus + x * x * one_minus_cosinus,
                x * y * one_minus_cosinus - z * sinus,
                x * z * one_minus_cosinus + y * sinus,
            ],
            [
                y * x * one_minus_cosinus + z * sinus,
                cosinus + y * y * one_minus_cosinus,
                y * z * one_minus_cosinus - x * sinus,
            ],
            [
                z * x * one_minus_cosinus - y * sinus,
                z * y * one_minus_cosinus + x * sinus,
                cosinus + z * z * one_minus_cosinus,
            ],
        ]
    )

    resolved_vertex_filter = resolve_topology_filter(solid, len(solid.vertex_coordinates), vertex_filter)
    return solid.recoordinate(
        rotate_vertex_coordinates(solid.vertex_coordinates, R, pivot, resolved_vertex_filter)
    )
