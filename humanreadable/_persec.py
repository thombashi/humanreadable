"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from collections import OrderedDict
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, NamedTuple, Optional, Pattern, Union, cast

from ._base import HumanReadableValue
from ._common import compile_units_regex_pattern
from ._types import HumanReadableStyle, SupportsUnit, TextUnitsMap, Units


try:
    from typing import Final
except ImportError:
    # typing.Final and typing.Protocol are only available starting from Python 3.8.
    from ._typing import Final  # type: ignore


_BPS_PATTERN: Final[str] = r"bits?(/|\s?per\s?)(s|sec|second)"

_BPS_STR_UNITS: Final[Units] = ("bps", _BPS_PATTERN)
_KBPS_STR_UNITS: Final[Units] = ("[kK]bps", "[kK]" + _BPS_PATTERN)
_KIBPS_STR_UNITS: Final[Units] = ("[kK]ibps", "[kK]i" + _BPS_PATTERN)
_MBPS_STR_UNITS: Final[Units] = ("[mM]bps", "[mM]" + _BPS_PATTERN)
_MIBPS_STR_UNITS: Final[Units] = ("[mM]ibps", "[mM]i" + _BPS_PATTERN)
_GBPS_STR_UNITS: Final[Units] = ("[gG]bps", "[gG]" + _BPS_PATTERN)
_GIBPS_STR_UNITS: Final[Units] = ("[gG]ibps", "[gG]i" + _BPS_PATTERN)
_TBPS_STR_UNITS: Final[Units] = ("[tT]bps", "[tT]" + _BPS_PATTERN)
_TIBPS_STR_UNITS: Final[Units] = ("[tT]ibps", "[tT]i" + _BPS_PATTERN)


class ByteUnit(NamedTuple):
    name: str
    regexp: Pattern[str]
    k_size: int
    factor: int
    full_unit_expr: str


