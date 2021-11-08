import os

def create_tree(path):
    files = []
    files_names = []
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
                files.append(os.path.join(root,f))
                files_names.append(os.path.join(f))
    return files, files_names

