import os


def sync_a_b(a_path, b_path):
    a_mtime = os.path.getmtime(a_path)
    b_mtime = os.path.getmtime(b_path)
    return a_mtime-b_mtime

