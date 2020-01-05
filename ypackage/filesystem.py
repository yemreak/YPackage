import json
import os
import re
from urllib.request import urlopen


def find_level(root: str, startpath: str) -> int:
    return root.replace(startpath, '').count(os.sep)


def write_file(filepath: str, string: str, debug=False):
    filepath = os.path.realpath(filepath)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(string)

        if debug:
            print(f"Değişen dosya: {file.name}")


def read_file(filepath: str, debug=False) -> str:
    string = ""
    filepath = os.path.realpath(filepath)
    with open(filepath, "r", encoding="utf-8") as file:
        string = file.read()
        if debug:
            print(f"Okunan dosya: {file.name}")

    return string


def read_json(filepath, debug=False) -> dict:
    return json.loads(read_file(filepath, debug=debug))


def read_part_of_file(filepath, string, index, new_index=None, debug=False) -> str:
    filestr = ""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            read = False
            for line in file:
                if index in line.replace(" ", ""):
                    read = not read
                    continue

                if read:
                    filestr += line

    return filestr


def insert_file(filepath, string, index, new_index=None, debug=False):
    def get_index():
        return new_index if new_index else index

    def generate_insertion():
        insertion = ""
        if bool(string):
            index = get_index()
            insertion += index + "\n\n"
            insertion += string + "\n"
            insertion += index + "\n"
        return insertion

    filestr = ""
    inserted = False
    if os.path.exists(filepath):
        with open(filepath, "r+", encoding="utf-8") as file:
            save = True

            for line in file:
                if not inserted and index in line.replace(" ", ""):
                    filestr += generate_insertion()
                    save = False
                    inserted = True
                else:
                    if not inserted or save:
                        filestr += line
                    else:
                        if index in line.replace(" ", ""):
                            save = True

    else:
        filestr = generate_insertion()
        inserted = True

    # If no insertion happend, create new section
    if not inserted:
        # BUG: If index is not found in the file while new index used, index string is dublicated
        # WARN: "\n" olmazsa satırın ucuna eklemekte, bu da indexin olduğu satırın kaybolmasından dolayı verinin silinmesine neden olmakta
        new_line_count = 2 - filestr[-2:].count("\n")
        filestr += "\n" * new_line_count
        filestr += generate_insertion()
        inserted = True

    write_file(filepath, filestr, debug=debug)

    if debug:
        print(f"Index: {index} New Index: {new_index}")


def listdir_grouped(root: str, privates=[], include_hidden=False) -> tuple:
    paths = os.listdir(root)
    dirs, files = [], []
    for path in paths:
        if not (not include_hidden and path.startswith('.')) and path not in privates:
            path = os.path.join(root, path)
            dirs.append(path) if os.path.isdir(
                path) else files.append(path)

    dirs, files = sorted(dirs), sorted(files)
    return dirs, files


def readFileWithURL(rawUrl, encoding="utf-8"):
    return urlopen(rawUrl).read().decode(encoding)


def repeat_for_subdirectories(startpath, func):

    for root, dirs, files in os.walk(startpath):
        # Sıralama her OS için farklı olabiliyor
        dirs.sort()
        files.sort()

        lvl = find_level(root, startpath)
        func(root, lvl, "dir")

        for f in files:
            fpath = os.path.join(root, f)
            func(fpath, lvl, "file")


def rename(regex, to, path, silent=False):
    result = regex.search(path)
    if result:
        for i in range(result.lastindex + 1):
            to = to.replace(f"${i}", result[i])

        dst = regex.sub(to, path)
        os.rename(path, dst)

        if not silent:
            print(path, dst)


def rename_folders(startpath: str, pattern, to, ignore_case=True, silent=False):
    p = re.compile(pattern, re.IGNORECASE if ignore_case else None)
    for root, dirs, _ in os.walk(startpath):
        # Sıralama her OS için farklı olabiliyor
        dirs.sort()

        rename(p, to, root, silent=silent)


def rename_files(startpath: str, pattern, to, ignore_case=True, silent=False):
    p = re.compile(pattern, re.IGNORECASE if ignore_case else None)
    for root, dirs, files in os.walk(startpath):
        # Sıralama her OS için farklı olabiliyor
        dirs.sort()
        files.sort()

        for f in files:
            path = os.path.join(root, f)
            rename(p, to, path, silent=silent)
