import os
# from pydriller import RepositoryMining
from datetime import datetime

from .markdown import create_link, encodedpath

# diff-528720652ae91788d21a1334d1696e75
# https://github.com/YEmreAk/IstanbulUniversity-CE/commit/cd3459443690ac13d45f845842e407aa386aa018?short_path = 5287206
DIFF_TEMPLATE = "{}/commit/{}?diff=split"


def get_github_url():
    return r"https://github.com"


def get_github_userprofile_url(username):
    return get_github_url() + "/" + username


def get_github_repo_url(username):
    return get_github_userprofile_url(username) + "/" + os.path.basename(os.getcwd())


def get_raw_master_url(username) -> str:
    return get_github_repo_url(username) + "/raw/master"


def get_github_raw_link(username, filepath: str):
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


def push_to_github(startpath: str, paths: list, commit: str):
    if len(paths) > 0:
        cur_dir = os.getcwd()
        os.chdir(startpath)
        print(f"----------------------------------------")
        print(f"{startpath} için push işlemi:")
        print(f"----------------------------------------")
        command = " &&".join([f"git add {os.path.relpath(path)}" for path in paths])
        command += " &&" + f'git commit -m "{commit}"'
        command += " &&" + f"git push -u origin master"

        os.system(command)
        os.chdir(cur_dir)


def get_remote_url(path):
    from subprocess import Popen, PIPE

    cur_dir = os.getcwd()
    os.chdir(path)

    remote_url = ""
    with Popen(r'git config --get remote.origin.url', stdout=PIPE, stderr=PIPE) as p:
        output, errors = p.communicate()
        remote_url = output.decode('utf-8').splitlines()[0].replace(".git", "")

    os.chdir(cur_dir)

    return remote_url


def list_commit_links(path, repo_url=None, ignore_commits=[], since: datetime = None, to: datetime = None):
    from pydriller import RepositoryMining

    if not repo_url:
        repo_url = get_remote_url(path)

    links = []
    for commit in RepositoryMining(path, reversed_order=True).traverse_commits():
        title = commit.msg.split("\n")[0]

        ignore = False
        for ignore_commit in ignore_commits:
            if ignore_commit in title:
                ignore = True
                continue

        if not ignore:
            hash_value = commit.hash
            time = commit.author_date.strftime("%d/%m/%Y - %H:%M:%S")
            url = DIFF_TEMPLATE.format(repo_url, hash_value)
            header = f"{title} ~ {str(time)}"
            link = create_link(url, header=header)
            links.append(link)

    return links
