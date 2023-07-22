from typing import Dict, Pattern, Tuple


try:
    from typing import Literal, Protocol
except ImportError:
    # typing.Final and typing.Protocol are only available starting from Python 3.8.
    from ._typing import Literal, Protocol  # type: ignore


class SupportsUnit(Protocol):
    @property
    def name(self) -> str:  # pragma: no cover
        ...

    @property
    def regexp(self) -> Pattern:  # pragma: no cover
        ...


Units = Tuple[str, ...]
TextUnitsMap = Dict[SupportsUnit, Units]
HumanReadableStyle = Literal["full", "short", "abbr"]
