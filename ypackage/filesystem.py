import json
import os


def write_file(filepath, string, debug=False):
    filepath = os.path.realpath(filepath)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(string)

        if debug:
            print(f"Değişen dosya: {file.name}")


def read_file(filepath, debug=False) -> str:
    string = ""
    filepath = os.path.realpath(filepath)
    with open(filepath, "r", encoding="utf-8") as file:
        string = file.read()
        if debug:
            print(f"Okunan dosya: {file.name}")

    return string


def read_json(filepath, debug=False) -> dict:
    return json.loads(read_file(filepath, debug=debug))


def create_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def find_level(root, startpath):
    return root.replace(startpath, '').count(os.sep)


def print_files(startpath):
    for root, _, files in os.walk(startpath):
        level = find_level(root, startpath)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def insert_file(filepath, string, index, new_index=None, debug=False):
    def get_index():
        return new_index if new_index else index

    def generate_insertion():
        index = get_index()
        insertion = index + "\n\n"

        if bool(string):
            insertion += string + "\n\n"

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
        # BUG: Yeni indeks girildiğinde, eski indeks bulunmazsa birden fazla yazılıyor
        filestr += generate_insertion()
        inserted = True

    write_file(filepath, filestr, inserted)

    if debug:
        print(f"İndeks: {index} Yeni İndeks: {new_index}")
