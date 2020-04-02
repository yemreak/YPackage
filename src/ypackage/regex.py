import logging
import re
from typing import AnyStr, Pattern

logger = logging.getLogger(__name__)


def words_regex(*words):
    """Kelime arayan regex döndürme
    """
    pattern = []
    for word in words:
        pattern.append(r"\b" + word)

    return "|".join(pattern)


def compile_pattern(pattern, ignore_case=False) -> Pattern[AnyStr]:
    if ignore_case:
        p = re.compile(pattern, re.IGNORECASE)
    else:
        p = re.compile(pattern)

    return p


def remove_comments(filestr: str, commentstr: str) -> str:
    return re.sub(f"{commentstr}.*", "", filestr, flags=re.MULTILINE)
