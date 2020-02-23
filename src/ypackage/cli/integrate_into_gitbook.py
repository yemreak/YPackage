import configparser
import logging
import shlex
import sys
from argparse import ArgumentParser
from glob import glob
from pathlib import Path
from typing import Dict

from .. import common, filesystem, gitbook, github, markdown

logger = logging.getLogger(__name__)

INTEGRATION_FILE = ".ygitbookintegration"
INTEGRATION_MODULE = "integration"
SUBMODULE_MODULE = "submodule"
COMMIT_UPDATE_SUBMODULES = "✨ Alt sayfalar güncellendi"

# CLI arguments
PATHSTR_LIST, DEBUG = None, None
GENERATE, RECREATE = None, None
UPDATE, CHANGELOG, REPO_URL = None, None, None
IGNORE_COMMITS, COMMIT_MSG, PUSH = None, None, None
IGNORE_COMMITS, COMMIT_MSG, PUSH = None, None, None
LEVEL_LIMIT, PRIVATES = None, None
INDEX_STR, NEW_INDEX_STR = None, None
FOOTER_PATH = None

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


def read_config(cpath: Path) -> dict:
    try:
        config = configparser.ConfigParser(inline_comment_prefixes="#")
        config.read(cpath, encoding="utf-8")
    except Exception as e:
        logger.error(f"Hata oluştu {e}")
        return {}

    return config


def updateSubSummaries(config: Dict, workdir: Path, index: str, push=False):
    """Alt modülleri günceller

    Arguments:
            config {dict} -- Yapılandırma dosyası verileri
            startpath {str} -- Yapılandırma dosyasının dizini

    Keyword Arguments:
            index {str} -- Limit (default: {"Index"})
            push {bool} -- Otomatik olarak git push işlemi yapma (default: {False})
    """

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
                if not markdown.is_url(path):
                    fixedpath = path.replace(".md", "").replace("README", "")
                    fixedpath = root + "/" + fixedpath
                    line = line.replace(path, fixedpath)

            fixedlines.append(line)

        return "\n".join(fixedlines)

    paths = []
    for name in config.sections():
        if name.split()[0] == SUBMODULE_MODULE:
            section = config[name]

            path = workdir / section['path']
            url = section['url']
            root = section['root']

            description = ""
            if "description" in section:
                description = section['description']

            until = ""
            if "until" in section:
                until = section['until']

            content = gitbook.read_summary_from_url(url)

            substrings = markdown.generate_substrings(content, index)
            if substrings:
                content = substrings[0]

            content = fixTitle(content)
            content = fixUrls(content, root)
            content = add_description(content, description)

            if until:
                until = "## " + until
                content = content[:content.find(until)]

            filesystem.write_file(path, content)

            paths.append(path)

    if push:
        github.push_to_github(workdir, paths, COMMIT_UPDATE_SUBMODULES)


def initialize_parser():
    parser = ArgumentParser(
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
        "--changelog",
        "-c",
        action="store_true",
        dest="changelog",
        help="Değişikliklerin raporlandığı CHANGELOG.mg dosyasını verilen URL'e göre oluşturur"
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
        "--push",
        "-p",
        action="store_true",
        dest="push",
        help="İşlem sonrası GitHub'a otomatik pushlar"
    )
    parser.add_argument(
        "--repo-url",
        "-ru",
        dest="repo_url",
        help="Projenin git repo urli",
        type=str
    )
    parser.add_argument(
        "--commit-msg",
        "-cm",
        dest="commit_msg",
        help="Otomatik pushlama içim commit başlığı (emoji desteklemez)",
        type=str
    )
    parser.add_argument(
        "--ignore-commits",
        "-ic",
        nargs="+",
        metavar='ignore_commits',
        default=[],
        help="Değişiklik raporuna dahil edilmeyecek commit başlıkları (emoji desteklemez)"
    )
    # WARN: Kullanışsız parametreler
    parser.add_argument(
        '--index',
        '-ix',
        dest="indexStr",
        default="YPackage.YGitbookIntegration-tarafından-otomatik-oluşturulmuştur",
        help='Generated string will be inserted between given indexes',
        type=str,
    )
    # BUG: Bu yapı çalışmaz, nargs olması lazım
    parser.add_argument(
        '--privates',
        "-pp",
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
        help="Oluşturulan metin verilen yeni indekslerin arasına yazılır",
        type=str,
    )

    return parser


def register_args(parser: ArgumentParser, register_all=False):
    args = parser.parse_args()

    if register_all:
        global PATHSTR_LIST, DEBUG
        PATHSTR_LIST, DEBUG = args.paths, args.debug

    global GENERATE, RECREATE
    GENERATE, RECREATE = args.generate, args.recreate

    global UPDATE, CHANGELOG, REPO_URL
    UPDATE, CHANGELOG, REPO_URL = args.update, args.changelog, args.repo_url

    global IGNORE_COMMITS, COMMIT_MSG, PUSH
    IGNORE_COMMITS, COMMIT_MSG, PUSH = args.ignore_commits, args.commit_msg, args.push

    global LEVEL_LIMIT, PRIVATES
    LEVEL_LIMIT, PRIVATES = args.level_limit, args.privates

    global INDEX_STR, NEW_INDEX_STR
    INDEX_STR, NEW_INDEX_STR = args.indexStr, args.newIndex

    global FOOTER_PATH
    FOOTER_PATH = args.footerPath


def register_config_args(config: dict, path: Path) -> Dict:
    new_args = ""
    for section in config.sections():
        if section.split()[0] == INTEGRATION_MODULE:
            new_args = config[section]["args"]
            break

    if new_args:
        sys.argv = [__file__, str(path)] + shlex.split(new_args)
    else:
        logger.warning(f"""
        {str(path)} için entegrasyon özelliği mevcut değil
        {INTEGRATION_FILE}` dosyası içerisindeki `integration` alanında `args` özelliği yok
        """.strip())
        return

    parser = initialize_parser()
    register_args(parser)


def integrate(path: Path, override=False):
    if path.is_dir():
        config = read_config(path / INTEGRATION_FILE)

        if not override:
            register_config_args(config, path)

        logger.info(f"`{str(path)}` için gitbook entegrasyonu başlatılıyor.")

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
            updateSubSummaries(config, path, INDEX_STR, push=PUSH)

        # TIP: Committe iken yapmaktadır (önceden push edilmesine gerek yok)
        if CHANGELOG:
            gitbook.create_changelog(
                path, repo_url=REPO_URL, push=PUSH,
                ignore_commits=IGNORE_COMMITS, commit_msg=COMMIT_MSG
            )

        logger.info(f"`{str(path)}` için gitbook entegrasyonu tamamlandı.")

    else:
        logger.error(f"Hatalı yol: {path}")


def main():
    parser = initialize_parser()

    register_args(parser, register_all=True)

    log_level = logging.DEBUG if DEBUG else logging.INFO
    common.initialize_logging(level=log_level)

    override_config = any([GENERATE, RECREATE, UPDATE, CHANGELOG])
    for pathstr in PATHSTR_LIST:
        paths = [Path(p) for p in glob(pathstr)]
        for path in paths:
            integrate(path, override=override_config)


if __name__ == "__main__":
    main()
