# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, division, unicode_literals

import abc
import re
from decimal import Decimal

import six
from typepy import RealNumber, String

from .error import ParameterError, UnitNotFoundError


_BASE_ATTRS = ("name", "regexp")
_RE_NUMBER = re.compile(r"^[-\+]?[0-9\.]+$")


def _get_unit_msg(text_units):
    return ", ".join([", ".join(values) for values in text_units.values()])


@six.add_metaclass(abc.ABCMeta)
class HumanReadableValue(object):
    @abc.abstractproperty
    def _text_units(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def _units(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def get_as(self, unit):  # pragma: no cover
        pass

    def __init__(self, readable_value, default_unit=None):
        self._default_unit = default_unit
        self._number, self._from_unit = self.__preprocess(readable_value)

    def __repr__(self):
        items = [six.text_type(self._number)]
        if self._from_unit.name:
            items.append(self._from_unit.name)

        return " ".join(items)

    def __split_unit(self, readable_value):
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
            "unit not found", value=readable_value, available_units=_get_unit_msg(self._text_units),
        )

    def __preprocess(self, readable_value):
        if readable_value is None:
            raise TypeError("readable_value must be a string")

        number, from_unit = self.__split_unit(readable_value)
        if number is not None:
            number = self.__to_number(number)

        if from_unit is None:
            raise UnitNotFoundError(
                "unit not found",
                value=readable_value,
                available_units=_get_unit_msg(self._text_units),
            )

        return (number, from_unit)

    def __to_number(self, readable_num):
        match = _RE_NUMBER.search(readable_num)
        if not match:
            raise ParameterError(
                "human-readable value should only include a number", value=readable_num
            )

        return Decimal(match.group())
