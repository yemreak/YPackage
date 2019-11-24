import os
import re
from enum import Enum
from urllib.parse import quote

from .filesystem import (
    insert_file as fs_insert_file
)
from .common import (
    generate_substrings as c_generate_substrings
)

LINK_REGEX = r"\[([^\[]+)\]\((.*)\)"


class SpecialFile(Enum):
    README_FILE = "README.md"
    CHANGELOG_FILE = "CHANGELOG.md"
    CODE_OF_CONTACT = "CODE_OF_CONDUCT.md"
    CONTRIBUTING_FILE = "CONTRIBUTING.md"
    LICANSE_FILE = "Licanse.md"

    def get_filepath(self, root=os.getcwd(), symbolic=False) -> str:
        if symbolic:
            return os.path.join(root, self.value)

        for path in os.listdir(root):
            path = os.path.join(root, path)
            if os.path.isfile(path) and os.path.basename(path) == self.value:
                return os.path.join(root, self.value)

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


def make_linkstr(header, link):
    return f"- [{header}]({link})\n"


def create_link(path: str, header: str = None, root: str = os.getcwd(), ilvl=0, isize=2) -> str:
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

    pathname = barename(path) if not header else header
    path = os.path.relpath(path, root)
    path = encodedpath(path)

    indent = create_indent(ilvl, size=isize)
    linkstr = make_linkstr(pathname, path)

    return '{}{}'.format(indent, linkstr)


def create_header(name: str, headerlvl: int) -> str:
    return "#" * headerlvl + f" {name}\n\n"


def read_first_header(filepath):
    header = ""
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#"):
                header = line.strip().replace("# ", "")
                break

    if "<!--" in header:
        header = header[:header.index("<!--")].strip()

    return header


def read_first_link(string: str) -> dict:
    """İlk link verisini döndürür

    Arguments:
        string {str} -- Link aranacak metin dosyası

    Returns:
        dict -- Link verisi

    Examples:
        >>> result[0] = "[name](url)"
        >>> result[1] = "name"
        >>> result[2] = "url"
    """
    return re.search(f"{LINK_REGEX}|$", string)


def remove_title(string: str) -> str:
    lines = string.split("\n")
    for line in lines:
        if line.count("#") == 1:
            lines.remove(line)
            break
        # 1'den fazla gelirse title yok demektir
        elif line.count("#") >= 1:
            break

    return "\n".join(lines)


def find_link(line: str) -> dict:
    """Varsa link verisini döndürür

    Arguments:
        string {str} -- Bağlantı aranacak metin dosyası

    Returns:
        dict -- Bulunan bağlantılar

    Examples:
        >>> result[0] = "[name](url)"
        >>> result[1] = "name"
        >>> result[2] = "url"
    """
    return re.search(LINK_REGEX, line)


def findall_links(string: str) -> dict:
    """Tüm linkleri döndürür

    Arguments:
        string {str} -- Bağlantı aranacak metin dosyası

    Returns:
        dict -- Bulunan bağlantılar

    Examples:
        >>> result[0] = ('name', 'url')
        >>> result[0][1] = "name"
        >>> result[0][1] = "url"
    """
    return re.findall(LINK_REGEX, string)


def generate_filelink(fpath: str, startpath: str = os.getcwd(), header: str = None, ilvl=0, isize=2) -> str:
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
        header = read_first_header(fpath)

    return create_link(fpath, header=header, root=startpath, isize=isize, ilvl=ilvl)


def generate_dirlink(root: str, startpath: str = os.getcwd(), ilvl=0, isize=2) -> str:
    """Dizin için markdown linki oluşturur
    README.md varsa ona bağlantı verir

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

    dirlink = ""
    readme_path = SpecialFile.README_FILE.get_filepath(root)
    if readme_path:
        header = read_first_header(readme_path)
        dirlink = create_link(
            readme_path, header=header, root=startpath, isize=isize, ilvl=ilvl
        )
    else:
        dirlink = create_link(root, root=startpath, isize=isize, ilvl=ilvl)

    return dirlink


def make_comment(string):
    return f"<!--{string}-->"


def insert_file(filepath, string, index, force=False, fileheader=None, new_index=None):
    if force and not os.path.exists(filepath):
        create_markdown_file(filepath, header=fileheader)

    index = make_comment(index)

    if bool(new_index):
        new_index = make_comment(new_index)

    fs_insert_file(filepath, string, index, new_index)


def create_markdown_file(filepath, header=None):
    if not bool(header):
        header = os.path.basename(filepath)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(create_header(header,  1))


def generate_substrings(content, index):
    index = make_comment(index)
    return c_generate_substrings(content, index)
