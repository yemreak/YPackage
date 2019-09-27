import os
from urllib.parse import quote
from .filesystem import insert_file as fs_insert_file


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


def relativepath(path: str, root=os.getcwd()) -> str:
    """ Statik yol verisini dinamik yol verisine dönüştürme

    Args:
        pathname (str): Yol ismi

    Returns:
        str: Dönüştürülen metin
    """

    return path.replace(root, '.')


def encodedpath(path: str) -> str:
    """ Verilen yolu url formatında kodlama

    Windows için gelen '\\' karakteri '/' karakterine çevrilir

    Args:
        pathname (str): Yol ismi

    Returns:
        str: Kodlanmış metin
    """

    return quote(path.replace("\\", "/"))


def create_indent(level, size=4):
    return ' ' * size * (level)


def create_link(path: str, header=None, root=os.getcwd()) -> str:
    """Verilen yola uygun kodlanmış markdown linki oluşturma

    Args:
        pathname (str): Yol
        header (str): Link

    Returns:
        str: Oluşturulan link metni
    """

    pathname = barename(path) if not header else header
    path = relativepath(path, root=root)
    path = encodedpath(path)

    link = f"- [{pathname}]({path})\n"
    return link


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
