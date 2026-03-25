from __future__ import annotations

from collections.abc import Iterable, Sequence
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self, final

from scadpy.color.constants import BLACK, WHITE

if TYPE_CHECKING:
    # Lazy: IPython (~0.6s) is heavy; used only as a return type annotation here.
    from IPython.core.display import HTML

    from scadpy import TopologyFilter
    from scadpy.color import Color
    from scadpy.core.part import Part

import numpy as np
from numpy.typing import NDArray
from trimesh import Trimesh

from scadpy.core.assembly import Assembly


@final
class Solid(Assembly[Trimesh]):
    """A 3D assembly of :class:`~trimesh.Trimesh` parts.

    ``Solid`` is the central 3D modeling object in ScadPy.  It wraps one or
    more colored Trimesh meshes and exposes a fluent API for boolean
    operations, geometric transforms, topology queries, and 3D export.

    Use the primitives (:func:`~scadpy.cuboid`, :func:`~scadpy.cylinder`,
    :func:`~scadpy.sphere`, …) or importers (:meth:`Solid.from_stl`) to
    create solids; do not instantiate this class directly.

    Examples
    --------
    >>> from scadpy import cuboid, sphere
    >>> s = cuboid(4) - sphere(3)
    >>> s.is_empty
    False
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pyright: ignore[reportExplicitAny, reportAny]
        """Initialize a Solid (internal — use primitives instead)."""
        super().__init__(*args, **kwargs)

    @classmethod
    def dimensions(cls) -> int:
        """Return the number of spatial dimensions: always ``3``.

        Returns
        -------
        int
            Always ``3``.

        Examples
        --------
        >>> from scadpy import Solid
        >>> Solid.dimensions()
        3
        """
        return 3

    ##########
    # vertex #
    ##########

    @cached_property
    def vertex_coordinates(self: Self) -> NDArray[np.float64]:
        """For each vertex in the solid, return its coordinates.

        See :func:`get_solid_vertex_coordinates` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> vertex_coordinates = cuboid(2).vertex_coordinates
        >>> vertex_coordinates.shape
        (8, 3)
        """
        from scadpy.d3.solid import get_solid_vertex_coordinates

        return get_solid_vertex_coordinates(self)

    @cached_property
    def vertex_to_part(self: Self) -> NDArray[np.int64]:
        """For each vertex in the solid, return its part index.

        See :func:`get_solid_vertex_to_part` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> solid = cuboid(2) + cuboid(2).translate(5)
        >>> solid.vertex_to_part
        array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])
        """
        from scadpy.d3.solid import get_solid_vertex_to_part

        return get_solid_vertex_to_part(self)

    ############
    # features #
    ############

    @cached_property
    def is_empty(self: Self) -> bool:
        """Return whether the solid has no vertices.

        See :func:`is_solid_empty` for parameter documentation.

        Examples
        --------
        >>> from scadpy import Solid, cuboid

        >>> Solid.from_parts([]).is_empty
        True

        >>> cuboid(2).is_empty
        False
        """
        from scadpy.d3.solid import is_solid_empty

        return is_solid_empty(self)

    @cached_property
    def bounds(self: Self) -> NDArray[np.float64]:
        """Return the axis-aligned bounding box of the solid.

        See :func:`get_solid_bounds` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(2).bounds
        array([-1., -1., -1.,  1.,  1.,  1.])
        """
        from scadpy.d3.solid import get_solid_bounds

        return get_solid_bounds(self)

    @cached_property
    def bounding_box(self: Self) -> Solid:
        """Return the axis-aligned bounding box of the solid as a cuboid.

        See :func:`get_solid_bounding_box` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(2).bounding_box.bounds
        array([-1., -1., -1.,  1.,  1.,  1.])
        """
        from scadpy import get_solid_bounding_box

        return get_solid_bounding_box(self)

    @cached_property
    def centroid(self: Self) -> NDArray[np.float64]:
        """Return the geometric centroid of the solid, weighted by part volume.

        See :func:`get_solid_centroid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(2).centroid
        array([0., 0., 0.])
        """
        from scadpy import get_solid_centroid

        return get_solid_centroid(self)

    ##############
    # topologies #
    ##############

    @cached_property
    def part_colors(self: Self) -> NDArray[np.float64]:
        """For each part in the solid, return its RGBA color.

        See :func:`get_solid_part_colors` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid, DEFAULT_OPACITY

        >>> colors = cuboid(2).part_colors
        >>> colors.shape
        (1, 4)
        >>> bool(colors[0, 3] == DEFAULT_OPACITY)
        True
        """
        from scadpy.d3.solid import get_solid_part_colors

        return get_solid_part_colors(self)

    @cached_property
    def triangle_to_vertex(self: Self) -> NDArray[np.int64]:
        """For each triangle in the solid, return the indices of its three vertices.

        See :func:`get_solid_triangle_to_vertex` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> triangle_to_vertex = cuboid(2).triangle_to_vertex
        >>> triangle_to_vertex.shape[1]
        3
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
        """Intersect two solids. Shortcut for :func:`intersect_solid`.

        Examples
        --------
        >>> from scadpy import cuboid, sphere
        >>> (cuboid(4) & sphere(3)).is_empty
        False
        """
        from scadpy import intersect_solid

        return intersect_solid(solids=[self, other])

    def __sub__(self: Self, other: Solid) -> Solid:
        """Subtract a solid from this solid. Shortcut for :func:`subtract_solid`."""
        from scadpy import subtract_solid

        return subtract_solid(to_be_subtracted=self, to_subtract=other)

    def __xor__(self: Self, other: Solid) -> Solid:
        """Compute symmetric difference with another solid. Shortcut for :func:`exclude_solid`.

        Examples
        --------
        >>> from scadpy import cuboid, sphere
        >>> (cuboid(4) ^ sphere(3)).is_empty
        False
        """
        from scadpy import exclude_solid

        return exclude_solid(solids=[self, other])

    def concat(self: Self, solids: Sequence[Solid]) -> Solid:
        """Concatenate this solid with others without any boolean operation.

        See :func:`concat_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid, sphere

        >>> cuboid(4).concat([sphere(radius=2).translate([3, 2, 0])])  # doctest: +SKIP

        .. render-example::
            :name: concat_solid
            :example: cuboid(4).concat([sphere(radius=2).translate([3, 2, 0])])
        """
        from scadpy import concat_solid

        return concat_solid(solids=[self, *solids])

    def unify(self: Self, solids: Sequence[Solid]) -> Solid:
        """Unite this solid with others using boolean union.

        See :func:`unify_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid, sphere, x

        >>> cuboid(4).unify([sphere(radius=2).translate(x(2))])  # doctest: +SKIP

        .. render-example::
            :name: unify_solid
            :example: cuboid(4).unify([sphere(radius=2).translate(x(2))])
        """
        from scadpy import unify_solid

        return unify_solid(solids=[self, *solids])

    def intersect(self: Self, solids: Sequence[Solid]) -> Solid:
        """Compute the intersection of this solid with others.

        See :func:`intersect_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid, sphere

        >>> cuboid(4).intersect([sphere(radius=2).translate(1)])  # doctest: +SKIP

        .. render-example::
            :name: intersect_solid
            :example: cuboid(4).intersect([sphere(radius=2).translate(1)])
            :ghost: cuboid(4) + sphere(radius=2).translate(1)
        """
        from scadpy import intersect_solid

        return intersect_solid(solids=[self, *solids])

    def subtract(self: Self, to_subtract: Solid) -> Solid:
        """Subtract a solid from this solid using boolean difference.

        See :func:`subtract_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid, sphere

        >>> cuboid(4).subtract(sphere(radius=2))  # doctest: +SKIP

        .. render-example::
            :name: subtract_solid
            :example: cuboid(4).subtract(sphere(radius=2))
            :ghost: cuboid(4)
        """
        from scadpy import subtract_solid

        return subtract_solid(to_be_subtracted=self, to_subtract=to_subtract)

    def exclude(self: Self, solids: Sequence[Solid]) -> Solid:
        """Compute the symmetric difference (XOR) of this solid with others.

        See :func:`exclude_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid, concat_solid, x

        >>> cuboid(4).exclude([cuboid(4).translate(x(2))])  # doctest: +SKIP

        .. render-example::
            :name: exclude_solid
            :example: cuboid(4).exclude([cuboid(4).translate(x(2))])
            :ghost: concat_solid(solids=[cuboid(4), cuboid(4).translate(x(2))])
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
        """Translate this solid by a given vector.

        See :func:`translate_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(4).translate([3, 2, 1])  # doctest: +SKIP

        .. render-example::
            :name: translate_solid
            :example: cuboid(4).translate([3, 2, 1])
            :ghost: cuboid(4)
        """
        from scadpy.d3.solid import translate_solid

        return translate_solid(
            solid=self, translation=translation, vertex_filter=vertex_filter
        )

    def scale(
        self: Self,
        scale: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Scale this solid by a given factor, relative to a pivot point.

        See :func:`scale_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(4).scale(2, pivot=[2, 2, 2])  # doctest: +SKIP

        .. render-example::
            :name: scale_solid
            :example: cuboid(4).scale(2, pivot=[2, 2, 2])
            :ghost: cuboid(4)
        """
        from scadpy.d3.solid import scale_solid

        return scale_solid(
            solid=self, scale=scale, pivot=pivot, vertex_filter=vertex_filter
        )

    def resize(
        self: Self,
        size: Iterable[float | None],
        auto: bool = False,
        pivot: float | Iterable[float] | None = None,
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Resize this solid to fit target dimensions.

        See :func:`resize_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> # resize to an exact size on all axes:
        >>> cuboid([4, 2, 1]).resize([6, 6, 6])  # doctest: +SKIP

        .. render-example::
           :name: resize_solid_exact
           :example: cuboid([4, 2, 1]).resize([6, 6, 6])
           :ghost: cuboid([4, 2, 1])

        >>> # freeze two axes (``None``) and scale only the first:
        >>> cuboid([4, 2, 1]).resize([6, None, None])  # doctest: +SKIP

        .. render-example::
           :name: resize_solid_freeze
           :example: cuboid([4, 2, 1]).resize([6, None, None])
           :ghost: cuboid([4, 2, 1])

        >>> # scale frozen axes proportionally with ``auto=True``:
        >>> cuboid([4, 2, 1]).resize([6, None, None], auto=True)  # doctest: +SKIP

        .. render-example::
           :name: resize_solid_auto
           :example: cuboid([4, 2, 1]).resize([6, None, None], auto=True)
           :ghost: cuboid([4, 2, 1])
        """
        from scadpy.d3.solid import resize_solid

        return resize_solid(
            solid=self, size=size, auto=auto, pivot=pivot, vertex_filter=vertex_filter
        )

    def mirror(
        self: Self,
        normal: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
    ) -> Solid:
        """Mirror this solid across a plane defined by a normal vector and a pivot point.

        See :func:`mirror_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(4).mirror([1, 0, 0], pivot=[2, 0, 0])  # doctest: +SKIP

        .. render-example::
            :name: mirror_solid
            :example: cuboid(4).mirror([1, 0, 0], pivot=[2, 0, 0])
            :ghost: cuboid(4)
        """
        from scadpy.d3.solid import mirror_solid

        return mirror_solid(solid=self, normal=normal, pivot=pivot)

    def pull(
        self: Self,
        distance: float,
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Move a subset of vertices of this solid toward a pivot point by a given distance.

        See :func:`pull_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(4).pull(distance=1.0, pivot=[2, 2, 2], vertex_filter=cuboid(4).vertex_coordinates[:, 0] < 1)  # doctest: +SKIP

        .. render-example::
            :name: pull_solid
            :example: cuboid(4).pull(distance=1.0, pivot=[2, 2, 2], vertex_filter=cuboid(4).vertex_coordinates[:, 0] < 1)
            :ghost: cuboid(4)
        """
        from scadpy.d3.solid import pull_solid

        return pull_solid(
            solid=self, distance=distance, pivot=pivot, vertex_filter=vertex_filter
        )

    def push(
        self: Self,
        distance: float,
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Move a subset of vertices of this solid away from a pivot point by a given distance.

        See :func:`push_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(4).push(distance=1.0, pivot=[2, 2, 2], vertex_filter=cuboid(4).vertex_coordinates[:, 0] < 1)  # doctest: +SKIP

        .. render-example::
            :name: push_solid
            :example: cuboid(4).push(distance=1.0, pivot=[2, 2, 2], vertex_filter=cuboid(4).vertex_coordinates[:, 0] < 1)
            :ghost: cuboid(4)
        """
        from scadpy.d3.solid import push_solid

        return push_solid(
            solid=self, distance=distance, pivot=pivot, vertex_filter=vertex_filter
        )

    def rotate(
        self: Self,
        angle: float,
        axis: float | Iterable[float],
        pivot: float | Iterable[float] = 0,
        vertex_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Rotate this solid by a given angle around an axis passing through a pivot point.

        See :func:`rotate_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(4).rotate(angle=45, axis=[0, 0, 1], pivot=[2, 2, 2])  # doctest: +SKIP

        .. render-example::
            :name: rotate_solid
            :example: cuboid(4).rotate(angle=45, axis=[0, 0, 1], pivot=[2, 2, 2])
            :ghost: cuboid(4)
        """
        from scadpy.d3.solid import rotate_solid

        return rotate_solid(
            solid=self, angle=angle, axis=axis, pivot=pivot, vertex_filter=vertex_filter
        )

    def color(self: Self, color: Color) -> Solid:
        """Set the color of all parts in this solid.

        See :func:`color_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid
        >>> from scadpy.color.constants import RED

        >>> cuboid(4).color(RED)  # doctest: +SKIP

        .. render-example::
            :name: color_solid
            :example: cuboid(4).color(RED)
            :keep-color:
        """
        from scadpy.d3.solid import color_solid

        return color_solid(solid=self, color=color)

    def convexify(
        self: Self,
        part_filter: TopologyFilter[Solid] | None = None,
    ) -> Solid:
        """Create a new solid whose selected parts are replaced by their convex hull.

        See :func:`convexify_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid, sphere

        >>> (cuboid(4) + sphere(radius=2).translate([3, 3, 3])).convexify()  # doctest: +SKIP

        .. render-example::
            :name: convexify_solid
            :example: (cuboid(4) + sphere(radius=2).translate([3, 3, 3])).convexify()
            :ghost: cuboid(4) + sphere(radius=2).translate([3, 3, 3])
        """
        from scadpy.d3.solid import convexify_solid

        return convexify_solid(solid=self, part_filter=part_filter)

    def recoordinate(self: Self, vertex_coordinates: NDArray[np.float64]) -> Solid:
        """Rebuild this solid with new vertex coordinates, preserving topology and colors.

        See :func:`recoordinate_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(4).recoordinate(cuboid(4).vertex_coordinates + [2.0, 1.0, 0.0])  # doctest: +SKIP

        .. render-example::
            :name: recoordinate_solid
            :example: cuboid(4).recoordinate(cuboid(4).vertex_coordinates + [2.0, 1.0, 0.0])
            :ghost: cuboid(4)
        """
        from scadpy.d3.solid import recoordinate_solid

        return recoordinate_solid(self, vertex_coordinates)

    def linear_pattern(
        self: Self,
        counts: int | Sequence[int],
        steps: NDArray[np.float64] | Sequence[NDArray[np.float64]],
    ) -> Solid:
        """Repeat this solid in a linear or grid pattern.

        See :func:`linear_pattern_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import sphere, x, y, z

        >>> sphere(1).linear_pattern(counts=4, steps=x(3))  # doctest: +SKIP

        .. render-example::
            :name: linear_pattern_solid_method
            :example: sphere(1).linear_pattern(counts=4, steps=x(3))

        >>> sphere(1).linear_pattern(counts=[3, 2], steps=[x(3), y(3)])  # doctest: +SKIP

        .. render-example::
            :name: linear_pattern_solid_method_2d
            :example: sphere(1).linear_pattern(counts=[3, 2], steps=[x(3), y(3)])

        >>> sphere(1).linear_pattern(counts=[3, 2, 4], steps=[x(3), y(3), z(4)])  # doctest: +SKIP

        .. render-example::
            :name: linear_pattern_solid_method_3d
            :example: sphere(1).linear_pattern(counts=[3, 2, 4], steps=[x(3), y(3), z(4)])
        """
        from scadpy import linear_pattern_solid

        return linear_pattern_solid(solid=self, counts=counts, steps=steps)

    def radial_pattern(
        self: Self,
        count: int,
        axis: float | Iterable[float],
        angle: float = 360,
        pivot: float | Iterable[float] = 0,
    ) -> Solid:
        """Repeat this solid in a radial pattern around an axis.

        See :func:`radial_pattern_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import sphere, x

        >>> sphere(1).translate(x(3)).radial_pattern(count=6, axis=z())  # doctest: +SKIP

        .. render-example::
            :name: radial_pattern_solid_method
            :example: sphere(1).translate(x(3)).radial_pattern(count=6, axis=z())
        """
        from scadpy import radial_pattern_solid

        return radial_pattern_solid(
            solid=self, count=count, angle=angle, axis=axis, pivot=pivot
        )

    #############
    # importers #
    #############

    @classmethod
    def from_parts(cls, parts: Sequence[Part[Trimesh]]) -> Solid:
        """Assemble a :class:`Solid` from a sequence of :class:`~scadpy.Part`.

        This is the low-level constructor used internally.  In most cases you
        should use primitives or boolean operations instead.

        Parameters
        ----------
        parts : Sequence[Part[Trimesh]]
            The parts that make up the solid.

        Returns
        -------
        Solid
            A new solid containing exactly the given parts.

        Examples
        --------
        >>> from scadpy import Solid
        >>> Solid.from_parts([]).is_empty
        True
        """
        solid = Solid()
        solid._parts = parts
        return solid

    @classmethod
    def from_geometries(cls, geometries: Sequence[Trimesh]) -> Solid:
        """Map a sequence of Trimesh geometries to a solid.

        See :func:`map_geometries_to_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> Solid.from_geometries([cuboid(4)._parts[0].geometry])  # doctest: +SKIP

        .. render-example::
            :name: map_geometries_to_solid
            :example: Solid.from_geometries([cuboid(4)._parts[0].geometry])
        """
        from scadpy.d3.solid.importers import map_geometries_to_solid

        return map_geometries_to_solid(geometries)

    @classmethod
    def from_geometry(cls, geometry: Trimesh) -> Solid:
        """Map a single Trimesh geometry to a solid.

        See :func:`map_geometry_to_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> Solid.from_geometry(cuboid(4)._parts[0].geometry)  # doctest: +SKIP

        .. render-example::
            :name: map_geometry_to_solid
            :example: Solid.from_geometry(cuboid(4)._parts[0].geometry)
        """
        from scadpy.d3.solid.importers import map_geometry_to_solid

        return map_geometry_to_solid(geometry)

    @classmethod
    def from_stl(cls, source: str | Path) -> Solid:
        """Load a solid from an STL file.

        See :func:`map_stl_to_solid` for parameter documentation.

        Examples
        --------
        >>> from scadpy import Solid

        >>> Solid.from_stl("model.stl")  # doctest: +SKIP
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
        """Render this solid as an interactive HTML widget.

        See :func:`map_solid_to_html` for parameter documentation.

        Examples
        --------
        >>> from IPython.core.display import HTML
        >>> from scadpy import cuboid

        >>> html = cuboid(4).to_html()
        >>> isinstance(html, HTML)
        True
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
        """Save this solid as an HTML file.

        See :func:`map_solid_to_html_file` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(4).to_html_file(path="output.html")  # doctest: +SKIP
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

        See :func:`map_solid_to_screen` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(4).to_screen()  # doctest: +SKIP
        """
        from scadpy import map_solid_to_screen

        map_solid_to_screen(
            solid=self,
            background_color=background_color,
            foreground_color=foreground_color,
        )

    def to_stl_file(self: Self, path: str | Path) -> int:
        """Export this solid to an STL file.

        See :func:`map_solid_to_stl_file` for parameter documentation.

        Examples
        --------
        >>> from scadpy import cuboid

        >>> cuboid(4).to_stl_file(path="output.stl")  # doctest: +SKIP
        """
        from scadpy import map_solid_to_stl_file

        return map_solid_to_stl_file(solid=self, path=path)
