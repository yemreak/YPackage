import logging
import os
import re
from enum import Enum
from pathlib import Path
from typing import Any, List
from urllib.parse import quote

from deprecated import deprecated

from . import common, filesystem

logger = logging.getLogger(__name__)


class Link:

    TEMPLATE = "[{}]({})"
    REGEX = r"\[([^\[]+)\]\((.*)\)"

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def __str__(self):
        return Link.TEMPLATE.format(self.name, self.path)

    def is_url(self):
        return "https://" in self.path or "http://" in self.path

    @property
    def filepath(self) -> Path:
        if not self.is_url():
            return Path(self.path)

    @staticmethod
    def find_first(string) -> Any:
        result = re.search(Link.REGEX, string)
        if result:
            name = result[1]
            path = result[2]

            return Link(name, path)

    @staticmethod
    def find_all(string: str) -> List[Any]:
        links = []

        results = re.findall(Link.REGEX, string)
        for result in results:
            name = result[0]
            path = result[1]

            links.append(Link(name, path))

        return links

    @staticmethod
    def map_function(link):
        return link


def find_all_links(string) -> List[Link]:
    return Link.find_all(string)


def find_first_link(string) -> Link:
    return Link.find_first(string)


@deprecated
def is_url(link: str) -> bool:
    return "https://" in link or "http://" in link


