from os import makedirs, remove
from pathlib import Path
from shutil import rmtree

from ...ypackage.core.markdown import (create_markdownfile,
                                       find_all_headers_from_file,
                                       find_first_header_from_file,
                                       generate_nonmarkdown_fileliststring,
                                       map_links_in_markdownfile,
                                       update_markdownfile_by_commentstring,
                                       update_title_of_markdownfile)
from ...ypackage.model.markdown import Header, Link

TEMP_PATH = Path("temp.md")
WRONG_PATH = Path("./.")
TEMP_DIRPATH = Path("temp")
TEMP_FILES = [
    Path("hello.md"),
    Path("yunus.py"),
    Path("yunus.md"),
    Path("emre.py"),
    Path("yunuss.pdf")
]


def markdownfile(func):

    def inner(*args, **kwargs):
        content = (
            "---\n"
            "description: > -\n"
            "Computer Networks and Technologies için Vize notları\n"
            "- --\n"
            "\n"
            "# 📅 Vize \| CNaT\n"
            "<!--Index-->\n"
            "\n"
            "* [Chapter_1_V7.01.pdf](Chapter_1_V7.01.pdf)\n"
            "* [Chapter_2_V7.01.pdf](Chapter_2_V7.01.pdf)\n"
            "* [Chapter_3_V7.01.pdf](Chapter_3_V7.01.pdf)\n"
            "* [Chapter_4_V7.01.pdf](Chapter_4_V7.01.pdf)\n"
            "\n"
            "<!--Index-->\n"
            "## 🕐 Temp\n"
            "### 🕐 Temp2\n"
        )
        TEMP_PATH.write_text(content, encoding="utf-8")
        func(*args, **kwargs)
        remove(TEMP_PATH.as_posix())

    return inner


def customdir(func):

    def inner(*args, **kwargs):
        makedirs(TEMP_DIRPATH.as_posix(), exist_ok=True)
        for filepath in TEMP_FILES:
            filepath = TEMP_DIRPATH / filepath
            filepath.write_text("")

        func(*args, **kwargs)

        rmtree(TEMP_DIRPATH)

    return inner


def do(link: Link):
    link.name = "a" + link.name
    link.path = "b" + link.path


@markdownfile
def test_update_markdownfile_by_commentstring():
    string = "Hello"
    commentstring = "Index"

    assert update_markdownfile_by_commentstring(
        string,
        TEMP_PATH,
        commentstring
    ), "Değişiklik varsa True döndürmeli"

    assert TEMP_PATH.read_text(encoding="utf-8") == (
        "---\n"
        "description: > -\n"
        "Computer Networks and Technologies için Vize notları\n"
        "- --\n"
        "\n"
        "# 📅 Vize \| CNaT\n"
        "<!--Index-->\n"
        "\n"
        "Hello\n"
        "\n"
        "<!--Index-->\n"
        "## 🕐 Temp\n"
        "### 🕐 Temp2\n"
    )

    assert not update_markdownfile_by_commentstring(
        string,
        TEMP_PATH,
        " Index "
    ), "Değişiklik yapmadıysa False döndürmeli"


def test_create_markdownfile():
    assert create_markdownfile(TEMP_PATH)
    assert TEMP_PATH.exists()
    assert TEMP_PATH.read_text() == (
        "# Temp\n"
        "\n"
        ""
    )
    remove(TEMP_PATH.as_posix())

    assert create_markdownfile(TEMP_PATH, "🚀 test")
    assert TEMP_PATH.read_text(encoding="utf-8") == (
        "# 🚀 test\n"
        "\n"
        ""
    )
    remove(TEMP_PATH.as_posix())

    assert not create_markdownfile(WRONG_PATH)


@markdownfile
def test_find_all_headers_from_file():
    headers = find_all_headers_from_file(TEMP_PATH)
    assert headers == [
        Header(1, "📅 Vize \| CNaT"),
        Header(2, "🕐 Temp"),
        Header(3, "🕐 Temp2"),
    ]

    headers = find_all_headers_from_file(WRONG_PATH)
    assert headers == []


@markdownfile
def test_find_first_header_from_file():
    header = find_first_header_from_file(TEMP_PATH)
    assert header == Header(1, "📅 Vize \| CNaT")

    headers = find_all_headers_from_file(WRONG_PATH)
    assert not headers


@markdownfile
def test_update_title_of_markdownfile():
    assert update_title_of_markdownfile("Hello", TEMP_PATH)
    assert Header.find_first_in_markdownfile(TEMP_PATH).name == "Hello"


@customdir
def test_generate_nonmarkdown_fileliststring():
    content = generate_nonmarkdown_fileliststring(TEMP_DIRPATH)
    assert content == (
        "* [emre.py](emre.py)\n"
        "* [yunus.py](yunus.py)\n"
        "* [yunuss.pdf](yunuss.pdf)"
    )


@markdownfile
def test_map_links_in_markdownfile():
    assert map_links_in_markdownfile(TEMP_PATH, do)
    assert TEMP_PATH.read_text(encoding="utf-8") == (
        "---\n"
        "description: > -\n"
        "Computer Networks and Technologies için Vize notları\n"
        "- --\n"
        "\n"
        "# 📅 Vize \| CNaT\n"
        "<!--Index-->\n"
        "\n"
        "* [aChapter_1_V7.01.pdf](bChapter_1_V7.01.pdf)\n"
        "* [aChapter_2_V7.01.pdf](bChapter_2_V7.01.pdf)\n"
        "* [aChapter_3_V7.01.pdf](bChapter_3_V7.01.pdf)\n"
        "* [aChapter_4_V7.01.pdf](bChapter_4_V7.01.pdf)\n"
        "\n"
        "<!--Index-->\n"
        "## 🕐 Temp\n"
        "### 🕐 Temp2\n"
    )

    assert not map_links_in_markdownfile(WRONG_PATH, do)
