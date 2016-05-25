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
#           |
#           |-glm_parser.py  -> Main function
#

import os
print(os.path.join(os.path.dirname(os.getcwd()), 'src') + os.sep)
