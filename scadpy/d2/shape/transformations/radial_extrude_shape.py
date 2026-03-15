from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from trimesh import Trimesh
from trimesh.creation import triangulate_polygon
from trimesh.geometry import faces_to_edges
from trimesh.grouping import group_rows

if TYPE_CHECKING:
    from shapely.geometry.polygon import Polygon

    from scadpy.d2.shape import Shape
    from scadpy.d3.solid import Solid


def _rotate_3d(points, axis, angle, pivot):
    points = points - pivot

    axis = axis / np.linalg.norm(axis)
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    one_minus_cos = 1 - cos_a
    x, y, z = axis

    R = np.array(
        [
            [
                cos_a + x * x * one_minus_cos,
                x * y * one_minus_cos - z * sin_a,
                x * z * one_minus_cos + y * sin_a,
            ],
            [
                y * x * one_minus_cos + z * sin_a,
                cos_a + y * y * one_minus_cos,
                y * z * one_minus_cos - x * sin_a,
            ],
            [
                z * x * one_minus_cos - y * sin_a,
                z * y * one_minus_cos + x * sin_a,
                cos_a + z * z * one_minus_cos,
            ],
        ]
    )

    rotated = points @ R.T

    return rotated + pivot



def _radial_extrude_shapely_polygon_into_trimesh(
    polygon: Polygon,
    axis: float | Iterable[float],
    start: float = 0,
    end: float = 360,
    pivot: float | Iterable[float] = 0,
    segment_count: int = 64,
) -> Trimesh:
    from scadpy import resolve_vector_2d, resolve_vector_3d

    slice_count = segment_count + 1

    start = start % 360
    end = end % 360
    is_ring = False
    if start == end:
        slice_count -= 1
        is_ring = True
    if end <= start:
        end += 360

    angles = np.linspace(np.radians(start), np.radians(end), segment_count + 1)
    axis = resolve_vector_2d(axis, 0)
    pivot = resolve_vector_2d(pivot, 0)

    triangulated_vertex_coordinates, triangulated_face_to_vertex = triangulate_polygon(
        polygon, engine="triangle"
    )
    triangulated_edge_to_vertex = faces_to_edges(triangulated_face_to_vertex)

    slice_border_vertex_coordinates = _create_slice_border_vertex_coordinates(
        triangulated_vertex_coordinates, slice_count
    )

    triangulated_border_vertex_count = len(triangulated_vertex_coordinates)
    triangulated_edge_to_vertex_sorted = np.sort(triangulated_edge_to_vertex, axis=1)
    triangulated_edge_unique = group_rows(
        triangulated_edge_to_vertex_sorted, require_count=1
    )
    slice_border_faces = _create_slice_border_faces(
        triangulated_edge_to_vertex[triangulated_edge_unique],
        triangulated_border_vertex_count,
        slice_count - 1,
        is_ring,
    )

    # make slices
    final_vertex_coordinate_slices = [
        slice_border_vertex_coordinates[
            i * triangulated_border_vertex_count : i * triangulated_border_vertex_count
            + triangulated_border_vertex_count
        ]
        for i in range(0, slice_count)
    ]
    for i, slice in enumerate(final_vertex_coordinate_slices):
        slice[:] = _rotate_3d(
            slice, resolve_vector_3d(axis, 0), angles[i], resolve_vector_3d(pivot, 0)
        )

    centroid_x = polygon.centroid.x - float(pivot[0])
    centroid_y = polygon.centroid.y - float(pivot[1])
    chirality = float(axis[0]) * centroid_y - float(axis[1]) * centroid_x

    if chirality < 0:
        slice_border_faces = slice_border_faces[:, ::-1]

    last_slice_border_faces = (
        triangulated_face_to_vertex + triangulated_border_vertex_count * (slice_count - 1)
    )
    if not is_ring:
        start_cap_faces = triangulated_face_to_vertex
        end_cap_faces = last_slice_border_faces
        if chirality < 0:
            end_cap_faces = end_cap_faces[:, ::-1]
        else:
            start_cap_faces = start_cap_faces[:, ::-1]

        slice_border_faces = np.concatenate(
            [start_cap_faces, slice_border_faces, end_cap_faces]
        )

    mesh = Trimesh(vertices=slice_border_vertex_coordinates, faces=slice_border_faces)
    return mesh


