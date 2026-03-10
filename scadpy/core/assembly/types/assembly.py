from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from scadpy.core.part import Part


class Assembly[G](ABC):
    def __init__(self, *args: Any, **kwargs: Any):  # pyright: ignore[reportExplicitAny, reportAny]
        super().__init__(*args, **kwargs)
        self._parts: Sequence[Part[G]] = []
