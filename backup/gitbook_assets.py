ASSETS_PATH = os.path.normpath(".gitbook/assets")
ASSETS_EXIST = False


def create_assets_dir():
    if not os.path.isdir(ASSETS_PATH):
        os.makedirs(ASSETS_PATH)


def move_to_assets(filepath: str) -> str:
    basename = os.path.basename(filepath)

    dstpath = os.path.join(ASSETS_PATH, basename)
    fname, ext = os.path.splitext(dstpath)

    i = 1
    while os.path.exists(dstpath):
        fname += str(i)
        dstpath = fname + ext
        i += 1
    try:
        os.rename(filepath, dstpath)
    except Exception as e:
        print(e)

    return dstpath


def create_file_link(filepath: str, root: str = os.getcwd()):
    filepath = os.path.relpath(filepath, root)
    print(filepath)
    filepath = encodedpath(filepath)
    return r'{% file src="' + filepath + r'" %}' + '\n'


def make_file_link(filepath: str, root: str = os.getcwd()) -> str:
    create_assets_dir()
    dstpath = move_to_assets(filepath)
    return create_file_link(dstpath, root)
