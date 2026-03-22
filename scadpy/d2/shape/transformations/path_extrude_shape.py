from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import ArrayLike, NDArray
from trimesh import Trimesh
from trimesh.creation import triangulate_polygon
from trimesh.geometry import faces_to_edges
from trimesh.grouping import group_rows

if TYPE_CHECKING:
    from shapely.geometry.polygon import Polygon

    from scadpy.d2.shape import Shape
    from scadpy.d3.solid import Solid


def _fillet_path(
    path: NDArray[np.float64],
    radius: float | list[float],
    segments_per_corner: int = 16,
) -> NDArray[np.float64]:
    n_points = len(path)
    if n_points < 3:
        return path

    corner_radii: list[float] = (
        [float(radius)] * (n_points - 2)
        if isinstance(radius, (int, float))
        else list(radius)
    )

    if all(r <= 0 for r in corner_radii):
        return path

    result_points = [path[0]]

    for i in range(1, n_points - 1):
        corner_radius = corner_radii[i - 1]

        if corner_radius <= 0:
            result_points.append(path[i])
            continue

        incoming_dir: NDArray[np.float64] = np.asarray(
            path[i] - path[i - 1], dtype=np.float64
        )
        outgoing_dir: NDArray[np.float64] = np.asarray(
            path[i + 1] - path[i], dtype=np.float64
        )
        incoming_length: float = float(np.linalg.norm(incoming_dir))
        outgoing_length: float = float(np.linalg.norm(outgoing_dir))

        if incoming_length < 1e-10 or outgoing_length < 1e-10:
            result_points.append(path[i])
            continue

        incoming_dir /= incoming_length
        outgoing_dir /= outgoing_length

        cos_angle: float = float(
            np.clip(np.dot(incoming_dir, outgoing_dir), -1.0, 1.0)
        )

        if cos_angle > 1.0 - 1e-10:
            result_points.append(path[i])
            continue

        turn_angle: float = float(np.arccos(cos_angle))
        half_turn_angle: float = (np.pi - turn_angle) / 2.0

        trim_distance: float = float(corner_radius / np.tan(half_turn_angle))

        max_trim = min(incoming_length * 0.49, outgoing_length * 0.49)
        if trim_distance > max_trim:
            trim_distance = max_trim
            radius_clamped: float = float(trim_distance * np.tan(half_turn_angle))
        else:
            radius_clamped = corner_radius

        arc_start: NDArray[np.float64] = np.asarray(
            path[i] - incoming_dir * trim_distance, dtype=np.float64
        )
        arc_end: NDArray[np.float64] = np.asarray(
            path[i] + outgoing_dir * trim_distance, dtype=np.float64
        )

        bisector: NDArray[np.float64] = np.asarray(
            outgoing_dir - incoming_dir, dtype=np.float64
        )
        bisector_length: float = float(np.linalg.norm(bisector))
        if bisector_length < 1e-10:
            result_points.append(path[i])
            continue
        bisector /= bisector_length

        center_distance: float = float(radius_clamped / np.sin(half_turn_angle))
        arc_center: NDArray[np.float64] = np.asarray(
            path[i] + bisector * center_distance, dtype=np.float64
        )

        radial_u: NDArray[np.float64] = arc_start - arc_center
        radial_u_length: float = float(np.linalg.norm(radial_u))
        if radial_u_length < 1e-10:
            result_points.append(path[i])
            continue
        radial_u /= radial_u_length

        radial_w: NDArray[np.float64] = arc_end - arc_center
        radial_w_length: float = float(np.linalg.norm(radial_w))
        if radial_w_length < 1e-10:
            result_points.append(path[i])
            continue
        radial_w /= radial_w_length

        radial_v: NDArray[np.float64] = radial_w - float(np.dot(radial_w, radial_u)) * radial_u
        radial_v_length: float = float(np.linalg.norm(radial_v))
        if radial_v_length < 1e-10:
            result_points.append(path[i])
            continue
        radial_v /= radial_v_length

        arc_params = np.linspace(0, turn_angle, segments_per_corner + 1)

        arc_points: NDArray[np.float64] = (
            arc_center[:, np.newaxis]
            + radius_clamped * np.cos(arc_params)[np.newaxis, :] * radial_u[:, np.newaxis]
            + radius_clamped * np.sin(arc_params)[np.newaxis, :] * radial_v[:, np.newaxis]
        ).T

        for arc_point in arc_points:
            result_points.append(arc_point)

    result_points.append(path[-1])
    return np.array(result_points, dtype=np.float64)


