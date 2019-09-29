import os


def find_level(root, startpath):
    return root.replace(startpath, '').count(os.sep)


def print_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = find_level(root, startpath)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def write_file(filepath, string, debug=False):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(string)

        if debug:
            print(f"File changed: {file.name}")


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
