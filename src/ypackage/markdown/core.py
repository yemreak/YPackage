from pathlib import Path
from typing import List, Tuple, Union

from deprecated import deprecated

from .. import common, filesystem
from .entity import Comment, Header, Indent, Link, SpecialFile


def generate_insert_position_strings(index_string: str) -> Tuple:
    """Verilen indeks için başlangıç ve bitiş index metni oluşturur

    Arguments:
        index_string {str} -- İndeks metni

    Returns:
        Tuple -- (başlangıç, bitiş) indeks metinleri

    Examples:
        >>> generate_insert_position_strings('Index')
        ('<!-- Index -->\\n\\n', '\\n\\n<!-- Index -->')
    """
    start_string = Comment(index_string) + "\n\n"
    end_string = "\n\n" + Comment(index_string)
    return start_string, end_string


def insert_to_file(
    string: str,
    filepath: Path,
    index_string: str,
) -> bool:
    start_string, end_string = generate_insert_position_strings(index_string)
    return filesystem.insert_to_file(string, filepath, start_string, end_string)


def create_markdown_file(filepath: Path, header: str = None):
    if not header:
        header = filepath.name

    content = generate_header_section(header, 1)
    filesystem.write_to_file(filepath, content)


def generate_substrings(content, index):
    index = str(Comment(index))
    return common.generate_substrings(content, index)


def find_all_headers(string, level=1) -> List[Header]:
    headers = Header.find_all(string, level=level)
    return headers


def find_all_headers_from_file(filepath, level=1) -> List[Header]:
    if not filesystem.must_exist(filepath):
        return []

    content = filesystem.read_file(filepath)
    headers = find_all_headers(content, level=level)
    return headers


def find_first_header(string, level=1) -> Union[Header, None]:
    header = Header.find_first(string, level=level)
    return header


def find_first_header_from_file(filepath, level=1) -> Union[Header, None]:
    if not filesystem.must_exist(filepath):
        return None

    content = filesystem.read_file(filepath)
    header = find_first_header(content, level=level)
    return header


def change_title_of_string(title: str, content: str) -> str:
    title_changed = False

    lines = common.parse_to_lines(content)
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

    return common.merge_lines(lines)


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

    Examples:
        >>> generate_name_for_file(Path('docs/README.md'))
        '📦 YPackage'
    """

    header = find_first_header_from_file(filepath)
    name = header.name if header else filepath.name

    return name


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
        single_line {bool} -- Tek satırda yer alan link '\\n' ekler (default: {False})


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
    root: Path = None,
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
        single_line {bool} -- Tek satırda yer alan link '\\n' ekler (default: {False})

    Returns:
        {str} -- Oluşturulan link metni

    Examples:
        >>> generate_file_link_string(           \
            Path('./src/ypackage/markdown.py'),  \
            name        = 'YPackage',            \
            root        = Path('src/ypackage/'), \
            indent      = Indent(2),             \
            is_list     = True,                  \
            single_line = True                   \
        )
        '    - [YPackage](markdown.py)\\n'
    """
    if not name:
        name = generate_name_for_file(filepath)

    if root:
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
        single_line {bool} -- Tek satırda yer alan link '\\n' ekler (default: {False})

    Returns:
        {str} -- Oluşturulan link metni

    Examples:
        >>> generate_dir_link_string(               \
            Path('src/ypackage/markdown.py'),       \
            Path('src'),                            \
            indent      = Indent(2),                \
            is_list     = True,                     \
            single_line = True                      \
        )
        '    [README.md](ypackage/markdown.py/README.md)\\n'
    """

    readmepath = SpecialFile.README.get_filepath(dirpath)

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
    lines = common.parse_to_lines(content)
    for i, line in enumerate(lines):
        oldlinks = Link.find_all(line)
        for oldlink in oldlinks:
            newlink = func(oldlink)
            lines[i] = lines[i].replace(str(oldlink), str(newlink))

    return common.merge_lines(lines)


def replace_in_links(content: str, old: str, new: str) -> str:

    def replace_link(link: Link):
        link.path = link.path.replace(old, new)
        return link

    map_links(content, replace_link)
