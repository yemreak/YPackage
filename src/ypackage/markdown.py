import logging
import re
from enum import Enum
from pathlib import Path
from typing import Any, List, Union

from deprecated import deprecated

from . import common, filesystem

logger = logging.getLogger(__name__)


class Comment:

    TEMPLATE = "<!-- {} -->"

    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return Comment.TEMPLATE.format(self.content)


class Indent:

    TAB_SIZE = 2
    INDENT_CHAR = " "

    def __init__(self, level: int):
        self.level = level

    def __str__(self):
        return Indent.INDENT_CHAR * self.level * Indent.TAB_SIZE

    def to_str(self) -> str:
        return self.__str__()


class Header:

    REGEX = r"(#+) (.*)"
    HEADER_CHAR = "#"

    def __init__(self, name, level: int = 1):
        self.name = name
        self.level = level

    def __str__(self):
        return (self.level * Header.HEADER_CHAR) + " " + self.name

    def to_str(self):
        return self.__str__()

    @staticmethod
    def find_first(string: str, level=1) -> Union[Any, None]:
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


def find_first_header(string, level=1) -> Union[Header, None]:
    return Header.find_first(string, level=level)


def find_first_header_from_file(filepath, level=1) -> Union[Header, None]:
    if not filesystem.is_exist(filepath):
        return None

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


def generate_name_for_file(filepath: Path) -> str:
    """Markdown dosyası için isim belirleme

    Arguments:
        filepath {Path} -- Markdown dosyasının yolu

    Returns:
        str -- Başlığı varsa başlığı, yoksa dosya ismini döndürür
    """

    header = find_first_header_from_file(filepath)
    name = header.to_str() if header else filepath.name

    return name


class Link:

    TEMPLATE = "[{}]({})"
    REGEX = r"\[([^\[]+)\]\((.*)\)"

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def __str__(self):
        return Link.TEMPLATE.format(self.name, self.path)

    def to_str(
        self,
        indent: Indent = None,
        is_list: bool = False,
        single_line: bool = False
    ) -> str:
        string = indent.to_str()
        string += "- " if is_list else ""
        string += self.__str__()
        string += "\n" if single_line else ""

        return string

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


def generate_custom_link_string(
    name: str,
    path: str,
    indent: Indent = None,
    is_list: bool = False,
    single_line: bool = False
) -> str:
    """Özel link metni oluşturma

    Arguments:
        name {str} -- Link'in ismi
        path {str} -- Link'in adresi

    Keyword Arguments:
        intent {Indent} -- Varsa girinti objesi (default: {None})
        is_list {bool} -- Liste elamanı olarak tanımlama '- ' ekler (default: {False})
        single_line {bool} -- Tek satırda yer alan link '\n' ekler (default: {False})


    Returns:
        {str} -- Oluşturulan link metni

    Examples:
        >>> generate_custom_link_string(\
            'YPackage',\
            'https://ypackage.yemreak.com',\
            indent=Indent(2),\
            is_list=True,\
            single_line=True\
        )
        '    - [YPackage](https://ypackage.yemreak.com)\\n'

    """
    return Link(name, path).to_str(indent=indent, is_list=is_list, single_line=single_line)


def generate_file_link_string(
    filepath: Path,
    name: str = None,
    root: Path = Path.cwd(),
    indent: Indent = None,
    is_list: bool = False,
    single_line: bool = False
) -> str:
    """Özel dosya linki metni oluşturma

    Arguments:
        filepath {Path} -- Dosya yolu objesi

    Keyword Arguments:
        name {str} -- Link'in ismi
        intent {Indent} -- Varsa girinti objesi (default: {None})
        is_list {bool} -- Liste elamanı olarak tanımlama '- ' ekler (default: {False})
        single_line {bool} -- Tek satırda yer alan link '\n' ekler (default: {False})

    Returns:
        {str} -- Oluşturulan link metni

    Examples: 
        >>> generate_file_link_string(\
            Path('./src/ypackage/markdown.py'),\
            name        = 'YPackage',            \
            root        = Path('src/ypackage/'), \
            indent      = Indent(2),             \
            is_list     = True,                  \
            single_line = True\
        )
        '    - [YPackage](markdown.py)\\n'
    """
    if not name:
        name = generate_name_for_file(filepath)

    root = root.absolute()
    filepath = filepath.absolute()

    filepath = filepath.relative_to(root)
    filepath_string = filepath.as_posix()

    return generate_custom_link_string(
        name,
        filepath_string,
        indent=indent,
        is_list=is_list,
        single_line=single_line
    )


def generate_dir_link_string(
    dirpath: Path,
    root: Path = Path.cwd(),
    indent: Indent = None,
    is_list: bool = False,
    single_line: bool = False
) -> str:
    """Özel dosya linki metni oluşturma

    Arguments:
        filepath {Path} -- Dosya yolu objesi

    Keyword Arguments:
        name {str} -- Link'in ismi
        intent {Indent} -- Varsa girinti objesi (default: {None})
        is_list {bool} -- Liste elamanı olarak tanımlama '- ' ekler (default: {False})
        single_line {bool} -- Tek satırda yer alan link '\n' ekler (default: {False})

    Returns:
        {str} -- Oluşturulan link metni

    Examples:
        >>> generate_dir_link_string(   \
            Path('src/ypackage/markdown.py'),                \
            Path('src'),            \
            indent      = Indent(2),    \
            is_list     = True,         \
            single_line = True          \
        )
        '    [README.md](ypackage/markdown.py/README.md)\\n'
    """

    readmepath = SpecialFile.README_FILE.get_filepath(dirpath)

    return generate_file_link_string(
        readmepath if readmepath else dirpath,
        root=root,
        indent=indent,
        single_line=single_line
    )


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


class SpecialFile(Enum):

    README_FILE = "README.md"
    CHANGELOG_FILE = "CHANGELOG.md"
    CODE_OF_CONTACT = "CODE_OF_CONDUCT.md"
    CONTRIBUTING_FILE = "CONTRIBUTING.md"
    LICANSE_FILE = "Licanse.md"

    def get_filepath(self, root: Path = Path.cwd()) -> Path:
        """Özel dosyalar için dosya yolu oluşturur

        Keyword Arguments:
            root {Path} -- Çalışma dizini (default: {Path.cwd()})

        Returns:
            Path -- Oluşturulan dosya yolu objesi

        Examples:
            >>> SpecialFile.README_FILE.get_filepath(Path('./src/ypackage'))
            WindowsPath('src/ypackage/README.md')
        """
        return root / self.value


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
    if not header:
        header = filepath.name

    content = generate_header_section(header, 1)
    filesystem.write_file(filepath, content)


def generate_substrings(content, index):
    index = str(Comment(index))
    return common.generate_substrings(content, index)
