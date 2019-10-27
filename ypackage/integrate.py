import argparse
import os

from . import gitbook

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
        '--level-limit',
        '-ll',
        dest="level_limit",
        default=-1,
        help='Fonksiyonların çalışacağı en yüksek derinlik (0 => ana dizinde çalışır sadece)',
        type=int,
    )
    parser.add_argument(
        '--index',
        '-ix',
        dest="indexStr",
        default="Index",
        help='Generated string will be inserted between given indexes',
        type=str,
    )
    # WARN: Nargs olursa birden fazla path için kullanılabilir
    parser.add_argument(
        '--link',
        '-l',
        dest="link",
        help='Bağlantılı olduğu dosyanın yolu. (SUMMARY.md içerikleri bağlantılara da eklenir)',
        type=str,
    )
    # WARN: Nargs olursa birden fazla path için kullanılabilir
    parser.add_argument(
        '--url',
        '-u',
        dest="url",
        help='Bağlantılı dosyalara eklenecek olan url (relativepath -> realpath)',
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
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        dest="debug",
        help="Bilgilendirici metinleri gösterme"
    )

    args = parser.parse_args()
    PATHS, PRIVATES, INDEX_STR, NEW_INDEX_STR, FOOTER_PATH, LEVEL_LIMIT, DEBUG, LINK, URL = args.paths, args.privates, args.indexStr, args.newIndex, args.footerPath, args.level_limit, args.debug, args.link, args.url

    for path in PATHS:
        if os.path.isdir(path):
            gitbook.generate_readmes(
                path, privates=PRIVATES, index=INDEX_STR,
                new_index=NEW_INDEX_STR, level_limit=LEVEL_LIMIT
            )
            filestr = gitbook.generate_summary_filestr(
                path, level_limit=LEVEL_LIMIT, privates=PRIVATES,
                footer_path=FOOTER_PATH
            )

            gitbook.create_summary_file(path)
            gitbook.insert_summary_file(path, filestr, index=INDEX_STR, new_index=NEW_INDEX_STR)

            if LINK and URL:
                filestr_url = convert_url_form(filestr, URL)
                gitbook.insert_file(LINK, filestr_url, index=INDEX_STR, new_index=NEW_INDEX_STR)

        elif DEBUG:
            print(f"Hatalı yol: {path}")


if __name__ == "__main__":
    main()
