#
# A simple helper procedure that prints out the
# absolute path to src/ folder in glm-parser project

# Please change this file accordingly when the structure
# of project is changed

# We made these assumptions about the directory structure:
# -
# |-glm-parser
#        |
#        |-script  -> Where this script lies
#        |
#        |-src     -> Where the main procedure lies
#

import os
from sys import exit

cwd = os.getcwd()

if '\\' in cwd:
    # Windows
    path_list = cwd.split('\\')
    src_path = ''
    for i in path_list[:-1]:
        src_path += (i + '\\')
    src_path += 'src\\'
    print(src_path)
    exit(0)
elif '/' in cwd:
    # UNIX or LINUX
    path_list = cwd.split('/')
    src_path = ''
    for i in path_list[:-1]:
        src_path += (i + '/')
    src_path += 'src/'
    print(src_path)
    exit(0)
else:
    print(cwd)
    exit(0)
