import logging
from argparse import ArgumentParser

from .common import initialize_logging

PATTERN_ID = "?id="
URL_DRIVE = "https://drive.google.com"
PATTERN_OPEN = "open"
PATTERN_DOWNLOAD = "uc"
PATTERN_DRİVE = "https://drive.google.com"


def drive_to_direct(url: str) -> str:
    return make_direct_link(get_id(url))


def direct_to_drive(url: str) -> str:
    return make_drive_link(get_id(url))


def make_drive_link(file_id: str) -> str:
    return f"{URL_DRIVE}/{PATTERN_OPEN}{PATTERN_ID}{file_id}"


def make_direct_link(file_id: str) -> str:
    return f"{URL_DRIVE}/{PATTERN_DOWNLOAD}{PATTERN_ID}{file_id}"


def get_id(url: str) -> str:
    ix = url.find(PATTERN_ID) + len(PATTERN_ID)
    return url[ix:]


def initialize_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description='Google Drive için direkt url oluşturucu',
    )
    parser.add_argument(
        'urls',
        nargs="+",
        metavar='urls',
        help='Url verileri',
    )
    parser.add_argument(
        "--reverse",
        "-r",
        action="store_true",
        dest="revers",
        help="Direkt urlden ön izlenebilir url oluşturma (Kullanıcılar için)"
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        dest="debug",
        help="Bilgilendirici metinleri gösterme"
    )

    return parser


def main():
    args = initialize_parser().parse_args()
    URLS, REVERSE, DEBUG = args.urls, args.revers, args.debug

    log_level = logging.DEBUG if DEBUG else logging.INFO
    initialize_logging(level=log_level)

    function = drive_to_direct if not REVERSE else direct_to_drive
    for url in URLS:
        logging.info(function(url))


if __name__ == "__main__":
    main()
