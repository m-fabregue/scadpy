from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from trimesh import Trimesh, load
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


@typechecked
def map_stl_to_solid(source: str | Path) -> Solid:
    """Load a solid from an STL file.

    Parameters
    ----------
    source : str or Path
        Path to the ``.stl`` file.

    Returns
    -------
    Solid
        A new solid loaded from the STL file.
    """
    from typing import cast

    from scadpy.d3.solid.importers import map_geometry_to_solid

    return map_geometry_to_solid(cast(Trimesh, load(source, force="mesh")))
