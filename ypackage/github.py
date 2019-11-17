import os
from .markdown import (
    encodedpath
)
from .filesystem import (
    readFileWithURL
)


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
