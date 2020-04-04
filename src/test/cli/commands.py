import subprocess


def _check(command: str, args: str):
    return subprocess.check_output(
        f"{command} {args}",
        shell=True,
        encoding="utf-8"
    )


def check_filerenamer(args: str):
    return _check("yfilerenamer", args)


def check_gitbook(args: str):
    return _check("ygitbookintegration", args)


def check_googledrive(args: str):
    return _check("ygoogledrive", args)


def check_googlesearch(args: str):
    return _check("ygooglesearch", args)


def check_themecreator(args: str):
    return _check("ythemecreator", args)
