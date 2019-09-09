import os
from .filesystem import find_level
from .markdown import create_indent, create_link, create_header, read_first_header, insert_file

SUMMARY_FILE_HEADER = "# Summary"
SUMMARY_FILE = "SUMMARY.md"
README_FILE = "README.md"


def list_workspace(startpath: str, privates: list = [], debug: bool = False):
    """Summary dosyasının içeriğini oluşturur
    Dosya oluşturulması sırasında başlıklar markdown dosyasının başlığı olarak belirlenir. Dosya isimlerine bakılmaz

    Arguments:
        startpath {str} -- Summary dosyası oluşturulacak dizinin yolu

    Keyword Arguments:
        privates {list} -- Atlanacak dosyalar (default: {[]})
        debug {bool} -- Bilgilendirme mesajlarını aktif eder (default: {False})
    """
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

            # Skip the startpath files
            continue

        if debug:
            print(f"\nRoot: {root}\nStartpath: {startpath}")

        level = find_level(root, startpath)
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

                lines.append('{}{}'.format(
                    subindent, create_link(os.path.join(root, f), root=startpath)))

    return lines


def generate_summary(dirpath: str, privates: list = [], footer_path: bool = None, index: str = "Index", new_index: str = None):
    filepath = os.path.join(dirpath, SUMMARY_FILE)
    lines = list_workspace(dirpath, privates)

    filestr = ""
    if footer_path and os.path.isfile(footer_path):
        with open(os.path.join(footer_path), "r", encoding="utf-8") as file:
            filestr = "\n" + file.read()

    filestr = "".join(lines) + filestr
    insert_file(filepath, filestr, index=index, new_index=new_index)


def generate_readmes(startpath: str, privates: list = [], index: str = "Index", header: str = "🔗 Harici Dosyalar", new_index: str = None):
    for root, dirs, files in os.walk(startpath):
        # Remove private directories
        dirs[:] = [d for d in dirs if not d.startswith(
            '.') and d not in privates]

        # Skip startpath
        if root == startpath:
            continue

        links = []
        for f in files:
            # Only looks non-markdown files
            if not ".md" in f:
                links.append(create_link(os.path.join(".", f), root=startpath))

        if bool(links):
            filepath = os.path.join(root, README_FILE)

            filestr = create_header(header, 2)
            filestr += "".join(links)

            if not os.path.exists(filepath):
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(create_header(os.path.basename(root), 1))

            insert_file(filepath, filestr, index=index, new_index=new_index)
