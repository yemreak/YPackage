import argparse
import os
import configparser
import urllib.request

from . import gitbook
from . import filesystem
from . import common
from . import markdown

SUBMODULE_FILE = ".ysubmodules"

# def execute_integrate(path: str, option: str):
#     COMMANDS = f"""
#     echo "---
#     description: Sitede neler olup bittiğinin raporudur.
#     ---" > {os.path.join(path, "CHANGELOG.md")}
#     ygitchangelog -d >> {os.path.join(path, "CHANGELOG.md")}
#     bash github {path}
#     """
#
#     # subprocess.run(f"bash -c '{COMMANDS}'")


def convert_url_form(filestr: str, url: str):
    return filestr.replace("./", url + "/").replace("README.md", "").replace(".md", "")


def add_description(content: str, description: str) -> str:
    if description:
        return gitbook.make_description(description) + content
    else:
        return content


def fixTitle(content: str) -> str:
    title = f"# {markdown.read_first_link(content)[1]}"
    title_changed = False

    lines = content.split("\n")

    for i in range(len(lines)):
        count = lines[i].count("#")
        if count == 1:
            lines[i] = title
            title_changed = True
            break
        elif count >= 1:
            lines[0] = title
            title_changed = True
            break

    if not title_changed:
        lines[0] = title
        title_changed = True

    return "\n".join(lines)


def fixUrls(content, root):
    fixedlines = []
    lines = content.split("\n")
    for line in lines:
        link = markdown.find_link(line)
        if link:
            path: str = link[2]
            if "http" not in path:
                fixedpath = path.replace(".md", "").replace("README", "")
                fixedpath = root + "/" + fixedpath
                line = line.replace(path, fixedpath)

        fixedlines.append(line)

    return "\n".join(fixedlines)


def updateSubSummaries(startpath, index: str = "Index"):
    config = configparser.ConfigParser(inline_comment_prefixes="#")
    config.read(os.path.join(startpath, SUBMODULE_FILE), encoding="utf-8")

    for name in config:
        if name == "DEFAULT":
            continue

        section = config[name]
        path = os.path.join(startpath, section['path'])
        url = section['url']
        root = section['root']

        description = None
        if "description" in section:
            description = section['description']

        content = gitbook.read_summary_from_url(url)

        substrings = markdown.generate_substrings(content, index)
        if substrings:
            content = substrings[0]

        content = fixTitle(content)
        content = fixUrls(content, root)
        content = add_description(content, description)

        filesystem.write_file(path, content)


def generate_changelog():
    pass


def main():
    parser = argparse.ArgumentParser(
        description='Create `README.md` and `SUMMARY.md` file for GitBook synchronization',
    )
    parser.add_argument(
        'paths',
        nargs="+",
        metavar='paths',
        help='Projelerin yolları',
    )
    parser.add_argument(
        "--update",
        "-u",
        action="store_true",
        dest="update",
        help="Alt modüllerin summary'lerini güncelleme"
    )
    parser.add_argument(
        "--recreate",
        "-r",
        action="store_true",
        dest="recreate",
        help="Summary dosyasını baştan oluşturur"
    )
    parser.add_argument(
        "--generate",
        "-g",
        action="store_true",
        dest="generate",
        help="Markdown dışı dosyalar için README'ye bağlantılar oluşturma"
    )
    parser.add_argument(
        '--level-limit',
        '-ll',
        dest="level_limit",
        default=-1,
        help='Fonksiyonların çalışacağı en yüksek derinlik (0 => ana dizinde çalışır sadece)',
        type=int,
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        dest="debug",
        help="Bilgilendirici metinleri gösterme"
    )
    parser.add_argument(
        '--index',
        '-ix',
        dest="indexStr",
        default="Index",
        help='Generated string will be inserted between given indexes',
        type=str,
    )
    # BUG: Bu yapı çalışmaz, nargs olması lazım
    parser.add_argument(
        '--privates',
        "-p",
        dest="privates",
        default=["res", "__pycache__"],
        help='List of folder names that you dont want to add',
        type=list
    )
    parser.add_argument(
        "--footer-path",
        '-fp',
        dest="footerPath",
        help="Append the given file to end of the output. "
    )
    parser.add_argument(
        '--new-index',
        '-nix',
        dest="newIndex",
        default=None,
        help='Generated string will be inserted between given indexes with changing the indexes',
        type=str,
    )

    args = parser.parse_args()
    PATHS, PRIVATES, INDEX_STR, NEW_INDEX_STR, FOOTER_PATH, LEVEL_LIMIT, DEBUG, UPDATE, RECREATE, GENERATE = args.paths, args.privates, args.indexStr, args.newIndex, args.footerPath, args.level_limit, args.debug, args.update, args.recreate, args.generate

    for path in PATHS:
        if os.path.isdir(path):
            if GENERATE:
                gitbook.generate_readmes(
                    path, privates=PRIVATES, index=INDEX_STR,
                    new_index=NEW_INDEX_STR, level_limit=LEVEL_LIMIT
                )

            if RECREATE:
                filestr = gitbook.generate_summary_filestr(
                    path, level_limit=LEVEL_LIMIT, privates=PRIVATES,
                    footer_path=FOOTER_PATH
                )
                gitbook.create_summary_file(path)
                gitbook.insert_summary_file(
                    path, filestr, index=INDEX_STR, new_index=NEW_INDEX_STR)

            if UPDATE:
                updateSubSummaries(path, INDEX_STR)

        elif DEBUG:
            print(f"Hatalı yol: {path}")


if __name__ == "__main__":
    main()