Examples
========

.. _chamfered-mounting-plate:

.. doctest::

   >>> # 2D — chamfered mounting plate
   >>> from scadpy import circle, cuboid, rectangle, sphere, square, text
   >>> from scadpy import x, y, z, GRAY, ORANGE
   >>> import numpy as np
   >>> import math

   >>> PLATE_WIDTH  = 80
   >>> PLATE_HEIGHT = 50
   >>> PLATE_THICKNESS = 10
   >>> HOLE_RADIUS  = 4
   >>> HOLE_MARGIN  = 10
   >>> CHAMFER_SIZE = 8

   >>> base  = rectangle([PLATE_WIDTH, PLATE_HEIGHT])
   >>> plate = base.chamfer(CHAMFER_SIZE)

   >>> for position, normal in zip(base.vertex_coordinates, base.vertex_normals):
   ...     hole_center = position - HOLE_MARGIN * np.sqrt(2) * normal
   ...     plate -= circle(HOLE_RADIUS).translate(hole_center)

   >>> plate.to_screen() # doctest: +SKIP

.. render-example::
   :name: examples_plate
   :example: plate

.. _extruded-plate-with-label:

.. doctest::

   >>> # 3D — extruded plate with label
   >>> TEXT_THICKNESS = 2

   >>> extruded_plate = plate.linear_extrude(PLATE_THICKNESS)
   >>> label = text("ScadPy", size=15).linear_extrude(TEXT_THICKNESS)
   >>> labelized_extruded_plate = extruded_plate | label.translate(z(PLATE_THICKNESS))
   >>> labelized_extruded_plate.to_screen() # doctest: +SKIP

.. render-example::
   :name: examples_labelized_extruded_plate
   :example: labelized_extruded_plate

.. _honeycomb-plate:

.. doctest::

   >>> # 3D — mounting plate with honeycomb pattern
   >>> HEX_RADIUS = 5
   >>> HEX_WALL_THICKNESS = 1
   >>> NB_X, NB_Y = 5, 4

   >>> spacing_x = HEX_RADIUS * np.sqrt(3)
   >>> spacing_y = HEX_RADIUS * 1.5

   >>> hole = circle(HEX_RADIUS, segment_count=6).rotate(30)
   >>> hole = hole.shrink(HEX_WALL_THICKNESS / 2)

   >>> holes = hole.linear_pattern(
   ...     counts=[NB_X, math.ceil(NB_Y / 2)],
   ...     steps=[np.array([spacing_x, 0]), np.array([0, 2 * spacing_y])],
   ... )
   >>> holes += holes.translate([spacing_x / 2, spacing_y])
   >>> holes = holes.translate(-holes.centroid)

   >>> honeycomb_extruded_plate = extruded_plate - holes.linear_extrude(PLATE_THICKNESS)
   >>> honeycomb_extruded_plate.to_screen() # doctest: +SKIP

.. render-example::
   :name: examples_honeycomb_extruded_plate
   :example: honeycomb_extruded_plate

.. _waved-sphere:

.. doctest::

   >>> # 3D — apply a math function to a solid coordinates
   >>> waved_sphere = sphere(10)
   >>> vertex_coordinates = waved_sphere.vertex_coordinates
   >>> vertex_coordinates[:, 2] += 2 * np.sin(vertex_coordinates[:, 0])
   >>> waved_sphere = waved_sphere.recoordinate(vertex_coordinates)
   >>> waved_sphere.to_screen() # doctest: +SKIP

.. render-example::
   :name: examples_waved_sphere
   :example: waved_sphere

.. _ball-bearing:

.. doctest::

   >>> # 3D — parametric ball bearing
   >>> BALL_RADIUS    = 3
   >>> RACE_RADIUS    = 15
   >>> NB_BALLS       = 11
   >>> CLEARANCE      = 0.1
   >>> RING_HEIGHT    = 7
   >>> RACE_THICKNESS = 10

   >>> groove  = circle(BALL_RADIUS + CLEARANCE) | rectangle([BALL_RADIUS, RING_HEIGHT])
   >>> race    = rectangle([RACE_THICKNESS, RING_HEIGHT]) - groove
   >>> bearing = race.radial_extrude(axis=y(), pivot=x(RACE_RADIUS)).color(GRAY)

   >>> ball = sphere(BALL_RADIUS).color(ORANGE)
   >>> bearing += ball.radial_pattern(count=NB_BALLS, axis=y(), pivot=x(RACE_RADIUS))

   >>> bearing.to_screen() # doctest: +SKIP

.. render-example::
   :name: examples_bearing
   :example: bearing
   :keep-color:

.. _dice:

.. doctest::

   >>> # 3D — dice
   >>> SIZE = 20

   >>> dice = cuboid(SIZE)
   >>> pip  = sphere(SIZE / 12).translate(z(SIZE / 2))

   >>> one   = pip
   >>> two = (
   ...     pip.translate([SIZE / 4, SIZE / 4, 0]) +
   ...     pip.translate([-SIZE / 4, -SIZE / 4, 0])
   ... )
   >>> three = one + two
   >>> four  = two + two.rotate(90, z())
   >>> five  = one + four
   >>> six   = four + pip.translate(x(SIZE / 4)) + pip.translate(x(-SIZE / 4))

   >>> dice -= (
   ...     one
   ...     + two.rotate(90, x())
   ...     + three.rotate(90, y())
   ...     + four.rotate(-90, y())
   ...     + five.rotate(-90, x())
   ...     + six.rotate(-180, x())
   ... )

   >>> dice.to_screen() # doctest: +SKIP

.. render-example::
   :name: examples_dice
   :example: dice

.. _storage-box:

.. doctest::

   >>> # 3D — storage box
   >>> SIZE_OUTER = 20
   >>> SIZE_INNER = 18
   >>> FILLET = 1
   >>> BASE_HEIGHT = 10
   >>> CUT_HEIGHT = 8
   >>> CAP_HEIGHT_OUTER = 1.5
   >>> CAP_HEIGHT_INNER = 3
   >>> CAP_OFFSET_X = 25
   >>> CUT_OFFSET_Z = 2

   >>> outer_base = square(SIZE_OUTER).fillet(FILLET).linear_extrude(BASE_HEIGHT)
   >>> inner_cut = square(SIZE_INNER).linear_extrude(CUT_HEIGHT).translate(z(CUT_OFFSET_Z))
   >>> base = outer_base - inner_cut

   >>> cap_outer = square(SIZE_OUTER).fillet(FILLET).linear_extrude(CAP_HEIGHT_OUTER)
   >>> cap_inner = square(SIZE_INNER).linear_extrude(CAP_HEIGHT_INNER)
   >>> cap = (cap_outer | cap_inner).translate(x(CAP_OFFSET_X))

   >>> storage_box = base + cap
   >>> storage_box.to_screen() # doctest: +SKIP

.. render-example::
   :name: examples_storage_box
   :example: storage_box
