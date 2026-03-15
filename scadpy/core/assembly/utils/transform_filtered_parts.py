from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from scadpy import Part, TopologyFilter


def transform_filtered_parts[A, G](
    assembly: A,
    parts: Sequence[Part[G]],
    part_filter: TopologyFilter[A] | None,
    transform: Callable[[Sequence[Part[G]]], Sequence[Part[G]]],
    concat_parts: Callable[[Sequence[Part[G]]], A],
) -> A:
    """Apply a transformation to a filtered subset of parts, keeping the rest unchanged.

    Parameters
    ----------
    assembly : A
        The assembly used to evaluate *part_filter*.
    parts : Sequence[Part[G]]
        All parts of the assembly.
    part_filter : TopologyFilter[A] | None
        Optional filter selecting which parts to transform. If ``None``, all
        parts are transformed.
    transform : Callable[[Sequence[Part[G]]], Sequence[Part[G]]]
        Function applied to the selected parts.
    concat_parts : Callable[[Sequence[Part[G]]], A]
        Function that assembles transformed and untouched parts into a new
        assembly of type *A*.

    Returns
    -------
    A
        New assembly with the filtered parts transformed and the rest unchanged.
    """
    from scadpy import resolve_topology_filter

    mask = resolve_topology_filter(
        assembly=assembly, count=len(parts), topology_filter=part_filter
    )
    if mask is None:
        mask = np.ones(len(parts), dtype=bool)

    selected = [p for p, m in zip(parts, mask) if m]
    unselected = [p for p, m in zip(parts, mask) if not m]

    transformed = transform(selected)
    return concat_parts([*transformed, *unselected])
