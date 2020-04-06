import re
from typing import AnyStr, List, Pattern, Tuple


def has_indexes(content: str, start_string: str, end_string: str) -> bool:
    """Metin içerisinde string indekslerinin varlığını kontrol eder

    Arguments:
        content {str} -- Metin
        start_string {str} -- Başlangıç indeksi
        end_string {str} -- Bitiş indeksi

    Returns:
        bool -- Var ise `True`

    Examples:
        >>> has_indexes(                \
                'Selam ben YEmreAk',    \
                'Selam',                \
                'YEmreAk'               \
            )
        True
        >>> has_indexes(                \
                'Selam ben YEmreAk',    \
                'YPackage',             \
                'YEmreAk'               \
            )
        False
        >>> has_indexes(                \
                'Selam ben YEmreAk',    \
                'YEmreAk',              \
                'Selam'                 \
            )
        False

    """
    positions = position_index_from_string_index(content, start_string, end_string)
    return bool(positions)


def position_index_from_string_index(
    content: str,
    start_string: str,
    end_string: str
) -> List[Tuple[int, int]]:
    """String indekslerinde pozisyon indeksleri üretir

    Arguments:
        content {str} -- İndekslerin aranacağı metin
        start_string {str} -- Başlangıç indeksi
        end_string {str} -- Bitiş indeksi

    Returns:
        List[Tuple[int, int]] -- Üretilen pozisyon indeksleri

    Examples:
        >>> position_index_from_string_index( \
                'Merhaba YEmreAk Merhaba',  \
                'Merhaba ',                 \
                ' Merhaba'                  \
            )
        [(8, 15)]
        >>> position_index_from_string_index( \
                'Merhaba YEmreAk Merhaba',  \
                'Hey ',                    \
                ' Merhaba'                  \
            )
        []
        >>> position_index_from_string_index( \
                'Merhaba YEmreAk Merhaba',  \
                'Merhaba',                  \
                'Merhaba'                   \
            )
        [(7, 16)]
    """
    spos = [m.start() + len(start_string) for m in re.finditer(start_string, content)]
    epos = [m.start() for m in re.finditer(end_string, content)]

    positions = match_start_and_end_positions(spos, epos)
    return positions


def update_string_by_stringindexes(
        string: str,
        content: str,
        start_string: str,
        end_string: str
) -> str:
    """Metnin içerisideki indekslerin arasındaki metni değiştirme

    Arguments:
        string {str} -- Yeni metin
        content {str} -- Asıl içerik
        start_string {str} -- Başlangıç metni
        end_string {str} -- Bitiş metni

    Returns:
        str -- Değiştirilmiş içerik

    Examples:
        >>> update_string_by_stringindexes( \
                'YPackage',                 \
                'Merhaba YEmreAk Merhaba',  \
                'Merhaba ',                 \
                ' Merhaba'                  \
            )
        'Merhaba YPackage Merhaba'
        >>> update_string_by_stringindexes( \
                'YPackage',                 \
                'Merhaba YEmreAk Merhaba',  \
                'Hey ',                    \
                ' Merhaba'                  \
            )
        'Merhaba YEmreAk Merhaba'
        >>> update_string_by_stringindexes( \
                'YPackage',                 \
                'Merhaba YEmreAk Merhaba',  \
                'Merhaba',                  \
                'Merhaba'                   \
            )
        'MerhabaYPackageMerhaba'
    """

    positions = position_index_from_string_index(content, start_string, end_string)
    for start_pos, end_pos in positions:
        content = update_string_by_indexes(string, content, start_pos, end_pos)

    return content


def find_substrings_by_strings(
    content: str,
    start_index: str,
    end_index: str
) -> List[str]:
    """Metnin içerisideki indekslerin arasındaki metinleri alma

    Arguments:
        content {str} -- Metin
        start_string {str} -- Başlangıç metni
        end_string {str} -- Bitiş metni

    Returns:
        List[str] -- Bulunan metinlerin listesi

    Examles:
        >>> find_substrings_by_strings('- Yeni - A - Yapıt -', '-', '-')
        [' Yeni ', ' A ', ' Yapıt ']
        >>> find_substrings_by_strings('Sıkıcı bir gün oldu', ' ', ' ')
        ['bir', 'gün']
        >>> find_substrings_by_strings('Sıkıcı _bir gün_ oldu', '_', '_')
        ['bir gün']
    """
    substrings = []

    positions = position_index_from_string_index(content, start_index, end_index)
    for start_pos, end_pos in positions:
        substring = find_substring(content, start_pos, end_pos)
        substrings.append(substring)

    return substrings


