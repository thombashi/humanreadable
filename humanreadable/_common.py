import re
from re import Pattern

from ._const import PATTERN_TEMPLATE
from ._types import Units


def compile_units_regex_pattern(units: Units, flags: int = 0) -> Pattern[str]:
    return re.compile("|".join([PATTERN_TEMPLATE.format(unit) for unit in units]), flags)
