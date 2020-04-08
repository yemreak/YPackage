import logging
import re
from configparser import ConfigParser
from json import dumps as dumps_json
from json import loads as loads_json
from os import listdir as os_listdir
from os import rename as os_rename
from os import walk as os_walk
from os.path import join as os_path_join
from pathlib import Path
from shutil import copyfile
from typing import AnyStr, Dict, List, Pattern, Tuple
from urllib.error import HTTPError
from urllib.request import urlopen

from . import common

logger = logging.getLogger(__name__)


def must_exist(filepath: Path) -> bool:
    """Dosya sisteminde soyayı kontrol eder ve raporlar

    Arguments:
        filepath {Path} -- Dosya yolu objesi

    Returns:
        bool -- Varsa true

    Examples:
        >>> must_exist(Path('docs/README.md'))
        True
    """

    if not filepath.exists():
        logger.error("Dosya yolu geçersiz: " + str(filepath))
        return False
    return True


def find_in_file(pattern: str, filepath: Path) -> List[str]:
    """Dosya içeriğinde pattern arama

    Arguments:
        pattern {str} -- Aranacak metin veya regex patterni
        filepath {Path} -- Dosya yolu objesi

    Returns:
        List[str] -- Sonuçlar

    Examples:
        >>> find_in_file('# ..(.*)ack', Path('docs/README.md'))
        ['YP']

        >>> find_in_file('# ..(.)(.)ack', Path('docs/README.md'))
        [('Y', 'P')]
    """
    content = read_file(filepath)
    return re.findall(pattern, content)


def find_level(filepath: Path, root: Path) -> int:
    """Dizin seviyesini bulma

    Arguments:
        root {Path} -- Dizin yolu
        startpath {Path} -- Ana dizin yolu

    Returns:
        int -- Derinlik seviyesi

    Examples:
        >>> find_level(Path("./Documents/Configuration"), Path("."))
        2
    """

    filepath = filepath.relative_to(root)
    level = len(filepath.parts)
    return level


def read_file(filepath: Path) -> str:
    """Dosyayı okur.
    Dosya bulunamazsa ekrana raporlar hata fırlatmaz

    Arguments:
        filepath {Path} -- Okunacak dosyanın yolu

    Returns:
        str -- Okunan metin veya ''
    """
    content = ""
    try:
        logger.debug(f"Dosya okunuyor: {filepath}")
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        logger.debug(f"Dosya okunamadı: {filepath}")
    return content


def read_json(filepath: Path, strict=False) -> dict:
    """Dosya içerisindeki JSON metnini okur.
    Dosya bulunamazsa ekrana raporlar hata fırlatmaz

    Arguments:
        filepath {Path} -- Okunacak dosyanın yolu

    Returns:
        str -- Okunan metin veya ''
    """
    content = read_file(filepath)
    json_object = loads_json(content, strict=strict)
    return json_object


def read_jsonc(filepath: Path, strict=False) -> dict:
    """Dosya içerisindeki yorum satırlı JSON metnini okur.
    Dosya bulunamazsa ekrana raporlar hata fırlatmaz

    Arguments:
        filepath {Path} -- Okunacak dosyanın yolu

    Returns:
        str -- Okunan metin veya ''
    """
    content = read_file(filepath)
    content = re.sub("//.*", "", content)
    return loads_json(content, strict=strict)


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


def read_file_from_url(url: str, encoding="utf-8") -> str:
    """URL ile dosya okuma

    Arguments:
        rawUrl {str} -- URL (https, http)

    Keyword Arguments:
        encoding {str} -- Dosya kodlanması (default: {"utf-8"})

    Returns:
        str -- Okunan metin
    """

    content = ""
    try:
        file = urlopen(url)
        content = file.read()
        content = content.decode(encoding)
        file.close()
        logger.debug(f"URL üzerinden dosya okundu: {url}")
    except HTTPError as error:
        logger.error(
            f"Dosya okunamadı: {error.url} <HTTPError {error.code}: {error.msg}>")

    return content


def write_to_file(filepath: Path, content: str) -> bool:
    """Dosyaya 'utf-8' metni yazar.
    Dosya bulunamazsa ekrana raporlar hata fırlatmaz

    Arguments:
        filepath {Path} -- Okunacak dosyanın yolu

    Returns:
        bool -- Yazma işlemi başarılı ise `True`
    """
    try:
        filepath.write_text(content, encoding="utf-8")
        logger.info(f"Dosya güncellendi: {filepath}")
        return True
    except Exception:
        logger.exception(f"Dosyaya yazılamadı: {filepath}")
        return False


def write_json_to_file(filepath: Path, jsonstr: Dict[str, str], indent: int = 4, eof_line=True):
    """Dosyaya JSON yazar.
    Dosya bulunamazsa ekrana raporlar hata fırlatmaz

    Arguments:
        filepath {Path} -- Okunacak dosyanın yolu
        jsonstr {Dict[str, str]} -- JSON objesi
        indent {int} -- JSON yazımı için varsayılan girinti uzunluğu
        eof_line {bool} -- Dosyanın sonuna '\\n' koyar

    Returns:
        bool -- Yazma işlemi başarılı ise `True`
    """
    jsonstr = dumps_json(jsonstr, indent=4)
    jsonstr += "\n" if eof_line else ""
    return write_to_file(filepath, jsonstr)


def has_indexes(filepath: Path, start_string: str, end_string: str) -> bool:
    """Dosya içerisinde string indekslerinin varlığını kontrol eder

    Arguments:
        content {str} -- Metin
        start_string {str} -- Başlangıç indeksi
        end_string {str} -- Bitiş indeksi

    Returns:
        bool -- Var ise `True`
    """
    content = read_file(filepath)
    result = common.has_indexes(content, start_string, end_string)
    return result


