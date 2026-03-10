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
        """
        Shortcut for :func:`get_shape_vertex_coordinates`.

        See :func:`get_shape_vertex_coordinates` for full documentation.
        """
        from scadpy import get_shape_vertex_coordinates

        return get_shape_vertex_coordinates(self)

    @cached_property
    def vertex_to_part(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_shape_vertex_to_part`.

        See :func:`get_shape_vertex_to_part` for full documentation.
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
        """
        Shortcut for :func:`is_shape_empty`.

        See :func:`is_shape_empty` for full documentation.
        """
        from scadpy import is_shape_empty

        return is_shape_empty(self)

    @cached_property
    def bounds(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_shape_bounds`.

        See :func:`get_shape_bounds` for full documentation.
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
        """Concatenate this shape with others.

        Shortcut for :func:`concat_shape`.
        See :func:`concat_shape` for full documentation.
        """
        from scadpy import concat_shape

        return concat_shape(shapes=[self, *shapes])

    def unify(self: Self, shapes: Sequence[Shape]) -> Shape:
        """Unite this shape with others.

        Shortcut for :func:`unify_shape`.
        See :func:`unify_shape` for full documentation.
        """
        from scadpy import unify_shape

        return unify_shape(shapes=[self, *shapes])

    def intersect(self: Self, shapes: Sequence[Shape]) -> Shape:
        """Intersect this shape with others.

        Shortcut for :func:`intersect_shape`.
        See :func:`intersect_shape` for full documentation.
        """
        from scadpy import intersect_shape

        return intersect_shape(shapes=[self, *shapes])

    def subtract(self: Self, other: Shape) -> Shape:
        """Subtract a shape from this shape.

        Shortcut for :func:`subtract_shape`.
        See :func:`subtract_shape` for full documentation.
        """
        from scadpy import subtract_shape

        return subtract_shape(to_be_subtracted=self, to_subtract=other)

    def exclude(self: Self, shapes: Sequence[Shape]) -> Shape:
        """Compute the symmetric difference of this shape with others.

        Shortcut for :func:`exclude_shape`.
        See :func:`exclude_shape` for full documentation.
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
        """
        Shortcut for :func:`get_shape_ring_to_part`.

        See :func:`get_shape_ring_to_part` for full documentation.
        """
        from scadpy.d2.shape import get_shape_ring_to_part

        return get_shape_ring_to_part(self)

    @cached_property
    def ring_types(self: Self) -> NDArray[np.object_]:
        """
        Shortcut for :func:`get_shape_ring_types`.

        See :func:`get_shape_ring_types` for full documentation.
        """
        from scadpy.d2.shape import get_shape_ring_types

        return get_shape_ring_types(self)

    @cached_property
    def vertex_to_ring(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_shape_vertex_to_ring`.

        See :func:`get_shape_vertex_to_ring` for full documentation.
        """
        from scadpy.d2.shape import get_shape_vertex_to_ring

        return get_shape_vertex_to_ring(self)

    @cached_property
    def corner_to_vertex(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_shape_corner_to_vertex`.

        See :func:`get_shape_corner_to_vertex` for full documentation.
        """
        from scadpy.d2.shape import get_shape_corner_to_vertex

        return get_shape_corner_to_vertex(self)

    @cached_property
    def corner_angles(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_shape_corner_angles`.

        See :func:`get_shape_corner_angles` for full documentation.
        """
        from scadpy.d2.shape import get_shape_corner_angles

        return get_shape_corner_angles(self)

    @cached_property
    def are_corners_convex(self: Self) -> NDArray[np.bool_]:
        """
        Shortcut for :func:`are_shape_corners_convex`.

        See :func:`are_shape_corners_convex` for full documentation.
        """
        from scadpy.d2.shape import are_shape_corners_convex

        return are_shape_corners_convex(self)

    @cached_property
    def corner_normals(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_shape_corner_normals`.

        See :func:`get_shape_corner_normals` for full documentation.
        """
        from scadpy.d2.shape import get_shape_corner_normals

        return get_shape_corner_normals(self)

    @cached_property
    def corner_to_outgoing_directed_edge(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_shape_corner_to_outgoing_directed_edge`.

        See :func:`get_shape_corner_to_outgoing_directed_edge` for full documentation.
        """
        from scadpy.d2.shape import get_shape_corner_to_outgoing_directed_edge

        return get_shape_corner_to_outgoing_directed_edge(self)

    @cached_property
    def corner_to_incoming_directed_edge(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_shape_corner_to_incoming_directed_edge`.

        See :func:`get_shape_corner_to_incoming_directed_edge` for full documentation.
        """
        from scadpy.d2.shape import get_shape_corner_to_incoming_directed_edge

        return get_shape_corner_to_incoming_directed_edge(self)

    @cached_property
    def directed_edge_to_corner(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_shape_directed_edge_to_corner`.

        See :func:`get_shape_directed_edge_to_corner` for full documentation.
        """
        from scadpy.d2.shape import get_shape_directed_edge_to_corner

        return get_shape_directed_edge_to_corner(self)

    @cached_property
    def directed_edge_to_vertex(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_shape_directed_edge_to_vertex`.

        See :func:`get_shape_directed_edge_to_vertex` for full documentation.
        """
        from scadpy.d2.shape import get_shape_directed_edge_to_vertex

        return get_shape_directed_edge_to_vertex(self)

    @cached_property
    def directed_edge_to_edge(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_shape_directed_edge_to_edge`.

        See :func:`get_shape_directed_edge_to_edge` for full documentation.
        """
        from scadpy.d2.shape import get_shape_directed_edge_to_edge

        return get_shape_directed_edge_to_edge(self)

    @cached_property
    def directed_edge_directions(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_shape_directed_edge_directions`.

        See :func:`get_shape_directed_edge_directions` for full documentation.
        """
        from scadpy.d2.shape import get_shape_directed_edge_directions

        return get_shape_directed_edge_directions(self)

    @cached_property
    def edge_to_vertex(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_shape_edge_to_vertex`.

        See :func:`get_shape_edge_to_vertex` for full documentation.
        """
        from scadpy.d2.shape import get_shape_edge_to_vertex

        return get_shape_edge_to_vertex(self)

    @cached_property
    def edge_lengths(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_shape_edge_lengths`.

        See :func:`get_shape_edge_lengths` for full documentation.
        """
        from scadpy.d2.shape import get_shape_edge_lengths

        return get_shape_edge_lengths(self)

    @cached_property
    def edge_midpoints(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_shape_edge_midpoints`.

        See :func:`get_shape_edge_midpoints` for full documentation.
        """
        from scadpy.d2.shape import get_shape_edge_midpoints

        return get_shape_edge_midpoints(self)

    @cached_property
    def edge_normals(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_shape_edge_normals`.

        See :func:`get_shape_edge_normals` for full documentation.
        """
        from scadpy.d2.shape import get_shape_edge_normals

        return get_shape_edge_normals(self)

    #############
    # importers #
    #############

    @classmethod
    def from_parts(cls, parts: Sequence[Part[Polygon]]) -> Shape:
        """Shortcut for :func:`map_parts_to_shape`.

        See :func:`map_parts_to_shape` for full documentation.
        """
        from scadpy import map_parts_to_shape

        return map_parts_to_shape(parts)

    @classmethod
    def from_geometries(cls, geometries: Sequence[Polygon]) -> Shape:
        """Shortcut for :func:`map_geometries_to_shape`.

        See :func:`map_geometries_to_shape` for full documentation.
        """
        from scadpy.d2.shape.importers import map_geometries_to_shape

        return map_geometries_to_shape(geometries)

    @classmethod
    def from_geometry(cls, geometry: Polygon) -> Shape:
        """Shortcut for :func:`map_geometry_to_shape`.

        See :func:`map_geometry_to_shape` for full documentation.
        """
        from scadpy.d2.shape.importers import map_geometry_to_shape

        return map_geometry_to_shape(geometry)

    @classmethod
    def from_svg(cls, source: str | Path) -> Shape:
        """Shortcut for :func:`map_svg_to_shape`.

        See :func:`map_svg_to_shape` for full documentation.
        """
        from scadpy import map_svg_to_shape

        return map_svg_to_shape(source)

    @classmethod
    def from_dxf(cls, source: str | Path) -> Shape:
        """Shortcut for :func:`map_dxf_to_shape`.

        See :func:`map_dxf_to_shape` for full documentation.
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

        Shortcut for :func:`translate_shape`.
        See :func:`translate_shape` for full documentation.
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

        Shortcut for :func:`scale_shape`.
        See :func:`scale_shape` for full documentation.
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
        """Resize this shape.

        Shortcut for :func:`resize_shape`.
        See :func:`resize_shape` for full documentation.
        """
        from scadpy import resize_shape

        return resize_shape(shape=self, size=size, auto=auto, pivot=pivot, vertex_filter=vertex_filter)

    def mirror(
        self: Self,
        normal: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
    ) -> Shape:
        """Mirror this shape.

        Shortcut for :func:`mirror_shape`.
        See :func:`mirror_shape` for full documentation.
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

        Shortcut for :func:`pull_shape`.
        See :func:`pull_shape` for full documentation.
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

        Shortcut for :func:`push_shape`.
        See :func:`push_shape` for full documentation.
        """
        from scadpy import push_shape

        return push_shape(
            shape=self, distance=distance, pivot=pivot, vertex_filter=vertex_filter
        )

    def color(self: Self, color: Color) -> Shape:
        """Set the color of all parts in this shape.

        Shortcut for :func:`color_shape`.
        See :func:`color_shape` for full documentation.
        """
        from scadpy import color_shape

        return color_shape(shape=self, color=color)

    def chamfer(
        self: Self,
        size: float | np.ndarray,
        corner_filter: TopologyFilter[Shape] | None = None,
        epsilon: float = 1e-8,
    ) -> Shape:
        """
        Shortcut for :func:`chamfer_shape`.

        See :func:`chamfer_shape` for full documentation.
        """
        from scadpy import chamfer_shape

        return chamfer_shape(
            shape=self, size=size, corner_filter=corner_filter, epsilon=epsilon
        )

    def fillet(
        self: Self,
        size: float | np.ndarray,
        corner_filter: TopologyFilter[Shape] | None = None,
        segment_count: int = 32,
        epsilon: float = 1e-8,
    ) -> Shape:
        """
        Shortcut for :func:`fillet_shape`.

        See :func:`fillet_shape` for full documentation.
        """
        from scadpy import fillet_shape

        return fillet_shape(
            shape=self,
            size=size,
            corner_filter=corner_filter,
            segment_count=segment_count,
            epsilon=epsilon,
        )

    def convexify(self: Self) -> Shape:
        """
        Shortcut for :func:`convexify_shape`.

        See :func:`convexify_shape` for full documentation.
        """
        from scadpy import convexify_shape

        return convexify_shape(shape=self)

    def fill(self: Self) -> Shape:
        """
        Shortcut for :func:`fill_shape`.

        See :func:`fill_shape` for full documentation.
        """
        from scadpy import fill_shape

        return fill_shape(shape=self)

    def grow(self: Self, distance: float) -> Shape:
        """
        Shortcut for :func:`grow_shape`.

        See :func:`grow_shape` for full documentation.
        """
        from scadpy import grow_shape

        return grow_shape(shape=self, distance=distance)

    def linear_cut(
        self: Self,
        axis: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
    ) -> Shape:
        """
        Shortcut for :func:`linear_cut_shape`.

        See :func:`linear_cut_shape` for full documentation.
        """
        from scadpy import linear_cut_shape

        return linear_cut_shape(shape=self, axis=axis, pivot=pivot)

    def linear_extrude(self: Self, height: float) -> Solid:
        """
        Shortcut for :func:`linear_extrude_shape`.

        See :func:`linear_extrude_shape` for full documentation.
        """
        from scadpy import linear_extrude_shape

        return linear_extrude_shape(shape=self, height=height)

    def linear_slice(
        self: Self,
        thickness: float,
        direction: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
    ) -> Shape:
        """
        Shortcut for :func:`linear_slice_shape`.

        See :func:`linear_slice_shape` for full documentation.
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
        """
        Shortcut for :func:`radial_extrude_shape`.

        See :func:`radial_extrude_shape` for full documentation.
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
        """
        Shortcut for :func:`radial_slice_shape`.

        See :func:`radial_slice_shape` for full documentation.
        """
        from scadpy import radial_slice_shape

        return radial_slice_shape(shape=self, start=start, end=end, pivot=pivot)

    def rotate(
        self: Self,
        angle: float,
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Shape] | None = None,
    ) -> Shape:
        """
        Shortcut for :func:`rotate_shape`.

        See :func:`rotate_shape` for full documentation.
        """
        from scadpy import rotate_shape

        return rotate_shape(shape=self, angle=angle, pivot=pivot, vertex_filter=vertex_filter)

    def shrink(self: Self, distance: float) -> Shape:
        """
        Shortcut for :func:`shrink_shape`.

        See :func:`shrink_shape` for full documentation.
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
        """
        Shortcut for :func:`map_shape_to_screen`.

        See :func:`map_shape_to_screen` for full documentation.
        """
        from scadpy import map_shape_to_screen

        map_shape_to_screen(
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
        """
        Shortcut for :func:`map_shape_to_html_file`.

        See :func:`map_shape_to_html_file` for full documentation.
        """
        from scadpy import map_shape_to_html_file

        return map_shape_to_html_file(
            shape=self,
            path=path,
            background_color=background_color,
            foreground_color=foreground_color,
        )

    def to_svg(self: Self) -> str:
        """
        Shortcut for :func:`map_shape_to_svg`.

        See :func:`map_shape_to_svg` for full documentation.
        """
        from scadpy import map_shape_to_svg

        return map_shape_to_svg(shape=self)

    def to_svg_file(self: Self, path: str | Path) -> int:
        """
        Shortcut for :func:`map_shape_to_svg_file`.

        See :func:`map_shape_to_svg_file` for full documentation.
        """
        from scadpy import map_shape_to_svg_file

        return map_shape_to_svg_file(shape=self, path=path)

    def to_dxf(self: Self) -> str:
        """
        Shortcut for :func:`map_shape_to_dxf`.

        See :func:`map_shape_to_dxf` for full documentation.
        """
        from scadpy import map_shape_to_dxf

        return map_shape_to_dxf(shape=self)

    def to_dxf_file(self: Self, path: str | Path) -> int:
        """
        Shortcut for :func:`map_shape_to_dxf_file`.

        See :func:`map_shape_to_dxf_file` for full documentation.
        """
        from scadpy import map_shape_to_dxf_file

        return map_shape_to_dxf_file(shape=self, path=path)
