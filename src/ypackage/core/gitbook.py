import logging
from pathlib import Path
from typing import List, Optional

from . import filesystem, github, markdown

logger = logging.getLogger(__name__)

# TODO: Class yapısına alınmalı
DESCRIPTION_TEMPLATE = """---
description: >-
  {}
---

"""

SUMMARY_FILE = "SUMMARY.md"
SUMMARY_FILE_HEADER = "📋 Table of Contents"

CHANGELOG_HEADER = u"👀 Neler değişti"
CONTRIBUTING_HEADER = u"💖 Katkıda Bulunma Rehberi"
GITHUB_USERNAME = "yedhrab"


def generate_readme_for_project(
    projectpath: Path,
    commentindex: str,
    ignore: List[str] = [],
    must_inserted=False
) -> bool:
    """Proje için markdown olmayan dosyaların bağlantılarının listesini README
    dosyasına verilen indeksler arasına yerleştirir

    Arguments:
        dirpath {Path} -- Dizin yolu objesi
        commentindex {str} -- İndeks metni
        ignore {List[str]} -- Görmezden gelinecek dizin isimleri

    Keyword Arguments:
        must_inserted {bool} -- Dosyada indeks olmaza, dosya sonuna indeks ile ekler \
            (default: {False})

    Returns:
        {bool} -- Değişim varsa True
    """

    # TODO: Depth özelliği eklenmeli
    dirpaths = filesystem.list_nonhidden_dirs(projectpath)
    for dirpath in dirpaths:
        if dirpath.name not in ignore:
            generate_readme_for_dir(
                dirpath,
                commentindex,
                must_inserted=must_inserted
            )
            generate_readme_for_project(
                dirpath,
                commentindex,
                ignore=ignore,
                must_inserted=must_inserted
            )


def generate_readme_for_dir(dirpath: Path, index_string: str, must_inserted=False) -> bool:
    """Dizin için markdown olmayan dosyaların bağlantılarının listesini README
    dosyasına verilen indeksler arasına yerleştirir

    Arguments:
        dirpath {Path} -- Dizin yolu objesi
        index_string {str} -- İndeks metni

    Keyword Arguments:
        must_inserted {bool} -- Dosyada indeks olmaza, dosya sonuna indeks ile ekler \
            (default: {False})

    Returns:
        {bool} -- Değişim varsa True
    """

    content = markdown.generate_nonmarkdown_fileliststring(dirpath)
    if not content:
        return False

    readme_path = markdown.readmepath_for_dir(dirpath)
    if not readme_path.exists():
        markdown.create_markdownfile(readme_path, header=dirpath.name)

    return insert_to_file(
        content,
        readme_path,
        index_string,
        must_inserted=must_inserted
    )


def insert_to_file(
    string: str,
    filepath: Path,
    index_string: str,
    must_inserted=False
) -> bool:
    """Verilen metni markdown dosyasına indeks metinlerini yorum satırlarına alarak ekler

    Arguments:
        string {str} -- Yerleştirilecek metin
        filepath {Path} -- Dosya yolu objesi
        index_string {str} -- Başlangıç metni

    Keyword Arguments:
        must_inserted {bool} -- Verilen indeksler bulunamazsa dosyanın sonuna indeksler ile ekler

    Returns:
        bool -- Dosyada değişiklik olduysa True
    """
    return markdown.update_markdownfile_by_commentstring(
        string,
        filepath,
        index_string,
        must_inserted=True
    )


def generate_filelink_string(
    filepath: Path,
    root: Optional[Path] = None,
    github_link=False,
    indent_level=0,
    single_line=False,
    is_list=False
) -> str:
    """GitBook için dosya link metni oluşturma

    Arguments:
        filepath {Path} -- Dosya yolu objesi

    Keyword Arguments:
        root {Path} -- Çalışma dizini yolu objesi (default: {Path.cwd()})
        github_link {bool} -- GitHub adresini işaret etme (default: {False})

    Returns:
        str -- Oluşturulan link metni

    Examples:
        >>> generate_filelink_string(    \
            Path('./docs/README.md'),     \
            root = Path('./docs'),        \
            single_line=True,             \
            is_list=True,                 \
        )
        '* [📦 YPackage](README.md)\\n'
        >>> generate_filelink_string(    \
            Path('./docs/README.md'),     \
            github_link = True            \
        )
        '[📦 YPackage](https://github.com/yedhrab/YPackage/raw/master/docs/README.md)'
    """

    if github_link:
        name = markdown.generate_name_for_markdownfile(filepath)
        rawlink = github.get_github_raw_link(
            GITHUB_USERNAME,
            "YPackage" if Path.cwd().name == "project" else Path.cwd().name,  # TODO: burayı düzelt
            filepath
        )
        return markdown.generate_linkstring(
            name,
            rawlink,
            indent_level=indent_level,
            single_line=single_line,
            is_list=is_list
        )

    return markdown.generate_filelinkstring(
        filepath,
        root=root,
        indent_level=indent_level,
        single_line=single_line,
        is_list=is_list
    )


def summary_path_for_project(projectpath: Path) -> Path:
    """Dizin için SUMMARY dosya yolu objesi oluşturur

    Arguments:
        projectpath {Path} -- Dizin

    Returns:
        Path -- README dosya yolu objesi

    Examples:
        >>> summary_path_for_project(Path('.')).as_posix()
        'SUMMARY.md'
        >>> summary_path_for_project(Path('docs')).as_posix()
        'docs/SUMMARY.md'
    """

    # TODO: Buraya uygun bir yapı lazım
    return projectpath / SUMMARY_FILE