class BitsPerSecond(HumanReadableValue):
    """
    String converter that human-readable byte size to a number.

    Args:
        readable_value (str):
            Human readable size (bit per second). e.g. 256 Mbps
    """

    @dataclass(frozen=True)
    class Unit:
        BPS = ByteUnit(
            name="bps",
            regexp=compile_units_regex_pattern(_BPS_STR_UNITS),
            k_size=1000,
            factor=0,
            full_unit_expr="bits per second",
        )
        KBPS = ByteUnit(
            name="Kbps",
            regexp=compile_units_regex_pattern(_KBPS_STR_UNITS),
            k_size=1000,
            factor=1,
            full_unit_expr="kilobits per second",
        )
        KIBPS = ByteUnit(
            name="Kibps",
            regexp=compile_units_regex_pattern(_KIBPS_STR_UNITS),
            k_size=1024,
            factor=1,
            full_unit_expr="kibibits per second",
        )
        MBPS = ByteUnit(
            name="Mbps",
            regexp=compile_units_regex_pattern(_MBPS_STR_UNITS),
            k_size=1000,
            factor=2,
            full_unit_expr="megabits per second",
        )
        MIBPS = ByteUnit(
            name="Mibps",
            regexp=compile_units_regex_pattern(_MIBPS_STR_UNITS),
            k_size=1024,
            factor=2,
            full_unit_expr="mebibits per second",
        )
        GBPS = ByteUnit(
            name="Gbps",
            regexp=compile_units_regex_pattern(_GBPS_STR_UNITS),
            k_size=1000,
            factor=3,
            full_unit_expr="gigabits per second",
        )
        GIBPS = ByteUnit(
            name="Gibps",
            regexp=compile_units_regex_pattern(_GIBPS_STR_UNITS),
            k_size=1024,
            factor=3,
            full_unit_expr="gibibits per second",
        )
        TBPS = ByteUnit(
            name="Tbps",
            regexp=compile_units_regex_pattern(_TBPS_STR_UNITS),
            k_size=1000,
            factor=4,
            full_unit_expr="terabits per second",
        )
        TIBPS = ByteUnit(
            name="Tibps",
            regexp=compile_units_regex_pattern(_TIBPS_STR_UNITS),
            k_size=1024,
            factor=4,
            full_unit_expr="tebibits per second",
        )

    _TEXT_UNITS: Final[TextUnitsMap] = OrderedDict(
        {
            Unit.KBPS: _KBPS_STR_UNITS,
            Unit.KIBPS: _KIBPS_STR_UNITS,
            Unit.MBPS: _MBPS_STR_UNITS,
            Unit.MIBPS: _MIBPS_STR_UNITS,
            Unit.GBPS: _GBPS_STR_UNITS,
            Unit.GIBPS: _GIBPS_STR_UNITS,
            Unit.TBPS: _TBPS_STR_UNITS,
            Unit.TIBPS: _TIBPS_STR_UNITS,
            Unit.BPS: _BPS_STR_UNITS,
        }
    )

    @classmethod
    def get_text_units(cls) -> TextUnitsMap:
        return cls._TEXT_UNITS

    @property
    def _text_units(self) -> TextUnitsMap:
        return self._TEXT_UNITS

    @property
    def _units(self) -> List[SupportsUnit]:
        return [
            self.Unit.BPS,
            self.Unit.KBPS,
            self.Unit.KIBPS,
            self.Unit.MBPS,
            self.Unit.MIBPS,
            self.Unit.GBPS,
            self.Unit.GIBPS,
            self.Unit.TBPS,
            self.Unit.TIBPS,
        ]

    @property
    def bps(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.BPS))

    @property
    def byte_per_sec(self) -> float:
        return self.bps / 8

    @property
    def kilo_bps(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.KBPS))

    @property
    def kilo_byte_per_sec(self) -> float:
        return self.kilo_bps / 8

    @property
    def kibi_bps(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.KIBPS))

    @property
    def kibi_byte_per_sec(self) -> float:
        return self.kibi_bps / 8

    @property
    def mega_bps(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.MBPS))

    @property
    def mega_byte_per_sec(self) -> float:
        return self.mega_bps / 8

    @property
    def mebi_bps(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.MIBPS))

    @property
    def mebi_byte_per_sec(self) -> float:
        return self.mebi_bps / 8

    @property
    def giga_bps(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.GBPS))

    @property
    def giga_byte_per_sec(self) -> float:
        return self.giga_bps / 8

    @property
    def gibi_bps(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.GIBPS))

    @property
    def gibi_byte_per_sec(self) -> float:
        return self.gibi_bps / 8

    @property
    def tera_bps(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.TBPS))

    @property
    def tera_byte_per_sec(self) -> float:
        return self.tera_bps / 8

    @property
    def tebi_bps(self) -> float:
        return float(self._number * self.__calc_coef(self._from_unit, self.Unit.TIBPS))

    @property
    def tebi_byte_per_sec(self) -> float:
        return self.tebi_bps / 8

    def __eq__(self, other) -> bool:
        return self.bps == other.bps

    def __ne__(self, other) -> bool:
        return self.bps != other.bps

    def __lt__(self, other) -> bool:
        return self.bps < other.bps

    def __le__(self, other) -> bool:
        return self.bps <= other.bps

    def __gt__(self, other) -> bool:
        return self.bps > other.bps

    def __ge__(self, other) -> bool:
        return self.bps >= other.bps

    def __add__(self, other: "BitsPerSecond") -> "BitsPerSecond":
        number = self._number + Decimal(other.get_as(self._from_unit))
        return BitsPerSecond(str(number), default_unit=self._from_unit)

    def get_as(self, unit: Union[str, SupportsUnit]) -> float:
        unit_maps: Dict[SupportsUnit, str] = {
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
        norm_unit = self._normalize_unit(unit)
        assert norm_unit

        return getattr(self, unit_maps[norm_unit])

    def _normalize_unit(self, unit: Union[str, SupportsUnit, None]) -> Optional[SupportsUnit]:
        if isinstance(unit, ByteUnit):
            return unit

        return super()._normalize_unit(unit)

    def __calc_coef(self, from_unit: SupportsUnit, to_unit: ByteUnit) -> Decimal:
        from_unit_bu = cast(ByteUnit, from_unit)
        if from_unit_bu.k_size == to_unit.k_size:
            return Decimal(from_unit_bu.k_size ** (from_unit_bu.factor - to_unit.factor))

        return Decimal(from_unit_bu.k_size**from_unit_bu.factor) / Decimal(
            to_unit.k_size**to_unit.factor
        )

    def __filter_units_by_k(
        self, units: List[SupportsUnit], from_unit: SupportsUnit
    ) -> List[SupportsUnit]:
        from_unit_bu = cast(ByteUnit, from_unit)
        return [u for u in units if cast(ByteUnit, u).k_size == from_unit_bu.k_size]

    def to_humanreadable(self, style: HumanReadableStyle = "full") -> str:
        def _to_unit_str(unit, style: str) -> str:
            if style == "full":
                return f" {unit.full_unit_expr}"

            return f" {unit.name}"

        filtered_units = self.__filter_units_by_k(self._units, self._from_unit)
        for unit in reversed(sorted(filtered_units, key=lambda u: cast(ByteUnit, u).factor)):
            number = self.get_as(unit)
            if number < 1:
                continue

            return f"{number:.1f}{_to_unit_str(unit, style)}"

        raise ValueError("unit not found")


BitPerSecond = BitsPerSecond
