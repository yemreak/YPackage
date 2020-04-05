import shlex
import sys

from ...ypackage.cli import filesystem, gdrive, gitbook, gsearch, theme

CONSOLE_SCRIPTS = {
    "ygitbookintegration": gitbook.main,
    "yfilerenamer": filesystem.main,
    "ygoogledrive": gdrive.main,
    "ygooglesearch": gsearch.main,
    "ythemecreator": theme.main
}


def _check(command: str, args: list):
    if isinstance(args, str):
        args = shlex.split(args)

    sys.argv = [command] + args
    return CONSOLE_SCRIPTS[command]()


def check_filerenamer(args: list):
    return _check("yfilerenamer", args)


def check_gitbook(args: str):
    return _check("ygitbookintegration", args)


def check_googledrive(args: str):
    return _check("ygoogledrive", args)


def check_googlesearch(args: str):
    return _check("ygooglesearch", args)


def check_themecreator(args: str):
    return _check("ythemecreator", args)
