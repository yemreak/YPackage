import logging
import re

logger = logging.getLogger(__name__)


def initialize_logging(level=logging.INFO):
    import coloredlogs

    if level == logging.DEBUG:
        log_format = r"%(levelname)s:%(filename)s %(message)s"
    else:
        log_format = r"%(message)s"

    coloredlogs.install(fmt=log_format, level=level)
    logger.debug("Rekli raporlayıcı aktif edildi")


def exit_if_not(condition, message=None):
    if not condition:
        exit(message)


def list_difference(list1: list, list2: list, safe: bool = True) -> list:
    """İki listenin farkını alır

    Arguments:
            list1 {list} -- Ana liste
            list2 {list} -- Çıkarılacak liste

    Keyword Arguments:
            safe {bool} -- Çıkarma işlemi sırasında verilerin sırasını korur ve tekrarları \
                                kaldırmaz (default: {True})

    Returns:
            list -- Sonuç listesi
    """
    if safe:
        list2 = set(list2)
        return [x for x in list1 if x not in list2]
    else:
        return list(set(list1) - set(list2))


def generate_substrings(string: str, index: str) -> list:
    """String içerisinde verilen indeksler arasında kalan stringleri döndürür

    Arguments:
            string {str} -- Aramanın yapılacağı metin
            index {str} -- İndeks

    Returns:
            list -- Bulunan alt metinler
    """
    substrings = []

    keys = [m.start() for m in re.finditer(index, string)]
    length = len(index)
    for i in range(0, len(keys), 2):
        start = keys[i] + length
        stop = keys[i + 1] if i + 1 != len(keys) else None
        substrings.append(string[start:stop])

    return substrings


def prod(numbers: list) -> int:
    """Verilen listedeki tüm elemanları çarpar

    Arguments:
            numbers {list} -- Sayı listesi

    Returns:
            int -- Çarpımın sonucu
    """
    result = 1
    for number in numbers:
        result *= number
    return result


def sort(string: str) -> str:
    lines = string.split("\n")
    lines.sort()
    result = "\n".join(lines)
    return result
