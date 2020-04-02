import re
from enum import Enum
from pathlib import Path
from typing import Any, List, Union


class Template:

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __add__(self, other: Any) -> str:
        if isinstance(other, str):
            return self.__str__() + other
        elif isinstance(other, self):
            return self.__str__() + other.__str__()
        else:
            raise TypeError

    def __radd__(self, other: Any) -> str:
        if isinstance(other, str):
            return other + self.__str__()
        elif isinstance(other, self):
            return other.__str__() + self.__str__()
        else:
            raise TypeError()


class Comment(Template):

    TEMPLATE = "<!-- {} -->"

    def __init__(self, content: str):
        self.content = content

    def __repr__(self):
        return f"Comment({self.content.__repr__()})"

    def __str__(self):
        return Comment.TEMPLATE.format(self.content)


class Indent(Template):

    TAB_SIZE = 2
    INDENT_CHAR = " "

    def __init__(self, level: int):
        self.level = level

    def __repr__(self):
        return f"Indent({self.level.__repr__()})"

    def __str__(self):
        return Indent.INDENT_CHAR * self.level * Indent.TAB_SIZE

    def to_str(self) -> str:
        return self.__str__()


class Header(Template):

    REGEX = r"(#+) *(.*)"
    HEADER_CHAR = "#"

    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level

    def __repr__(self):
        return f"Header({self.name.__repr__()}, {self.level.__repr__()})"

    def __str__(self):
        return (self.level * Header.HEADER_CHAR) + " " + self.name

    def to_str(self, is_section=False):
        return self.__str__() + "\n\n"

    @classmethod
    def find_first(cls, content: str, level=1) -> Union[Any, None]:
        """İçerik içerisindeki ilk header objesini bulma

        Arguments:
            string {str} -- İçerik

        Keyword Arguments:
            level {int} -- Header seviyesi (default: {1})

        Returns:
            Union[Any, None] -- Bulunan Header objesi

        Examples:
            >>> header = Header.find_first('# HEHO\\n#HOHO')
            >>> header.name
            'HEHO'
            >>> header.level
            1
        """

        result = re.search(cls.REGEX, content)
        if result:
            lvl = result[1].count(cls.HEADER_CHAR)
            name = result[2].strip()

            return cls(name, level=lvl)

    @classmethod
    def find_all(cls, string, level=1) -> List[Any]:
        """İçerik içerisindeki tüm header'ları buluyor

        Arguments:
            string {str} -- İçerik metni

        Keyword Arguments:
            level {int} -- Bulunacak header seviyesi (default: {1})

        Returns:
            List[Any] -- Header listesi

        Examples:
            >>> headers = Header.find_all('# HEHO\\n# HOHO')
            >>> headers[0].name
            'HEHO'
            >>> headers[1].name
            'HOHO'
        """

        headers = []

        results = re.findall(cls.REGEX, string)
        for result in results:
            lvl = result[0].count(cls.HEADER_CHAR)
            name = result[1].strip()

            if lvl == level:
                headers.append(cls(name, level=lvl))

        return headers

    @staticmethod
    def from_file(filepath: Path, level=1) -> List[Any]:
        with filepath.open("r", encoding="utf-8") as file:
            return Header.find_all(file.read(), level=level)


class Link(Template):

    TEMPLATE = "[{}]({})"
    REGEX = r"\[([^\[]+)\]\((.*)\)"

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def __repr__(self):
        return f"Link({self.name.__repr__()}, {self.path.__repr__()})"

    def __str__(self):
        return Link.TEMPLATE.format(self.name, self.path)

    def to_str(
        self,
        indent: Indent = None,
        is_list: bool = False,
        single_line: bool = False
    ) -> str:
        string = indent.to_str() if indent else ""
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

    @classmethod
    def find_first(cls, content: str) -> Any:
        result = re.search(Link.REGEX, content)
        if result:
            name = result[1]
            path = result[2]

            return cls(name, path)

    @classmethod
    def find_all(cls, content: str) -> List[Any]:
        links = []

        results = re.findall(Link.REGEX, content)
        for result in results:
            name = result[0]
            path = result[1]

            links.append(cls(name, path))

        return links

    @staticmethod
    def map_function(link):
        return link


class SpecialFile(Enum):

    # TODO: Bu yapının değişmesi lazım

    README = "README.md"
    CHANGELOG = "CHANGELOG.md"
    CODE_OF_CONDUCT = "CODE_OF_CONDUCT.md"
    CONTRIBUTING = "CONTRIBUTING.md"
    LICENSE = "LICENSE"

    def get_filepath(self, root: Path = Path.cwd()) -> Path:
        """Özel dosyalar için dosya yolu oluşturur

        Keyword Arguments:
            root {Path} -- Çalışma dizini (default: {Path.cwd()})

        Returns:
            Path -- Oluşturulan dosya yolu objesi

        Examples:
            >>> SpecialFile.README.get_filepath(Path('./src/ypackage')).as_posix()
            'src/ypackage/README.md'

            >>> SpecialFile.CHANGELOG.get_filepath(Path('./src/ypackage')).as_posix()
            'src/ypackage/CHANGELOG.md'

            >>> SpecialFile.CODE_OF_CONDUCT.get_filepath(Path('./src/ypackage')).as_posix()
            'src/ypackage/CODE_OF_CONDUCT.md'

            >>> SpecialFile.CONTRIBUTING.get_filepath(Path('./src/ypackage')).as_posix()
            'src/ypackage/CONTRIBUTING.md'

            >>> SpecialFile.LICENSE.get_filepath(Path('./src/ypackage')).as_posix()
            'src/ypackage/LICENSE'

        """
        return root / self.value