def _refine_path_uniform(
    path: NDArray[np.float64], num_points_to_add: int
) -> NDArray[np.float64]:
    if num_points_to_add <= 0 or len(path) < 2:
        return path

    segment_deltas = np.diff(path, axis=0)
    segment_lengths: NDArray[np.float64] = np.linalg.norm(segment_deltas, axis=1)
    cumulative_length: NDArray[np.float64] = np.insert(
        np.cumsum(segment_lengths), 0, 0.0
    )
    total_length: float = float(cumulative_length[-1])

    if total_length < 1e-10:
        return path

    step = total_length / (num_points_to_add + 1)
    candidate_targets = np.linspace(step, total_length - step, num_points_to_add)

    # Drop targets that would land too close to an existing vertex
    min_gap = total_length * 1e-4
    target_distances = candidate_targets[
        np.min(
            np.abs(candidate_targets[:, np.newaxis] - cumulative_length[np.newaxis, :]),
            axis=1,
        )
        > min_gap
    ]

    all_distances = np.sort(np.concatenate([cumulative_length, target_distances]))
    return np.column_stack(
        [np.interp(all_distances, cumulative_length, path[:, dim]) for dim in range(3)]
    )


def _compute_corner_ideal_radii(
    path: NDArray[np.float64],
    cross_section_vertices: NDArray[np.float64],
    strategies: list[Callable[[NDArray[np.float64], float], NDArray[np.float64]]]
    | None = None,
) -> list[float]:
    """Return ideal fillet radius per interior vertex of *path*.

    Strategies are applied to the cross-section at the specific 't' value of
    each corner to determine the correct size for collision avoidance.
    """
    n_points = len(path)
    if n_points < 3:
        return []

    expanded_path = _expand_sharp_corners(path)
    _, frame_normals, frame_binormals = _compute_rmf_frames(expanded_path)

    segment_deltas = np.diff(path, axis=0)
    segment_lengths_raw = np.linalg.norm(segment_deltas, axis=1)
    segment_lengths: NDArray[np.float64] = np.maximum(
        segment_lengths_raw, 1e-10
    ).reshape(-1, 1)
    segment_tangents: NDArray[np.float64] = (
        segment_deltas / segment_lengths
    ).astype(np.float64)

    scalar_lengths: NDArray[np.float64] = np.linalg.norm(segment_deltas, axis=1)
    cumulative_length: NDArray[np.float64] = np.insert(
        np.cumsum(scalar_lengths), 0, 0.0
    )
    total_length: float = float(cumulative_length[-1])

    corner_radii: list[float] = []
    for i in range(1, n_points - 1):
        t_value: float = (
            float(cumulative_length[i]) / total_length if total_length > 1e-10 else 0.0
        )

        cross_section_at_corner = cross_section_vertices.copy()
        if strategies:
            for strategy in strategies:
                cross_section_at_corner = strategy(cross_section_at_corner, t_value)

        tangent_in: NDArray[np.float64] = segment_tangents[i - 1]
        tangent_out: NDArray[np.float64] = segment_tangents[i]

        turn_cross: NDArray[np.float64] = np.asarray(
            np.cross(tangent_in, tangent_out), dtype=np.float64
        )
        turn_norm: float = float(np.linalg.norm(turn_cross))
        if turn_norm < 1e-8:
            corner_radii.append(0.0)
            continue
        turn_normal: NDArray[np.float64] = turn_cross / turn_norm

        # Arrival frame at the duplicated corner vertex
        arrival_frame_index = 2 * i - 1
        frame_u: NDArray[np.float64] = frame_normals[arrival_frame_index]
        frame_v: NDArray[np.float64] = frame_binormals[arrival_frame_index]

        offsets: NDArray[np.float64] = (
            cross_section_at_corner[:, 0:1] * frame_u[np.newaxis, :]
            + cross_section_at_corner[:, 1:2] * frame_v[np.newaxis, :]
        )
        projection_onto_normal = np.sum(offsets * turn_normal[np.newaxis, :], axis=1)
        in_plane_offsets: NDArray[np.float64] = (
            offsets - projection_onto_normal[:, np.newaxis] * turn_normal[np.newaxis, :]
        )
        corner_radii.append(float(np.max(np.linalg.norm(in_plane_offsets, axis=1))))

    return corner_radii


