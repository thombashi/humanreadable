# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import division, print_function, unicode_literals

import sys
from decimal import Decimal

import pytest
from six import text_type

from humanreadable import BitPerSecond, ParameterError, UnitNotFoundError


KILO = Decimal(1000 ** 1)
MEGA = Decimal(1000 ** 2)
GIGA = Decimal(1000 ** 3)
TERA = Decimal(1000 ** 4)
KIBI = Decimal(1024 ** 1)
MEBI = Decimal(1024 ** 2)
GIBI = Decimal(1024 ** 3)
TEBI = Decimal(1024 ** 4)


class Test_BitPerSecond_constructor(object):
    @pytest.mark.parametrize(
        ["value", "exception"],
        [
            ["10", UnitNotFoundError],
            [None, TypeError],
            [True, TypeError],
            [float("nan"), TypeError],
            ["", ParameterError],
            ["a", ParameterError],
            ["1k0 ", ParameterError],
            ["10kb", ParameterError],
            ["-2m", ParameterError],
            ["2m", ParameterError],
            ["2ms", ParameterError],
            ["two Gbps", ParameterError],
        ],
    )
    def test_exception(self, value, exception):
        with pytest.raises(exception):
            BitPerSecond(value).bps


class Test_BitPerSecond_repr(object):
    @pytest.mark.parametrize(["value", "expected"], [["2 Kbps", "2 Kbps"]])
    def test_exception(self, value, expected):
        assert text_type(BitPerSecond(value)) == expected


class Test_eq(object):
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [["5 bps", "5.0 bit/s", True], ["60000bps", "60 Kbps", True], ["1 bps", "2 bps", False]],
    )
    def test_exception(self, lhs, rhs, expected):
        assert (BitPerSecond(lhs) == BitPerSecond(rhs)) is expected


class Test_less_than(object):
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [["20 Gbps", "32Gbps", True], ["20 Gibps", "32Gbps", True], ["40 Gibps", "32Gbps", False]],
    )
    def test_exception(self, lhs, rhs, expected):
        lhs = BitPerSecond(lhs)
        rhs = BitPerSecond(rhs)

        print("lhs={}Mbps, rhs={}Mbps".format(lhs.mega_bps, rhs.mega_bps), file=sys.stderr)

        assert (lhs < rhs) is expected
        assert (lhs <= rhs) is expected


class Test_BitPerSecond_bps(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["2bps", 2],
            ["2 bps", 2],
            ["2kbps", 2 * 1000 ** 1],
            ["2 Kbps", 2 * 1000 ** 1],
            ["+1.25Kbps", 1.25 * 1000 ** 1],
            ["2.5 Kibit/s", 2.5 * 1024 ** 1],
            ["2Mbps", 2 * 1000 ** 2],
            ["2 Mbps", 2 * 1000 ** 2],
            ["2.5 Mibit/s", 2.5 * 1024 ** 2],
            ["2Gbps", 2 * 1000 ** 3],
            ["2 Gbps", 2 * 1000 ** 3],
            ["2.5 Gibit/s", 2.5 * 1024 ** 3],
            ["2Tbps", 2 * 1000 ** 4],
            ["2 Tbps", 2 * 1000 ** 4],
            ["2.5 Tibit/s", 2.5 * 1024 ** 4],
        ],
    )
    def test_normal(self, value, expected):
        value = BitPerSecond(value)
        assert value.bps == expected
        assert value.byte_per_sec == value.bps / 8


class Test_BitPerSecond_kbps(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["2bps", 2 * 1000 ** -1],
            ["2Kbps", 2 * 1000 ** 0],
            ["2Mbps", 2 * 1000 ** 1],
            ["2Gbps", 2 * 1000 ** 2],
            ["2Tbps", 2 * 1000 ** 3],
            ["2Kibps", 2 * KIBI / KILO],
            ["2Mibps", 2 * MEBI / KILO],
            ["2Gibps", 2 * GIBI / KILO],
            ["2Tibps", 2 * TEBI / KILO],
        ],
    )
    def test_normal_kilo(self, value, expected):
        value = BitPerSecond(value)
        assert value.kilo_bps == float(expected)
        assert value.kilo_byte_per_sec == value.kilo_bps / 8

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["2Kbps", 2 * KILO / KIBI],
            ["2Mbps", 2 * MEGA / KIBI],
            ["2Gbps", 2 * GIGA / KIBI],
            ["2Tbps", 2 * TERA / KIBI],
            ["2Kibps", 2 * 1024 ** 0],
            ["2Mibps", 2 * 1024 ** 1],
            ["2Gibps", 2 * 1024 ** 2],
            ["2Tibps", 2 * 1024 ** 3],
        ],
    )
    def test_normal_kibi(self, value, expected):
        value = BitPerSecond(value)
        assert value.kibi_bps == expected
        assert value.kibi_byte_per_sec == value.kibi_bps / 8


