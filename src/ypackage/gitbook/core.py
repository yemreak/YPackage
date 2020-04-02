import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List

from .. import common, filesystem, github, markdown

logger = logging.getLogger(__name__)

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
    index_string: str,
    ignored_folders: List[Path] = [],
    must_inserted=False
) -> bool:
    """Proje için markdown olmayan dosyaların bağlantılarının listesini README
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

    # TODO: Depth özelliği eklenmeli

    dirpaths = filesystem.list_nonhidden_dirs(projectpath)
    for dirpath in dirpaths:
        if dirpath.name not in ignored_folders:
            generate_readme_for_dir(
                dirpath,
                index_string,
                must_inserted=must_inserted
            )
            generate_readme_for_project(
                dirpath,
                index_string,
                ignored_folders=ignored_folders,
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

    content = generate_nonmarkdown_filelist_string(dirpath)
    if not content:
        return False

    readme_path = markdown.readme_path_for_dir(dirpath)
    if not readme_path.exists():
        markdown.create_markdown_file(readme_path, header=dirpath.name)

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
    return markdown.insert_to_file(
        string,
        filepath,
        index_string,
        must_inserted=True
    )


def generate_filelink_string(
    filepath: Path,
    root: Path = None,
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
        >>> generate_file_link_string(    \
            Path('./docs/README.md'),     \
            root = Path('./docs'),        \
            single_line=True,             \
            is_list=True,                 \
        )
        '- [📦 YPackage](README.md)\\n'
        >>> generate_file_link_string(    \
            Path('./docs/README.md'),     \
            github_link = True            \
        )
        '[📦 YPackage](https://github.com/yedhrab/YPackage/raw/master/docs/README.md)'
    """

    if github_link:
        name = markdown.generate_name_for_file(filepath)
        rawlink = github.get_github_raw_link(
            GITHUB_USERNAME,
            "YPackage" if Path.cwd().name == "project" else Path.cwd().name,  # TODO: burayı düzelt
            filepath
        )
        return markdown.generate_link_string(
            name,
            rawlink,
            indent_level=indent_level,
            single_line=single_line,
            is_list=is_list
        )

    return markdown.generate_filelink_string(
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
        >>> summary_path_for_dir(Path('.')).as_posix()
        'SUMMARY.md'
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
        False
    """
    summary_path = summary_path_for_project(projectpath)
    return summary_path.exists()


def create_summary_file_for_project(projectpath: Path) -> bool:
    content = generate_summary_filelist_string(projectpath)
    summary_path = summary_path_for_project(projectpath)
    return filesystem.write_to_file(summary_path, content)


def generate_nonmarkdown_filelist_string(dirpath: Path) -> str:
    # TODO: Markdown içine alınabilir
    nonmarkdown_filepaths = markdown.list_nonmarkdown_files(dirpath)

    if not nonmarkdown_filepaths:
        return ""

    filelink_strings = []
    for filepath in nonmarkdown_filepaths:
        filelink_strings.append(
            generate_filelink_string(
                filepath,
                root=dirpath,
                is_list=True
            )
        )

    content = common.merge_lines(filelink_strings)
    return content


def generate_description_section(string: str) -> str:
    """GitBook için açıklama metni oluşturur

    Arguments:
        string {str} -- Açıklama metni

    Returns:
        str -- Oluşturulan açıklama metni alanı
    Examles:
        >>> generate_description('Selam')
        '---\\ndescription: >-\\n Selam\\n---\\n\\n'
    """
    return DESCRIPTION_TEMPLATE.format(string)


def generate_summary_filelist_string(projectpath: Path) -> str:
    content = generate_summary_header_section()
    content += generate_summary_filelinks_string(
        projectpath,
        projectpath,
        indent_level=0
    )

    return content


def generate_summary_filelinks_string(
        projectpath: Path,
        dirpath: Path,
        indent_level=1
) -> str:
    content = ""

    readme_path = markdown.readme_path_for_dir(dirpath)
    content += generate_filelink_string(
        readme_path,
        root=projectpath,
        indent_level=indent_level,
        single_line=True,
        is_list=True
    )

    mpaths = markdown.list_markdown_files(dirpath)
    if readme_path in mpaths:
        mpaths.remove(readme_path)

    for mpath in mpaths:
        content += generate_filelink_string(
            mpath,
            root=projectpath,
            indent_level=indent_level + 1,
            single_line=True,
            is_list=True
        )

    directories = filesystem.list_nonhidden_dirs(dirpath)
    for directory in directories:
        content += generate_summary_filelinks_string(
            projectpath,
            directory,
            indent_level=indent_level + 1
        )

    return content


def generate_summary_header_section() -> str:
    """SUMMARY dosyası için başlık metnin oluşturur

    Returns:
        str -- Oluşturulan metin

    Examles:
        >>> generate_summary_header_section()
        '# Tablo of Contents\n\n'
    """
    header_section = markdown.generate_header_section(SUMMARY_FILE_HEADER, 1)
    return header_section


def generate_summary_for_dir(
    projectpath: Path,
    index_string: str,
    must_inserted=False
) -> bool:
    """Verilen dizin için markdown dosyalarının bağlantılarının listesini SUMMARY
    dosyasına verilen indeksler arasına yerleştirir

    Arguments:
        projectpath {Path} -- Proje dizini yolu
        index_string {str} -- [description]

    Keyword Arguments:
        must_inserted {bool} -- [description] (default: {False})

    Returns:
        {bool} -- Değişim varsa True
    """

    content = generate_summary_filelist_string(projectpath)
    if not content:
        return False

    summary_path = summary_path_for_project(projectpath)
    if not summary_path.exists():
        create_summary_file(summary_path)

    return insert_to_file(
        content,
        summary_path,
        index_string,
        must_inserted=True
    )


# -------------------- OLD ONES --------------------------


def get_specialfile_header(specialfile: markdown.SpecialFile) -> str:
    if specialfile == markdown.entity.SpecialFile.CHANGELOG:
        return CHANGELOG_HEADER
    elif specialfile == markdown.SpecialFile.CONTRIBUTING:
        return CONTRIBUTING_HEADER


def generate_fs_link(
        lines: list, root: Path, startpath: Path = None, depth_limit: int = -1, ignore_folders=[]
) -> list:
    # TODO: Buranın markdown'a aktarılması lazım
    # RES: Decalator kavramının araştırılması lazım olabilir

    def append_rootlink(lines: list, root: Path, level: int) -> str:
        dirlink_string = markdown.generate_dirlink_string(
            root,
            root=startpath,
            indent=markdown.Indent(level),
            is_list=True,
            single_line=True
        )
        lines.append(dirlink_string)
        return lines

    def append_filelink(lines: list, fpath: Path, level: int):
        filelink_string = markdown.generate_filelink_string(
            fpath,
            root=startpath,
            indent=markdown.Indent(level),
            is_list=True,
            single_line=True
        )
        lines.append(filelink_string)
        return lines

    def append_sublinks(lines: list, root: Path, level: int, dirs_only=False):
        dirs, files = filesystem.listdir_grouped(root, ignore_folders=ignore_folders)
        for dpath in dirs:
            lines = generate_fs_link(lines, dpath, startpath=startpath,
                                     ignore_folders=ignore_folders)

        if not dirs_only:
            for fpath in files:
                if all([
                    ".md" in fpath.name,
                    markdown.SpecialFile.README.value not in fpath.name
                ]):
                    lines = append_filelink(lines, fpath, level)

        return lines

    def append_links(lines: list):
        nonlocal startpath
        if startpath is None:
            startpath = root
            level = filesystem.find_level(root, startpath)
            if depth_limit == -1 or level <= depth_limit:
                lines = append_sublinks(lines, root, level + 1, dirs_only=True)
        else:
            level = filesystem.find_level(root, startpath)
            if depth_limit == -1 or level <= depth_limit:
                lines = append_rootlink(lines, root, level)
                lines = append_sublinks(lines, root, level + 1)
        return lines

    return append_links(lines)


def get_summary_path(workdir: Path) -> Path:
    return workdir / SUMMARY_FILE


def create_summary_file(workdir: Path):
    filepath = get_summary_path(workdir)
    if not filepath.exists():
        filesystem.write_to_file(filepath, SUMMARY_FILE_HEADER + "\n\n")


def generate_summary_filestr(
        workdir: Path, depth_limit: int = -1, ignore_folders=[], footer_path=None
):

    def append_header(filestr):

        def append_firstline(lines: list) -> list:
            headpath = markdown.SpecialFile.README.get_filepath(root=workdir)
            headerlink_string = markdown.generate_filelink_string(
                headpath,
                root=workdir,
                is_list=True,
                single_line=True
            )
            lines.append(headerlink_string)
            return lines

        def append_specialfiles(lines: list, *specialfiles: markdown.SpecialFile) -> list:
            for specialfile in specialfiles:
                specialfile_path = specialfile.get_filepath(workdir)
                if specialfile_path:
                    level = filesystem.find_level(workdir, workdir) + 1
                    specialfilelink_string = markdown.generate_filelink_string(
                        specialfile_path,
                        name=get_specialfile_header(specialfile),
                        root=workdir,
                        indent=markdown.Indent(level),
                        is_list=True,
                        single_line=True
                    )
                    lines.append(specialfilelink_string)

            return lines

        lines = append_firstline([])
        lines = append_specialfiles(
            lines,
            markdown.SpecialFile.CHANGELOG,
            markdown.SpecialFile.CONTRIBUTING
        )

        filestr += "".join(lines)
        return filestr

    def append_markdown_links(filestr: str):
        lines = generate_fs_link([], workdir, depth_limit=depth_limit,
                                 ignore_folders=ignore_folders)
        filestr += "".join(lines)
        return filestr

    def append_footer(filestr: str):
        if footer_path and os.path.isfile(footer_path):
            with open(os.path.join(footer_path), "r", encoding="utf-8") as file:
                filestr = "\n" + \
                    file.read()
        return filestr

    filestr = append_header("")
    filestr = append_markdown_links(filestr)
    filestr = append_footer(filestr)

    return filestr


def insert_summary_file(
    workdir: Path, filestr: str, index: str = "Index", new_index: str = None
):
    FILEPATH = get_summary_path(workdir)
    markdown.insert_to_file(FILEPATH, filestr, index_string=index)
    # new_index=new_index


def generate_summary(
        workdir, depth_limit: int = -1, ignore_folders=[], footer_path=None,
        index: str = "Index", new_index: str = None
):
    filestr = generate_summary_filestr(
        workdir, depth_limit=depth_limit, ignore_folders=ignore_folders, footer_path=footer_path)
    insert_summary_file(workdir, filestr, index=index, new_index=new_index)


def generate_readmes(
        startpath: Path, depth_limit: int = -1, ignore_folders=[], index="Index", header=None,
        new_index=None, clearify=False, github_link: bool = False
):
    # DEV: Ders notlarını README'ye ekleme direkt olarak dizin dosya oluştur
    def clear_private_dirs() -> list:
        return [d for d in dirs if not d.startswith('.') and d not in ignore_folders]

    def generate_links_for_nonmarkdowns(files) -> str:
        # OLD: Eski yapıdır, kontrollü bir şekilde kaldırılmalı
        filestr = ""
        links = []
        for f in files:
            if ".md" not in f:
                link_string = generate_filelink_string(startpath / f, github_link=github_link)
                links.append(link_string)

        if bool(links):
            filestr = markdown.generate_header_section(header, 2) if header else ""
            filestr += "".join(links)

        return filestr

    def generate_markdown_files_for_subitems(startpath: Path, clearify=False) -> str:
        # DEV: Aynı dizindekiler aynı dosya altına yazılacak
        for root, dirs, files in os.walk(startpath):
            # Sıralama her OS için farklı olabiliyor
            dirs.sort()
            files.sort()

            root = Path(root)
            if root == startpath:
                continue

            level = filesystem.find_level(root, startpath)
            link_root = root.parent
            for _ in range(level - 1):
                link_root = link_root.parent

            links = []
            for f in files:
                subfilepath = root / f
                if ".md" not in f:
                    link_string = generate_filelink_string(
                        subfilepath,
                        root=root,
                        github_link=github_link
                    )
                    links.append(link_string)
                elif f != markdown.SpecialFile.README.value:
                    # DEV: Markdown dosyaları README'nin altına eklensin

                    subfilepath = subfilepath.relative_to(link_root)
                    subfilepath_str = subfilepath.as_posix()

                    link = markdown.Link(subfilepath.name, subfilepath_str)
                    links.append(link.to_str(one_line=True))

            if bool(links):
                filestr = markdown.generate_header_section(header, 2) if header else ""
                filestr += "".join(links)

                filepath = markdown.SpecialFile.README.get_filepath(root=Path(root))
                if not os.path.exists(filepath):
                    oldfile = os.path.join(startpath, os.path.basename(root) + ".md")
                    if clearify:
                        try:
                            os.rename(oldfile, filepath)

                            logger.info(oldfile + " -> " + filepath + " taşındı")
                        except Exception as e:
                            markdown.create_markdown_file(filepath, os.path.basename(root))
                            logger.error(f"{oldfile} aktarılamadı. {e}")

                markdown.insert_file(filepath, filestr, index=index, force=True,
                                     fileheader=os.path.basename(root), new_index=new_index)

    filestr = ""
    for root, dirs, files in os.walk(startpath):
        # Remove private directories
        dirs[:] = clear_private_dirs()

        # Sıralama her OS için farklı olabiliyor
        dirs.sort()
        files.sort()

        root = Path(root)

        # Skip startpath
        if root == startpath:
            continue

        filestr = ""
        level = filesystem.find_level(root, startpath)
        if depth_limit == -1 or level < depth_limit:
            filestr = generate_links_for_nonmarkdowns(files)
        elif level == depth_limit:  # 1
            generate_markdown_files_for_subitems(root, clearify=clearify)
        else:
            if clearify and level > depth_limit:
                readme_path = markdown.SpecialFile.README.get_filepath(root=root)
                if os.path.exists(readme_path):
                    os.remove(readme_path)
            continue

        if bool(filestr):
            filepath = markdown.SpecialFile.README.get_filepath(root=root)
            fileheader = os.path.basename(root)

            if filepath.exists():
                markdown.create_markdown_file(filepath, fileheader)

            markdown.insert_to_file(
                filestr,
                filepath,
                index_string=index
            )


def get_summary_url_from_repo_url(repo_url):
    return github.generate_raw_url_from_repo_url(repo_url) + "/" + SUMMARY_FILE


def read_summary_from_url(repo_url):
    raw_url = get_summary_url_from_repo_url(repo_url)
    return filesystem.read_file_from_url(raw_url)


def check_summary(path):
    spath = os.path.join(path, SUMMARY_FILE)
    markdown.check_links(spath)


def create_changelog(
    path: Path, ignore_commits=[], repo_url=None, since: datetime = None,
    to: datetime = None, push=False, commit_msg=None
):
    if not commit_msg:
        commit_msg = "💫 YGitBookIntegration"

    cpath = markdown.SpecialFile.CHANGELOG.get_filepath(path)

    filestr = "# " + CHANGELOG_HEADER
    filestr += "\n\n"
    filestr += "## 📋 Tüm Değişiklikler"
    filestr += "\n\n"

    links = github.list_commit_links(
        path, repo_url=repo_url, since=since, to=to,
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
