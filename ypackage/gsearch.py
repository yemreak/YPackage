import googlesearch
import requests
import argparse
import re


def get_status_code(url) -> str:
    try:
        status_code = str(requests.head(url).status_code)
    except:
        status_code = "404+"
    return status_code


def log_url_by_status(query: str, fpath: str, status_code: str = None, mode="a") -> None:
    file = open(fpath, mode)

    urls = googlesearch.search(query)
    for url in urls:
        scode = get_status_code(url)
        if not status_code:
            result = f"{url},{scode}\n"
            file.write(result)
            file.flush()
        elif scode == status_code:
            file.write(url)
            file.flush()

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
        help='HTTP durum kodu)',
        default=None
    )

    args = parser.parse_args()
    QUERIES, STATUS_CODE = args.queries, args.status_code

    for query in QUERIES:
        filename = re.sub(r"[^\w ]", "", query) + ".txt"

        condition = f"{STATUS_CODE} durumuna sahip olan" if STATUS_CODE else "tüm"
        print(f"`{query}` için `{filename}` dosyasına `{condition}` bağlantılar raporlanıyor.")

        log_url_by_status(query, filename, status_code=STATUS_CODE)


if __name__ == "__main__":
    main()
