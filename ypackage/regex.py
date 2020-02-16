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


def rename_string(regex: Pattern[AnyStr], to: str, string: str) -> str:
    """Metni yeniden adlandırma

    Arguments:
        regex {Pattern[AnyStr]} -- Aranan regex
        to {str} -- Yeni isim
        path {str} -- Yol

    Returns:
        bool -- Adlandırma yapıldıysa true
    """
    result = regex.search(string)
    if result:
        if result.lastindex:
            for i in range(result.lastindex + 1):
                to = to.replace(f"${i}", result[i])

        string = regex.sub(to, string)

    return string


def compile_pattern(pattern, ignore_case=False) -> Pattern[AnyStr]:
    if ignore_case:
        p = re.compile(pattern, re.IGNORECASE)
    else:
        p = re.compile(pattern)

    return p


def remove_comments(filestr: str, commentstr: str) -> str:
    return re.sub(f"{commentstr}.*", "", filestr, flags=re.MULTILINE)
