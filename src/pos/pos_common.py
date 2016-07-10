# These are the shared functions for the POS Tagger.
import os
import sys
import inspect
from data.file_io import *


# read the valid output tags for the task
def read_tagset(file_path, sparkContext=None):
    tagset = []
    in_file = fileRead(file_path, sparkContext)
    for line in in_file:
        line = line.strip()
        tagset.append(line)
    return tagset
