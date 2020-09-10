import re
from copy import deepcopy
from enum import Enum
from pathlib import Path
from typing import Any, Callable, List, Optional, Union

from ..core import filesystem
from . import common


class Base(common.Base):

    REGEX = ""
    TEMPLATE = ""

    def __str__(self):
        if not self.TEMPLATE:
            raise NotImplementedError

        return self.TEMPLATE.format(*(vars(self).values()))

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
            raise TypeError

    def to_str(self) -> str:
        return self.__str__()

    @classmethod
    def remove_all(cls, content: str) -> str:
        return re.sub(cls.REGEX, "", content)

    @classmethod
    def find_all(cls, content: str) -> List[Any]:
        if not cls.REGEX:
            raise NotImplementedError

        anylist = []

        results = re.findall(cls.REGEX, content, re.MULTILINE)
        for result in results:
            if not isinstance(result, tuple):
                result = result,

            anylist.append(cls(*result))

        return anylist

    @classmethod
    def find_first(cls, content: str) -> Optional[Any]:
        results = cls.find_all(content)
        if results:
            return results[0]

    @classmethod
    def find_all_in_markdownfile(cls, filepath: Path) -> List[Any]:
        content = filesystem.read_file(filepath)
        return cls.find_all(content)

    @classmethod
    def find_first_in_markdownfile(cls, filepath: Path) -> List[Any]:
        content = filesystem.read_file(filepath)
        return cls.find_first(content)

    @classmethod
    def map(cls, content: str, do: Callable[[Any], None]) -> str:
        # BUG: Tekrarlı değişiklikler oluyor (Indent için '  ' 2 kere değişiyor)
        anylist = cls.find_all(content)
        for anyobject in anylist:
            oldone = deepcopy(anyobject)
            do(anyobject)
            content = content.replace(oldone.to_str(), anyobject.to_str())

        return content

    @classmethod
    def map_in_file(cls, filepath: Path, do: Callable[[Any], None]) -> bool:
        content = filesystem.read_file(filepath)
        content = cls.map(content, do)
        return filesystem.write_to_file(filepath, content)


class Comment(Base):

    REGEX = r"<!--(.*?)-->"
    TEMPLATE = "<!--{}-->"

    def __init__(self, content: str):
        if not isinstance(content, str):
            content = str(content)

        if "-->" in content:
            raise ValueError("--> metni içeremez")

        self.content = content.strip()


class Indent(Base):

    REGEX = r"^(\s+)"

    TAB_SIZE = 2
    CHAR = " "

    def __init__(self, level: Union[str, int]):
        if isinstance(level, str):
            self.level = level.count(self.CHAR * self.TAB_SIZE)
        elif isinstance(level, int):
            if level < 0:
                raise ValueError("Pozitif tam sayı girilmelidir")

            self.level = level
        else:
            raise TypeError("Metin veya pozitif tam sayı girilmelidir")

    def __str__(self):
        return Indent.CHAR * self.level * self.TAB_SIZE

    @classmethod
    def map(cls, content, do):
        raise NotImplementedError


class Header(Base):

    REGEX = r"(#{1,6}) *(.*)"
    TEMPLATE = "{} {}"

    CHAR = "#"

    def __init__(self, level: int, name: str):

        if isinstance(level, str):
            self.level = level.count(self.CHAR)
        elif isinstance(level, int):
            if level < 1:
                raise TypeError("1 den küçük olamaz")

            self.level = level
        else:
            raise TypeError

        if not isinstance(name, str):
            name = str(name)

        self.name = name.strip()

    def __str__(self):
        return self.TEMPLATE.format(self.level * self.CHAR, self.name)

    def to_str(self, is_section=False):
        string = self.__str__()
        if is_section:
            string += "\n\n"
        return string


class Link(Base):

    REGEX = r"\[([^\[\]]+)\]\(([^\(\)]+)\)"
    TEMPLATE = "[{}]({})"

    def __init__(self, name: str, path: str):
        self.name = name.strip()
        self.path = path.strip()

    def to_str(
        self,
        indent: Optional[Indent] = None,
        is_list: Optional[bool] = None,
        single_line: Optional[bool] = None
    ) -> str:
        string = indent.to_str() if indent else ""
        string += "* " if is_list else ""
        string += self.__str__()
        string += "\n" if single_line else ""

        return string

    def is_url(self):
        return "https://" in self.path or "http://" in self.path

    @property
    def filepath(self) -> Path:
        if not self.is_url():
            return Path(self.path)


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
            root {Path} - - Çalışma dizini(default: {Path.cwd()})

        Returns:
            Path - - Oluşturulan dosya yolu objesi

        Examples:
            >> > SpecialFile.README.get_filepath(Path('./src/ypackage')).as_posix()
            'src/ypackage/README.md'

            >> > SpecialFile.CHANGELOG.get_filepath(Path('./src/ypackage')).as_posix()
            'src/ypackage/CHANGELOG.md'

            >> > SpecialFile.CODE_OF_CONDUCT.get_filepath(Path('./src/ypackage')).as_posix()
            'src/ypackage/CODE_OF_CONDUCT.md'

            >> > SpecialFile.CONTRIBUTING.get_filepath(Path('./src/ypackage')).as_posix()
            'src/ypackage/CONTRIBUTING.md'

            >> > SpecialFile.LICENSE.get_filepath(Path('./src/ypackage')).as_posix()
            'src/ypackage/LICENSE'

        """
        return root / self.value
