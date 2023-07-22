try:
    from typing import Final
except ImportError:
    # typing.Final and typing.Protocol are only available starting from Python 3.8.
    from ._typing import Final  # type: ignore


PATTERN_TEMPLETE: Final[str] = r"\s?{}$"
