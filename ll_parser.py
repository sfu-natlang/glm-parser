
from regular_expression import *

def LLParser():
    """
    A simple LL(1) parser that uses context-free grammar to describe a set
    of rules to form a string. This parser will not always return the best
    parse, however it tries its best to achieve the optimism.
    """
    def __init__(self):
        pass

    def check_cfg_arrow(self,line_list):
        """
        Internally called - Check whether the CFG has an arrow and whether
        the arrow is the 2nd element
        """
        for line in line_list:
            if line[1] != '->':
                raise ValueError("""Each context-free grammar rule must has
                                    an arrow and it must be the second
                                    token in the line.""")
        return

    def extract_cfg_nonterminal(self,line_list):
        """
        Extract all nonterminals in the CFG. All symbols that has a definition
        (i.e. appears as the first element of each line) is considered as
        non-terminal. All other elements are considered as terminals

        :return: A list of nonterminals
        :rtype: list(str)
        """
        return [line[0] for line in line_list] 

    def parse_cfg(self,s):
        # We process the grammar in a line basis
        lines_unprocessed = s.splitlines()
        line_list = []
        for i in lines_unprocessed:
            # Only use lines that are not empty
            trimed_line = i.strip()
            if trimed_line != '':
                # Store the list of tokens into line_list
                line_list.append(trimed_line.split())
        # We only check the arrow
        check_cfg_arrow(line_list)
        nonterminal_list = extract_cfg_nonterminal(line_list)
        # Store all defined nonterminal
        symbol_table = {}
        