def has_summary_file(projectpath: Path) -> bool:
    """Verilen dizinde SUMMARY dosyasını varlığını kontrol eder

    Arguments:
        projectpath {Path} -- Kontrol edilecek dizin

    Returns:
        bool -- Varsa True

    Examples:
        >>> has_summary_file(Path('docs'))
        True
        >>> has_summary_file(Path('.'))
        False
    """
    summary_path = summary_path_for_project(projectpath)
    return summary_path.exists()


def generate_description_section(string: str) -> str:
    """GitBook için açıklama metni oluşturur

    Arguments:
        string {str} -- Açıklama metni

    Returns:
        str -- Oluşturulan açıklama metni alanı
    Examles:
        >>> generate_description_section('Selam')
        '---\\ndescription: >-\\n  Selam\\n---\\n\\n'
    """
    return DESCRIPTION_TEMPLATE.format(string)


def generate_summary_fileliststring(projectpath: Path, ignore: List[str] = []) -> str:
    return generate_summary_filelinks_string(
        projectpath,
        projectpath,
        indent_level=0,
        ignore=ignore
    )


def generate_summary_filelinks_string(
    projectpath: Path,
    dirpath: Path,
    indent_level: int = 0,
    ignore: List[str] = []
) -> str:
    content = ""

    readme_path = markdown.readmepath_for_dir(dirpath)
    content += generate_filelink_string(
        readme_path,
        root=projectpath,
        indent_level=indent_level - 1 if indent_level else 0,
        single_line=True,
        is_list=True
    )

    mpaths = markdown.list_markdownfiles(dirpath)
    if readme_path in mpaths:
        mpaths.remove(readme_path)

    for mpath in mpaths:
        if mpath.name not in ignore:
            content += generate_filelink_string(
                mpath,
                root=projectpath,
                indent_level=indent_level,
                single_line=True,
                is_list=True
            )

    directories = filesystem.list_nonhidden_dirs(dirpath)
    for directory in directories:
        if directory.name not in ignore:
            content += generate_summary_filelinks_string(
                projectpath,
                directory,
                indent_level=indent_level + 1,
                ignore=ignore
            )

    return content


def generate_summary_headersection() -> str:
    """SUMMARY dosyası için başlık metnin oluşturur

    Returns:
        str -- Oluşturulan metin

    Examles:
        >>> generate_summary_headersection()
        '# 📋 Table of Contents\\n\\n'
    """
    header_section = markdown.generate_headersection(1, SUMMARY_FILE_HEADER)
    return header_section


def generate_summary_for_project(
    projectpath: Path,
    index_string: str,
    ignore: List[str] = [],
    must_inserted=False
) -> bool:
    """Verilen dizin için markdown dosyalarının bağlantılarının listesini SUMMARY
    dosyasına verilen indeksler arasına yerleştirir

    Arguments:
        projectpath {Path} -- Proje dizini yolu
        index_string {str} -* [description]
        ignore {List[str]} -- Görmezden gelinecek dizin isimleri

    Keyword Arguments:
        must_inserted {bool} -* [description] (default: {False})

    Returns:
        {bool} -- Değişim varsa True
    """

    summary_path = summary_path_for_project(projectpath)
    if not all([summary_path.exists(), filesystem.read_file(summary_path)]):
        create_summary_file(summary_path)

    content = generate_summary_fileliststring(
        projectpath,
        ignore=ignore
    )
    if not content:
        return False

    return insert_to_file(
        content,
        summary_path,
        index_string,
        must_inserted=True
    )


def create_summary_file(filepath: Path) -> bool:
    """SUMMARY dosyası oluşturur

    Arguments:
        filepath {Path} -- Dosya yolu objesi

    Returns:
        bool -- Oluşturma başarılı ise True
    """

    return markdown.create_markdownfile(filepath, header=SUMMARY_FILE_HEADER)


# -------------------- OLD ONES --------------------------


def get_summary_url_from_repo_url(repo_url):
    return github.generate_raw_url_from_repo_url(repo_url) + "/" + SUMMARY_FILE


def read_summary_from_url(repo_url):
    raw_url = get_summary_url_from_repo_url(repo_url)
    return filesystem.read_file_from_url(raw_url)


def create_changelog(
    path: Path, ignore_commits=[], repo_url=None, push=False, commit_msg=None
):
    if not commit_msg:
        commit_msg = "💫 YGitBookIntegration"

    cpath = markdown.SpecialFile.CHANGELOG.get_filepath(path)

    filestr = "# " + CHANGELOG_HEADER
    filestr += "\n\n"
    filestr += "## 📋 Tüm Değişiklikler"
    filestr += "\n\n"

    links = github.list_commit_links(
        path, repo_url=repo_url,
        ignore_commits=ignore_commits + [commit_msg]
    )

    if not links:
        return

    filestr += "\n".join(links)

    oldfilestr = ""
    if cpath.exists():
        with cpath.open("r", encoding="utf-8") as file:
            oldfilestr = file.read()

    if oldfilestr != filestr:
        filesystem.write_to_file(cpath, filestr)

        if push:
            github.push_to_github(path, [cpath], commit_msg)
