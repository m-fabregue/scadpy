from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from shapely.geometry import Polygon
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Shape, TopologyFilter


@typechecked
def fillet_shape(
    shape: Shape,
    size: float | np.ndarray,
    corner_filter: TopologyFilter[Shape] | None = None,
    segment_count: int = 32,
    epsilon: float = 1e-8,
) -> Shape:
    """
    Apply a fillet (circular arc) to every corner of a shape.

    Convex corners are rounded; concave corners are filled with a circular arc.

    Parameters
    ----------
    shape : Shape
        The input shape to fillet.
    size : float or ndarray
        Fillet size: distance from the corner vertex to each tangent point along
        the edges. Can be:

        - ``float``: same size on both sides of every corner.
        - ``(n_active,)``: per-active-corner size, same on both sides.
        - ``(n_active, 2)``: per-active-corner, per-side size. Column 0 is
          the incoming side, column 1 is the outgoing side.

        ``n_active`` is the number of corners selected by ``corner_filter``
        (or all corners if no filter). In all cases, each value is
        automatically clamped to half the length of the corresponding edge
        to avoid overlapping tangent points.
    corner_filter : TopologyFilter[Shape] | None, optional
        Boolean mask or callable ``(shape) -> NDArray[bool]`` of length ``n_corners``
        selecting which corners to fillet. If None, all corners are filleted.
    segment_count : int, optional
        Number of arc segments per corner. Defaults to 32.
    epsilon : float, optional
        Small offset used to avoid coincident edges in boolean operations.
        Defaults to ``1e-8``.

    Returns
    -------
    Shape
        A new shape with filleted corners.

    Examples
    --------
    >>> from scadpy import square, polygon, fillet_shape

    >>> sq = square(4)
    >>> l_shape = polygon(
    ...     [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]
    ... )
    >>> arrow = polygon(
    ...     [(0, 1), (3, 0), (5, 2), (3, 4),
    ...      (0, 3), (1, 2.5), (1, 1.5)]
    ... )

    >>> # all corners
    >>> fillet_shape(sq, size=1.0)  # doctest: +SKIP

    .. render-example::
        :name: fillet_shape_all
        :example: fillet_shape(sq, size=1.0)
        :ghost: sq

    >>> # convex corners only (the 5 outer corners of the L-shape)
    >>> fillet_shape(  # doctest: +SKIP
    ...     l_shape, size=0.5,
    ...     corner_filter=lambda s: s.are_corners_convex,
    ... )

    .. render-example::
        :name: fillet_shape_convex_only
        :example: fillet_shape(l_shape, size=0.5, corner_filter=lambda s: s.are_corners_convex)
        :ghost: l_shape

    >>> import numpy as np

    >>> # asymmetric: one side fills the full edge (length 2),
    >>> # the other stays at 1.0
    >>> fillet_shape(  # doctest: +SKIP
    ...     l_shape, size=np.array([[2.0, 1.0]]),
    ...     corner_filter=lambda s: ~s.are_corners_convex,
    ... )

    .. render-example::
        :name: fillet_shape_concave_asymmetric
        :example: fillet_shape(l_shape, size=np.array([[2.0, 1.0]]), corner_filter=lambda s: ~s.are_corners_convex)
        :ghost: l_shape

    >>> # only sharp convex corners (angle > 100°):
    >>> # the two 135° corners of the arrow tail
    >>> fillet_shape(  # doctest: +SKIP
    ...     arrow, size=0.4,
    ...     corner_filter=lambda s: (
    ...         s.are_corners_convex & (s.corner_angles > 100)
    ...     ),
    ... )

    .. render-example::
        :name: fillet_shape_sharp_convex
        :example: fillet_shape(arrow, size=0.4, corner_filter=lambda s: s.are_corners_convex & (s.corner_angles > 100))
        :ghost: arrow

    >>> # oversized: the 2 concave corners share an edge of length ~1;
    >>> # size=10 is clamped proportionally so their contributions
    >>> # sum to the edge length (0.5 + 0.5 each)
    >>> fillet_shape(  # doctest: +SKIP
    ...     arrow, size=10,
    ...     corner_filter=lambda s: ~s.are_corners_convex,
    ... )

    .. render-example::
        :name: fillet_shape_clamp_proportional
        :example: fillet_shape(arrow, size=10, corner_filter=lambda s: ~s.are_corners_convex)
        :ghost: arrow

    >>> # wrong size length raises ValueError
    >>> fillet_shape(
    ...     sq, size=np.array([0.5, 0.5, 0.5])
    ... )  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: size array shape (3, 2) does not match...
    """
    from scadpy import resolve_topology_filter, Shape

    corner_to_vertex = shape.corner_to_vertex
    if len(corner_to_vertex) == 0:
        return shape

    vertex_coordinates = shape.vertex_coordinates
    is_corner_convex = shape.are_corners_convex

    active_mask = resolve_topology_filter(shape, len(corner_to_vertex), corner_filter)
    if active_mask is not None and not np.any(active_mask):
        return shape

    # Filter all per-corner data to active corners only
    active_indices = (
        np.where(active_mask)[0]
        if active_mask is not None
        else np.arange(len(corner_to_vertex))
    )
    active_is_corner_convex = is_corner_convex[active_indices]

    current_vertices = vertex_coordinates[corner_to_vertex[active_indices, 1]]

    incoming_de = shape.corner_to_incoming_directed_edge[active_indices]
    outgoing_de = shape.corner_to_outgoing_directed_edge[active_indices]
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
            f"expected ({n_active}, 2) for {n_active} active corners"
        )
    # Clamp sizes proportionally so adjacent corners don't overlap on a shared edge.
    # For each active corner, find the adjacent corner on its outgoing/incoming edge.
    # If both are active: scale both contributions so they sum to at most edge_length.
    # If only one is active: it can use the full edge length.
    active_index_of = np.full(len(shape.corner_to_vertex), -1, dtype=np.int64)
    active_index_of[active_indices] = np.arange(n_active, dtype=np.int64)
    de_to_corner = shape.directed_edge_to_corner
    sizes_orig = sizes.copy()

    adj_target_out = de_to_corner[outgoing_de, 1]
    adj_idx_out = active_index_of[adj_target_out]
    adj_size_out = np.where(adj_idx_out >= 0, sizes_orig[adj_idx_out.clip(0), 0], 0.0)
    total_out = sizes_orig[:, 1] + adj_size_out
    scale_out = np.where(
        total_out > edge_lengths_outgoing, edge_lengths_outgoing / total_out, 1.0
    )
    sizes[:, 1] *= scale_out

    adj_source_in = de_to_corner[incoming_de, 0]
    adj_idx_in = active_index_of[adj_source_in]
    adj_size_in = np.where(adj_idx_in >= 0, sizes_orig[adj_idx_in.clip(0), 1], 0.0)
    total_in = sizes_orig[:, 0] + adj_size_in
    scale_in = np.where(
        total_in > edge_lengths_incoming, edge_lengths_incoming / total_in, 1.0
    )
    sizes[:, 0] *= scale_in

    signs = np.where(active_is_corner_convex, 1.0, -1.0)

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

    # Extended corner vertex: push outward along the bisector
    corner_normals = shape.corner_normals[active_indices]
    current_vertices_extended = current_vertices + corner_normals * epsilon

    # Elliptic arc centered on the corner vertex:
    # P(t) = corner - a*cos(t)*incoming_dir + b*sin(t)*outgoing_dir,  t ∈ [0, π/2]
    # At t=0: corner - a*incoming_dir = tp_in
    # At t=π/2: corner + b*outgoing_dir = tp_out
    # The arc bulges away from the corner (toward the shape interior for convex corners).
    t_values = np.linspace(0.0, np.pi / 2, segment_count)  # (segment_count,)
    cos_t = np.cos(t_values)  # (segment_count,)
    sin_t = np.sin(t_values)  # (segment_count,)

    cutters: list[Polygon] = []
    fillers: list[Polygon] = []
    for i in range(n_active):
        a = sizes[i, 0] + epsilon
        b = sizes[i, 1] + epsilon
        corner_ext = current_vertices_extended[i]
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

        # Polygon: extended corner → outer tp_in → arc → outer tp_out
        # For convex: corner_ext is outside the arc → polygon is the wedge to cut
        # For concave: corner_ext is inside the arc → polygon is the notch to fill
        polygon = Polygon(
            [
                corner_ext,
                tangent_points_outgoing_outer[i],
                *arc_points,
                tangent_points_incoming_outer[i],
            ]
        )
        if polygon.is_empty or not polygon.is_valid:
            continue
        if active_is_corner_convex[i]:
            cutters.append(polygon)
        else:
            fillers.append(polygon)

    result = shape
    if cutters:
        result = result - Shape.from_geometries(cutters)
    if fillers:
        result = result | Shape.from_geometries(fillers)

    return result
