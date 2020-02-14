import logging
from argparse import ArgumentParser

from .filesystem import rename_files, rename_folders


def initialize_parser():
    parser = ArgumentParser(
        description="Dosya veya dizinleri topluca adlandırma aracı"
    )

    parser.add_argument(
        'paths',
        nargs="+",
        metavar='paths',
        help='Dizin yolları',
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        dest="recursive",
        help="Dizin içerisindeki tüm içerikleri ele alır"
    )
    parser.add_argument(
        "--silent",
        "-s",
        action="store_true",
        dest="silent",
        help="İşlemleri çıktı göstermeden tamamlar"
    )
    parser.add_argument(
        "--dir",
        "-d",
        action="store_true",
        dest="dir_mode",
        help="Dosya yerine dizinlerin adlarını değiştirir"
    )
    parser.add_argument(
        "--pattern",
        "-p",
        dest="pattern",
        help="Değiştirilecek isimleri belirten regex şablonu",
        required=True
    )
    parser.add_argument(
        "--to",
        "-t",
        dest="to",
        help="Şablona uygun isimleri verilen değer ile değiştirir",
        required=True
    )
    parser.add_argument(
        "--c",
        "--case-sensitive",
        action="store_true",
        dest="case_sensitive",
        help="BÜyük küçük harf duyarlılığını aktif eder"
    )

    return parser


def register_args(parser: ArgumentParser):
    args = parser.parse_args()

    global PATHS
    PATHS = args.paths

    global RECURSIVE, CASE_SENSITIVE, DIR_MODE
    RECURSIVE, CASE_SENSITIVE, DIR_MODE = args.recursive, args.case_sensitive, args.dir_mode

    global PATTERN, TO
    PATTERN, TO = args.pattern, args.to

    global SILENT
    SILENT = args.silent


def main():
    logging.basicConfig(level=logging.INFO)

    parser = initialize_parser()
    register_args(parser)

    if SILENT:
        logging.basicConfig(level=logging.ERROR)

    for path in PATHS:
        function = rename_folders if DIR_MODE else rename_files
        function(path, PATTERN, TO, ignore_case=not CASE_SENSITIVE)


if __name__ == "__main__":
    main()
