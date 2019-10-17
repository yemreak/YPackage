def exit_if_not(condition, message=None):
    if not condition:
        exit(message)


def list_difference(list1: list, list2: list, safe: bool = True) -> list:
    """İki listenin farkını alır

    Arguments:
        list1 {list} -- Ana liste
        list2 {list} -- Çıkarılacak liste

    Keyword Arguments:
        safe {bool} -- Çıkarma işlemi sırasında verilerin sırasını korur ve tekrarları kaldırmaz (default: {True})

    Returns:
        list -- Sonuç listesi
    """
    if safe:
        list2 = set(list2)
        return [x for x in list1 if x not in list2]
    else:
        return list(set(list1) - set(list2))


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
