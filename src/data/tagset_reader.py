from data.file_io import *


def read_tagset(file_path, sparkContext=None):
    tagset = []
    in_file = fileRead(file_path, sparkContext)
    for line in in_file:
        line = line.strip()
        tagset.append(line)
    return tagset