@deprecated
def check_links(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        for line in f:
            links = find_all_links(line)
            for link in links:
                if not link.filepath:
                    print(link.path)


def map_links(content: str, func: Link.map_function) -> str:
    """Dosyadaki tüm linkler için verilen fonksiyonu uygular

    Arguments:
        content {str} -- Metin içeriği
        func {Link.map_function} -- Link alan ve Link döndüren fonksiyon

    Returns:
        str -- Değişen metin içeriği
    """
    lines = filesystem.parse_to_lines(content)
    for i, line in enumerate(lines):
        oldlinks = Link.find_all(line)
        for oldlink in oldlinks:
            newlink = func(oldlink)
            lines[i] = lines[i].replace(str(oldlink), str(newlink))

    return filesystem.merge_lines(lines)


def replace_in_links(content: str, old: str, new: str) -> str:

    def replace_link(link: Link):
        link.path = link.path.replace(old, new)
        return link

    map_links(content, replace_link)


class Header:

    REGEX = r"(#+) (.*)"
    HEADER_CHAR = "#"

    def __init__(self, name, level: int = 1):
        self.name = name
        self.level = level

    def __str__(self):
        return (self.level * Header.HEADER_CHAR) + " " + self.name

    @staticmethod
    def find_first(string: str, level=1) -> Any:
        result = re.search(Header.REGEX, string)
        if result:
            lvl = result[1].count(Header.HEADER_CHAR)
            name = result[2]

            return Header(name, level=lvl)

    @staticmethod
    def find_all(string, level=1) -> List[Any]:
        headers = []

        results = re.findall(Header.REGEX, string)
        for result in results:
            lvl = result[0].count(Header.HEADER_CHAR)
            name = result[1]

            if lvl == level:
                headers.append(Header(name, level=lvl))

        return headers

    @staticmethod
    def from_file(filepath: Path, level=1) -> List[Any]:
        with filepath.open("r", encoding="utf-8") as file:
            return Header.find_all(file.read(), level=level)


def find_all_headers(string, level=1) -> List[Header]:
    return Header.find_all(string, level=level)


def find_all_headers_from_file(filepath, level=1) -> List[Header]:
    if not filesystem.is_exist(filepath):
        return []

    with filepath.open("r", encoding="utf-8") as file:
        return Header.find_all(file.read(), level=level)


def find_first_header(string, level=1) -> Header:
    return Header.find_first(string, level=level)


def find_first_header_from_file(filepath, level=1) -> Header:
    with filepath.open("r", encoding="utf-8") as file:
        return Header.find_first(file.read(), level=level)


def change_title_of_string(title: str, content: str) -> str:
    title_changed = False

    lines = filesystem.parse_to_lines(content)
    for i, line in enumerate(lines):
        header = find_first_header(line)
        if header:
            if header.level == 1:
                lines[i] = title
                title_changed = True
                break
            elif header.level >= 1:
                lines[0] = title
                title_changed = True
                break

    if not title_changed:
        lines[0] = title
        title_changed = True

    return filesystem.merge_lines(lines)


def change_title_of_file(title: str, filepath: Path):
    content = filesystem.read_file(filepath)
    content = change_title_of_string(title, content)
    filesystem.write_file(filepath, content)


def generate_header_section(name: str, level: str) -> str:
    """Markdown dosyaları için standartlara uygun header alanı metni oluşturur

    Arguments:
        name {str} -- Başlık ismi
        level {str} -- Başlık seviyesi

    Returns:
        str -- Oluşturulan başlık alanı metni

    Examples:
        >>> generate_header_section("YPackage", 1)
        '# YPackage\\n\\n'
    """
    return str(Header(name, level)) + "\n\n"


class Comment:

    TEMPLATE = "<!-- {} -->"

    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return Comment.TEMPLATE.format(self.content)


class SpecialFile(Enum):

    README_FILE = "README.md"
    CHANGELOG_FILE = "CHANGELOG.md"
    CODE_OF_CONTACT = "CODE_OF_CONDUCT.md"
    CONTRIBUTING_FILE = "CONTRIBUTING.md"
    LICANSE_FILE = "Licanse.md"

    def get_filepath(self, root: Path = Path.cwd()) -> Path:
        return root / self.value


# DEV: Figure out index string in markdown file


def remove_extension(filepath: str) -> str:
    """Dosya uzantısını kaldırma

    Args:
            filepath (str): Dosya yolu

    Returns:
            str: Uzantsız dosya yolu
    """

    filepath, _ = os.path.splitext(filepath)
    return filepath


def barename(path: str) -> str:
    """Dosya veya dizin yolundan, yol ve uzantıyı temizleme

    Args:
            filepath (str): Dosya yolu

    Returns:
            str: Sadece dosya ismi
    """

    pathname = path
    if os.path.isfile(path):
        pathname = remove_extension(path)

    pathname = os.path.basename(pathname)

    return pathname


def encodedpath(path: str) -> str:
    """ Verilen yolu url formatında kodlama

    Windows için gelen '\\' karakteri '/' karakterine çevrilir

    Args:
            pathname (str): Yol ismi

    Returns:
            str: Kodlanmış metin
    """

    return quote(path.replace("\\", "/"))


def create_indent(level, size=2):
    return ' ' * size * (level)


def create_link(path: Path, header: str = None, root: Path = Path.cwd(), ilvl=0, isize=2) -> str:
    """Verilen yola uygun kodlanmış markdown linki oluşturma

    Arguments:
            path {str} -- Yol

    Keyword Arguments:
            header {str} -- Link başlığı (default: {None})
            root {str} -- Ana dizin (default: {os.getcwd()})
            ilvl {int} -- Girinti seviyesi (default: {0})
            isize {int} -- Girinti birim uzunluğu (default: {2})

    Returns:
            str -- Girintili markdown bağlatısı
    """

    if not header:
        header = path.name

    if not is_url(str(path)):
        path = path.relative_to(root)
        path = encodedpath(str(path))

    indent = create_indent(ilvl, size=isize)
    linkstr = f"- {str(Link(header, path))}\n"

    return '{}{}'.format(indent, linkstr)


def generate_filelink(
    fpath: Path, startpath: str = os.getcwd(),
    header: str = None, ilvl=0, isize=2
) -> str:
    """Dosya için markdown linki oluşturur

    Arguments:
            path {str} -- Yol

    Keyword Arguments:
            header {str} -- Link başlığı (default: {None})
            root {str} -- Ana dizin (default: {os.getcwd()})
            ilvl {int} -- Girinti seviyesi (default: {0})
            isize {int} -- Girinti birim uzunluğu (default: {2})

    Returns:
            str -- Girintili markdown bağlatısı
    """
    if not header:
        header = find_all_headers_from_file(fpath)
        header = str(find_first_header_from_file(fpath)) if header else ""

    return create_link(fpath, header=header, root=startpath, isize=isize, ilvl=ilvl)


def generate_dirlink(root: Path, startpath: str = os.getcwd(), ilvl=0, isize=2) -> str:
    """Dizin için markdown linki oluşturur
    README.md varsa ona bağlantı verir

    Arguments:
            path {Path} -- Yol

    Keyword Arguments:
            header {str} -- Link başlığı (default: {None})
            root {str} -- Ana dizin (default: {os.getcwd()})
            ilvl {int} -- Girinti seviyesi (default: {0})
            isize {int} -- Girinti birim uzunluğu (default: {2})

    Returns:
            str -- Girintili markdown bağlatısı
    """

    dirlink = ""
    readme_path = SpecialFile.README_FILE.get_filepath(root)
    if readme_path:
        header = str(find_first_header_from_file(readme_path))
        dirlink = create_link(
            readme_path, header=header, root=startpath, isize=isize, ilvl=ilvl
        )
    else:
        dirlink = create_link(root, root=startpath, isize=isize, ilvl=ilvl)

    return dirlink


def insert_file(
    filepath: Path, string, index, force=False, fileheader=None, new_index=None
):
    if force and not filepath.exists():
        create_markdown_file(filepath, header=fileheader)

    index = str(Comment(index))

    if bool(new_index):
        new_index = str(Comment(new_index))

    filesystem.insert_file(filepath, string, index=index, new_index=new_index)


def create_markdown_file(filepath: Path, header=None):
    if not bool(header):
        header = filepath.name

    with filepath.open("w", encoding="utf-8") as file:
        file.write(generate_header_section(header, 1))


def generate_substrings(content, index):
    index = str(Comment(index))
    return common.generate_substrings(content, index)