def _create_slice_border_vertex_coordinates(
    triangulated_border_vertex_coordinates: NDArray[np.float64],
    triangulated_slice_count: int,
) -> NDArray[np.float64]:
    border_vertex_count = len(triangulated_border_vertex_coordinates)
    vertex_coordinates = np.zeros(
        (
            border_vertex_count * triangulated_slice_count,
            3,
        ),
        dtype=np.float64,
    )
    vertex_coordinates[:, :2] = np.tile(
        triangulated_border_vertex_coordinates, (triangulated_slice_count, 1)
    )
    return vertex_coordinates


def _create_slice_border_faces(
    triangulated_border_edge_to_vertex: NDArray[np.int64],
    triangulated_border_vertex_count: int,
    slice_count: int,
    is_ring: bool,
) -> NDArray[np.int64]:
    all_edges = np.tile(triangulated_border_edge_to_vertex, (slice_count, 1))
    layer_offsets = (
        np.repeat(np.arange(slice_count), len(triangulated_border_edge_to_vertex))
        * triangulated_border_vertex_count
    )
    all_edges += layer_offsets.reshape(-1, 1)

    v0 = all_edges[:, 0]
    v1 = all_edges[:, 1]
    v2 = v0 + triangulated_border_vertex_count
    v3 = v1 + triangulated_border_vertex_count

    triangle1 = np.column_stack([v0, v1, v2])
    triangle2 = np.column_stack([v1, v3, v2])

    faces = np.vstack([triangle1, triangle2])

    if is_ring:
        last_edges = (
            triangulated_border_edge_to_vertex
            + triangulated_border_vertex_count * slice_count
        )
        first_edges = triangulated_border_edge_to_vertex
        v0 = last_edges[:, 0]
        v1 = last_edges[:, 1]
        v2 = first_edges[:, 0]
        v3 = first_edges[:, 1]

        triangle1 = np.column_stack([v0, v1, v2])
        triangle2 = np.column_stack([v1, v3, v2])

        ring_faces = np.vstack([triangle1, triangle2])
        faces = np.vstack([faces, ring_faces])

    return faces


def radial_extrude_shape(
    shape: Shape,
    axis: float | Iterable[float],
    start: float = 0,
    end: float = 360,
    pivot: float | Iterable[float] = 0,
    segment_count: int = 64,
) -> Solid:
    """Revolve a 2D shape around an axis to produce a 3D solid.

    Each part of the shape is independently revolved around the given axis.
    The axis is defined in 2D (the Z component is always 0). The revolution
    spans from ``start`` to ``end`` degrees. A full 360° revolution produces
    a closed solid; a partial revolution leaves the ends open. If ``start``
    equals ``end``, an empty solid is returned.

    Parameters
    ----------
    shape : Shape
        The 2D shape to revolve.
    axis : float or Iterable[float]
        The 2D axis of revolution (e.g. ``[0, 1]`` for the Y-axis).
    start : float, optional
        Starting angle in degrees. Default is ``0``.
    end : float, optional
        Ending angle in degrees. Default is ``360`` (full revolution). If
        equal to ``start``, an empty solid is returned.
    pivot : float or Iterable[float], optional
        2D pivot point for the revolution. Default is ``0`` (origin).
    segment_count : int, optional
        Number of angular segments used to approximate the revolution.
        Higher values produce smoother results. Default is ``64``.

    Returns
    -------
    Solid
        The resulting 3D solid.
    """
    from scadpy import Part, Solid, linear_cut_shape, unify_solid

    if start == end:
        return Solid.from_parts([])

    cut_shape = linear_cut_shape(shape=shape, axis=axis, pivot=pivot)
    parts = [
        Part[Trimesh].from_geometry(
            _radial_extrude_shapely_polygon_into_trimesh(
                p.geometry, axis, start, end, pivot, segment_count
            ),
            p.color,
        )
        for p in cut_shape._parts
    ]

    if not parts:
        return Solid.from_parts([])
    solids = [Solid.from_parts([p]) for p in parts]
    if len(solids) == 1:
        return solids[0]
    return unify_solid(solids=solids)
