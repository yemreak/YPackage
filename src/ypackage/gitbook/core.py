import logging
import os
from datetime import datetime
from pathlib import Path

from .. import filesystem, github, markdown

logger = logging.getLogger(__name__)

DESCRIPTIPON_TEMPLATE = """---
description: >-
  {}
---

"""

SUMMARY_FILE = "SUMMARY.md"
SUMMARY_FILE_HEADER = "# Summary"

CHANGELOG_FILE = "changelog.md"
CHANGELOG_HEADER = u"👀 Neler değişti"
CONTRIBUTING_HEADER = u"💖 Katkıda Bulunma Rehberi"
GITHUB_USERNAME = "yedhrab"


def generate_description(string: str) -> str:
    return DESCRIPTIPON_TEMPLATE.format(string)


def get_specialfile_header(specialfile: markdown.SpecialFile) -> str:
    if specialfile == markdown.SpecialFile.CHANGELOG_FILE:
        return CHANGELOG_HEADER
    elif specialfile == markdown.SpecialFile.CONTRIBUTING_FILE:
        return CONTRIBUTING_HEADER


def make_file_link(filepath: Path, root: Path = None, direct_link: bool = False) -> str:
    if root is None:
        root = filepath.parent

    if direct_link:
        return markdown.make_linkstr(
            filepath.name,
            github.get_github_raw_link(GITHUB_USERNAME, filepath)
        )
    else:
        return markdown.create_link(filepath, root=root)


def generate_fs_link(
        lines: list, root: Path, startpath: Path = None, depth_limit: int = -1, ignore_folders=[]
) -> list:
    # TODO: Buranın markdown'a aktarılması lazım
    # RES: Decalator kavramının araştırılması lazım olabilir

    def append_rootlink(lines: list, root: Path, level: int) -> str:
        dirlink = markdown.generate_dirlink(root, startpath=startpath, ilvl=level, isize=2)
        lines.append(dirlink)
        return lines

    def append_filelink(lines: list, fpath: Path, level: int):
        filelink = markdown.generate_filelink(fpath, startpath=startpath, ilvl=level, isize=2)
        lines.append(filelink)
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
                    markdown.SpecialFile.README_FILE.value not in fpath.name
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
        filesystem.write_file(filepath, SUMMARY_FILE_HEADER + "\n\n")


def generate_summary_filestr(
        workdir: Path, depth_limit: int = -1, ignore_folders=[], footer_path=None
):

    def append_header(filestr):

        def append_firstline(lines: list) -> list:
            headpath = markdown.SpecialFile.README_FILE.get_filepath(root=workdir)
            header_link = markdown.generate_filelink(headpath, startpath=workdir)
            lines.append(header_link)
            return lines

        def append_specialfiles(lines: list, *specialfiles: markdown.SpecialFile) -> list:
            for specialfile in specialfiles:
                specialfile_path = specialfile.get_filepath(workdir)
                if specialfile_path:
                    specialfile_link = markdown.generate_filelink(
                        specialfile_path,
                        header=get_specialfile_header(specialfile),
                        startpath=workdir,
                        ilvl=filesystem.find_level(workdir, workdir) + 1,
                        isize=2
                    )
                    lines.append(specialfile_link)

            return lines

        lines = append_firstline([])
        lines = append_specialfiles(
            lines,
            markdown.SpecialFile.CHANGELOG_FILE,
            markdown.SpecialFile.CONTRIBUTING_FILE
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
    markdown.insert_file(FILEPATH, filestr, index=index, new_index=new_index)


def generate_summary(
        workdir, depth_limit: int = -1, ignore_folders=[], footer_path=None,
        index: str = "Index", new_index: str = None
):
    filestr = generate_summary_filestr(
        workdir, depth_limit=depth_limit, ignore_folders=ignore_folders, footer_path=footer_path)
    insert_summary_file(workdir, filestr, index=index, new_index=new_index)


def generate_readmes(
        startpath: Path, depth_limit: int = -1, ignore_folders=[], index="Index", header=None,
        new_index=None, clearify=False, direct_link: bool = False
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
                links.append(make_file_link(startpath / f, direct_link=direct_link))

        if bool(links):
            filestr = markdown.create_header(header, 2) if header else ""
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
                    links.append(make_file_link(subfilepath, root=root, direct_link=direct_link))
                elif f != markdown.SpecialFile.README_FILE.value:
                    # DEV: Markdown dosyaları README'nin altına eklensin
                    links.append(markdown.create_link(subfilepath, root=link_root))

            if bool(links):
                filestr = markdown.create_header(header, 2) if header else ""
                filestr += "".join(links)

                filepath = markdown.SpecialFile.README_FILE.get_filepath(root=Path(root))
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
                readme_path = markdown.SpecialFile.README_FILE.get_filepath(root=root)
                if os.path.exists(readme_path):
                    os.remove(readme_path)
            continue

        if bool(filestr):
            filepath = markdown.SpecialFile.README_FILE.get_filepath(root=root)
            fileheader = os.path.basename(root)
            markdown.insert_file(filepath, filestr, index=index, force=True,
                                 fileheader=fileheader, new_index=new_index)


def get_summary_url_from_repo_url(repo_url):
    return github.generate_raw_url_from_repo_url(repo_url) + "/" + SUMMARY_FILE


def read_summary_from_url(repo_url):
    raw_url = get_summary_url_from_repo_url(repo_url)
    return filesystem.read_file_by_url(raw_url)


def check_summary(path):
    spath = os.path.join(path, SUMMARY_FILE)
    markdown.check_links(spath)


def create_changelog(
    path: Path, ignore_commits=[], repo_url=None, since: datetime = None,
    to: datetime = None, push=False, commit_msg=None
):
    if not commit_msg:
        commit_msg = "💫 YGitBookIntegration"

    cpath = path / CHANGELOG_FILE

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
        filesystem.write_file(cpath, filestr)

        if push:
            github.push_to_github(path, [cpath], commit_msg)