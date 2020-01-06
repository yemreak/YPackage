import os
from datetime import datetime
from pathlib import Path

from .filesystem import (find_level, listdir_grouped, read_file_by_url,
                         write_file)
from .github import (generate_raw_url_from_repo_url, get_github_raw_link,
                     list_commit_links, push_to_github)
from .markdown import (SpecialFile, check_links, create_header, create_link,
                       create_markdown_file, generate_dirlink,
                       generate_filelink, insert_file, make_linkstr)

DESCRIPTIPON_TEMPLATE = """---
description: >-
  {}
---

"""

SUMMARY_FILE = "SUMMARY.md"
SUMMARY_FILE_HEADER = "# Summary"

CHANGELOG_FILE = "CHANGELOG.md"
CHANGELOG_HEADER = u"👀 Neler değişti"
CONTRIBUTING_HEADER = u"💖 Katkıda Bulunma Rehberi"
GITHUB_USERNAME = "yedhrab"


def make_description(string: str) -> str:
    return DESCRIPTIPON_TEMPLATE.format(string)


def get_specialfile_header(specialfile: SpecialFile) -> str:
    if specialfile == SpecialFile.CHANGELOG_FILE:
        return CHANGELOG_HEADER
    elif specialfile == SpecialFile.CONTRIBUTING_FILE:
        return CONTRIBUTING_HEADER


def make_file_link(filepath: Path, root: Path = None, direct_link: bool = False) -> str:
    if root is None:
        root = filepath.parent

    if direct_link:
        return make_linkstr(filepath.name, get_github_raw_link(GITHUB_USERNAME, filepath))
    else:
        return create_link(filepath, root=root)


def generate_fs_link(
    lines: list, root: Path, startpath: Path = None, level_limit: int = -1, privates=[]
) -> list:
    # TODO: Buranın markdown'a aktarılması lazım
    # RES: Decalator kavramının araştırılması lazım olabilir

    def append_rootlink(lines: list, root: Path, level: int) -> str:
        dirlink = generate_dirlink(root, startpath=startpath, ilvl=level, isize=2)
        lines.append(dirlink)
        return lines

    def append_filelink(lines: list, fpath: Path, level: int):
        filelink = generate_filelink(fpath, startpath=startpath, ilvl=level, isize=2)
        lines.append(filelink)
        return lines

    def append_sublinks(lines: list, root: Path, level: int, dirs_only=False):
        dirs, files = listdir_grouped(root, privates=privates)
        for dpath in dirs:
            lines = generate_fs_link(lines, dpath, startpath=startpath, privates=privates)

        if not dirs_only:
            for fpath in files:
                if ".md" in fpath.name and SpecialFile.README_FILE.value not in fpath.name:
                    lines = append_filelink(lines, fpath, level)

        return lines

    def append_links(lines: list):
        nonlocal startpath
        if startpath is None:
            startpath = root
            level = find_level(root, startpath)
            if level_limit == -1 or level <= level_limit:
                lines = append_sublinks(lines, root, level + 1, dirs_only=True)
        else:
            level = find_level(root, startpath)
            if level_limit == -1 or level <= level_limit:
                lines = append_rootlink(lines, root, level)
                lines = append_sublinks(lines, root, level + 1)
        return lines

    return append_links(lines)


def get_summary_path(workdir: Path) -> Path:
    return workdir / SUMMARY_FILE


def create_summary_file(workdir: Path, debug=False):
    filepath = get_summary_path(workdir)
    if not filepath.exists():
        write_file(filepath, SUMMARY_FILE_HEADER + "\n\n", debug=debug)


def generate_summary_filestr(
    workdir: Path, level_limit: int = -1, privates=[], footer_path=None
):

    def append_header(filestr):

        def append_firstline(lines: list) -> list:
            headpath = SpecialFile.README_FILE.get_filepath(root=workdir)
            header_link = generate_filelink(headpath, startpath=workdir)
            lines.append(header_link)
            return lines

        def append_specialfiles(lines: list, *specialfiles: SpecialFile) -> list:
            for specialfile in specialfiles:
                specialfile_path = specialfile.get_filepath(workdir)
                if specialfile_path:
                    specialfile_link = generate_filelink(
                        specialfile_path,
                        header=get_specialfile_header(specialfile),
                        startpath=workdir,
                        ilvl=find_level(workdir, workdir) + 1,
                        isize=2
                    )
                    lines.append(specialfile_link)

            return lines

        lines = append_firstline([])
        lines = append_specialfiles(
            lines,
            SpecialFile.CHANGELOG_FILE,
            SpecialFile.CONTRIBUTING_FILE
        )

        filestr += "".join(lines)
        return filestr

    def append_markdown_links(filestr: str):
        lines = generate_fs_link([], workdir, level_limit=level_limit, privates=privates)
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
        workdir: Path, filestr: str, index: str = "Index", new_index: str = None,
        debug=False
):
    FILEPATH = get_summary_path(workdir)
    insert_file(FILEPATH, filestr, index=index, new_index=new_index, debug=debug)


