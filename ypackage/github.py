import logging
import os
# from pydriller import RepositoryMining
from datetime import datetime
from pathlib import Path
from typing import List

from .markdown import create_link, encodedpath

logger = logging.getLogger(__name__)

DIFF_TEMPLATE = "{}/commit/{}?diff=split"


def get_github_url() -> str:
    return r"https://github.com"


def get_github_userprofile_url(username) -> str:
    return get_github_url() + "/" + username


def get_github_repo_url(username) -> str:
    return get_github_userprofile_url(username) + "/" + os.path.basename(os.getcwd())


def get_raw_master_url(username) -> str:
    return get_github_repo_url(username) + "/raw/master"


def get_github_raw_link(username, filepath: str) -> str:
    filepath = os.path.relpath(filepath, start=os.getcwd())
    filepath = encodedpath(filepath)
    return get_raw_master_url(username) + "/" + filepath


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
    except Exception as e:
        logger.error("Repo URL'i tanımlanamadı" + e)
        exit(-1)

    os.chdir(cur_dir)

    return remote_url


def list_commit_links(
    path: Path, repo_url=None, ignore_commits=[],
    since: datetime = None, to: datetime = None, table_form=False
) -> List[str]:
    from pydriller import RepositoryMining

    if not repo_url:
        repo_url = get_remote_url(path)

    links = []

    if table_form:
        links.append("|📅 Tarih|🔀 Commit|🐥 Sahibi|")
        links.append("|-|-|-|")

    for commit in RepositoryMining(str(path), reversed_order=True).traverse_commits():
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

            link = create_link(url, header=title).replace("- ", "").replace("\n", "")

            if table_form:
                link = f"|{str(time)}|{link}|{author}|"
            else:
                link = f"- {str(time)} - {link} ~ {author}"

            links.append(link)

    return links
