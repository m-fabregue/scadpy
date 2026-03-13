from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import trimesh
from typeguard import typechecked

if TYPE_CHECKING:
    from scadpy import Solid


@typechecked
def map_solid_to_stl_file(solid: Solid, path: str | Path) -> int:
    """Export a solid to an STL file.

    All parts of the solid are merged into a single mesh before export.
    The resulting file is in binary STL format.

    Parameters
    ----------
    solid : Solid
        The solid to export.
    path : str or Path
        Destination file path.  The ``.stl`` extension is recommended but
        not enforced.

    Returns
    -------
    int
        The number of bytes written.
    """
    meshes = [p.geometry for p in solid._parts if len(p.geometry.faces) > 0]
    if not meshes:
        data = b""
    else:
        combined = trimesh.util.concatenate(meshes)
        data = combined.export(file_type="stl")

    path = Path(path)
    path.write_bytes(data)
    return len(data)
