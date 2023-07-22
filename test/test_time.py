"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

from humanreadable import ParameterError, Time


class Test_Time_constructor:
    @pytest.mark.parametrize(
        ["value", "exception"],
        [
            [None, TypeError],
            [True, TypeError],
            [float("nan"), TypeError],
            ["", ParameterError],
            ["a", ParameterError],
            ["1k0 ", ParameterError],
            ["10kb", ParameterError],
            ["2micro", ParameterError],
            ["two secs", ParameterError],
        ],
    )
    def test_exception(self, value, exception):
        with pytest.raises(exception):
            Time(value)


class Test_Time_repr:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["5seconds", "5 seconds"],
        ],
    )
    def test_exception(self, value, expected):
        assert str(Time(value)) == expected


class Test_Time_eq:
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [
            ["5seconds", "5.0 sec", True],
            ["60000ms", "1min", True],
            ["1 sec", "2 sec", False],
        ],
    )
    def test_exception(self, lhs, rhs, expected):
        assert (Time(lhs) == Time(rhs)) is expected


class Test_Time_add:
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [
            ["1s", "1seconds", "2 sec"],
            ["1s", "1000ms", "2 sec"],
        ],
    )
    def test_exception(self, lhs, rhs, expected):
        assert (Time(lhs) + Time(rhs)) == Time(expected)


class Test_Time_days:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["12hours", 0.5],
            ["1day", 1],
            ["3 days", 3],
        ],
    )
    def test_normal(self, value, expected):
        assert Time(value).days == expected


class Test_Time_hours:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["3600 seconds", 1],
            ["30minutes", 0.5],
            ["2hours", 2],
            ["1day", 24],
            ["3 days", 72],
        ],
    )
    def test_normal(self, value, expected):
        assert Time(value).hours == expected


class Test_Time_minutes:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["30 seconds", 0.5],
            ["60000ms", 1],
            ["1m", 1],
            ["2hour", 120],
        ],
    )
    def test_normal(self, value, expected):
        assert Time(value).minutes == expected


class Test_Time_seconds:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["1s", 1],
            ["123 seconds", 123],
            ["1000ms", 1],
            ["123000 MSEC", 123],
            ["123000000 usecs", 123],
            ["1m", 60],
            ["2hour", 7200],
            ["12m40s", 760],
            ["12m 40s", 760],
            ["12min 40sec", 760],
            ["12 minutes 40 seconds", 760],
            ["1 hour 12 minutes 40 seconds", 4360],
        ],
    )
    def test_normal(self, value, expected):
        assert Time(value).seconds == expected

    @pytest.mark.parametrize(
        ["value", "default_unit", "expected"],
        [
            ["2", Time.Unit.SECOND, 2],
            ["2", "seconds", 2],
            ["2", Time.Unit.MINUTE, 120],
            ["2", "minutes", 120],
        ],
    )
    def test_normal_default_unit(self, value, default_unit, expected):
        assert Time(value, default_unit=default_unit).seconds == expected


class Test_Time_milliseconds:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["1sec", 1000],
            ["-2 secs", -2000],
            ["123 seconds", 123000],
            ["0ms", 0],
            ["1ms", 1],
            ["123 msecs", 123],
            ["1000us", 1],
            ["123000 usecs", 123],
            ["500 usecs", 0.5],
            ["1m", 60000],
            ["1 minutes", 60000],
            ["2hour", 7200000],
            ["2 hours", 7200000],
        ],
    )
    def test_normal(self, value, expected):
        assert Time(value).milliseconds == expected


class Test_Time_microseconds:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["123 seconds", 123000000],
            ["1ms", 1000],
            ["123000 usecs", 123000],
            ["1m", 60000000],
            ["2hour", 7200000000],
        ],
    )
    def test_normal(self, value, expected):
        assert Time(value).microseconds == expected


class Test_Time_validate:
    @pytest.mark.parametrize(
        ["value", "min_value", "max_value"],
        [
            ["1s", "0s", "60m"],
            ["1s", Time("0s"), Time("60m")],
            ["1s", "1s", "60m"],
            ["10ms", "0s", "60m"],
            ["100us", "0s", "60m"],
        ],
    )
    def test_normal(self, value, min_value, max_value):
        Time(value).validate(min_value=min_value, max_value=max_value)

    @pytest.mark.parametrize(
        ["value", "min_value", "max_value", "expected"],
        [
            ["1s", "0s", "1ms", ParameterError],
            ["-1s", "0s", "60m", ParameterError],
            ["10ms", "0s", "1ms", ParameterError],
            ["-10ms", "0s", "60m", ParameterError],
            ["100us", "0s", "60us", ParameterError],
            ["-100us", "0s", "60m", ParameterError],
        ],
    )
    def test_exception(self, value, min_value, max_value, expected):
        with pytest.raises(expected):
            Time(value).validate(min_value=min_value, max_value=max_value)


class Test_Time_get_as:
    @pytest.mark.parametrize(
        ["value", "default_unit", "expected"],
        [
            ["2", Time.Unit.DAY, 2],
            ["2", "day", 2],
            ["2", Time.Unit.HOUR, 2],
            ["2", Time.Unit.MINUTE, 2],
            ["2", Time.Unit.SECOND, 2],
            ["2", Time.Unit.MILLISECOND, 2],
            ["2", Time.Unit.MICROSECOND, 2],
        ],
    )
    def test_normal_default_unit(self, value, default_unit, expected):
        assert Time(value, default_unit=default_unit).get_as(default_unit) == expected


class Test_Time_to_humanreadable:
    @pytest.mark.parametrize(
        ["value", "default_unit", "style", "expected"],
        [
            ["0", Time.Unit.SECOND, "full", "0 seconds"],
            ["4000", Time.Unit.SECOND, "full", "1 hours 6 minutes 40 seconds"],
            ["4000", Time.Unit.SECOND, "short", "1h 6m 40s"],
            ["400000", Time.Unit.SECOND, "short", "4d 15h 6m 40s"],
        ],
    )
    def test_normal_default_unit(self, value, default_unit, style, expected):
        assert Time(value, default_unit=default_unit).to_humanreadable(style=style) == expected
