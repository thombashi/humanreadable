# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, division, unicode_literals

import re
from collections import OrderedDict, namedtuple
from decimal import Decimal

from ._base import _BASE_ATTRS, HumanReadableValue
from .error import ParameterError


_PATTERN_TEMPLETE = r"\s?{}$"

_DAY_STR_UNITS = ["d", "day", "days"]
_HOUR_STR_UNITS = ["h", "hour", "hours"]
_MINUTE_STR_UNITS = ["m", "min", "mins", "minute", "minutes"]
_SEC_STR_UNITS = ["s", "sec", "secs", "second", "seconds"]
_MSEC_STR_UNITS = ["ms", "msec", "msecs", "millisecond", "milliseconds"]
_USEC_STR_UNITS = ["us", "usec", "usecs", "microsecond", "microseconds"]


TimeUnit = namedtuple(
    "TimeUnit", "{} thousand_factor sixty_factor day_factor".format(" ".join(_BASE_ATTRS))
)


class Time(HumanReadableValue):
    class Unit(object):
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

    _TEXT_UNITS = OrderedDict(
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
    def get_text_units(cls):
        return cls._TEXT_UNITS

    @property
    def days(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.DAY))

    @property
    def hours(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.HOUR))

    @property
    def minutes(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.MINUTE))

    @property
    def seconds(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.SECOND))

    @property
    def milliseconds(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.MILLISECOND))

    @property
    def microseconds(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.MICROSECOND))

    @property
    def _text_units(self):
        return self._TEXT_UNITS

    @property
    def _units(self):
        return (
            self.Unit.DAY,
            self.Unit.HOUR,
            self.Unit.MINUTE,
            self.Unit.SECOND,
            self.Unit.MILLISECOND,
            self.Unit.MICROSECOND,
        )

    def __eq__(self, other):
        return self.microseconds == other.microseconds

    def __ne__(self, other):
        return self.microseconds != other.microseconds

    def __lt__(self, other):
        return self.microseconds < other.microseconds

    def __le__(self, other):
        return self.microseconds <= other.microseconds

    def __gt__(self, other):
        return self.microseconds > other.microseconds

    def __ge__(self, other):
        return self.microseconds >= other.microseconds

    def validate(self, min_value=None, max_value=None):
        if min_value is not None:
            if not isinstance(min_value, Time):
                min_value = Time(min_value)

            if self < min_value:
                raise ParameterError(
                    "time value is too low",
                    expected="greater than or equal to {}".format(min_value),
                    value=self,
                )

        if max_value is not None:
            if not isinstance(max_value, Time):
                max_value = Time(max_value)

            if self > max_value:
                raise ParameterError(
                    "time value is too high",
                    expected="less than or equal to {}".format(max_value),
                    value=self,
                )

    def get_as(self, unit):
        unit_maps = {
            self.Unit.DAY: "days",
            self.Unit.HOUR: "hours",
            self.Unit.MINUTE: "minutes",
            self.Unit.SECOND: "seconds",
            self.Unit.MILLISECOND: "milliseconds",
            self.Unit.MICROSECOND: "microseconds",
        }

        return getattr(self, unit_maps[unit])

    def __calc_coef(self, from_unit, to_unit):
        thousand_coef = Decimal(1000 ** (to_unit.thousand_factor - from_unit.thousand_factor))
        sixty_coef = Decimal(60 ** (to_unit.sixty_factor - from_unit.sixty_factor))
        day_coef = Decimal(24 ** (to_unit.day_factor - from_unit.day_factor))

        return day_coef * sixty_coef * thousand_coef
