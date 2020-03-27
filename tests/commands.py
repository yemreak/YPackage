import subprocess


def _check(command: str, args: str):
    subprocess.check_output(
        f"python -m {command} {args}",
        universal_newlines=True
    )


def check_filerenamer(args: str):
    _check("yfilerenamer", args)


def check_gitbook(args: str):
    _check("ygitbookintegration", args)


def check_googledrive(args: str):
    _check("ygoogledrive", args)


def check_googlesearch(args: str):
    _check("ygooglesearch", args)


def check_themecreator(args: str):
    _check("ythemecreator", args)
