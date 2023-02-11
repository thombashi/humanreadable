"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import re
from collections import OrderedDict
from decimal import Decimal
from typing import Dict, List, NamedTuple, Optional, Pattern, Union, cast

from ._base import HumanReadableValue, SupportsUnit, TextUnitsMap
from .error import ParameterError


_PATTERN_TEMPLETE = r"\s?{}$"

_DAY_STR_UNITS = ["d", "day", "days"]
_HOUR_STR_UNITS = ["h", "hour", "hours"]
_MINUTE_STR_UNITS = ["m", "min", "mins", "minute", "minutes"]
_SEC_STR_UNITS = ["s", "sec", "secs", "second", "seconds"]
_MSEC_STR_UNITS = ["ms", "msec", "msecs", "millisecond", "milliseconds"]
_USEC_STR_UNITS = ["us", "usec", "usecs", "microsecond", "microseconds"]


class TimeUnit(NamedTuple):
    name: str
    regexp: Pattern
    thousand_factor: int
    sixty_factor: int
    day_factor: int


class Time(HumanReadableValue):
    class Unit:
        DAY = TimeUnit(
            name="days",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _DAY_STR_UNITS]), re.IGNORECASE
            ),
            thousand_factor=0,
            sixty_factor=0,
            day_factor=0,
        )
        HOUR = TimeUnit(
            name="hours",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _HOUR_STR_UNITS]),
                re.IGNORECASE,
            ),
            thousand_factor=0,
            sixty_factor=0,
            day_factor=1,
        )
        MINUTE = TimeUnit(
            name="minutes",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _MINUTE_STR_UNITS]),
                re.IGNORECASE,
            ),
            thousand_factor=0,
            sixty_factor=1,
            day_factor=1,
        )
        SECOND = TimeUnit(
            name="seconds",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _SEC_STR_UNITS]), re.IGNORECASE
            ),
            thousand_factor=0,
            sixty_factor=2,
            day_factor=1,
        )
        MILLISECOND = TimeUnit(
            name="milliseconds",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _MSEC_STR_UNITS]),
                re.IGNORECASE,
            ),
            thousand_factor=1,
            sixty_factor=2,
            day_factor=1,
        )
        MICROSECOND = TimeUnit(
            name="microseconds",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _USEC_STR_UNITS]),
                re.IGNORECASE,
            ),
            thousand_factor=2,
            sixty_factor=2,
            day_factor=1,
        )

    _TEXT_UNITS: TextUnitsMap = OrderedDict(
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

    def validate(self, min_value=None, max_value=None):
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
