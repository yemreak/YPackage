import logging
import os
from pathlib import Path
from typing import List

from . import markdown

logger = logging.getLogger(__name__)

# TODO: Class yapısına dahil olmalı
DIFF_TEMPLATE = "{}/commit/{}?diff=split"


def get_github_url() -> str:
    return r"https://github.com"


def get_github_userprofile_url(username) -> str:
    return get_github_url() + "/" + username


def get_github_repo_url(username: str, projectname: str) -> str:
    return get_github_userprofile_url(username) + "/" + projectname


def get_raw_master_url(username: str, projectname: str) -> str:
    return get_github_repo_url(username, projectname) + "/raw/master"


def get_github_raw_link(username: str, projectname: str, filepath: Path) -> str:
    """GitHub raw dosyalarına URL metni oluşturur

    Arguments:
        username {str} -- GitHub kullanıcı adı
        filepath {Path} -- Dosya yolu objesi

    Returns:
        str -- URL metni

    Examples:
        >>> get_github_raw_link('yedhrab', 'YPackage', Path('src'))
        'https://github.com/yedhrab/YPackage/raw/master/src'
    """
    filepath = filepath.absolute().relative_to(Path.cwd())
    filepath_string = filepath.as_posix()

    return get_raw_master_url(username, projectname) + "/" + filepath_string


def split_repo_url(repo_url) -> tuple:
    return repo_url.split("/")[-2:]


def create_rawurl(username, reponame) -> str:
    return f"https://raw.githubusercontent.com/{username}/{reponame}/master"


def generate_raw_url_from_repo_url(repo_url) -> str:
    username, reponame = split_repo_url(repo_url)
    return create_rawurl(username, reponame)


def push_to_github(gpath: Path, paths: List[Path], commit: str):
    if len(paths) > 0:
        cur_dir = os.getcwd()
        os.chdir(gpath)

        logger.info("""
        ----------------------------------------
        f"{gpath} için push işlemi:"
        ----------------------------------------
        """.strip())

        command = " &&".join([f"git add {path.relative_to(gpath)}" for path in paths])
        command += " &&" + f'git commit -m "{commit}"'
        command += " &&" + f"git push -u origin master"

        os.system(command)
        os.chdir(cur_dir)


def get_remote_url(path) -> str:
    from subprocess import Popen, PIPE

    cur_dir = os.getcwd()
    os.chdir(path)

    remote_url = ""
    try:
        with Popen(r'git config --get remote.origin.url', stdout=PIPE, stderr=PIPE) as p:
            output, errors = p.communicate()
            remote_url = output.decode('utf-8').splitlines()[0].replace(".git", "")
    except Exception:
        logger.error("Repo URL is undefined")

    os.chdir(cur_dir)

    return remote_url


def list_commit_links(
    path: Path,
    repo_url=None,
    ignore_commits=[],
    table_form=False
) -> List[str]:
    from pydriller import RepositoryMining
    logging.getLogger('pydriller').setLevel(logging.ERROR)

    if not repo_url:
        repo_url = get_remote_url(path)

    if not repo_url:
        return []

    links = []

    if table_form:
        links.append("|📅 Tarih|🔀 Commit|🐥 Sahibi|")
        links.append("|-|-|-|")

    for commit in RepositoryMining(str(path), order="reverse").traverse_commits():
        title = commit.msg.split("\n")[0]
        author = commit.author.name

        ignore = False
        for ignore_commit in ignore_commits:
            if ignore_commit in title:
                ignore = True
                continue

        if not ignore:
            hash_value = commit.hash
            time = commit.author_date.strftime("%d/%m/%Y - %H:%M:%S")
            url = DIFF_TEMPLATE.format(repo_url, hash_value)

            link = markdown.Link(title, url)
            link_str = link.to_str()

            if table_form:
                link_str = f"|{str(time)}|{link_str}|{author}|"
            else:
                link = f"- {str(time)} - {link_str} ~ {author}"

            links.append(link)

    return links
