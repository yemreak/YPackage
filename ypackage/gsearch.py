import googlesearch
import requests
import argparse
import re
import time


def get_status_code(url) -> str:
    try:
        status_code = str(requests.head(url).status_code)
    except:
        status_code = "404+"
    return status_code


def log_url_by_status(query: str, fpath: str, status_code: str = None, exclude: str = None, mode="a") -> None:

    def write_file(string, file):
        file.write(string + "\n")
        file.flush()

    file = open(fpath, mode)

    removal = []
    if exclude:
        with open(exclude, "r") as exfile:
            removal = exfile.read().split("\n")

    urls = googlesearch.search(query, pause=5.0)
    for url in urls:
        if url not in removal:
            scode = get_status_code(url)
            if not status_code:
                result = f"{url},{scode}"
                write_file(result, file)
            elif scode == status_code:
                write_file(url, file)

    file.close()


def main():
    parser = argparse.ArgumentParser(
        description='Google arama sonuçlarını raporlama',
    )
    parser.add_argument(
        'queries',
        nargs="+",
        metavar='queries',
        help='Sorgular (google üzerinde aratılan metin)',
    )
    parser.add_argument(
        '--status-code',
        "-sc",
        dest='status_code',
        help='HTTP durum kodu',
        default=None
    )
    parser.add_argument(
        '--output',
        "-o",
        dest='output',
        help='Tüm çıktılar tek bir dosyaya aktarılır',
        default=None
    )
    parser.add_argument(
        '--exclude',
        "-ex",
        dest='exclude',
        help='Verilen dosya içerisindeki urlleri raporlamaz',
        default=None
    )

    args = parser.parse_args()
    QUERIES, STATUS_CODE, OUTPUT, EXCLUDE = args.queries, args.status_code, args.output, args.exclude

    for query in QUERIES:
        filename = re.sub(r"[^\w ]", "_", query) + ".txt" if not OUTPUT else OUTPUT

        condition = f"{STATUS_CODE} durumuna sahip olan" if STATUS_CODE else "tüm"
        print(f"`{query}` için `{filename}` dosyasına `{condition}` bağlantılar raporlanıyor.")

        log_url_by_status(query, filename, status_code=STATUS_CODE, exclude=EXCLUDE)


if __name__ == "__main__":
    main()
