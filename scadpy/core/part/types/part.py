from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from scadpy.color import DEFAULT_COLOR

if TYPE_CHECKING:
    from scadpy.color import Color


@dataclass(frozen=True)
class Part[G]:
    _geometry: G
    _color: Color

    @property
    def color(self) -> Color:
        return self._color

    @classmethod
    def from_geometry_ref(
        cls: type[Self], geometry: G, color: Color = DEFAULT_COLOR
    ) -> Self:
        return cls(_geometry=geometry, _color=color)

    @classmethod
    def from_geometry(cls: type[Self], geometry: G, color: Color = DEFAULT_COLOR) -> Self:
        return cls(_geometry=deepcopy(geometry), _color=color)

    @property
    def geometry(self) -> G:
        return self._geometry
