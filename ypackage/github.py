from urllib import parse
# from pydriller import RepositoryMining
from datetime import datetime
import os
from .markdown import (
    encodedpath,
    create_link
)
from .filesystem import (
    readFileWithURL
)

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


def log_git_commits(since, to):
    with open("changes.md", "w+", encoding="utf-8") as file:
        file.write("# ✨ Değişiklikler")
        file.write("\n\n")

        for commit in RepositoryMining('../IstanbulUniversity-CE', since=since, to=to, reversed_order=True).traverse_commits():
            time = commit.author_date.strftime("%d/%m/%Y - %H:%M:%S")
            msg = commit.msg
            changes = []
            for modification in commit.modifications:
                path = modification.new_path
                if path:
                    path = os.path.join(".", path)
                    path = parse.quote(path)
                    changes.append(path)

        file.write("## " + str(time))
        file.write("\n\n")
        for change in changes:
            file.write(f"- [{msg}]({path})\n")
        file.write("\n\n")


def create_changelog(path, repo_url, since: datetime = None, to: datetime = None):
    import os
    from datetime import datetime
    from pydriller import RepositoryMining
    from urllib import parse

    with open(f"{path}/CHANGELOG.md", "w+", encoding="utf-8") as file:
        file.write("# ✨ Değişiklikler")
        file.write("\n\n")
        file.write("## 📋 Tüm Değişiklikler")
        file.write("\n\n")

        for commit in RepositoryMining(path, reversed_order=True).traverse_commits():
            hash_value = commit.hash
            time = commit.author_date.strftime("%d/%m/%Y - %H:%M:%S")
            msg = commit.msg
            title = msg.split("\n")[0]

            url = DIFF_TEMPLATE.format(repo_url, hash_value)
            header = f"{title} ~ {str(time)}"
            link = create_link(url, header=header)
            file.write(link)
