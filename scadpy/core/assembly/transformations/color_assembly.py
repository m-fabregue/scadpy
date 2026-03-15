from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scadpy.color import Color
    from scadpy.core.part import Part


def color_assembly[A, G](
    assembly: A,
    color: Color,
    get_assembly_parts: Callable[[A], Iterable[Part[G]]],
    concat_parts: Callable[[Sequence[Part[G]]], A],
) -> A:
    from scadpy.core.part import Part

    return concat_parts(
        [Part[G].from_geometry(p.geometry, color) for p in get_assembly_parts(assembly)]
    )
