import os
from ypackage.filesystem import find_level
from ypackage.markdown import create_indent, create_link, create_header, read_first_header, insert_file, create_markdown_file

SUMMARY_FILE_HEADER = "# Summary"
SUMMARY_FILE = "SUMMARY.md"
README_FILE = "README.md"
CHANGELOG_FILE = "CHANGELOG.md"
CHANGELOG_HEADER = u"👀 Neler değişti"


def list_workspace(startpath, level_limit: int = -1, privates=[], debug=False):
    # Fixs "Folder\" "Folder" difference. All of them is equel "Folder"
    startpath = os.path.normpath(startpath)

    lines = [SUMMARY_FILE_HEADER + "\n\n"]
    for root, dirs, files in os.walk(startpath):
        # Remove private directories
        dirs[:] = [d for d in dirs if not d.startswith(
            '.') and d not in privates]

        if root == startpath:
            # Find title of repo from README.md
            headpath = os.path.join(root, README_FILE)
            header = read_first_header(headpath)
            header = create_link(headpath, header=header, root=startpath)
            lines.append(header)

            for f in files:
                if f == CHANGELOG_FILE:
                    changelog_path = os.path.join(root, CHANGELOG_FILE)
                    changelog_link = create_link(
                        changelog_path, header=CHANGELOG_HEADER, root=startpath)

                    # Sadece 1 master link olur (indent)
                    level = find_level(root, startpath) + 1
                    indent = create_indent(level, size=2)
                    lines.append('{}{}'.format(indent, changelog_link))

            # Skip the startpath files
            continue

        if debug:
            print(f"\nRoot: {root}\nStartpath: {startpath}")

        level = find_level(root, startpath)
        if level_limit == -1 or level <= level_limit:  # MAX
            indent = create_indent(level, size=2)

            # If there exist README in dir, link it instead folder (like GitHub)
            if README_FILE in files:
                readme_path = os.path.join(root, README_FILE)
                dirlink = create_link(
                    readme_path, header=read_first_header(readme_path), root=startpath)
            else:
                dirlink = create_link(root, root=startpath)

            lines.append('{}{}'.format(indent, dirlink))

            subindent = create_indent(level + 1, size=2)
            for f in files:
                # Only looks markdown files
                if ".md" in f:
                    if "README.md" in f:
                        continue

                    filepath = os.path.join(root, f)
                    lines.append('{}{}'.format(
                        subindent, create_link(filepath, header=read_first_header(filepath), root=startpath)))

    return lines


def generate_summary(inputDir, level_limit: int = -1, privates=[], footer_path=None, index="Index", new_index=None):
    filepath = os.path.join(inputDir, SUMMARY_FILE)
    lines = list_workspace(
        inputDir, level_limit=level_limit, privates=privates)

    filestr = ""
    if footer_path and os.path.isfile(footer_path):
        with open(os.path.join(footer_path), "r", encoding="utf-8") as file:
            filestr = "\n" + file.read()

    filestr = "".join(lines) + filestr
    insert_file(filepath, filestr, index=index, new_index=new_index)


def generate_readmes(startpath, level_limit: int = -1, privates=[], index="Index", header="📂 Harici Dosyalar", new_index=None, clearify=False):
    # DEV: Ders notlarını README'ye ekleme direkt olarak dizin dosya oluştur
    def clear_private_dirs() -> list:
        return [d for d in dirs if not d.startswith(
            '.') and d not in privates]

    def generate_links_for_nonmarkdowns(files) -> str:
        # OLD: Eski yapıdır, kontrollü bir şekilde kaldırılmalı
        filestr = ""
        links = []
        for f in files:
            if not ".md" in f:
                links.append(create_link(
                    os.path.join(".", f), root=startpath))

        if bool(links):
            filestr = create_header(header, 2)
            filestr += "".join(links)

        return filestr

    def get_readme_path(root) -> str:
        return os.path.join(root, README_FILE)

    def generate_markdown_files_for_subitems(startpath) -> str:
        for root, _, files in os.walk(startpath):
            if root == startpath:
                continue

            filestr = ""
            fileheader = os.path.basename(root)
            filepath = os.path.join(startpath, fileheader + ".md")

            level = find_level(root, startpath)
            link_root = os.path.dirname(root)
            for _ in range(level - 1):
                link_root = os.path.dirname(link_root)

            for f in files:
                subfilepath = os.path.join(root, f)
                filestr += create_link(subfilepath, root=link_root)

            if bool(filestr):
                insert_file(filepath, filestr, index=index,
                            force=True, fileheader=fileheader, new_index=new_index)

    filestr = ""
    for root, dirs, files in os.walk(startpath):
        # Remove private directories
        dirs[:] = clear_private_dirs()

        # Skip startpath
        if root == startpath:
            continue

        filestr = ""
        level = find_level(root, startpath)
        if level_limit == -1 or level < level_limit:
            filestr = generate_links_for_nonmarkdowns(files)
        elif level == level_limit:  # 1
            generate_markdown_files_for_subitems(root)
        else:
            if clearify and level > level_limit:
                readme_path = get_readme_path(root)
                if os.path.exists(readme_path):
                    os.remove(readme_path)
            continue

        if bool(filestr):
            filepath = get_readme_path(root)
            fileheader = os.path.basename(root)
            insert_file(filepath, filestr, index=index,
                        force=True, fileheader=fileheader, new_index=new_index)