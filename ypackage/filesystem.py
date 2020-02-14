import json
import logging
import re
from os import listdir as oslistdir
from os import rename as osrename
from os import walk
from os.path import join as path_join
from pathlib import Path
from typing import AnyStr, List, Pattern, Tuple
from urllib.request import urlopen

logger = logging.getLogger(__name__)


def find_level(root: Path, startpath: Path) -> int:
    """Dizin seviyesini bulma

    Arguments:
            root {Path} -- Dizin yolu
            startpath {Path} -- Ana dizin yolu

    Returns:
            int -- Derinlik seviyesi

    Examples:
            >>> result = find_level(Path("./Documents/Configuration"), Path("."))
            >>> print(result) # 2
    """
    return len(root.relative_to(startpath).parts)


def write_file(filepath: Path, string: str):
    with filepath.open("w", encoding="utf-8") as file:
        file.write(string)

        logger.info(f"{filepath} dosyası güncellendi")


def read_file(filepath: Path) -> str:
    with filepath.open("r", encoding="utf-8") as file:
        return file.read()

        logger.info(f"{filepath} dosyası okundu")


def read_json(filepath: Path) -> dict:
    return json.loads(read_file(filepath))


def write_json(filepath: Path, jsonstr: str, indent=4, eof_line=True):
    write_file(filepath, json.dumps(jsonstr, indent=indent) + "\n" if eof_line else "")


def read_part_of_file(filepath: Path, index: str) -> str:
    """Doysanın verilen indeksler arasında kalan kısmını okuma

    Arguments:
            filepath {Path} -- Dosya yolu objesi
            index {str} -- İndeks

    Returns:
            str -- Okunan veri
    """
    filestr = ""
    with filepath.open("r", encoding="utf-8") as file:
        read = False
        for line in file:
            if index in line.replace(" ", ""):
                read = not read
                continue

            if read:
                filestr += line

        logger.info(f"{filepath} dosyasının {index} alanı okundu")
    return filestr


def insert_file(filepath: Path, string: str, index: str, new_index: str) -> None:
    """Dosyadaki belirlirli indekslerin arasına yazma

    Arguments:
            filepath {Path} -- Dosya yolu objesi
            string {str} -- Yazılacak metin
            index {str} -- İndeks
    """
    def get_index():
        return index if not new_index else new_index

    def generate_insertion():
        insertion = ""
        if bool(string):
            index = get_index()
            insertion += index + "\n\n"
            insertion += string + "\n"
            insertion += index + "\n"
        return insertion

    def generate_filestr():
        filestr = ""
        inserted = False
        if filepath.exists():
            with filepath.open("r+", encoding="utf-8") as file:
                save = True

                for line in file:
                    if not inserted and index in line.replace(" ", ""):
                        filestr += generate_insertion()
                        save = False
                        inserted = True
                    else:
                        if not inserted or save:
                            filestr += line
                        else:
                            if index in line.replace(" ", ""):
                                save = True

        else:
            filestr = generate_insertion()
            inserted = True

        # If no insertion happend, create new section
        if not inserted:
            # BUG: If index is not found in the file while new index used, index string is
            # BUG: dublicated
            # WARN: "\n" olmazsa satırın ucuna eklemekte, bu da indexin olduğu satırın
            # WARN: kaybolmasından dolayı verinin silinmesine neden olmakta
            new_line_count = 2 - filestr[-2:].count("\n")
            filestr += "\n" * new_line_count
            filestr += generate_insertion()
            inserted = True

        return filestr

    def write_insertion() -> None:
        filestr = generate_filestr()

        if filestr != read_file(filepath):
            write_file(filepath, filestr)

    return write_insertion()


def listdir_grouped(root: Path, privates=[], include_hidden=False) -> Tuple[List, List]:
    """Dizindeki dosya ve dizinleri sıralı olarak listeler

    Arguments:
            root {Path} -- Listenelecek dizin

    Keyword Arguments:
            privates {list} -- Atlanılacak yollar (default: {[]})
            include_hidden {bool} -- Gizli dosyaları dahil etme (default: {False})

    Returns:
            tuple -- dizin, dosya listesi

    Examples:
            >>> dirs, files = listdir_grouped(".")
    """
    paths = [x for x in root.iterdir()]

    dirs, files = [], []
    for path in paths:
        if not (not include_hidden and path.name.startswith('.')) and path.name not in privates:
            dirs.append(path) if path.is_dir() else files.append(path)

    dirs.sort()
    files.sort()

    return dirs, files


def read_file_by_url(rawUrl: str, encoding="utf-8") -> str:
    """URLdeki dosyayı okuma

    Arguments:
            rawUrl {str} -- URL (https, http)

    Keyword Arguments:
            encoding {str} -- Dosya kodlanması (default: {"utf-8"})

    Returns:
            str -- Okunan metin
    """
    return urlopen(rawUrl).read().decode(encoding)


def repeat_for_subdirectories(startpath: Path, func: callable) -> None:
    for root, dirs, files in walk(startpath):
        # Sıralama her OS için farklı olabiliyor
        dirs.sort()
        files.sort()

        root = Path(root)

        lvl = find_level(root, startpath)
        func(root, lvl, "dir")

        for f in files:
            fpath = path_join(root, f)
            func(fpath, lvl, "file")


def rename(regex: Pattern[AnyStr], to: str, path: str) -> None:
    result = regex.search(path)
    if result:
        if result.lastindex:
            for i in range(result.lastindex + 1):
                to = to.replace(f"${i}", result[i])

        dst = regex.sub(to, path)
        osrename(path, dst)

        logger.info(f"{path} -> {dst} taşındı")


def compile_regex(pattern, ignore_case=False) -> Pattern[AnyStr]:
    if ignore_case:
        p = re.compile(pattern, re.IGNORECASE)
    else:
        p = re.compile(pattern)

    return p


def rename_folders(
        startpath: str, pattern: str, to: str,
        ignore_case=True, recursive=False
):
    p = compile_regex(pattern, ignore_case=ignore_case)
    if recursive:
        for root, dirs, _ in walk(startpath):
            rename(p, to, root)
    else:
        for path in oslistdir(startpath):
            if Path(path).is_dir():
                rename(p, to, path)


def rename_files(
        startpath: str, pattern: str, to: str,
        ignore_case=True, recursive=False
):
    p = compile_regex(pattern, ignore_case=ignore_case)
    if recursive:
        for root, dirs, files in walk(startpath):
            for f in files:
                path = path_join(root, f)
                rename(p, to, path)
    else:
        for path in oslistdir(startpath):
            if Path(path).is_file():
                rename(p, to, path)
