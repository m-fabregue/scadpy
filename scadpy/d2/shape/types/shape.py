from __future__ import annotations

from collections.abc import Iterable, Sequence
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self, final

import numpy as np
from numpy.typing import NDArray
from shapely.geometry.polygon import Polygon
from typeguard import typechecked

from scadpy.color.constants import BLACK, WHITE
from scadpy.core.assembly import Assembly

if TYPE_CHECKING:
    from IPython.core.display import HTML

    from scadpy import Color, Part, Solid, TopologyFilter


@final
@typechecked
class Shape(Assembly[Polygon]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pyright: ignore[reportExplicitAny, reportAny]
        super().__init__(*args, **kwargs)

    @classmethod
    def dimensions(cls) -> int:
        return 2

    ##########
    # vertex #
    ##########

    @cached_property
    def vertex_coordinates(self: Self) -> NDArray[np.float64]:
        """For each vertex in the shape, return its coordinates.

        See :func:`get_shape_vertex_coordinates` for parameter documentation.

        Examples
        --------
        >>> from shapely.geometry import Polygon
        >>> from scadpy import Shape

        >>> polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
        >>> Shape.from_geometry(polygon).vertex_coordinates  # doctest: +NORMALIZE_WHITESPACE
        array([[0., 0.],
               [2., 0.],
               [2., 2.],
               [0., 2.]])
        """
        from scadpy import get_shape_vertex_coordinates

        return get_shape_vertex_coordinates(self)

    @cached_property
    def vertex_to_part(self: Self) -> NDArray[np.int64]:
        """For each vertex in the shape, return its part index.

        See :func:`get_shape_vertex_to_part` for parameter documentation.

        Examples
        --------
        >>> from shapely.geometry import Polygon
        >>> from scadpy import Shape

        >>> p1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
        >>> p2 = Polygon([(10, 10), (12, 10), (12, 12), (10, 12)])
        >>> Shape.from_geometries([p1, p2]).vertex_to_part  # doctest: +NORMALIZE_WHITESPACE
        array([0, 0, 0, 0, 1, 1, 1, 1])
        """
        from scadpy import get_shape_vertex_to_part

        return get_shape_vertex_to_part(self)

    def recoordinate(self: Self, vertex_coordinates: NDArray[np.float64]) -> Shape:
        """Rebuild this shape with new vertex coordinates.

        Shortcut for :func:`recoordinate_shape`.
        See :func:`recoordinate_shape` for full documentation.
        """
        from scadpy.d2.shape import recoordinate_shape

        return recoordinate_shape(self, vertex_coordinates)

    ############
    # features #
    ############

    @cached_property
    def is_empty(self: Self) -> bool:
        """Return whether the shape has no vertices.

        See :func:`is_shape_empty` for parameter documentation.

        Examples
        --------
        >>> from shapely.geometry import Polygon
        >>> from scadpy import Shape

        >>> Shape.from_parts([]).is_empty
        True

        >>> polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
        >>> Shape.from_geometry(polygon).is_empty
        False
        """
        from scadpy import is_shape_empty

        return is_shape_empty(self)

    @cached_property
    def bounds(self: Self) -> NDArray[np.float64]:
        """Return the axis-aligned bounding box of the shape.

        See :func:`get_shape_bounds` for parameter documentation.

        Examples
        --------
        >>> from shapely.geometry import Polygon
        >>> from scadpy import Shape

        >>> polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
        >>> Shape.from_geometry(polygon).bounds
        array([0., 0., 2., 2.])
        """
        from scadpy import get_shape_bounds

        return get_shape_bounds(self)

    ################
    # combinations #
    ################

    def __add__(self: Self, other: Shape) -> Shape:
        """Concatenate two shapes. Shortcut for :func:`concat_shape`."""
        from scadpy import concat_shape

        return concat_shape(shapes=[self, other])

    def __or__(self: Self, other: Shape) -> Shape:
        """Unite two shapes. Shortcut for :func:`unify_shape`."""
        from scadpy import unify_shape

        return unify_shape(shapes=[self, other])

    def __and__(self: Self, other: Shape) -> Shape:
        """Intersect two shapes. Shortcut for :func:`intersect_shape`."""
        from scadpy import intersect_shape

        return intersect_shape(shapes=[self, other])

    def __sub__(self: Self, other: Shape) -> Shape:
        """Subtract a shape from this shape. Shortcut for :func:`subtract_shape`."""
        from scadpy import subtract_shape

        return subtract_shape(to_be_subtracted=self, to_subtract=other)

    def __xor__(self: Self, other: Shape) -> Shape:
        """Compute symmetric difference with another shape. Shortcut for :func:`exclude_shape`."""
        from scadpy import exclude_shape

        return exclude_shape(shapes=[self, other])

    def concat(self: Self, shapes: Sequence[Shape]) -> Shape:
        """Concatenate this shape with others (no boolean merge).

        See :func:`concat_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> square(4).concat([circle(2).translate([3, 2])])  # doctest: +SKIP

        .. render-example::
            :name: concat_shape
            :example: square(4) + circle(radius=2).translate([3, 2])
        """
        from scadpy import concat_shape

        return concat_shape(shapes=[self, *shapes])

    def unify(self: Self, shapes: Sequence[Shape]) -> Shape:
        """Unite this shape with others.

        See :func:`unify_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> square(4).unify([circle(2).translate([2, 0])])  # doctest: +SKIP

        .. render-example::
            :name: unify_shape
            :example: square(4) | circle(radius=2).translate([2, 0])
        """
        from scadpy import unify_shape

        return unify_shape(shapes=[self, *shapes])

    def intersect(self: Self, shapes: Sequence[Shape]) -> Shape:
        """Intersect this shape with others.

        See :func:`intersect_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> square(4).intersect([circle(2).translate([1, 1])])  # doctest: +SKIP

        .. render-example::
            :name: intersect_shape
            :example: square(4) & circle(radius=2).translate([1, 1])
            :ghost: square(4)
        """
        from scadpy import intersect_shape

        return intersect_shape(shapes=[self, *shapes])

    def subtract(self: Self, other: Shape) -> Shape:
        """Subtract a shape from this shape.

        See :func:`subtract_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> square(4).subtract(circle(1))  # doctest: +SKIP

        .. render-example::
            :name: subtract_shape
            :example: square(4) - circle(radius=1)
            :ghost: square(4)
        """
        from scadpy import subtract_shape

        return subtract_shape(to_be_subtracted=self, to_subtract=other)

    def exclude(self: Self, shapes: Sequence[Shape]) -> Shape:
        """Compute the symmetric difference of this shape with others.

        See :func:`exclude_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> square(4).exclude([circle(2).translate([1, 1])])  # doctest: +SKIP

        .. render-example::
            :name: exclude_shape
            :example: square(4) ^ circle(radius=2).translate([1, 1])
            :ghost: square(4)
        """
        from scadpy import exclude_shape

        return exclude_shape(shapes=[self, *shapes])

    ##############
    # topologies #
    ##############

    @cached_property
    def part_colors(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_assembly_part_colors`.

        See :func:`get_assembly_part_colors` for full documentation.
        """
        from scadpy.core.assembly import get_assembly_part_colors

        return get_assembly_part_colors(self)

    @cached_property
    def ring_to_part(self: Self) -> NDArray[np.int64]:
        """For each ring in the shape, return its part index.

        See :func:`get_shape_ring_to_part` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> # square with a hole (2 rings in part 0)
        >>> # unioned with a separate square (1 ring in part 1)
        >>> shape = (square(2) - square(1)) | square(1).translate([5, 0])
        >>> shape.ring_to_part  # doctest: +NORMALIZE_WHITESPACE
        array([0, 0, 1])
        """
        from scadpy.d2.shape import get_shape_ring_to_part

        return get_shape_ring_to_part(self)

    @cached_property
    def ring_types(self: Self) -> NDArray[np.object_]:
        """For each ring in the shape, return its type ('exterior' or 'interior').

        See :func:`get_shape_ring_types` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> # square with a hole (exterior + interior)
        >>> # unioned with a separate square (exterior only)
        >>> shape = (square(2) - square(1)) | square(1).translate([5, 0])
        >>> shape.ring_types  # doctest: +NORMALIZE_WHITESPACE
        array(['exterior', 'interior', 'exterior'], dtype=object)
        """
        from scadpy.d2.shape import get_shape_ring_types

        return get_shape_ring_types(self)

    @cached_property
    def vertex_to_ring(self: Self) -> NDArray[np.int64]:
        """For each vertex in the shape, return the index of the ring it belongs to.

        See :func:`get_shape_vertex_to_ring` for parameter documentation.

        Examples
        --------
        >>> from scadpy import polygon, square

        >>> # two separate triangles: 3 vertices in ring 0, 3 in ring 1
        >>> shape = (
        ...     polygon([(0, 0), (1, 0), (0.5, 1)])
        ...     | polygon([(5, 0), (6, 0), (5.5, 1)])
        ... )
        >>> shape.vertex_to_ring  # doctest: +NORMALIZE_WHITESPACE
        array([0, 0, 0, 1, 1, 1])

        >>> # square with a hole: 4 exterior vertices in ring 0,
        >>> # 4 interior vertices in ring 1
        >>> (square(4) - square(2)).vertex_to_ring  # doctest: +NORMALIZE_WHITESPACE
        array([0, 0, 0, 0, 1, 1, 1, 1])
        """
        from scadpy.d2.shape import get_shape_vertex_to_ring

        return get_shape_vertex_to_ring(self)

    @cached_property
    def vertex_to_neighbor_vertex(self: Self) -> NDArray[np.int64]:
        """For each vertex in the shape, return its two neighbor vertex indices (prev, next).

        See :func:`get_shape_vertex_to_neighbor_vertex` for parameter documentation.

        Examples
        --------
        >>> from scadpy import polygon

        >>> triangle = polygon([(0, 0), (1, 0), (0.5, 1)])
        >>> triangle.vertex_to_neighbor_vertex  # doctest: +NORMALIZE_WHITESPACE
        array([[2, 1],
               [0, 2],
               [1, 0]])
        """
        from scadpy.d2.shape import get_shape_vertex_to_neighbor_vertex

        return get_shape_vertex_to_neighbor_vertex(self)

    @cached_property
    def vertex_angles(self: Self) -> NDArray[np.float64]:
        """For each vertex in the shape, return its interior angle in degrees.

        See :func:`get_shape_vertex_angles` for parameter documentation.

        Examples
        --------
        >>> from scadpy import polygon

        >>> # arrow: 5 convex vertices + 2 concave vertices,
        >>> # all with different angles
        >>> arrow = polygon(
        ...     [(0, 1), (3, 0), (5, 2), (3, 4),
        ...      (0, 3), (1, 2.5), (1, 1.5)]
        ... )
        >>> arrow.vertex_angles.round(2).tolist()
        [135.0, 63.43, 90.0, 63.43, 135.0, 63.43, 63.43]
        """
        from scadpy.d2.shape import get_shape_vertex_angles

        return get_shape_vertex_angles(self)

    @cached_property
    def are_vertices_convex(self: Self) -> NDArray[np.bool_]:
        """For each vertex in the shape, return whether it is convex.

        See :func:`are_shape_vertices_convex` for parameter documentation.

        Examples
        --------
        >>> from scadpy import polygon

        >>> # arrow: 5 convex vertices (tip and sides)
        >>> # + 2 concave vertices (the tail notch)
        >>> arrow = polygon(
        ...     [(0, 1), (3, 0), (5, 2), (3, 4),
        ...      (0, 3), (1, 2.5), (1, 1.5)]
        ... )
        >>> arrow.are_vertices_convex.tolist()
        [True, True, True, True, True, False, False]
        """
        from scadpy.d2.shape import are_shape_vertices_convex

        return are_shape_vertices_convex(self)

    @cached_property
    def vertex_normals(self: Self) -> NDArray[np.float64]:
        """For each vertex in the shape, return its outward unit normal.

        See :func:`get_shape_vertex_normals` for parameter documentation.

        Examples
        --------
        >>> from scadpy import polygon

        >>> # arrow: 5 convex vertices (normals point outward)
        >>> # + 2 concave vertices (normals point inward,
        >>> # into the tail notch — x component is positive)
        >>> arrow = polygon(
        ...     [(0, 1), (3, 0), (5, 2), (3, 4),
        ...      (0, 3), (1, 2.5), (1, 1.5)]
        ... )
        >>> arrow.vertex_normals.round(4)  # doctest: +NORMALIZE_WHITESPACE
        array([[-0.9975, -0.0709],
               [ 0.2298, -0.9732],
               [ 1.    ,  0.    ],
               [ 0.2298,  0.9732],
               [-0.9975,  0.0709],
               [ 0.8507,  0.5257],
               [ 0.8507, -0.5257]])
        """
        from scadpy.d2.shape import get_shape_vertex_normals

        return get_shape_vertex_normals(self)

    @cached_property
    def vertex_to_outgoing_directed_edge(self: Self) -> NDArray[np.int64]:
        """For each vertex in the shape, return the index of its outgoing directed edge.

        See :func:`get_shape_vertex_to_outgoing_directed_edge` for parameter documentation.

        Examples
        --------
        >>> from scadpy import polygon

        >>> # triangle: vertices (2,0,1), (0,1,2), (1,2,0)
        >>> # outgoing: 0→1, 1→2, 2→0
        >>> triangle = polygon([(0, 0), (1, 0), (0.5, 1)])
        >>> triangle.vertex_to_outgoing_directed_edge
        array([0, 2, 4])
        """
        from scadpy.d2.shape import get_shape_vertex_to_outgoing_directed_edge

        return get_shape_vertex_to_outgoing_directed_edge(self)

    @cached_property
    def vertex_to_incoming_directed_edge(self: Self) -> NDArray[np.int64]:
        """For each vertex in the shape, return the index of its incoming directed edge.

        See :func:`get_shape_vertex_to_incoming_directed_edge` for parameter documentation.

        Examples
        --------
        >>> from scadpy import polygon

        >>> # triangle: vertices (2,0,1), (0,1,2), (1,2,0)
        >>> # incoming: 2→0, 0→1, 1→2
        >>> triangle = polygon([(0, 0), (1, 0), (0.5, 1)])
        >>> triangle.vertex_to_incoming_directed_edge
        array([4, 0, 2])
        """
        from scadpy.d2.shape import get_shape_vertex_to_incoming_directed_edge

        return get_shape_vertex_to_incoming_directed_edge(self)

    @cached_property
    def directed_edge_to_vertex(self: Self) -> NDArray[np.int64]:
        """For each directed edge in the shape, return the indices of its start and end vertices.

        See :func:`get_shape_directed_edge_to_vertex` for parameter documentation.

        Examples
        --------
        >>> from scadpy import polygon, square

        >>> # triangle: 3 edges → 6 directed edges
        >>> # (forward/backward interleaved)
        >>> triangle = polygon([(0, 0), (1, 0), (0.5, 1)])
        >>> triangle.directed_edge_to_vertex
        array([[0, 1],
               [1, 0],
               [1, 2],
               [2, 1],
               [2, 0],
               [0, 2]])

        >>> # square: 4 edges → 8 directed edges
        >>> square(1).directed_edge_to_vertex.shape
        (8, 2)
        """
        from scadpy.d2.shape import get_shape_directed_edge_to_vertex

        return get_shape_directed_edge_to_vertex(self)

    @cached_property
    def directed_edge_to_edge(self: Self) -> NDArray[np.int64]:
        """For each directed edge in the shape, return the index of its parent undirected edge.

        See :func:`get_shape_directed_edge_to_edge` for parameter documentation.

        Examples
        --------
        >>> from scadpy import polygon, square

        >>> # triangle: 3 edges → 6 directed edges
        >>> triangle = polygon([(0, 0), (1, 0), (0.5, 1)])
        >>> triangle.directed_edge_to_edge
        array([0, 0, 1, 1, 2, 2])

        >>> # square: 4 edges → 8 directed edges
        >>> square(1).directed_edge_to_edge
        array([0, 0, 1, 1, 2, 2, 3, 3])
        """
        from scadpy.d2.shape import get_shape_directed_edge_to_edge

        return get_shape_directed_edge_to_edge(self)

    @cached_property
    def directed_edge_directions(self: Self) -> NDArray[np.float64]:
        """For each directed edge in the shape, return its unit direction vector.

        See :func:`get_shape_directed_edge_directions` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> # unit square: 4 edges → 8 directed edges,
        >>> # forward then backward interleaved
        >>> square(1).directed_edge_directions.round(4)
        array([[ 1.,  0.],
               [-1.,  0.],
               [ 0.,  1.],
               [ 0., -1.],
               [-1.,  0.],
               [ 1.,  0.],
               [ 0., -1.],
               [ 0.,  1.]])
        """
        from scadpy.d2.shape import get_shape_directed_edge_directions

        return get_shape_directed_edge_directions(self)

    @cached_property
    def edge_to_vertex(self: Self) -> NDArray[np.int64]:
        """For each edge in the shape, return the indices of its start and end vertices.

        See :func:`get_shape_edge_to_vertex` for parameter documentation.

        Examples
        --------
        >>> from scadpy import polygon, square

        >>> # triangle: 3 vertices, 3 edges
        >>> triangle = polygon([(0, 0), (1, 0), (0.5, 1)])
        >>> triangle.edge_to_vertex
        array([[0, 1],
               [1, 2],
               [2, 0]])

        >>> # square: 4 vertices, 4 edges
        >>> square(1).edge_to_vertex.shape
        (4, 2)
        """
        from scadpy.d2.shape import get_shape_edge_to_vertex

        return get_shape_edge_to_vertex(self)

    @cached_property
    def edge_lengths(self: Self) -> NDArray[np.float64]:
        """For each edge in the shape, return its length.

        See :func:`get_shape_edge_lengths` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(2).edge_lengths
        array([2., 2., 2., 2.])
        """
        from scadpy.d2.shape import get_shape_edge_lengths

        return get_shape_edge_lengths(self)

    @cached_property
    def edge_midpoints(self: Self) -> NDArray[np.float64]:
        """For each edge in the shape, return the midpoint between its two vertices.

        See :func:`get_shape_edge_midpoints` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(2).edge_midpoints
        array([[ 0., -1.],
               [ 1.,  0.],
               [ 0.,  1.],
               [-1.,  0.]])
        """
        from scadpy.d2.shape import get_shape_edge_midpoints

        return get_shape_edge_midpoints(self)

    @cached_property
    def edge_normals(self: Self) -> NDArray[np.float64]:
        """For each edge in the shape, return its outward unit normal.

        See :func:`get_shape_edge_normals` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> # square(2) centered at origin: 4 edges,
        >>> # each normal points outward
        >>> square(2).edge_normals.round(4)
        array([[ 0., -1.],
               [ 1., -0.],
               [ 0.,  1.],
               [-1., -0.]])
        """
        from scadpy.d2.shape import get_shape_edge_normals

        return get_shape_edge_normals(self)

    #############
    # importers #
    #############

    @classmethod
    def from_parts(cls, parts: Sequence[Part[Polygon]]) -> Shape:
        """Map a sequence of parts to a shape, repairing and orienting each polygon.

        See :func:`map_parts_to_shape` for parameter documentation.

        Examples
        --------
        >>> from shapely.geometry import Polygon
        >>> from scadpy import Shape, map_parts_to_shape
        >>> from scadpy.core.part import Part

        >>> Shape.from_parts(  # doctest: +SKIP
        ...     [Part.from_geometry(Polygon([(0, 0), (4, 0), (4, 4), (0, 4)]))]
        ... )

        .. render-example::
            :name: map_parts_to_shape
            :example: map_parts_to_shape([Part.from_geometry(Polygon([(0, 0), (4, 0), (4, 4), (0, 4)]))])
        """
        from scadpy import map_parts_to_shape

        return map_parts_to_shape(parts)

    @classmethod
    def from_geometries(cls, geometries: Sequence[Polygon]) -> Shape:
        """Map a sequence of polygons to a shape.

        See :func:`map_geometries_to_shape` for parameter documentation.

        Examples
        --------
        >>> from shapely.geometry import Polygon
        >>> from scadpy import Shape, map_geometries_to_shape

        >>> Shape.from_geometries(  # doctest: +SKIP
        ...     [Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])]
        ... )

        .. render-example::
            :name: map_geometries_to_shape
            :example: map_geometries_to_shape([Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])])
        """
        from scadpy.d2.shape.importers import map_geometries_to_shape

        return map_geometries_to_shape(geometries)

    @classmethod
    def from_geometry(cls, geometry: Polygon) -> Shape:
        """Map a single polygon to a shape.

        See :func:`map_geometry_to_shape` for parameter documentation.

        Examples
        --------
        >>> from shapely.geometry import Polygon
        >>> from scadpy import Shape, map_geometry_to_shape

        >>> Shape.from_geometry(  # doctest: +SKIP
        ...     Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])
        ... )

        .. render-example::
            :name: map_geometry_to_shape
            :example: map_geometry_to_shape(Polygon([(0, 0), (4, 0), (4, 4), (0, 4)]))
        """
        from scadpy.d2.shape.importers import map_geometry_to_shape

        return map_geometry_to_shape(geometry)

    @classmethod
    def from_svg(cls, source: str | Path) -> Shape:
        """Load a 2D shape from an SVG file or URL.

        See :func:`map_svg_to_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import Shape, map_svg_to_shape

        >>> Shape.from_svg("https://upload.wikimedia.org/wikipedia/commons/0/04/Pentagon.svg")  # doctest: +SKIP

        .. render-example::
            :name: map_svg_to_shape
            :example: map_svg_to_shape("https://upload.wikimedia.org/wikipedia/commons/0/04/Pentagon.svg")
        """
        from scadpy import map_svg_to_shape

        return map_svg_to_shape(source)

    @classmethod
    def from_dxf(cls, source: str | Path) -> Shape:
        """Load a 2D shape from a DXF file or URL.

        See :func:`map_dxf_to_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import Shape, map_dxf_to_shape

        >>> Shape.from_dxf("https://raw.githubusercontent.com/mikedh/trimesh/main/models/2D/wrench.dxf")  # doctest: +SKIP

        .. render-example::
            :name: map_dxf_to_shape
            :example: map_dxf_to_shape("https://raw.githubusercontent.com/mikedh/trimesh/main/models/2D/wrench.dxf")
        """
        from scadpy import map_dxf_to_shape

        return map_dxf_to_shape(source)

    ###################
    # transformations #
    ###################

    def translate(
        self: Self,
        translation: float | Iterable[float],
        vertex_filter: TopologyFilter[Shape] | None = None,
    ) -> Shape:
        """Translate this shape.

        See :func:`translate_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(4).translate([3, 2])  # doctest: +SKIP

        .. render-example::
            :name: translate_shape
            :example: square(4).translate([3, 2])
            :ghost: square(4)
        """
        from scadpy import translate_shape

        return translate_shape(
            shape=self, translation=translation, vertex_filter=vertex_filter
        )

    def scale(
        self: Self,
        scale: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Shape] | None = None,
    ) -> Shape:
        """Scale this shape.

        See :func:`scale_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(4).scale(2, pivot=[2, 2])  # doctest: +SKIP

        .. render-example::
            :name: scale_shape
            :example: square(4).scale(2, pivot=[2, 2])
            :ghost: square(4)
        """
        from scadpy import scale_shape

        return scale_shape(shape=self, scale=scale, pivot=pivot, vertex_filter=vertex_filter)

    def resize(
        self: Self,
        size: Iterable[float | None],
        auto: bool = False,
        pivot: float | Iterable[float] | None = None,
        vertex_filter: TopologyFilter[Shape] | None = None,
    ) -> Shape:
        """Resize this shape to target dimensions.

        See :func:`resize_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import rectangle

        >>> # resize to an exact size on both axes
        >>> rectangle([4, 2]).resize([6, 6])  # doctest: +SKIP

        .. render-example::
           :name: resize_shape_exact
           :example: rectangle([4, 2]).resize([6, 6])
           :ghost: rectangle([4, 2])

        >>> # freeze one axis (None) to leave it unchanged
        >>> rectangle([4, 2]).resize([6, None])  # doctest: +SKIP

        .. render-example::
           :name: resize_shape_freeze
           :example: rectangle([4, 2]).resize([6, None])
           :ghost: rectangle([4, 2])

        >>> # scale frozen axes proportionally with auto=True
        >>> rectangle([4, 2]).resize([6, None], auto=True)  # doctest: +SKIP

        .. render-example::
           :name: resize_shape_auto
           :example: rectangle([4, 2]).resize([6, None], auto=True)
           :ghost: rectangle([4, 2])
        """
        from scadpy import resize_shape

        return resize_shape(shape=self, size=size, auto=auto, pivot=pivot, vertex_filter=vertex_filter)

    def mirror(
        self: Self,
        normal: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
    ) -> Shape:
        """Mirror this shape.

        See :func:`mirror_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(4).mirror([1, 0], pivot=[2, 0])  # doctest: +SKIP

        .. render-example::
            :name: mirror_shape
            :example: square(4).mirror([1, 0], pivot=[2, 0])
            :ghost: square(4)
        """
        from scadpy import mirror_shape

        return mirror_shape(shape=self, normal=normal, pivot=pivot)

    def pull(
        self: Self,
        distance: float,
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Shape] | None = None,
    ) -> Shape:
        """Move vertices of this shape toward a pivot point.

        See :func:`pull_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(4).pull(1.0, pivot=[2, 2], vertex_filter=square(4).vertex_coordinates[:, 0] < 1)  # doctest: +SKIP

        .. render-example::
            :name: pull_shape
            :example: square(4).pull(1.0, pivot=[2, 2], vertex_filter=square(4).vertex_coordinates[:, 0] < 1)
            :ghost: square(4)
        """
        from scadpy import pull_shape

        return pull_shape(
            shape=self, distance=distance, pivot=pivot, vertex_filter=vertex_filter
        )

    def push(
        self: Self,
        distance: float,
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Shape] | None = None,
    ) -> Shape:
        """Move vertices of this shape away from a pivot point.

        See :func:`push_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(4).push(1.0, pivot=[2, 2], vertex_filter=square(4).vertex_coordinates[:, 0] < 1)  # doctest: +SKIP

        .. render-example::
            :name: push_shape
            :example: square(4).push(1.0, pivot=[2, 2], vertex_filter=square(4).vertex_coordinates[:, 0] < 1)
            :ghost: square(4)
        """
        from scadpy import push_shape

        return push_shape(
            shape=self, distance=distance, pivot=pivot, vertex_filter=vertex_filter
        )

    def color(self: Self, color: Color) -> Shape:
        """Set the color of all parts in this shape.

        See :func:`color_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square
        >>> from scadpy.color.constants import RED

        >>> square(4).color(RED)  # doctest: +SKIP

        .. render-example::
            :name: color_shape
            :example: square(4).color(RED)
            :keep-color:
        """
        from scadpy import color_shape

        return color_shape(shape=self, color=color)

    def chamfer(
        self: Self,
        size: float | np.ndarray,
        vertex_filter: TopologyFilter[Shape] | None = None,
        epsilon: float = 1e-8,
    ) -> Shape:
        """Chamfer the vertices of this shape.

        See :func:`chamfer_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, polygon
        >>> import numpy as np

        >>> sq = square(4)
        >>> l_shape = polygon(
        ...     [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]
        ... )
        >>> arrow = polygon(
        ...     [(0, 1), (3, 0), (5, 2), (3, 4),
        ...      (0, 3), (1, 2.5), (1, 1.5)]
        ... )

        >>> # all vertices
        >>> sq.chamfer(1.0)  # doctest: +SKIP

        .. render-example::
            :name: chamfer_shape_all
            :example: sq.chamfer(1.0)
            :ghost: sq

        >>> # convex vertices only
        >>> l_shape.chamfer(  # doctest: +SKIP
        ...     0.5, vertex_filter=lambda s: s.are_vertices_convex
        ... )

        .. render-example::
            :name: chamfer_shape_convex_only
            :example: l_shape.chamfer(0.5, vertex_filter=lambda s: s.are_vertices_convex)
            :ghost: l_shape

        >>> # asymmetric: one side fills the full edge (length 2),
        >>> # the other stays at 1.0
        >>> l_shape.chamfer(  # doctest: +SKIP
        ...     np.array([[2.0, 1.0]]),
        ...     vertex_filter=lambda s: ~s.are_vertices_convex,
        ... )

        .. render-example::
            :name: chamfer_shape_concave_asymmetric
            :example: l_shape.chamfer(np.array([[2.0, 1.0]]), vertex_filter=lambda s: ~s.are_vertices_convex)
            :ghost: l_shape

        >>> # only sharp convex vertices (angle > 100°)
        >>> arrow.chamfer(  # doctest: +SKIP
        ...     0.4,
        ...     vertex_filter=lambda s: (
        ...         s.are_vertices_convex & (s.vertex_angles > 100)
        ...     ),
        ... )

        .. render-example::
            :name: chamfer_shape_sharp_convex
            :example: arrow.chamfer(0.4, vertex_filter=lambda s: s.are_vertices_convex & (s.vertex_angles > 100))
            :ghost: arrow

        >>> # oversized: clamped proportionally
        >>> arrow.chamfer(  # doctest: +SKIP
        ...     10, vertex_filter=lambda s: ~s.are_vertices_convex
        ... )

        .. render-example::
            :name: chamfer_shape_clamp_proportional
            :example: arrow.chamfer(10, vertex_filter=lambda s: ~s.are_vertices_convex)
            :ghost: arrow
        """
        from scadpy import chamfer_shape

        return chamfer_shape(
            shape=self, size=size, vertex_filter=vertex_filter, epsilon=epsilon
        )

    def fillet(
        self: Self,
        size: float | np.ndarray,
        vertex_filter: TopologyFilter[Shape] | None = None,
        segment_count: int = 32,
        epsilon: float = 1e-8,
    ) -> Shape:
        """Fillet the vertices of this shape.

        See :func:`fillet_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, polygon
        >>> import numpy as np

        >>> sq = square(4)
        >>> l_shape = polygon(
        ...     [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]
        ... )
        >>> arrow = polygon(
        ...     [(0, 1), (3, 0), (5, 2), (3, 4),
        ...      (0, 3), (1, 2.5), (1, 1.5)]
        ... )

        >>> # all vertices
        >>> sq.fillet(1.0)  # doctest: +SKIP

        .. render-example::
            :name: fillet_shape_all
            :example: sq.fillet(1.0)
            :ghost: sq

        >>> # convex vertices only
        >>> l_shape.fillet(  # doctest: +SKIP
        ...     0.5, vertex_filter=lambda s: s.are_vertices_convex
        ... )

        .. render-example::
            :name: fillet_shape_convex_only
            :example: l_shape.fillet(0.5, vertex_filter=lambda s: s.are_vertices_convex)
            :ghost: l_shape

        >>> # asymmetric
        >>> l_shape.fillet(  # doctest: +SKIP
        ...     np.array([[2.0, 1.0]]),
        ...     vertex_filter=lambda s: ~s.are_vertices_convex,
        ... )

        .. render-example::
            :name: fillet_shape_concave_asymmetric
            :example: l_shape.fillet(np.array([[2.0, 1.0]]), vertex_filter=lambda s: ~s.are_vertices_convex)
            :ghost: l_shape

        >>> # only sharp convex vertices (angle > 100°)
        >>> arrow.fillet(  # doctest: +SKIP
        ...     0.4,
        ...     vertex_filter=lambda s: (
        ...         s.are_vertices_convex & (s.vertex_angles > 100)
        ...     ),
        ... )

        .. render-example::
            :name: fillet_shape_sharp_convex
            :example: arrow.fillet(0.4, vertex_filter=lambda s: s.are_vertices_convex & (s.vertex_angles > 100))
            :ghost: arrow

        >>> # oversized: clamped proportionally
        >>> arrow.fillet(  # doctest: +SKIP
        ...     10, vertex_filter=lambda s: ~s.are_vertices_convex
        ... )

        .. render-example::
            :name: fillet_shape_clamp_proportional
            :example: arrow.fillet(10, vertex_filter=lambda s: ~s.are_vertices_convex)
            :ghost: arrow
        """
        from scadpy import fillet_shape

        return fillet_shape(
            shape=self,
            size=size,
            vertex_filter=vertex_filter,
            segment_count=segment_count,
            epsilon=epsilon,
        )

    def convexify(self: Self) -> Shape:
        """Compute the convex hull of each part of this shape.

        See :func:`convexify_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square
        >>> import numpy as np

        >>> a = square(5)
        >>> b = square(2).translate(10)
        >>> c = square(3).translate([4, 8])

        >>> (a + b + c).convexify()  # doctest: +SKIP

        .. render-example::
            :name: convexify_shape
            :example: (a + b + c).convexify()
            :ghost: a + b + c
        """
        from scadpy import convexify_shape

        return convexify_shape(shape=self)

    def fill(self: Self) -> Shape:
        """Fill holes in this shape.

        See :func:`fill_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> (square(10) - circle(3)).fill()  # doctest: +SKIP

        .. render-example::
            :name: fill_shape
            :example: (square(10) - circle(3)).fill()
            :ghost: square(10) - circle(3)
        """
        from scadpy import fill_shape

        return fill_shape(shape=self)

    def grow(self: Self, distance: float) -> Shape:
        """Grow this shape outward by a given distance.

        See :func:`grow_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(10).grow(2)  # doctest: +SKIP

        .. render-example::
            :name: grow_shape
            :example: square(10).grow(2)
            :ghost: square(10)

        >>> # shrink with negative distance
        >>> square(10).grow(-2)  # doctest: +SKIP

        .. render-example::
            :name: grow_shape_shrink
            :example: square(10).grow(-2)
            :ghost: square(10)
        """
        from scadpy import grow_shape

        return grow_shape(shape=self, distance=distance)

    def linear_cut(
        self: Self,
        axis: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
    ) -> Shape:
        """Cut this shape with a half-plane.

        See :func:`linear_cut_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> shape = square(6) - circle(2)

        >>> # vertical cut along the Y-axis
        >>> shape.linear_cut([0, 1], pivot=[-1, 0])  # doctest: +SKIP

        .. render-example::
            :name: linear_cut_shape
            :example: (square(6) - circle(2)).linear_cut([0, 1], pivot=[-1, 0])
            :ghost: square(6) - circle(2)

        >>> # diagonal cut
        >>> shape.linear_cut([1, 1])  # doctest: +SKIP

        .. render-example::
            :name: linear_cut_shape_diagonal
            :example: (square(6) - circle(2)).linear_cut([1, 1])
            :ghost: square(6) - circle(2)
        """
        from scadpy import linear_cut_shape

        return linear_cut_shape(shape=self, axis=axis, pivot=pivot)

    def linear_extrude(self: Self, height: float) -> Solid:
        """Extrude this shape linearly along the Z-axis.

        See :func:`linear_extrude_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> # simple box
        >>> square(10).linear_extrude(5)  # doctest: +SKIP

        .. render-example::
            :name: linear_extrude_shape_square
            :example: square(10).linear_extrude(5)

        >>> # tube from a hollow circle
        >>> (circle(5) - circle(3)).linear_extrude(10)  # doctest: +SKIP

        .. render-example::
            :name: linear_extrude_shape_tube
            :example: (circle(5) - circle(3)).linear_extrude(10)
        """
        from scadpy import linear_extrude_shape

        return linear_extrude_shape(shape=self, height=height)

    def linear_slice(
        self: Self,
        thickness: float,
        direction: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
    ) -> Shape:
        """Slice this shape with a linear band.

        See :func:`linear_slice_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> shape = square(10) - circle(3)

        >>> # horizontal slice through center
        >>> shape.linear_slice(3, [1, 0])  # doctest: +SKIP

        .. render-example::
            :name: linear_slice_shape_horizontal
            :example: (square(10) - circle(3)).linear_slice(3, [1, 0])
            :ghost: square(10) - circle(3)

        >>> # diagonal slice
        >>> shape.linear_slice(2, [1, 1])  # doctest: +SKIP

        .. render-example::
            :name: linear_slice_shape_diagonal
            :example: (square(10) - circle(3)).linear_slice(2, [1, 1])
            :ghost: square(10) - circle(3)

        >>> # off-center slice with pivot
        >>> shape.linear_slice(2, [0, 1], pivot=[3, 0])  # doctest: +SKIP

        .. render-example::
            :name: linear_slice_shape_pivot
            :example: (square(10) - circle(3)).linear_slice(2, [0, 1], pivot=[3, 0])
            :ghost: square(10) - circle(3)
        """
        from scadpy import linear_slice_shape

        return linear_slice_shape(
            shape=self, thickness=thickness, direction=direction, pivot=pivot
        )

    def radial_extrude(
        self: Self,
        axis: float | Iterable[float],
        start: float = 0,
        end: float = 360,
        pivot: float | Iterable[float] = 0,
        segment_count: int = 64,
    ) -> Solid:
        """Extrude this shape radially around an axis.

        See :func:`radial_extrude_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import circle

        >>> # torus: circle profile offset from the Y-axis, revolved 360°
        >>> circle(0.5).translate([2, 0]).radial_extrude([0, 1])  # doctest: +SKIP

        .. render-example::
            :name: radial_extrude_shape
            :example: circle(radius=0.5).translate([2, 0]).radial_extrude([0, 1])

        >>> # partial torus (270°)
        >>> circle(0.5).translate([2, 0]).radial_extrude([0, 1], end=270)  # doctest: +SKIP

        .. render-example::
            :name: radial_extrude_shape_partial
            :example: circle(radius=0.5).translate([2, 0]).radial_extrude([0, 1], end=270)
        """
        from scadpy import radial_extrude_shape

        return radial_extrude_shape(
            shape=self,
            axis=axis,
            start=start,
            end=end,
            pivot=pivot,
            segment_count=segment_count,
        )

    def radial_slice(
        self: Self, start: float = 0, end: float = 360, pivot: float | Iterable[float] = 0
    ) -> Shape:
        """Slice this shape to keep only a radial sector.

        See :func:`radial_slice_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> shape = square(10) - circle(3)

        >>> # quarter slice
        >>> shape.radial_slice(0, 90)  # doctest: +SKIP

        .. render-example::
            :name: radial_slice_shape_quarter
            :example: (square(10) - circle(3)).radial_slice(0, 90)
            :ghost: square(10) - circle(3)

        >>> # three-quarter slice
        >>> shape.radial_slice(45, 315)  # doctest: +SKIP

        .. render-example::
            :name: radial_slice_shape_three_quarter
            :example: (square(10) - circle(3)).radial_slice(45, 315)
            :ghost: square(10) - circle(3)

        >>> # off-center pivot
        >>> shape.radial_slice(0, 180, pivot=[3, 3])  # doctest: +SKIP

        .. render-example::
            :name: radial_slice_shape_pivot
            :example: (square(10) - circle(3)).radial_slice(0, 180, pivot=[3, 3])
            :ghost: square(10) - circle(3)
        """
        from scadpy import radial_slice_shape

        return radial_slice_shape(shape=self, start=start, end=end, pivot=pivot)

    def rotate(
        self: Self,
        angle: float,
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Shape] | None = None,
    ) -> Shape:
        """Rotate this shape.

        See :func:`rotate_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(4).rotate(45, pivot=[2, 2])  # doctest: +SKIP

        .. render-example::
            :name: rotate_shape
            :example: square(4).rotate(45, pivot=[2, 2])
            :ghost: square(4)
        """
        from scadpy import rotate_shape

        return rotate_shape(shape=self, angle=angle, pivot=pivot, vertex_filter=vertex_filter)

    def shrink(self: Self, distance: float) -> Shape:
        """Shrink this shape inward by a given distance.

        See :func:`shrink_shape` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(10).shrink(2)  # doctest: +SKIP

        .. render-example::
            :name: shrink_shape
            :example: square(10).shrink(2)
            :ghost: square(10)

        >>> # negative distance expands outward
        >>> square(10).shrink(-2)  # doctest: +SKIP

        .. render-example::
            :name: shrink_shape_negative
            :example: square(10).shrink(-2)
            :ghost: square(10)
        """
        from scadpy import shrink_shape

        return shrink_shape(shape=self, distance=distance)

    #############
    # exporters #
    #############

    def to_screen(
        self: Self,
        background_color: Color = WHITE,
        foreground_color: Color = BLACK,
    ) -> None:
        """Display a shape in a Qt-based window.

        See :func:`map_shape_to_screen` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(4).to_screen()  # doctest: +SKIP
        """
        from scadpy import map_shape_to_screen

        map_shape_to_screen(
            shape=self,
            background_color=background_color,
            foreground_color=foreground_color,
        )

    def to_html(
        self: Self,
        background_color: Color = WHITE,
        foreground_color: Color = BLACK,
    ) -> "HTML":
        """Render a shape as an SVG HTML object.

        See :func:`map_shape_to_html` for parameter documentation.

        Examples
        --------
        >>> from IPython.core.display import HTML
        >>> from scadpy import square

        >>> html = square(4).to_html()
        >>> isinstance(html, HTML)
        True
        """
        from scadpy import map_shape_to_html

        return map_shape_to_html(
            shape=self,
            background_color=background_color,
            foreground_color=foreground_color,
        )

    def to_html_file(
        self: Self,
        path: str,
        background_color: Color = WHITE,
        foreground_color: Color = BLACK,
    ) -> int:
        """Save a shape as an HTML file.

        See :func:`map_shape_to_html_file` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square

        >>> square(4).to_html_file(path="output.html")  # doctest: +SKIP
        """
        from scadpy import map_shape_to_html_file

        return map_shape_to_html_file(
            shape=self,
            path=path,
            background_color=background_color,
            foreground_color=foreground_color,
        )

    def to_svg(self: Self) -> str:
        """Export a shape to an SVG string.

        See :func:`map_shape_to_svg` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> svg = (square(4) - circle(1)).to_svg()
        >>> svg.startswith("<svg")
        True
        """
        from scadpy import map_shape_to_svg

        return map_shape_to_svg(shape=self)

    def to_svg_file(self: Self, path: str | Path) -> int:
        """Save a shape as an SVG file.

        See :func:`map_shape_to_svg_file` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> (square(4) - circle(1)).to_svg_file(path="output.svg")  # doctest: +SKIP
        """
        from scadpy import map_shape_to_svg_file

        return map_shape_to_svg_file(shape=self, path=path)

    def to_dxf(self: Self) -> str:
        """Export a shape to a DXF string.

        See :func:`map_shape_to_dxf` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> dxf = (square(4) - circle(1)).to_dxf()
        >>> dxf.startswith("999")
        True
        """
        from scadpy import map_shape_to_dxf

        return map_shape_to_dxf(shape=self)

    def to_dxf_file(self: Self, path: str | Path) -> int:
        """Save a shape as a DXF file.

        See :func:`map_shape_to_dxf_file` for parameter documentation.

        Examples
        --------
        >>> from scadpy import square, circle

        >>> (square(4) - circle(1)).to_dxf_file(path="output.dxf")  # doctest: +SKIP
        """
        from scadpy import map_shape_to_dxf_file

        return map_shape_to_dxf_file(shape=self, path=path)
