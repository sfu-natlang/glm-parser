# These are the shared functions for the POS Tagger.
import os
import sys
import inspect


# read the valid output tags for the task
def read_tagset(file_path):
    tagset = []
    with open(file_path, "r") as in_file:
        for line in in_file:
            line = line.strip()
            tagset.append(line)
    return tagset
