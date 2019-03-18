# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, division, unicode_literals

import re
from collections import OrderedDict, namedtuple
from decimal import Decimal

from ._base import _BASE_ATTRS, HumanReadableValue


_PATTERN_TEMPLETE = r"\s?{}$"

_BPS_STR_UNITS = ["bps", "bit/s"]
_KBPS_STR_UNITS = ["[kK]bps", "[kK]bit/s"]
_KIBPS_STR_UNITS = ["[kK]ibps", "[kK]ibit/s"]
_MBPS_STR_UNITS = ["[mM]bps", "[mM]bit/s"]
_MIBPS_STR_UNITS = ["[mM]ibps", "[mM]ibit/s"]
_GBPS_STR_UNITS = ["[gG]bps", "[gG]bit/s"]
_GIBPS_STR_UNITS = ["[gG]ibps", "[gG]ibit/s"]
_TBPS_STR_UNITS = ["[tT]bps", "[tT]bit/s"]
_TIBPS_STR_UNITS = ["[tT]ibps", "[tT]ibit/s"]


ByteUnit = namedtuple("ByteUnit", "{} kilo_size factor".format(" ".join(_BASE_ATTRS)))


class BitPerSecond(HumanReadableValue):
    """
    String converter that human-readable byte size to a number.

    Args:
        readable_value (str):
            Human readable size (bit per second). e.g. 256 Mbps
    """

    class Unit(object):
        BPS = ByteUnit(
            name="bps",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _BPS_STR_UNITS])
            ),
            kilo_size=1000,
            factor=0,
        )
        KBPS = ByteUnit(
            name="Kbps",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _KBPS_STR_UNITS])
            ),
            kilo_size=1000,
            factor=1,
        )
        KIBPS = ByteUnit(
            name="Kibps",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _KIBPS_STR_UNITS])
            ),
            kilo_size=1024,
            factor=1,
        )
        MBPS = ByteUnit(
            name="Mbps",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _MBPS_STR_UNITS])
            ),
            kilo_size=1000,
            factor=2,
        )
        MIBPS = ByteUnit(
            name="Mibps",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _MIBPS_STR_UNITS])
            ),
            kilo_size=1024,
            factor=2,
        )
        GBPS = ByteUnit(
            name="Gbps",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _GBPS_STR_UNITS])
            ),
            kilo_size=1000,
            factor=3,
        )
        GIBPS = ByteUnit(
            name="Gibps",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _GIBPS_STR_UNITS])
            ),
            kilo_size=1024,
            factor=3,
        )
        TBPS = ByteUnit(
            name="Tbps",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _TBPS_STR_UNITS])
            ),
            kilo_size=1000,
            factor=4,
        )
        TIBPS = ByteUnit(
            name="Tibps",
            regexp=re.compile(
                "|".join([_PATTERN_TEMPLETE.format(unit) for unit in _TIBPS_STR_UNITS])
            ),
            kilo_size=1024,
            factor=4,
        )

    _TEXT_UNITS = OrderedDict(
        {
            Unit.BPS: _BPS_STR_UNITS,
            Unit.KBPS: _KBPS_STR_UNITS,
            Unit.KIBPS: _KIBPS_STR_UNITS,
            Unit.MBPS: _MBPS_STR_UNITS,
            Unit.MIBPS: _MIBPS_STR_UNITS,
            Unit.GBPS: _GBPS_STR_UNITS,
            Unit.GIBPS: _GIBPS_STR_UNITS,
            Unit.TBPS: _TBPS_STR_UNITS,
            Unit.TIBPS: _TIBPS_STR_UNITS,
        }
    )

    @classmethod
    def get_text_units(cls):
        return cls._TEXT_UNITS

    @property
    def _text_units(self):
        return self._TEXT_UNITS

    @property
    def _units(self):
        return (
            self.Unit.BPS,
            self.Unit.KBPS,
            self.Unit.KIBPS,
            self.Unit.MBPS,
            self.Unit.MIBPS,
            self.Unit.GBPS,
            self.Unit.GIBPS,
            self.Unit.TBPS,
            self.Unit.TIBPS,
        )

    @property
    def bps(self):
        return int(self._number * self.__calc_coef(self._from_unit, self.Unit.BPS))

    @property
    def byte_per_sec(self):
        return self.bps / 8

    @property
    def kilo_bps(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.KBPS))

    @property
    def kilo_byte_per_sec(self):
        return self.kilo_bps / 8

    @property
    def kibi_bps(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.KIBPS))

    @property
    def kibi_byte_per_sec(self):
        return self.kibi_bps / 8

    @property
    def mega_bps(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.MBPS))

    @property
    def mega_byte_per_sec(self):
        return self.mega_bps / 8

    @property
    def mebi_bps(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.MIBPS))

    @property
    def mebi_byte_per_sec(self):
        return self.mebi_bps / 8

    @property
    def giga_bps(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.GBPS))

    @property
    def giga_byte_per_sec(self):
        return self.giga_bps / 8

    @property
    def gibi_bps(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.GIBPS))

    @property
    def gibi_byte_per_sec(self):
        return self.gibi_bps / 8

    @property
    def tera_bps(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.TBPS))

    @property
    def tera_byte_per_sec(self):
        return self.tera_bps / 8

    @property
    def tebi_bps(self):
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.TIBPS))

    @property
    def tebi_byte_per_sec(self):
        return self.tebi_bps / 8

    def __eq__(self, other):
        return self.bps == other.bps

    def __ne__(self, other):
        return self.bps != other.bps

    def __lt__(self, other):
        return self.bps < other.bps

    def __le__(self, other):
        return self.bps <= other.bps

    def __gt__(self, other):
        return self.bps > other.bps

    def __ge__(self, other):
        return self.bps >= other.bps

    def get_as(self, unit):
        unit_maps = {
            self.Unit.BPS: "bps",
            self.Unit.KBPS: "kilo_bps",
            self.Unit.KIBPS: "kibi_bps",
            self.Unit.MBPS: "mega_bps",
            self.Unit.MIBPS: "mebi_bps",
            self.Unit.GBPS: "giga_bps",
            self.Unit.GIBPS: "gibi_bps",
            self.Unit.TBPS: "tera_bps",
            self.Unit.TIBPS: "tebi_bps",
        }

        return getattr(self, unit_maps[unit])

    def __calc_coef(self, from_unit, to_unit):
        if from_unit.kilo_size == to_unit.kilo_size:
            return Decimal(from_unit.kilo_size ** (from_unit.factor - to_unit.factor))

        return Decimal(from_unit.kilo_size ** from_unit.factor) / Decimal(
            to_unit.kilo_size ** to_unit.factor
        )
