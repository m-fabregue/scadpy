from __future__ import annotations

from collections.abc import Iterable, Sequence
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self, final

from scadpy.color.constants import BLACK, WHITE

if TYPE_CHECKING:
    from scadpy.color import Color
    from scadpy.core.part import Part
    from scadpy import TopologyFilter

import numpy as np
from IPython.core.display import HTML
from numpy.typing import NDArray
from trimesh import Trimesh
from typeguard import typechecked

from scadpy.core.assembly import Assembly


@final
@typechecked
class Solid(Assembly[Trimesh]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pyright: ignore[reportExplicitAny, reportAny]
        super().__init__(*args, **kwargs)

    @classmethod
    def dimensions(cls) -> int:
        return 3

    ##########
    # vertex #
    ##########

    @cached_property
    def vertex_coordinates(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_solid_vertex_coordinates`.

        See :func:`get_solid_vertex_coordinates` for full documentation.
        """
        from scadpy.d3.solid import get_solid_vertex_coordinates

        return get_solid_vertex_coordinates(self)

    @cached_property
    def vertex_to_part(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_solid_vertex_to_part`.

        See :func:`get_solid_vertex_to_part` for full documentation.
        """
        from scadpy.d3.solid import get_solid_vertex_to_part

        return get_solid_vertex_to_part(self)

    ############
    # features #
    ############

    @cached_property
    def is_empty(self: Self) -> bool:
        """
        Shortcut for :func:`is_solid_empty`.

        See :func:`is_solid_empty` for full documentation.
        """
        from scadpy.d3.solid import is_solid_empty

        return is_solid_empty(self)

    @cached_property
    def bounds(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_solid_bounds`.

        See :func:`get_solid_bounds` for full documentation.
        """
        from scadpy.d3.solid import get_solid_bounds

        return get_solid_bounds(self)

    ##############
    # topologies #
    ##############

    @cached_property
    def part_colors(self: Self) -> NDArray[np.float64]:
        """
        Shortcut for :func:`get_assembly_part_colors`.

        See :func:`get_assembly_part_colors` for full documentation.
        """
        from scadpy.d3.solid import get_solid_part_colors

        return get_solid_part_colors(self)

    @cached_property
    def triangle_to_vertex(self: Self) -> NDArray[np.int64]:
        """
        Shortcut for :func:`get_solid_triangle_to_vertex`.

        See :func:`get_solid_triangle_to_vertex` for full documentation.
        """
        from scadpy.d3.solid import get_solid_triangle_to_vertex

        return get_solid_triangle_to_vertex(self)

    ################
    # combinations #
    ################

    def __add__(self: Self, other: Solid) -> Solid:
        """Concatenate two solids. Shortcut for :func:`concat_solid`."""
        from scadpy import concat_solid

        return concat_solid(solids=[self, other])

    def __or__(self: Self, other: Solid) -> Solid:
        """Unite two solids. Shortcut for :func:`unify_solid`."""
        from scadpy import unify_solid

        return unify_solid(solids=[self, other])

    def __and__(self: Self, other: Solid) -> Solid:
        """Intersect two solids. Shortcut for :func:`intersect_solid`."""
        from scadpy import intersect_solid

        return intersect_solid(solids=[self, other])

    def __sub__(self: Self, other: Solid) -> Solid:
        """Subtract a solid from this solid. Shortcut for :func:`subtract_solid`."""
        from scadpy import subtract_solid

        return subtract_solid(to_be_subtracted=self, to_subtract=other)

    def __xor__(self: Self, other: Solid) -> Solid:
        """Compute symmetric difference with another solid. Shortcut for :func:`exclude_solid`."""
        from scadpy import exclude_solid

        return exclude_solid(solids=[self, other])

    def concat(self: Self, solids: Sequence[Solid]) -> Solid:
        """Concatenate this solid with others.

        Shortcut for :func:`concat_solid`.
        See :func:`concat_solid` for full documentation.
        """
        from scadpy import concat_solid

        return concat_solid(solids=[self, *solids])

    def unify(self: Self, solids: Sequence[Solid]) -> Solid:
        """Unite this solid with others.

        Shortcut for :func:`unify_solid`.
        See :func:`unify_solid` for full documentation.
        """
        from scadpy import unify_solid

        return unify_solid(solids=[self, *solids])

    def intersect(self: Self, solids: Sequence[Solid]) -> Solid:
        """Intersect this solid with others.

        Shortcut for :func:`intersect_solid`.
        See :func:`intersect_solid` for full documentation.
        """
        from scadpy import intersect_solid

        return intersect_solid(solids=[self, *solids])

    def subtract(self: Self, to_subtract: Solid) -> Solid:
        """Subtract a solid from this solid.

        Shortcut for :func:`subtract_solid`.
        See :func:`subtract_solid` for full documentation.
        """
        from scadpy import subtract_solid

        return subtract_solid(to_be_subtracted=self, to_subtract=to_subtract)

    def exclude(self: Self, solids: Sequence[Solid]) -> Solid:
        """Compute the symmetric difference of this solid with others.

        Shortcut for :func:`exclude_solid`.
        See :func:`exclude_solid` for full documentation.
        """
        from scadpy import exclude_solid

        return exclude_solid(solids=[self, *solids])

    ###################
    # transformations #
    ###################

    def translate(
        self: Self,
        translation: float | Iterable[float],
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Translate this solid.

        Shortcut for :func:`translate_solid`.
        See :func:`translate_solid` for full documentation.
        """
        from scadpy.d3.solid import translate_solid

        return translate_solid(solid=self, translation=translation, vertex_filter=vertex_filter)

    def scale(
        self: Self,
        scale: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Scale this solid.

        Shortcut for :func:`scale_solid`.
        See :func:`scale_solid` for full documentation.
        """
        from scadpy.d3.solid import scale_solid

        return scale_solid(solid=self, scale=scale, pivot=pivot, vertex_filter=vertex_filter)

    def resize(
        self: Self,
        size: Iterable[float | None],
        auto: bool = False,
        pivot: float | Iterable[float] | None = None,
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Resize this solid.

        Shortcut for :func:`resize_solid`.
        See :func:`resize_solid` for full documentation.
        """
        from scadpy.d3.solid import resize_solid

        return resize_solid(solid=self, size=size, auto=auto, pivot=pivot, vertex_filter=vertex_filter)

    def mirror(
        self: Self,
        normal: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
    ) -> Solid:
        """Mirror this solid.

        Shortcut for :func:`mirror_solid`.
        See :func:`mirror_solid` for full documentation.
        """
        from scadpy.d3.solid import mirror_solid

        return mirror_solid(solid=self, normal=normal, pivot=pivot)

    def pull(
        self: Self,
        distance: float,
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Move vertices of this solid toward a pivot point.

        Shortcut for :func:`pull_solid`.
        See :func:`pull_solid` for full documentation.
        """
        from scadpy.d3.solid import pull_solid

        return pull_solid(solid=self, distance=distance, pivot=pivot, vertex_filter=vertex_filter)

    def push(
        self: Self,
        distance: float,
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Move vertices of this solid away from a pivot point.

        Shortcut for :func:`push_solid`.
        See :func:`push_solid` for full documentation.
        """
        from scadpy.d3.solid import push_solid

        return push_solid(solid=self, distance=distance, pivot=pivot, vertex_filter=vertex_filter)

    def rotate(
        self: Self,
        angle: float,
        axis: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Rotate this solid around an axis.

        Shortcut for :func:`rotate_solid`.
        See :func:`rotate_solid` for full documentation.
        """
        from scadpy.d3.solid import rotate_solid

        return rotate_solid(solid=self, angle=angle, axis=axis, pivot=pivot, vertex_filter=vertex_filter)

    def color(self: Self, color: Color) -> Solid:
        """Set the color of all parts in this solid.

        Shortcut for :func:`color_solid`.
        See :func:`color_solid` for full documentation.
        """
        from scadpy.d3.solid import color_solid

        return color_solid(solid=self, color=color)

    def convexify(
        self: Self,
        part_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Replace selected parts with their convex hull.

        Shortcut for :func:`convexify_solid`.
        See :func:`convexify_solid` for full documentation.
        """
        from scadpy.d3.solid import convexify_solid

        return convexify_solid(solid=self, part_filter=part_filter)

    def recoordinate(
        self: Self, vertex_coordinates: NDArray[np.float64]
    ) -> Solid:
        """Rebuild this solid with new vertex coordinates.

        Shortcut for :func:`recoordinate_solid`.
        See :func:`recoordinate_solid` for full documentation.
        """
        from scadpy.d3.solid import recoordinate_solid

        return recoordinate_solid(self, vertex_coordinates)

    #############
    # importers #
    #############

    @classmethod
    def from_parts(cls, parts: Sequence[Part[Trimesh]]) -> Solid:
        solid = Solid()
        solid._parts = parts
        return solid

    @classmethod
    def from_geometries(cls, geometries: Sequence[Trimesh]) -> Solid:
        """Shortcut for :func:`map_geometries_to_solid`.

        See :func:`map_geometries_to_solid` for full documentation.
        """
        from scadpy.d3.solid.importers import map_geometries_to_solid

        return map_geometries_to_solid(geometries)

    @classmethod
    def from_geometry(cls, geometry: Trimesh) -> Solid:
        """Shortcut for :func:`map_geometry_to_solid`.

        See :func:`map_geometry_to_solid` for full documentation.
        """
        from scadpy.d3.solid.importers import map_geometry_to_solid

        return map_geometry_to_solid(geometry)

    @classmethod
    def from_stl(cls, source: str | Path) -> Solid:
        """Shortcut for :func:`map_stl_to_solid`.

        See :func:`map_stl_to_solid` for full documentation.
        """
        from scadpy.d3.solid.importers import map_stl_to_solid

        return map_stl_to_solid(source)

    #############
    # exporters #
    #############

    def to_html(
        self: Self,
        background_color: Color = WHITE,
        foreground_color: Color = BLACK,
    ) -> HTML:
        """Render this solid to an interactive HTML widget.

        Shortcut for :func:`map_solid_to_html`.
        See :func:`map_solid_to_html` for full documentation.
        """
        from scadpy import map_solid_to_html

        return map_solid_to_html(
            solid=self,
            background_color=background_color,
            foreground_color=foreground_color,
        )

    def to_html_file(
        self: Self,
        path: str,
        background_color: Color = WHITE,
        foreground_color: Color = BLACK,
    ) -> int:
        """Write this solid to an HTML file.

        Shortcut for :func:`map_solid_to_html_file`.
        See :func:`map_solid_to_html_file` for full documentation.
        """
        from scadpy import map_solid_to_html_file

        return map_solid_to_html_file(
            solid=self,
            path=path,
            background_color=background_color,
            foreground_color=foreground_color,
        )

    def to_screen(
        self: Self,
        background_color: Color = WHITE,
        foreground_color: Color = BLACK,
    ) -> None:
        """Display this solid in an interactive viewer.

        Shortcut for :func:`map_solid_to_screen`.
        See :func:`map_solid_to_screen` for full documentation.
        """
        from scadpy import map_solid_to_screen

        map_solid_to_screen(
            solid=self,
            background_color=background_color,
            foreground_color=foreground_color,
        )

    def to_stl_file(self: Self, path: str | Path) -> int:
        """Export this solid to an STL file.

        Shortcut for :func:`map_solid_to_stl_file`.
        See :func:`map_solid_to_stl_file` for full documentation.
        """
        from scadpy import map_solid_to_stl_file

        return map_solid_to_stl_file(solid=self, path=path)
