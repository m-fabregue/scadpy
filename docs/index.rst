======
ScadPy
======

|coverage| |interrogate|

.. |coverage| image:: _static/badges/coverage.svg
   :alt: test coverage

.. |interrogate| image:: _static/badges/interrogate.svg
   :alt: doc coverage

**Programmatic CAD in Pure Python.**

ScadPy provides a fluent, type-safe API for 2D and 3D parametric modeling,
built on `Shapely <https://shapely.readthedocs.io>`_ and
`trimesh <https://trimesh.org>`_.
Write designs with the conciseness of OpenSCAD and the full power of Python.


Installation
============

.. code-block:: bash

   pip install scadpy

Requirements: Python ≥ 3.12.

Quick examples
==============

.. doctest::

   >>> # 2D — chamfered mounting plate
   >>> from scadpy import *
   >>> import numpy as np

   >>> PLATE_WIDTH  = 80
   >>> PLATE_HEIGHT = 50
   >>> HOLE_RADIUS  = 4
   >>> HOLE_MARGIN  = 10
   >>> CHAMFER_SIZE = 8

   >>> base               = rectangle([PLATE_WIDTH, PLATE_HEIGHT])
   >>> plate              = base.chamfer(CHAMFER_SIZE)
   >>> corner_coordinates = base.vertex_coordinates[base.corner_to_vertex[:, 1]]

   >>> for position, normal in zip(corner_coordinates, base.corner_normals):
   ...     hole_center = position - HOLE_MARGIN * np.sqrt(2) * normal
   ...     plate -= circle(HOLE_RADIUS).translate(hole_center)
   >>> plate # doctest: +SKIP

.. render-example::
   :name: index_2d
   :example: plate

.. doctest::

   >>> # 3D — parametric ball bearing
   >>> import numpy as np
   >>> from scadpy import *

   >>> BALL_RADIUS    = 3
   >>> RACE_RADIUS    = 15
   >>> NB_BALLS       = 11
   >>> CLEARANCE      = 0.1
   >>> RING_HEIGHT    = 7
   >>> RACE_THICKNESS = 10

   >>> groove = circle(BALL_RADIUS + CLEARANCE) | rectangle([BALL_RADIUS, RING_HEIGHT])
   >>> race   = rectangle([RACE_THICKNESS, RING_HEIGHT]) - groove
   >>> race   = race.radial_extrude(axis=y(1), pivot=x(RACE_RADIUS))

   >>> balls = Solid()
   >>> for angle in np.linspace(0, 360, NB_BALLS, endpoint=False):
   ...     balls += sphere(BALL_RADIUS).rotate(angle, axis=y(1), pivot=x(RACE_RADIUS))

   >>> bearing = race + balls
   >>> bearing # doctest: +SKIP

.. render-example::
   :name: index_3d
   :example: bearing

Cheat sheet
===========

*Parameters shown in* ``# comments`` *are optional, with their default values.*

**2D — Shape**

