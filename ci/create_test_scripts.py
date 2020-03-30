from ypackage import filesystem
from pathlib import Path
from shlex import join

MODULE_COMMAND = {
    "ypackage.cli.integrate_into_gitbook": "ygitbookintegration",
    "ypackage.cli.gitbook_integration": "ygitbookintegration",
    "ypackage.cli.gdrive": "ygoogledrive.exe",
    "ypackage.cli.gsearch": "ygooglesearch.exe",
    "ypackage.cli.file_renamer": "yfilerenamer.exe",
    "ypackage.cli.theme_creator": "ythemecreator.exe"
}

INIT_TEMPLATE = """@echo off

echo.
echo.
echo Python installation
echo -------------------
echo.

call pip install .
"""

NAME_TEMPLATE = """
echo.
echo.
echo {}
echo -------------------
echo.

"""

COMMAND_TEMPLATE = """
call {}

"""

END_TEMPLATE = """
exit /B
"""

path = Path(r".vscode/launch.json")
content = filesystem.read_json(path)

configurations = []

test_strings = {
    "ygitbookintegration": INIT_TEMPLATE,
    "ygoogledrive.exe": INIT_TEMPLATE,
    "ygooglesearch.exe": INIT_TEMPLATE,
    "yfilerenamer.exe": INIT_TEMPLATE,
    "ythemecreator.exe": INIT_TEMPLATE
}

outpaths = {
    "ygitbookintegration": "tests/test_gitbook.bat",
    "ygoogledrive.exe": "tests/test_googledrive.bat",
    "ygooglesearch.exe": "tests/test_googlesearch.bat",
    "yfilerenamer.exe": "tests/test_filerenamer.bat",
    "ythemecreator.exe": "tests/test_themecreator.bat"
}

for configuration in content["configurations"]:

    if "module" in configuration:
        name = configuration["name"]

        command = MODULE_COMMAND[configuration["module"]]
        args = join(configuration["args"]).replace("'", "\"")

        configurations.append({
            "name": name,
            "command": command,
            "args": args
        })

        test_strings[command] += NAME_TEMPLATE.format(name)
        test_strings[command] += COMMAND_TEMPLATE.format(f"{command} {args}")

for command in test_strings.keys():
    test_strings[command] += END_TEMPLATE
    filesystem.write_to_file(Path(outpaths[command]), test_strings[command])
