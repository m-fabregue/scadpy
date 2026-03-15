from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from shapely.geometry import Polygon

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


def fillet_shape(
    shape: Shape,
    size: float | np.ndarray,
    vertex_filter: TopologyFilter[Shape] | None = None,
    segment_count: int = 32,
    epsilon: float = 1e-8,
) -> Shape:
    """
    Apply a fillet (circular arc) to every vertex of a shape.

    Convex vertices are rounded; concave vertices are filled with a circular arc.

    Parameters
    ----------
    shape : Shape
        The input shape to fillet.
    size : float or ndarray
        Fillet size: distance from the vertex to each tangent point along
        the edges. Can be:

        - ``float``: same size on both sides of every vertex.
        - ``(n_active,)``: per-active-vertex size, same on both sides.
        - ``(n_active, 2)``: per-active-vertex, per-side size. Column 0 is
          the incoming side, column 1 is the outgoing side.

        ``n_active`` is the number of vertices selected by ``vertex_filter``
        (or all vertices if no filter). In all cases, each value is
        automatically clamped to half the length of the corresponding edge
        to avoid overlapping tangent points.
    vertex_filter : TopologyFilter[Shape] | None, optional
        Boolean mask or callable ``(shape) -> NDArray[bool]`` of length ``n_vertices``
        selecting which vertices to fillet. If None, all vertices are filleted.
    segment_count : int, optional
        Number of arc segments per vertex. Defaults to 32.
    epsilon : float, optional
        Small offset used to avoid coincident edges in boolean operations.
        Defaults to ``1e-8``.

    Returns
    -------
    Shape
        A new shape with filleted vertices.

    Examples
    --------
    >>> from scadpy import square, fillet_shape
    >>> import numpy as np

    >>> sq = square(4)

    >>> # wrong size length raises ValueError
    >>> fillet_shape(
    ...     sq, size=np.array([0.5, 0.5, 0.5])
    ... )  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: size array shape (3, 2) does not match...
    """
    from scadpy import resolve_topology_filter, Shape

    vertex_neighborhoods = shape.vertex_to_neighbor_vertex
    if len(vertex_neighborhoods) == 0:
        return shape

    vertex_coordinates = shape.vertex_coordinates
    is_vertex_convex = shape.are_vertices_convex

    active_mask = resolve_topology_filter(shape, len(vertex_neighborhoods), vertex_filter)
    if active_mask is not None and not np.any(active_mask):
        return shape

    # Filter all per-vertex data to active vertices only
    active_indices = (
        np.where(active_mask)[0]
        if active_mask is not None
        else np.arange(len(vertex_neighborhoods))
    )
    active_is_vertex_convex = is_vertex_convex[active_indices]

    current_vertices = vertex_coordinates[active_indices]

    incoming_de = shape.vertex_to_incoming_directed_edge[active_indices]
    outgoing_de = shape.vertex_to_outgoing_directed_edge[active_indices]
    incoming_edge = shape.directed_edge_to_edge[incoming_de]
    outgoing_edge = shape.directed_edge_to_edge[outgoing_de]

    incoming_directions_normalized = shape.directed_edge_directions[incoming_de]
    outgoing_directions_normalized = shape.directed_edge_directions[outgoing_de]
    edge_lengths_incoming = shape.edge_lengths[incoming_edge]
    edge_lengths_outgoing = shape.edge_lengths[outgoing_edge]
    outward_normals_incoming = shape.edge_normals[incoming_edge]
    outward_normals_outgoing = shape.edge_normals[outgoing_edge]

    # Resolve size to (n_active, 2): column 0 = incoming side, column 1 = outgoing side
    n_active = len(current_vertices)
    sizes = np.asarray(size, dtype=np.float64)
    if sizes.ndim == 0:
        sizes = np.full((n_active, 2), sizes)
    elif sizes.ndim == 1:
        sizes = np.stack([sizes, sizes], axis=1)
    if sizes.shape != (n_active, 2):
        raise ValueError(
            f"size array shape {sizes.shape} does not match "
            f"expected ({n_active}, 2) for {n_active} active vertices"
        )
    # Clamp sizes proportionally so adjacent vertices don't overlap on a shared edge.
    # For each active vertex, find the adjacent vertex on its outgoing/incoming edge.
    # If both are active: scale both contributions so they sum to at most edge_length.
    # If only one is active: it can use the full edge length.
    active_index_of = np.full(len(shape.vertex_to_neighbor_vertex), -1, dtype=np.int64)
    active_index_of[active_indices] = np.arange(n_active, dtype=np.int64)
    de_to_vertex = shape.directed_edge_to_vertex
    sizes_orig = sizes.copy()

    adj_target_out = de_to_vertex[outgoing_de, 1]
    adj_idx_out = active_index_of[adj_target_out]
    adj_size_out = np.where(adj_idx_out >= 0, sizes_orig[adj_idx_out.clip(0), 0], 0.0)
    total_out = sizes_orig[:, 1] + adj_size_out
    scale_out = np.where(
        total_out > edge_lengths_outgoing, edge_lengths_outgoing / total_out, 1.0
    )
    sizes[:, 1] *= scale_out

    adj_source_in = de_to_vertex[incoming_de, 0]
    adj_idx_in = active_index_of[adj_source_in]
    adj_size_in = np.where(adj_idx_in >= 0, sizes_orig[adj_idx_in.clip(0), 1], 0.0)
    total_in = sizes_orig[:, 0] + adj_size_in
    scale_in = np.where(
        total_in > edge_lengths_incoming, edge_lengths_incoming / total_in, 1.0
    )
    sizes[:, 0] *= scale_in

    signs = np.where(active_is_vertex_convex, 1.0, -1.0)

    # Tangent points: slightly beyond size to avoid coincident inner points
    tangent_points_incoming = current_vertices - incoming_directions_normalized * (
        sizes[:, 0:1] + epsilon
    )
    tangent_points_outgoing = current_vertices + outgoing_directions_normalized * (
        sizes[:, 1:2] + epsilon
    )

    # Outer offsets: perpendicular to edge to avoid coincident outer points
    tangent_points_incoming_outer = (
        tangent_points_incoming
        + signs[:, np.newaxis] * outward_normals_incoming * epsilon
    )
    tangent_points_outgoing_outer = (
        tangent_points_outgoing
        + signs[:, np.newaxis] * outward_normals_outgoing * epsilon
    )

    # Extended vertex: push outward along the bisector
    vertex_normals = shape.vertex_normals[active_indices]
    current_vertices_extended = current_vertices + vertex_normals * epsilon

    # Elliptic arc centered on the vertex:
    # P(t) = vertex - a*cos(t)*incoming_dir + b*sin(t)*outgoing_dir,  t ∈ [0, π/2]
    # At t=0: vertex - a*incoming_dir = tp_in
    # At t=π/2: vertex + b*outgoing_dir = tp_out
    # The arc bulges away from the vertex (toward the shape interior for convex vertices).
    t_values = np.linspace(0.0, np.pi / 2, segment_count)  # (segment_count,)
    cos_t = np.cos(t_values)  # (segment_count,)
    sin_t = np.sin(t_values)  # (segment_count,)

    cutters: list[Polygon] = []
    fillers: list[Polygon] = []
    for i in range(n_active):
        a = sizes[i, 0] + epsilon
        b = sizes[i, 1] + epsilon
        vertex_ext = current_vertices_extended[i]
        inc = incoming_directions_normalized[i]
        out = outgoing_directions_normalized[i]

        # Elliptic arc points using epsilon-extended sizes: (segment_count, 2)
        arc_points = (
            current_vertices[i]
            - a * cos_t[:, np.newaxis] * inc
            + b * sin_t[:, np.newaxis] * out
        )

        # Double mirror = 180° rotation around midpoint of p0→p1
        mid = (arc_points[0] + arc_points[-1]) / 2
        arc_points = 2 * mid - arc_points

        # Polygon: extended vertex → outer tp_in → arc → outer tp_out
        # For convex: vertex_ext is outside the arc → polygon is the wedge to cut
        # For concave: vertex_ext is inside the arc → polygon is the notch to fill
        polygon = Polygon(
            [
                vertex_ext,
                tangent_points_outgoing_outer[i],
                *arc_points,
                tangent_points_incoming_outer[i],
            ]
        )
        if polygon.is_empty or not polygon.is_valid:
            continue
        if active_is_vertex_convex[i]:
            cutters.append(polygon)
        else:
            fillers.append(polygon)

    result = shape
    if cutters:
        result = result - Shape.from_geometries(cutters)
    if fillers:
        result = result | Shape.from_geometries(fillers)

    return result