class Test_BitPerSecond_mbps(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["2bps", 2 * 1000 ** -2],
            ["2Kbps", 2 * 1000 ** -1],
            ["2Mbps", 2 * 1000 ** 0],
            ["2Gbps", 2 * 1000 ** 1],
            ["2Tbps", 2 * 1000 ** 2],
            ["2Kibps", 2 * KIBI / MEGA],
            ["2Mibps", 2 * MEBI / MEGA],
            ["2Gibps", 2 * GIBI / MEGA],
            ["2Tibps", 2 * TEBI / MEGA],
        ],
    )
    def test_normal_mega(self, value, expected):
        value = BitPerSecond(value)
        assert value.mega_bps == float(expected)
        assert value.mega_byte_per_sec == value.mega_bps / 8

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["2Kbps", 2 * KILO / MEBI],
            ["2Mbps", 2 * MEGA / MEBI],
            ["2Gbps", 2 * GIGA / MEBI],
            ["2Tbps", 2 * TERA / MEBI],
            ["2Kibps", 2 * 1024 ** -1],
            ["2Mibps", 2 * 1024 ** 0],
            ["2Gibps", 2 * 1024 ** 1],
            ["2Tibps", 2 * 1024 ** 2],
        ],
    )
    def test_normal_mebi(self, value, expected):
        value = BitPerSecond(value)
        assert value.mebi_bps == expected
        assert value.mebi_byte_per_sec == value.mebi_bps / 8


class Test_BitPerSecond_gbps(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["2bps", 2 * 1000 ** -3],
            ["2Kbps", 2 * 1000 ** -2],
            ["2Mbps", 2 * 1000 ** -1],
            ["2Gbps", 2 * 1000 ** 0],
            ["2Tbps", 2 * 1000 ** 1],
            ["2Kibps", 2 * KIBI / GIGA],
            ["2Mibps", 2 * MEBI / GIGA],
            ["2Gibps", 2 * GIBI / GIGA],
            ["2Tibps", 2 * TEBI / GIGA],
        ],
    )
    def test_normal_giga(self, value, expected):
        value = BitPerSecond(value)
        assert value.giga_bps == float(expected)
        assert value.giga_byte_per_sec == value.giga_bps / 8

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["2Kbps", 2 * KILO / GIBI],
            ["2Mbps", 2 * MEGA / GIBI],
            ["2Gbps", 2 * GIGA / GIBI],
            ["2Tbps", 2 * TERA / GIBI],
            ["2Kibps", 2 * 1024 ** -2],
            ["2Mibps", 2 * 1024 ** -1],
            ["2Gibps", 2 * 1024 ** 0],
            ["2Tibps", 2 * 1024 ** 1],
        ],
    )
    def test_normal_gibi(self, value, expected):
        value = BitPerSecond(value)
        assert value.gibi_bps == expected
        assert value.gibi_byte_per_sec == value.gibi_bps / 8


class Test_BitPerSecond_tbps(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["2bps", 2 * 1000 ** -4],
            ["2Kbps", 2 * 1000 ** -3],
            ["2Mbps", 2 * 1000 ** -2],
            ["2Gbps", 2 * 1000 ** -1],
            ["2Tbps", 2 * 1000 ** 0],
            ["2Kibps", 2 * KIBI / TERA],
            ["2Mibps", 2 * MEBI / TERA],
            ["2Gibps", 2 * GIBI / TERA],
            ["2Tibps", 2 * TEBI / TERA],
        ],
    )
    def test_normal_tera(self, value, expected):
        value = BitPerSecond(value)
        assert value.tera_bps == float(expected)
        assert value.tera_byte_per_sec == value.tera_bps / 8

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["2Kbps", 2 * KILO / TEBI],
            ["2Mbps", 2 * MEGA / TEBI],
            ["2Gbps", 2 * GIGA / TEBI],
            ["2Tbps", 2 * TERA / TEBI],
            ["2Kibps", 2 * 1024 ** -3],
            ["2Mibps", 2 * 1024 ** -2],
            ["2Gibps", 2 * 1024 ** -1],
            ["2Tibps", 2 * 1024 ** 0],
        ],
    )
    def test_normal_gibi(self, value, expected):
        value = BitPerSecond(value)
        assert value.tebi_bps == expected
        assert value.tebi_byte_per_sec == value.tebi_bps / 8


class Test_Time_get_as(object):
    @pytest.mark.parametrize(
        ["value", "default_unit", "expected"],
        [
            ["2bps", BitPerSecond.Unit.BPS, 2],
            ["2Kbps", BitPerSecond.Unit.KBPS, 2],
            ["2Kibps", BitPerSecond.Unit.KIBPS, 2],
            ["2Mbps", BitPerSecond.Unit.MBPS, 2],
            ["2Mibps", BitPerSecond.Unit.MIBPS, 2],
            ["2Gbps", BitPerSecond.Unit.GBPS, 2],
            ["2Gibps", BitPerSecond.Unit.GIBPS, 2],
            ["2Tbps", BitPerSecond.Unit.TBPS, 2],
            ["2Tibps", BitPerSecond.Unit.TIBPS, 2],
        ],
    )
    def test_normal_default_unit(self, value, default_unit, expected):
        assert BitPerSecond(value, default_unit=default_unit).get_as(default_unit) == expected