.. code-block:: python

   from scadpy import *

   # primitives
   circle(radius=3)                                # segment_count=64
   polygon(points=[(-2, -2), (2, -2), (0, 2)])
   rectangle(size=[6, 3])
   Shape.from_dxf("file.dxf")
   Shape.from_svg("file.svg")
   square(size=4)

   # boolean operations
   s = square(size=4);  c = circle(radius=3)
   s | c    # union
   s - c    # difference
   s & c    # intersection
   s ^ c    # symmetric difference
   s + c    # concat (no merge)

   # transforms
   s.chamfer(size=0.8)              # corner_filter=None, epsilon=1e-8
   s.color(color=RED)
   s.convexify()                    # part_filter=None
   s.fill()                         # part_filter=None
   s.fillet(size=0.8)               # corner_filter=None, segment_count=32, epsilon=1e-8
   s.grow(distance=0.5)             # part_filter=None
   s.linear_cut(axis=x(1))          # pivot=0
   s.linear_slice(thickness=2, direction=x(1))  # pivot=0, part_filter=None
   s.mirror(normal=[1, 0])          # pivot=0
   s.pull(distance=1.0)             # pivot=0, vertex_filter=None
   s.push(distance=1.0)             # pivot=0, vertex_filter=None
   s.radial_slice(start=0, end=180) # pivot=0, part_filter=None
   s.resize(size=[6, None])         # auto=False, pivot=None, vertex_filter=None
   s.rotate(angle=30)               # pivot=0, vertex_filter=None
   s.scale(scale=[2, 0.5])          # pivot=0, vertex_filter=None
   s.shrink(distance=0.5)           # part_filter=None
   s.translate(translation=[2, 1])  # vertex_filter=None

   # topology — coordinates & attributes
   s.are_corners_convex             # (n_corners,)    — convexity mask
   s.corner_angles                  # (n_corners,)    — interior angles (°)
   s.corner_normals                 # (n_corners,  2) — outward unit normals
   s.directed_edge_directions       # (2*n_edges, 2)
   s.edge_lengths                   # (n_edges,)
   s.edge_midpoints                 # (n_edges,  2)
   s.edge_normals                   # (n_edges,  2)
   s.ring_types                     # (n_rings,)  — "exterior"|"interior"
   s.vertex_coordinates             # (n_vertices, 2)

   # topology — bridges (*_to_*)
   s.corner_to_incoming_directed_edge  # corner        → directed_edge
   s.corner_to_outgoing_directed_edge  # corner        → directed_edge
   s.corner_to_vertex                  # corner        → [prev, curr, next]
   s.directed_edge_to_corner           # directed_edge → [source, target]
   s.directed_edge_to_edge             # directed_edge → edge
   s.directed_edge_to_vertex           # directed_edge → [start, end]
   s.edge_to_vertex                    # edge          → [start, end]
   s.ring_to_part                      # ring          → part
   s.vertex_to_part                    # vertex        → part
   s.vertex_to_ring                    # vertex        → ring

   # extrusions → Solid
   s.linear_extrude(height=3)
   s.radial_extrude(axis=y(1), pivot=x(5))  # start=0, end=360, segment_count=64

   # export
   s.to_dxf_file("output.dxf")
   s.to_html_file("output.html")
   s.to_screen()
   s.to_svg_file("output.svg")

**3D — Solid**

.. code-block:: python

   from scadpy import *

   # primitives
   cone(radius=2, height=4)         # section_count=32
   cuboid(size=[4, 3, 2])
   cylinder(radius=2, height=4)     # section_count=32
   polyhedron(vertices=vertices, faces=faces)
   sphere(radius=3)                 # subdivision_count=4
   Solid.from_stl("model.stl")

   # boolean operations
   a = cuboid(size=[4, 3, 2]);  b = sphere(radius=2)
   a | b    # union
   a - b    # difference
   a & b    # intersection
   a ^ b    # symmetric difference
   a + b    # concat (no merge)

   # transforms
   a.color(color=RED)
   a.convexify()                    # part_filter=None
   a.mirror(normal=[1, 0, 0])       # pivot=0
   a.pull(distance=1.0)             # pivot=0, vertex_filter=None
   a.push(distance=1.0)             # pivot=0, vertex_filter=None
   a.resize(size=[6, None, None])   # auto=False, pivot=None, vertex_filter=None
   a.rotate(angle=30, axis=z(1))    # pivot=0, vertex_filter=None
   a.scale(scale=[2, 1, 0.5])       # pivot=0, vertex_filter=None
   a.translate(translation=[1, 0, 0])  # vertex_filter=None

   # topology — coordinates & bridges (*_to_*)
   a.triangle_to_vertex    # triangle → [v0, v1, v2]
   a.vertex_coordinates    # (n_vertices,  3)
   a.vertex_to_part        # vertex   → part

   # export
   a.to_html_file("output.html")
   a.to_screen()
   a.to_stl_file("output.stl")

Roadmap
=======

- Improve documentation
- Richer topology for Shape and Solid
- Richer transformations for Shape and Solid
- Chamfer and fillet on Solid
- New assembly types: ``PointCloud2d``, ``Wire2d``, ``PointCloud3d``, ``Wire3d``
- Better error messages
- More import/export formats

Development
===========

.. code-block:: bash

   # Create and activate venv
   python3 -m venv .venv
   source .venv/bin/activate

   # Install with dev dependencies
   pip install -e .[dev]

   # Run doctests & generate documentation
   cd docs && make doctest && make html

License
=======

See ``LICENSE.md`` at the root of the repository.

API reference
=============

.. toctree::
   :maxdepth: 4

   core <scadpy/core>
   2D <scadpy/d2>
   3D <scadpy/d3>
