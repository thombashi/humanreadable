"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import re
from collections import OrderedDict
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, NamedTuple, Optional, Pattern, Union, cast

from ._base import HumanReadableValue
from ._common import compile_units_regex_pattern
from ._types import HumanReadableStyle, SupportsUnit, TextUnitsMap, Units
from .error import ParameterError


try:
    from typing import Final
except ImportError:
    # typing.Final and typing.Protocol are only available starting from Python 3.8.
    from ._typing import Final  # type: ignore


_DAY_STR_UNITS: Final[Units] = ("d", "day", "days")
_HOUR_STR_UNITS: Final[Units] = ("h", "hour", "hours")
_MINUTE_STR_UNITS: Final[Units] = ("m", "min", "mins", "minute", "minutes")
_SEC_STR_UNITS: Final[Units] = ("s", "sec", "secs", "second", "seconds")
_MSEC_STR_UNITS: Final[Units] = ("ms", "msec", "msecs", "millisecond", "milliseconds")
_USEC_STR_UNITS: Final[Units] = ("us", "usec", "usecs", "microsecond", "microseconds")


class TimeUnit(NamedTuple):
    name: str
    regexp: Pattern[str]
    thousand_factor: int
    sixty_factor: int
    day_factor: int


class Time(HumanReadableValue):
    @dataclass(frozen=True)
    class Unit:
        DAY = TimeUnit(
            name="days",
            regexp=compile_units_regex_pattern(_DAY_STR_UNITS, re.IGNORECASE),
            thousand_factor=0,
            sixty_factor=0,
            day_factor=0,
        )
        HOUR = TimeUnit(
            name="hours",
            regexp=compile_units_regex_pattern(_HOUR_STR_UNITS, re.IGNORECASE),
            thousand_factor=0,
            sixty_factor=0,
            day_factor=1,
        )
        MINUTE = TimeUnit(
            name="minutes",
            regexp=compile_units_regex_pattern(_MINUTE_STR_UNITS, re.IGNORECASE),
            thousand_factor=0,
            sixty_factor=1,
            day_factor=1,
        )
        SECOND = TimeUnit(
            name="seconds",
            regexp=compile_units_regex_pattern(_SEC_STR_UNITS, re.IGNORECASE),
            thousand_factor=0,
            sixty_factor=2,
            day_factor=1,
        )
        MILLISECOND = TimeUnit(
            name="milliseconds",
            regexp=compile_units_regex_pattern(_MSEC_STR_UNITS, re.IGNORECASE),
            thousand_factor=1,
            sixty_factor=2,
            day_factor=1,
        )
        MICROSECOND = TimeUnit(
            name="microseconds",
            regexp=compile_units_regex_pattern(_USEC_STR_UNITS, re.IGNORECASE),
            thousand_factor=2,
            sixty_factor=2,
            day_factor=1,
        )

    _TEXT_UNITS: Final[TextUnitsMap] = OrderedDict(
        {
            Unit.DAY: _DAY_STR_UNITS,
            Unit.HOUR: _HOUR_STR_UNITS,
            Unit.MINUTE: _MINUTE_STR_UNITS,
            Unit.SECOND: _SEC_STR_UNITS,
            Unit.MILLISECOND: _MSEC_STR_UNITS,
            Unit.MICROSECOND: _USEC_STR_UNITS,
        }
    )

    @classmethod
    def get_text_units(cls) -> TextUnitsMap:
        return cls._TEXT_UNITS

    @property
    def days(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.DAY))

    @property
    def hours(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.HOUR))

    @property
    def minutes(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.MINUTE))

    @property
    def seconds(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.SECOND))

    @property
    def milliseconds(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.MILLISECOND))

    @property
    def microseconds(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.MICROSECOND))

    @property
    def _text_units(self) -> TextUnitsMap:
        return self._TEXT_UNITS

    @property
    def _units(self) -> List[SupportsUnit]:
        return [
            self.Unit.DAY,
            self.Unit.HOUR,
            self.Unit.MINUTE,
            self.Unit.SECOND,
            self.Unit.MILLISECOND,
            self.Unit.MICROSECOND,
        ]

    def __init__(
        self, readable_value: str, default_unit: Union[str, SupportsUnit, None] = None
    ) -> None:
        values = re.findall(r"\d+\s*[a-zA-Z]+", readable_value)
        if len(values) <= 1:
            super().__init__(readable_value, default_unit)
            return

        t = _parse(readable_value, default_unit)
        self._default_unit = t._default_unit
        self._number = t._number
        self._from_unit = t._from_unit

        assert self._default_unit

    def __eq__(self, other) -> bool:
        return self.microseconds == other.microseconds

    def __ne__(self, other) -> bool:
        return self.microseconds != other.microseconds

    def __lt__(self, other) -> bool:
        return self.microseconds < other.microseconds

    def __le__(self, other) -> bool:
        return self.microseconds <= other.microseconds

    def __gt__(self, other) -> bool:
        return self.microseconds > other.microseconds

    def __ge__(self, other) -> bool:
        return self.microseconds >= other.microseconds

    def __add__(self, other: "Time") -> "Time":
        number = self._number + Decimal(other.get_as(self._from_unit))
        return Time(str(number), default_unit=self._from_unit)

    def validate(self, min_value=None, max_value=None) -> None:
        if min_value is not None:
            if not isinstance(min_value, Time):
                min_value = Time(min_value)

            if self < min_value:
                raise ParameterError(
                    "time value is too low",
                    expected=f"greater than or equal to {min_value}",
                    value=self,
                )

        if max_value is not None:
            if not isinstance(max_value, Time):
                max_value = Time(max_value)

            if self > max_value:
                raise ParameterError(
                    "time value is too high",
                    expected=f"less than or equal to {max_value}",
                    value=self,
                )

    def get_as(self, unit: Union[str, SupportsUnit]) -> float:
        unit_maps: Dict[SupportsUnit, str] = {
            self.Unit.DAY: "days",
            self.Unit.HOUR: "hours",
            self.Unit.MINUTE: "minutes",
            self.Unit.SECOND: "seconds",
            self.Unit.MILLISECOND: "milliseconds",
            self.Unit.MICROSECOND: "microseconds",
        }
        norm_unit = self._normalize_unit(unit)
        assert norm_unit

        return getattr(self, unit_maps[norm_unit])

    def to_humanreadable(self, style: HumanReadableStyle = "full") -> str:
        def _to_unit_str(unit: SupportsUnit, style: str) -> str:
            if style in ("short", "abbr"):
                return unit.name[0]

            if style == "full":
                return f" {unit.name}"

            return unit.name

        items: List[str] = []

        if self.days >= 1:
            items.append(f"{int(self.days):d}{_to_unit_str(self.Unit.DAY, style)}")
        if self.hours % 24 >= 1:
            items.append(f"{int(self.hours) % 24:d}{_to_unit_str(self.Unit.HOUR, style)}")
        if self.minutes % 60 >= 1:
            items.append(f"{int(self.minutes) % 60:d}{_to_unit_str(self.Unit.MINUTE, style)}")
        if self.seconds % 60 >= 1:
            items.append(f"{int(self.seconds) % 60:d}{_to_unit_str(self.Unit.SECOND, style)}")
        if self.milliseconds % 1000 >= 1:
            items.append(
                f"{int(self.milliseconds) % 1000:d}{_to_unit_str(self.Unit.MILLISECOND, style)}"
            )
        if self.microseconds % 1000 >= 1:
            items.append(
                f"{int(self.microseconds) % 1000:d}{_to_unit_str(self.Unit.MICROSECOND, style)}"
            )

        if not items:
            assert self._default_unit
            return f"0 {self._default_unit.name}"

        return " ".join(items)

    def _normalize_unit(self, unit: Union[str, SupportsUnit, None]) -> Optional[SupportsUnit]:
        if isinstance(unit, TimeUnit):
            return unit

        return super()._normalize_unit(unit)

    def __calc_coef(self, from_unit: SupportsUnit, to_unit: TimeUnit) -> Decimal:
        from_unit_tu = cast(TimeUnit, from_unit)
        thousand_coef = Decimal(1000 ** (to_unit.thousand_factor - from_unit_tu.thousand_factor))
        sixty_coef = Decimal(60 ** (to_unit.sixty_factor - from_unit_tu.sixty_factor))
        day_coef = Decimal(24 ** (to_unit.day_factor - from_unit_tu.day_factor))

        return day_coef * sixty_coef * thousand_coef


def _parse(value: Union[str, Time], default_unit: Union[str, SupportsUnit, None] = None) -> Time:
    if isinstance(value, Time):
        return value

    sum: Optional[Time] = None

    for item in reversed(re.findall(r"\d+\s*[a-zA-Z]+", value)):
        t = Time(item, default_unit=default_unit)
        if sum is None:
            sum = t
        else:
            sum += t

    assert sum is not None

    return sum
