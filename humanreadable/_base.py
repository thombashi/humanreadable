"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc
import re
from decimal import Decimal
from typing import List, Optional, Pattern, Tuple, Union, cast

from typepy import RealNumber, String

from ._types import SupportsUnit, TextUnitsMap
from .error import ParameterError, UnitNotFoundError


try:
    from typing import Final
except ImportError:
    # typing.Final and typing.Protocol are only available starting from Python 3.8.
    from ._typing import Final  # type: ignore


_RE_NUMBER: Final[Pattern] = re.compile(r"^[-\+]?[0-9\.]+$")


def _get_unit_msg(text_units: TextUnitsMap) -> str:
    return ", ".join([", ".join(values) for values in text_units.values()])


class HumanReadableValue(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def _text_units(self) -> TextUnitsMap:  # pragma: no cover
        pass

    @abc.abstractproperty
    def _units(self) -> List[SupportsUnit]:  # pragma: no cover
        pass

    @abc.abstractmethod
    def get_as(self, unit: Union[str, SupportsUnit]) -> float:  # pragma: no cover
        pass

    def __init__(
        self, readable_value: str, default_unit: Union[str, SupportsUnit, None] = None
    ) -> None:
        self._default_unit = self._normalize_unit(default_unit)
        self._number, self._from_unit = self.__preprocess(readable_value)

    def __repr__(self) -> str:
        items = [str(self._number)]
        if self._from_unit.name:
            items.append(self._from_unit.name)

        return " ".join(items)

    def _normalize_unit(self, unit: Union[str, SupportsUnit, None]) -> Optional[SupportsUnit]:
        if unit is None:
            return None

        for u in self._text_units:
            if u.regexp.search(cast(str, unit)):
                return u

        raise ValueError(f"unit not found: {unit}")

    def __split_unit(self, readable_value: str) -> Tuple[str, SupportsUnit]:
        if RealNumber(readable_value).is_type():
            if self._default_unit is None:
                raise UnitNotFoundError(
                    "unit not found",
                    value=readable_value,
                    available_units=_get_unit_msg(self._text_units),
                )

            return (readable_value, self._default_unit)

        if not String(readable_value).is_type():
            raise TypeError("readable_value must be a string")

        for unit in self._units:
            try:
                if unit.regexp.search(readable_value):
                    number = unit.regexp.split(readable_value)[0]
                    if not RealNumber(number).is_type():
                        continue

                    return (number, unit)
            except TypeError:
                continue

        raise UnitNotFoundError(
            "unit not found", value=readable_value, available_units=_get_unit_msg(self._text_units)
        )

    def __preprocess(self, readable_value: str) -> Tuple[Decimal, SupportsUnit]:
        if readable_value is None:
            raise TypeError("readable_value must be a string")

        number_str, from_unit = self.__split_unit(readable_value)
        number = self.__to_number(number_str)

        if from_unit is None:
            raise UnitNotFoundError(
                "unit not found",
                value=readable_value,
                available_units=_get_unit_msg(self._text_units),
            )

        return (number, from_unit)

    def __to_number(self, number_str: str) -> Decimal:
        match = _RE_NUMBER.search(number_str)
        if not match:
            raise ParameterError(
                "human-readable value should only include a number", value=number_str
            )

        return Decimal(match.group())
