import os


def get_files(path, ext='', recursive=False):
    path_list = [path]
    while len(path_list) > 0:
        cpath = path_list.pop()
        with os.scandir(cpath) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    if entry.name.endswith(ext):
                        yield entry.path
                    else:
                        if recursive:
                            path_list.append(entry.path)

def make_dirs(path):
    os.makedirs(path, exist_ok=True)

def std_path(path):
    user_path = os.path.expanduser(path)
    abs_path = os.path.abspath(user_path)

    return abs_path

