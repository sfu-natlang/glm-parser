#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#

import sys
if '..' not in sys.path:
    sys.path.append('..')

# This flag enables you to debug glm-parser components
# on a non-linux (e.g Win32) machine, or machine without
# necessary components installed (hvector, cython, etc)
#
# Please make sure this flag is set to False before running
# real tests
local_debug_flag = False

# If this flag is set to True then time usage for training a sentence will
# be collected and printed
time_accounting_flag = False

# If this is set to a positive value, then the training procedure will
# run the first [run_first_num] sentences, and then exit immediately
# This saves time for dumping, evaluating, and avoids other overheads
# Usually used for evaluating time usage by running a limited set of sentences
run_first_num = -1

# If this flag is True then all feature request will be logged
log_feature_request_flag = False

