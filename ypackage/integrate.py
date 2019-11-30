import argparse
import os
import configparser
import sys
import urllib.request

from . import gitbook
from . import filesystem
from . import common
from . import markdown

INTEGRATION_FILE = ".ygitbookintegration"
INTEGRATION_MODULE = "integration"
SUBMODULE_MODULE = "submodule"

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


def read_config(startpath: str, filepath: str) -> dict:
    try:
        config = configparser.ConfigParser(inline_comment_prefixes="#")
        config.read(os.path.join(startpath, filepath), encoding="utf-8")
    except:
        return None

    return config


def integrate(config: dict) -> None:
    for name in config:
        if name == "DEFAULT":
            continue

        section = config[name]


def updateSubSummaries(config: dict, startpath, index: str = "Index"):
    for name in config.sections():
        if name.split()[0] == SUBMODULE_MODULE:
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
        "--store",
        "-s",
        action="store_true",
        dest="store",
        help="Son komutu hızlı kullanım için yapılandırma dosyasında saklar"
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
    PATHS = args.paths

    new_args_start_index = (len(PATHS) + 1)
    override = len(sys.argv) > new_args_start_index

    for path in PATHS:
        if os.path.isdir(path):
            config = read_config(path, INTEGRATION_FILE)

            if not override:
                new_args = ""
                for section in config.sections():
                    if section.split()[0] == INTEGRATION_MODULE:
                        new_args = config[section]["args"].replace("\"", "")
                        break

                if new_args:
                    command = [__file__, path] + new_args.split()
                    args = parser.parse_args(command)
                else:
                    print(f"{os.path.basename(path)} için entegrasyon özelliği mevcut değil")
                    print(
                        f"    `{INTEGRATION_FILE}` dosyası içerisindeki `integration` alanında `args` özelliği yok")
                    continue

            PRIVATES, INDEX_STR, NEW_INDEX_STR, FOOTER_PATH, LEVEL_LIMIT, DEBUG, UPDATE, RECREATE, GENERATE, STORE = args.privates, args.indexStr, args.newIndex, args.footerPath, args.level_limit, args.debug, args.update, args.recreate, args.generate, args.store

            if STORE:
                last_args = sys.argv[new_args_start_index:]
                last_args = " ".join(last_args)

                ifpath = os.path.join(path, INTEGRATION_FILE)
                if not os.path.exists(ifpath):
                    with open(ifpath, "w", encoding="utf-8") as file:
                        file.write(f'[{INTEGRATION_MODULE} "auto"]\n')
                        file.write(f'\targs = {last_args}')
                else:
                    for name in config.sections():
                        if name.split()[0] == INTEGRATION_MODULE:
                            section = config[name]
                            section["args"] = last_args

                    with open(ifpath, "w", encoding="utf-8") as configfile:
                        config.write(configfile)

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
                    path, filestr, index=INDEX_STR, new_index=NEW_INDEX_STR
                )

            if UPDATE:
                updateSubSummaries(config, path, INDEX_STR)

        elif DEBUG:
            print(f"Hatalı yol: {path}")


if __name__ == "__main__":
    main()
