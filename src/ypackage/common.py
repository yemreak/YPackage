import logging
import re
from configparser import ConfigParser
from pathlib import Path
from typing import AnyStr, List, Pattern

logger = logging.getLogger(__name__)


def initialize_logging(level=logging.INFO):
    import coloredlogs

    if level == logging.DEBUG:
        log_format = r"%(name)s[%(process)d] %(levelname)s %(message)s"
    else:
        log_format = r"%(levelname)s %(message)s"

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


def read_config(cpath: Path) -> dict:
    """Read configuration file

    Arguments:
        cpath {Path} -- Configuration file path

    Returns:
        dict -- Dictionary that contains config keys
    """
    try:
        config = ConfigParser(inline_comment_prefixes="#")
        config.read(cpath, encoding="utf-8")
    except Exception as e:
        logger.error(f"Cannot read config file {e}")
        return {}

    return config


def sort(string: str) -> str:
    lines = string.split("\n")
    lines.sort()
    result = "\n".join(lines)
    return result


def parse_to_lines(content: str) -> List[str]:
    return content.split("\n")


def merge_lines(lines: List[str]) -> str:
    return "\n".join(lines)


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


def generate_insertion_string(string: str, index: str) -> str:
    insertion_string = index + "\n\n"
    insertion_string += string + "\n\n"
    insertion_string += index + "\n"
    return insertion_string


def insert_to_string(string: str, content: str, start_pos: int, end_pos: int) -> str:
    """String içerisideki verilen konumdaki metni değiştirme

    Arguments:
        string {str} -- Eklenecek string
        content {str} -- Asıl içerik
        start_pos {int} -- Başlangıç indeksi
        end_pos {int} -- Bitiş indeksi

    Returns:
        str -- Eklenme yapılmış string

    Exampls:
        >>> insert_to_string('Selam', 'Merhaba YEmreAk', 0, 7)
        'Selam YEmreAk'
    """
    content = content[:start_pos] + string + content[end_pos:]
    return content


def insert_to_string_by_string(
        string: str,
        content: str,
        start_string: str,
        end_string: str
) -> str:
    """İçerik içerisideki verilen indekslerin arasındaki metni değiştirme

    Arguments:
        string {str} -- Eklenecek string
        content {str} -- Asıl içerik
        index {str} -- İndeks metni

    Returns:
        str -- Değiştirilmiş içerik

    Exampls:
        >>> insert_to_string_by_string(     \
                'YPackage',                 \
                'Merhaba YEmreAk Merhaba',  \
                'Merhaba ',                 \
                ' Merhaba'                  \
            )
        'Merhaba YPackage Merhaba'
        >>> insert_to_string_by_string(     \
                'YPackage',                 \
                'Merhaba YEmreAk Merhaba',  \
                'Heey ',                    \
                ' Merhaba'                  \
            )
        'Merhaba YEmreAk Merhaba'
    """

    start_positions = [m.start() for m in re.finditer(start_string, content)]
    end_positions = [m.start() for m in re.finditer(end_string, content)]

    for start_pos, end_pos in zip(start_positions, end_positions):
        start_pos = start_pos + len(start_string)
        content = insert_to_string(string, content, start_pos, end_pos)

    return content