def _expand_sharp_corners(path: NDArray[np.float64]) -> NDArray[np.float64]:
    if len(path) < 3:
        return path
    return np.concatenate([path[:1], np.repeat(path[1:-1], 2, axis=0), path[-1:]])


def _compute_rmf_frames(
    path: NDArray[np.float64],
    closed: bool = False,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Compute rotation-minimizing (Bishop) frames along a path."""
    n_points = len(path)

    segment_deltas = np.diff(path, axis=0)
    segment_lengths: NDArray[np.float64] = np.maximum(
        np.linalg.norm(segment_deltas, axis=1, keepdims=True), 1e-10
    )
    segment_tangents: NDArray[np.float64] = segment_deltas / segment_lengths

    tangents: NDArray[np.float64] = np.zeros((n_points, 3), dtype=np.float64)
    tangents[0] = segment_tangents[0]
    tangents[-1] = segment_tangents[-1]
    if n_points > 2:
        averaged = segment_tangents[:-1] + segment_tangents[1:]
        tangents[1:-1] = averaged / np.maximum(
            np.linalg.norm(averaged, axis=1, keepdims=True), 1e-10
        )

    initial_tangent: NDArray[np.float64] = tangents[0]
    up = np.array([0.0, 0.0, 1.0])
    if abs(float(np.dot(initial_tangent, up))) > 0.9:
        up = np.array([0.0, 1.0, 0.0])
    initial_normal: NDArray[np.float64] = np.asarray(
        np.cross(up, initial_tangent), dtype=np.float64
    )
    initial_normal /= float(np.linalg.norm(initial_normal))

    frame_normals: NDArray[np.float64] = np.zeros((n_points, 3), dtype=np.float64)
    frame_binormals: NDArray[np.float64] = np.zeros((n_points, 3), dtype=np.float64)
    frame_normals[0] = initial_normal
    frame_binormals[0] = np.asarray(
        np.cross(initial_tangent, initial_normal), dtype=np.float64
    )

    rotation_axes: NDArray[np.float64] = np.asarray(
        np.cross(tangents[:-1], tangents[1:]), dtype=np.float64
    )
    sin_angles: NDArray[np.float64] = np.linalg.norm(rotation_axes, axis=1)
    cos_angles: NDArray[np.float64] = np.clip(
        np.sum(tangents[:-1] * tangents[1:], axis=1), -1.0, 1.0
    )

    for i in range(n_points - 1):
        if float(sin_angles[i]) < 1e-10:
            frame_normals[i + 1] = frame_normals[i]
        else:
            rotation_axis: NDArray[np.float64] = rotation_axes[i] / float(sin_angles[i])
            normal = frame_normals[i]
            dot_axis_normal = float(np.dot(rotation_axis, normal))
            frame_normals[i + 1] = (
                normal * float(cos_angles[i])
                + np.cross(rotation_axis, normal) * float(sin_angles[i])
                + rotation_axis * dot_axis_normal * (1.0 - float(cos_angles[i]))
            )
            frame_normals[i + 1] /= float(np.linalg.norm(frame_normals[i + 1]))
        frame_binormals[i + 1] = np.cross(tangents[i + 1], frame_normals[i + 1])
        frame_binormals[i + 1] /= float(
            np.maximum(np.linalg.norm(frame_binormals[i + 1]), 1e-10)
        )

    if closed and n_points > 2:
        normal_end: NDArray[np.float64] = frame_normals[-1]
        normal_start: NDArray[np.float64] = frame_normals[0]
        tangent_end: NDArray[np.float64] = tangents[-1]
        cos_residual: float = float(np.clip(np.dot(normal_end, normal_start), -1.0, 1.0))
        sin_residual: float = float(np.dot(np.cross(normal_end, normal_start), tangent_end))
        residual_twist: float = float(np.arctan2(sin_residual, cos_residual))

        corrections = np.linspace(0, -residual_twist, n_points)
        cos_corrections = np.cos(corrections)
        sin_corrections = np.sin(corrections)
        new_normals = (
            frame_normals * cos_corrections[:, np.newaxis]
            + frame_binormals * sin_corrections[:, np.newaxis]
        )
        new_binormals = (
            -frame_normals * sin_corrections[:, np.newaxis]
            + frame_binormals * cos_corrections[:, np.newaxis]
        )
        frame_normals, frame_binormals = new_normals, new_binormals

    return tangents, frame_normals, frame_binormals


def _create_side_faces(
    boundary_edges: NDArray[np.int64],
    n_cross_section_vertices: int,
    n_transitions: int,
) -> NDArray[np.int64]:
    n_edges = len(boundary_edges)
    total_quads = n_edges * n_transitions

    tiled_edges = np.tile(boundary_edges, (n_transitions, 1))
    ring_offsets = (
        np.repeat(np.arange(n_transitions, dtype=np.int64), n_edges)
        * n_cross_section_vertices
    )
    tiled_edges = tiled_edges + ring_offsets[:, np.newaxis]

    v0 = tiled_edges[:, 0]
    v1 = tiled_edges[:, 1]
    v2 = v0 + n_cross_section_vertices
    v3 = v1 + n_cross_section_vertices

    side_faces = np.empty((total_quads * 2, 3), dtype=np.int64)
    side_faces[:total_quads, 0] = v0
    side_faces[:total_quads, 1] = v1
    side_faces[:total_quads, 2] = v2
    side_faces[total_quads:, 0] = v1
    side_faces[total_quads:, 1] = v3
    side_faces[total_quads:, 2] = v2

    return side_faces


def _path_extrude_polygon(
    polygon: Polygon,
    path: NDArray[np.float64],
    closed: bool,
    strategies: list[Callable[[NDArray[np.float64], float], NDArray[np.float64]]] | None,
) -> Trimesh:
    n_path_points = len(path)

    triangulated_vertices, triangulated_faces = triangulate_polygon(
        polygon, engine="earcut"
    )
    n_cross_section_vertices = len(triangulated_vertices)

    all_edges: NDArray[np.int64] = np.asarray(
        faces_to_edges(triangulated_faces), dtype=np.int64
    )
    boundary_mask: NDArray[np.intp] = np.asarray(
        group_rows(np.sort(all_edges, axis=1), require_count=1), dtype=np.intp
    )
    boundary_edges: NDArray[np.int64] = all_edges[boundary_mask].astype(np.int64)

    _, frame_normals, frame_binormals = _compute_rmf_frames(path, closed=closed)

    segment_deltas = np.diff(path, axis=0)
    segment_lengths: NDArray[np.float64] = np.linalg.norm(segment_deltas, axis=1)
    cumulative_length: NDArray[np.float64] = np.insert(
        np.cumsum(segment_lengths), 0, 0.0
    )
    total_length: float = float(cumulative_length[-1])

    if not strategies:
        # Fully vectorised fast path: (n_path_points, n_cross_section_vertices, 3)
        cross_x: NDArray[np.float64] = triangulated_vertices[:, 0]
        cross_y: NDArray[np.float64] = triangulated_vertices[:, 1]
        vertices_3d: NDArray[np.float64] = (
            path[:, np.newaxis, :]
            + cross_x[np.newaxis, :, np.newaxis] * frame_normals[:, np.newaxis, :]
            + cross_y[np.newaxis, :, np.newaxis] * frame_binormals[:, np.newaxis, :]
        ).reshape(-1, 3)
    else:
        path_t_values = (
            cumulative_length / total_length
            if total_length > 1e-10
            else np.zeros(n_path_points)
        )
        rings: list[NDArray[np.float64]] = []
        for i in range(n_path_points):
            cross_section = triangulated_vertices.copy()
            for strategy in strategies:
                cross_section = strategy(cross_section, float(path_t_values[i]))
            cross_x_i: NDArray[np.float64] = cross_section[:, 0]
            cross_y_i: NDArray[np.float64] = cross_section[:, 1]
            rings.append(
                path[i]
                + cross_x_i[:, np.newaxis] * frame_normals[i]
                + cross_y_i[:, np.newaxis] * frame_binormals[i]
            )
        vertices_3d = np.vstack(rings)

    if closed:
        n_transitions = n_path_points - 1
        side_faces = _create_side_faces(
            boundary_edges, n_cross_section_vertices, n_transitions
        )

        last_ring_start = n_cross_section_vertices * (n_path_points - 1)
        wraps_to_first_ring = side_faces >= last_ring_start
        side_faces[wraps_to_first_ring] -= last_ring_start

        vertices_3d = vertices_3d[:last_ring_start]
        all_faces = side_faces
    else:
        side_faces = _create_side_faces(
            boundary_edges, n_cross_section_vertices, n_path_points - 1
        )

        start_cap_faces: NDArray[np.int64] = triangulated_faces[:, ::-1]
        end_cap_faces: NDArray[np.int64] = (
            triangulated_faces + n_cross_section_vertices * (n_path_points - 1)
        ).astype(np.int64)
        all_faces = np.vstack([start_cap_faces, side_faces, end_cap_faces])

    return Trimesh(vertices=vertices_3d, faces=all_faces, process=False)


def path_extrude_shape(
    shape: Shape,
    path: ArrayLike,
    fillet_segments: int | None = None,
    min_fillet_radius: float | None = None,
    intermediate_sections: int | None = None,
    strategy: list[Callable[[NDArray[np.float64], float], NDArray[np.float64]]]
    | Callable[[NDArray[np.float64], float], NDArray[np.float64]]
    | None = None,
) -> Solid:
    """Sweep a 2D shape along a 3D path to produce a solid.

    Parameters
    ----------
    shape : Shape
        The 2D cross-section to sweep.
    path : array-like of shape (n, 3)
        Sequence of 3D points defining the sweep path.
    fillet_segments : int or None, optional
        Number of arc segments per corner.  ``None`` disables filleting entirely
        (classic bishop extrusion with no corner rounding).
    min_fillet_radius : float or None, optional
        Lower bound on the per-corner fillet radius.  The ideal radius is
        computed automatically per corner; this clamps it from below.
    intermediate_sections : int or None, optional
        Number of intermediate cross-section planes to insert uniformly along
        the path, after filleting.
    strategy : Callable[[NDArray[np.float64], float], NDArray[np.float64]] or list[Callable[[NDArray[np.float64], float], NDArray[np.float64]]], optional
        A function or list of functions with signature ``(points, t) -> points``.
        ``points`` is an ``(N, 2)`` array of cross-section vertices and ``t`` is
        the normalised position along the path (0 → start, 1 → end).

    Returns
    -------
    Solid
        The resulting 3D solid.
    """
    from scadpy import Part, Solid

    path_array: NDArray[np.float64] = np.asarray(path, dtype=np.float64)

    strategies: list[Callable[[NDArray[np.float64], float], NDArray[np.float64]]] = []
    if strategy is not None:
        strategies = strategy if isinstance(strategy, list) else [strategy]

    # 1. Handle filleting
    if min_fillet_radius is not None and fillet_segments is None:
        fillet_segments = 16

    if fillet_segments:
        all_exterior_coords: list[NDArray[np.float64]] = []
        for part in shape._parts:
            coords = np.asarray(part.geometry.exterior.coords, dtype=np.float64)
            all_exterior_coords.append(coords[:, :2])
        cross_section_vertices = (
            np.concatenate(all_exterior_coords, axis=0)
            if all_exterior_coords
            else np.zeros((1, 2))
        )

        corner_radii = _compute_corner_ideal_radii(
            path_array, cross_section_vertices, strategies
        )

        if min_fillet_radius is not None:
            corner_radii = [max(r, min_fillet_radius) for r in corner_radii]

        if any(r > 0 for r in corner_radii):
            path_array = _fillet_path(path_array, corner_radii, fillet_segments)

    # 2. Handle intermediate sections
    if intermediate_sections is not None and intermediate_sections > 0:
        path_array = _refine_path_uniform(path_array, intermediate_sections)

    # Auto-detect closed path
    closed = bool(np.linalg.norm(path_array[0] - path_array[-1]) < 1e-6)

    parts = [
        Part[Trimesh].from_geometry(
            _path_extrude_polygon(
                part.geometry,
                path_array,
                closed=closed,
                strategies=strategies if strategies else None,
            ),
            part.color,
        )
        for part in shape._parts
    ]
    return Solid.from_parts(parts)
