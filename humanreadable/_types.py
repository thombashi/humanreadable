from re import Pattern
from typing import Literal, Protocol


class SupportsUnit(Protocol):
    @property
    def name(self) -> str:  # pragma: no cover
        ...

    @property
    def regexp(self) -> Pattern:  # pragma: no cover
        ...


Units = tuple[str, ...]
TextUnitsMap = dict[SupportsUnit, Units]
HumanReadableStyle = Literal["full", "short", "abbr"]
