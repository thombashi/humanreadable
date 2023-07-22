import re
from typing import Pattern

from ._const import PATTERN_TEMPLETE
from ._types import Units


def compile_units_regex_pattern(units: Units, flags: int = 0) -> Pattern[str]:
    return re.compile("|".join([PATTERN_TEMPLETE.format(unit) for unit in units]), flags)