def update_file_by_stringindexes(
    string: str,
    filepath: Path,
    start_string: str,
    end_string: str,
    must_inserted=False
) -> bool:
    """Metin arasına istenen metni yerleştirir

    Arguments:
        string {str} -- Yerleştirilecek metin
        filepath {Path} -- Dosya yolu objesi
        start_string {str} -- Başlangıç metni
        end_string {str} -- Bitiş metni

    Keyword Arguments:
        must_inserted {bool} -- Verilen indeksler bulunamazsa dosyanın sonuna indeksler ile ekler

    Returns:
        bool -- Dosyada değişiklik olduysa True
    """

    content = read_file(filepath)
    new_content = common.update_string_by_stringindexes(
        string,
        content,
        start_string,
        end_string
    )

    if new_content == content:
        insert_conditions = must_inserted
        insert_conditions &= not has_indexes(
            filepath, start_string, end_string)
        if insert_conditions:
            new_content += start_string + string + end_string
            return write_to_file(filepath, new_content)

        return False

    return write_to_file(filepath, new_content)


def copy_file(src: Path, dst: Path) -> bool:
    """Dosyayı kopyalar

    Arguments:
        src {Path} -- Kopyalanacak dosyanın yolu
        dst {Path} -- Kopyalanacağı yol

    Returns:
        bool -- Kopyalama başarılı ise `True`
    """
    result = copyfile(src, dst)
    logger.info(f"Dosya taşındı: {src} -> {dst}")
    return bool(result)


def rename(regex: Pattern[AnyStr], to: str, path: str) -> bool:
    """Dosya veya dizini yeniden adlandırma

    Arguments:
        regex {Pattern[AnyStr]} -- Aranan regex
        to {str} -- Yeni isim
        path {str} -- Yol

    Returns:
        bool -- Adlandırma yapıldıysa true
    """
    new_path = common.rename_string(regex, to, path)
    if path != new_path:
        os_rename(path, new_path)

        logger.info(f"{path} -> {new_path} taşındı")
        return True

    return False


def rename_folders(
        startpath: str, pattern_string: str, to: str,
        ignore_case=True, recursive=False
) -> bool:

    pattern: Pattern[AnyStr]
    if ignore_case:
        pattern = re.compile(pattern_string, re.IGNORECASE)
    else:
        pattern = re.compile(pattern_string)

    changed_happend = False

    if recursive:
        for root, dirs, _ in os_walk(startpath):
            result = rename(pattern, to, root)

            if not changed_happend and result:
                changed_happend = True
    else:
        for path in os_listdir(startpath):
            if Path(path).is_dir():
                result = rename(pattern, to, path)

                if not changed_happend and result:
                    changed_happend = True

    return changed_happend


def rename_files(
        startpath: str, pattern_string: str, to: str,
        ignore_case=True, recursive=False
) -> bool:

    pattern: Pattern[AnyStr]
    if ignore_case:
        pattern = re.compile(pattern_string, re.IGNORECASE)
    else:
        pattern = re.compile(pattern_string)

    changed_happend = False

    if recursive:
        for root, dirs, files in os_walk(startpath):
            for f in files:
                path = os_path_join(root, f)
                result = rename(pattern, to, path)

                if result:
                    changed_happend = True
    else:
        for path in os_listdir(startpath):
            if Path(path).is_file():
                result = rename(pattern, to, path)

                if result:
                    changed_happend = True

    return changed_happend


def listdir_grouped(root: Path, ignore_folders=[], include_hidden=False) -> Tuple[List, List]:
    """Dizindeki dosya ve dizinleri sıralı olarak listeler

    Arguments:
        root {Path} -- Listenelecek dizin

    Keyword Arguments:
        ignore_folders {list} -- Atlanılacak yollar (default: {[]})
        include_hidden {bool} -- Gizli dosyaları dahil etme (default: {False})

    Returns:
        tuple -- dizin, dosya listesi

    Examples:
        >>> dirs, files = listdir_grouped(".")
    """
    if isinstance(root, str):
        root = Path(root)

    paths = [x for x in root.iterdir()]

    dirs, files = [], []
    for path in paths:
        condition = not include_hidden and path.name.startswith('.')
        condition = condition and path.name not in ignore_folders
        condition = not condition
        if condition:
            dirs.append(path) if path.is_dir() else files.append(path)

    dirs.sort()
    files.sort()

    return dirs, files


def is_hidden(dirpath: Path) -> bool:
    """Dizin gizliliğini kontrol eder

    Arguments:
        dirpath {Path} -- Dizin yolu objesi

    Returns:
        bool -- Gizli ise True

    Examples:
        >>> is_hidden(Path('.github'))
        True
        >>> is_hidden(Path('random'))
        False
    """
    return dirpath.name.startswith(".")


def list_nonhidden_dirs(dirpath: Path) -> List[Path]:
    dirlist = []
    for path in sorted(dirpath.iterdir()):
        if path.is_dir() and not is_hidden(path):
            dirlist.append(path)
    return dirlist


def list_nonhidden_files(dirpath: Path) -> List[Path]:
    dirlist = []
    for path in sorted(dirpath.iterdir()):
        if path.is_file() and not is_hidden(path):
            dirlist.append(path)
    return dirlist


def read_config(configpath: Path) -> dict:
    """Read configuration file

    Arguments:
        cpath {Path} -- Configuration file path

    Returns:
        dict -- Dictionary that contains config keys
    """
    try:
        config = ConfigParser(inline_comment_prefixes="#")
        config.read(configpath, encoding="utf-8")
    except Exception as e:
        logger.error(f"Cannot read config file {e}")
        return {}

    return config
