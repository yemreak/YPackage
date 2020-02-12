import re


def words_regex(*words):
    """Kelime arayan regex döndürme
    """
    pattern = []
    for word in words:
        pattern.append(r"\b" + word)

    return "|".join(pattern)