def match_start_and_end_positions(spos: List[int], epos: List[int]) -> List[Tuple[int, int]]:
    """Başlangıç ve bitiş pozisyonları listesine göre başlangıç bitiş ikilisi oluşturur

    Arguments:
        spos {List[int]} -- Başlangıç pozisyonları listesi
        epos {List[int]} -- Bitiş pozisyonları listesi

    Returns:
        List[Tuple[int, int]] -- Başlangıç-bitiş ikilisi listesi

    Examples:
        >>> match_start_and_end_positions(  \
                [1, 3, 5],                  \
                [2, 4, 7]                   \
            )
        [(1, 2), (3, 4), (5, 7)]
        >>> match_start_and_end_positions(  \
                [1, 3, 5],                  \
                [1, 5, 9]                   \
            )
        [(1, 5), (5, 9)]
        >>> match_start_and_end_positions(  \
                [131],                      \
                [130, 275]                  \
            )
        [(131, 275)]
    """
    positions = []

    istart, iend = 0, 0
    while istart < len(spos):
        if istart != 0 and spos[istart] < epos[iend - 1]:
            istart += 1
            continue

        while iend < len(epos) and not (spos[istart] < epos[iend]):
            iend += 1

        if not (iend < len(epos)):
            break

        positions.append((spos[istart], epos[iend]))
        istart += 1
        iend += 1

    return positions


def update_string_by_indexes(string: str, content: str, start_pos: int, end_pos: int) -> str:
    """String içerisideki verilen konumdaki metni değiştirme

    Arguments:
        string {str} -- Eklenecek string
        content {str} -- Asıl içerik
        start_pos {int} -- Başlangıç indeksi
        end_pos {int} -- Bitiş indeksi

    Returns:
        str -- Eklenme yapılmış string

    Examples:
        >>> update_string_by_indexes('Selam', 'Merhaba YEmreAk', 0, 7)
        'Selam YEmreAk'
    """
    new_content = content[:start_pos] + string + content[end_pos:]
    return new_content


def find_substring(content: str, start_pos: int, end_pos: int) -> str:
    """Metin içerisinde metin arama

    Arguments:
        content {str} -- Metin
        start_pos {int} -- Başlangıç indeksi (dahil)
        end_pos {int} -- Bitiş indeksi (dahil değil)

    Returns:
        str -- Bulunan metin

    Examles:
        >>> find_substring('YEmreAk', 1, 5)
        'Emre'
    """
    new_content = content[start_pos:end_pos]
    return new_content


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


def parse_to_lines(content: str) -> List[str]:
    """Metin içerisindeki satırların listesini oluşturur

    Arguments:
        content {str} -- Metin

    Returns:
        List[str] -- Satır listesi

    Examles:
        >>> parse_to_lines('Selam\\nNaber\\nNasılsın')
        ['Selam', 'Naber', 'Nasılsın']
    """
    return content.split("\n")


def merge_lines(lines: List[str]) -> str:
    """Satırları birleştirip metin oluşturur

    Arguments:
        List[str] -- Satır listesi

    Returns:
        content {str} -- Metin

    Examles:
        >>> merge_lines(['Selam', 'Naber', 'Nasılsın'])
        'Selam\\nNaber\\nNasılsın'
    """
    return "\n".join(lines)


def prod_list(numbers: list) -> int:
    """Verilen listedeki tüm elemanları çarpar

    Arguments:
        numbers {list} -- Sayı listesi

    Returns:
        int -- Çarpımın sonucu

    Examples:
        >>> prod_list([2, 3, 5])
        30
    """
    result = 1
    for number in numbers:
        result *= number
    return result


def substract_list(list1: list, list2: list, safe: bool = True) -> list:
    """İki listenin farkını alır

    Arguments:
        list1 {list} -- Ana liste
        list2 {list} -- Çıkarılacak liste

    Keyword Arguments:
        safe {bool} -- Verilerin sırasını korur ve tekrarları kaldırmaz (default: {True})

    Returns:
        list -- Sonuç listesi

    Examples:
        >>> substract_list([1, 2, 3], [2, 4, 1])
        [3]
    """
    if safe:
        list2 = set(list2)
        return [x for x in list1 if x not in list2]
    else:
        return list(set(list1) - set(list2))
