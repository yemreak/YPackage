import configparser
import urllib.request


def readFileWithURL(rawUrl):
    return urllib.request.urlopen(rawUrl).read()


def getContent(path) -> str:
    print(url)
    username, repo = path.split("/")[-2:]
    rawPath = f"https://raw.githubusercontent.com/{username}/{repo}/master/SUMMARY.md"
    content = readFileWithURL(rawPath)
    return content


SUBMODULE_FILE = ".ysubmodules"

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read(SUBMODULE_FILE)

for section in config:
    if section == "DEFAULT":
        continue

    path = config[section]['path']
    url = config[section]['url']
    getContent(url)
