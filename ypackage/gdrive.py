import argparse

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


def main():
    parser = argparse.ArgumentParser(
        description='Google Drive için direkt url oluşturucu',
    )yy
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
        help="Direkt urlden önizlenebilir url oluşturma (Kullanıcılar için)"
    )

    args = parser.parse_args()
    URLS, REVERSE = args.urls, args.revers

    function = drive_to_direct if not REVERSE else direct_to_drive
    for url in URLS:
        print(function(url))


if __name__ == "__main__":
    main()
