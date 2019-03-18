# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, division, unicode_literals

import abc
import re
from decimal import Decimal

import six
from typepy import RealNumber

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
        self._readable_value = readable_value
        self._number = None
        self._from_unit = None
        self._default_unit = default_unit
        self.__preprocess()

    def __repr__(self):
        items = [six.text_type(self._number)]
        if self._from_unit.name:
            items.append(self._from_unit.name)

        return " ".join(items)

    def __split_unit(self):
        if RealNumber(self._readable_value).is_type():
            if self._default_unit is None:
                raise UnitNotFoundError(
                    "unit not found",
                    value=self._readable_value,
                    available_units=_get_unit_msg(self._text_units),
                )

            return (self._readable_value, self._default_unit)

        for unit in self._units:
            try:
                if unit.regexp.search(self._readable_value):
                    number = unit.regexp.split(self._readable_value)[0]
                    if not RealNumber(number).is_type():
                        continue

                    return (number, unit)
            except TypeError:
                continue

        return (self._readable_value, self._default_unit)

    def __preprocess(self):
        if self._readable_value is None:
            raise TypeError("readable_value must be a string")

        readable_num, self._from_unit = self.__split_unit()
        if readable_num is not None:
            self._number = self.__to_number(readable_num)

        if self._from_unit is None:
            raise UnitNotFoundError(
                "unit not found",
                value=self._readable_value,
                available_units=_get_unit_msg(self._text_units),
            )

    def __to_number(self, readable_num):
        match = _RE_NUMBER.search(readable_num)
        if not match:
            raise ParameterError(
                "human-readable value should only include a number", value=readable_num
            )

        return Decimal(match.group())
