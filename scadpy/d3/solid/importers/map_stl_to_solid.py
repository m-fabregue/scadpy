from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, cast

from trimesh import Trimesh, load

if TYPE_CHECKING:
    from scadpy.d3.solid import Solid


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

    from scadpy.d3.solid.importers import map_geometry_to_solid

    return map_geometry_to_solid(cast(Trimesh, load(source, force="mesh")))