def generate_summary(
    workdir, level_limit: int = -1, privates=[], footer_path=None,
    index: str = "Index", new_index: str = None
):
    filestr = generate_summary_filestr(
        workdir, level_limit=level_limit, privates=privates, footer_path=footer_path)
    insert_summary_file(workdir, filestr, index=index, new_index=new_index)


def generate_readmes(
    startpath: Path, level_limit: int = -1, privates=[], index="Index", header=None,
    new_index=None, clearify=False, debug=False, direct_link: bool = False
):
    # DEV: Ders notlarını README'ye ekleme direkt olarak dizin dosya oluştur
    def clear_private_dirs() -> list:
        return [d for d in dirs if not d.startswith('.') and d not in privates]

    def generate_links_for_nonmarkdowns(files) -> str:
        # OLD: Eski yapıdır, kontrollü bir şekilde kaldırılmalı
        filestr = ""
        links = []
        for f in files:
            if ".md" not in f:
                links.append(make_file_link(startpath / f, direct_link=direct_link))

        if bool(links):
            filestr = create_header(header, 2) if header else ""
            filestr += "".join(links)

        return filestr

    def generate_markdown_files_for_subitems(startpath: Path, clearify=False, debug=debug) -> str:
        # DEV: Aynı dizindekiler aynı dosya altına yazılacak
        for root, dirs, files in os.walk(startpath):
            # Sıralama her OS için farklı olabiliyor
            dirs.sort()
            files.sort()

            root = Path(root)
            if root == startpath:
                continue

            level = find_level(root, startpath)
            link_root = root.parent
            for _ in range(level - 1):
                link_root = link_root.parent

            links = []
            for f in files:
                subfilepath = root / f
                if ".md" not in f:
                    links.append(make_file_link(subfilepath, root=root, direct_link=direct_link))
                elif f != SpecialFile.README_FILE.value:
                    # DEV: Markdown dosyaları README'nin altına eklensin
                    links.append(create_link(subfilepath, root=link_root))

            if bool(links):
                filestr = create_header(header, 2) if header else ""
                filestr += "".join(links)

                filepath = SpecialFile.README_FILE.get_filepath(root=Path(root), force=True)
                if not os.path.exists(filepath):
                    oldfile = os.path.join(startpath, os.path.basename(root) + ".md")
                    if clearify:
                        try:
                            os.rename(oldfile, filepath)
                            print(oldfile + " -> " + filepath)
                        except Exception as e:
                            create_markdown_file(filepath, os.path.basename(root))
                            print(f"`{oldfile}` aktarılamadı. {e}")

                insert_file(filepath, filestr, index=index, force=True,
                            fileheader=os.path.basename(root), new_index=new_index, debug=debug)

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
        level = find_level(root, startpath)
        if level_limit == -1 or level < level_limit:
            filestr = generate_links_for_nonmarkdowns(files)
        elif level == level_limit:  # 1
            generate_markdown_files_for_subitems(root, clearify=clearify, debug=debug)
        else:
            if clearify and level > level_limit:
                readme_path = SpecialFile.README_FILE.get_filepath(root=root, force=True)
                if os.path.exists(readme_path):
                    os.remove(readme_path)
            continue

        if bool(filestr):
            filepath = SpecialFile.README_FILE.get_filepath(root=root, force=True)
            fileheader = os.path.basename(root)
            insert_file(filepath, filestr, index=index, force=True,
                        fileheader=fileheader, new_index=new_index, debug=debug)


def get_summary_url_from_repo_url(repo_url):
    return generate_raw_url_from_repo_url(repo_url) + "/" + SUMMARY_FILE


def read_summary_from_url(repo_url):
    raw_url = get_summary_url_from_repo_url(repo_url)
    return read_file_by_url(raw_url)


def check_summary(path):
    spath = os.path.join(path, SUMMARY_FILE)
    check_links(spath)


def create_changelog(
        path: Path, ignore_commits=[], repo_url=None, since: datetime = None,
        to: datetime = None, push=False, commit_msg=None, debug=False
):
    if not commit_msg:
        commit_msg = "💫 YGitBookIntegration"

    cpath = path / CHANGELOG_FILE

    oldfilestr = ""
    with cpath.open("r", encoding="utf-8") as file:
        oldfilestr = file.read()

    filestr = ""

    filestr = "# ✨ Değişiklikler"
    filestr += "\n\n"
    filestr += "## 📋 Tüm Değişiklikler"
    filestr += "\n\n"

    links = list_commit_links(path, repo_url=repo_url,
                              ignore_commits=ignore_commits + [commit_msg], since=since, to=to)
    filestr += "".join(links)

    if oldfilestr != filestr:
        write_file(cpath, filestr, debug=debug)

        if push:
            push_to_github(path, [cpath], commit_msg)
