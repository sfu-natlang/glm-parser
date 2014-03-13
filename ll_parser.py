
from regular_expression import *

class Nonterminal():
    """
    Nonterminal node used by LL parser
    """
    def __init__(self,name=""):
        """
        Initialize a child list. The children will be trated in order, and
        we do not pick the longest one
        """
        self.child_list = []
        self.name = name
        pass

    def append(self,child_node):
        """
        Add a new alternative into its child_list. All nodes in child_list is
        treated as "or" relation rather than concatenation
        """
        self.child_list.append(child_node)
        return

    def parse(self,s):
        """
        Parse the non-terminal
        """
        for i in child_list:
            ret = i.parse(s)
            if ret == None:
                return None
            else:
                return ret

class Terminal():
    """
    Terminal node used by LL parser
    """
    def __init__(self,regular_exp):
        """
        Initialize the terminal node with a regular expression
        """
        if not isinstance(regular_exp,RegExp):
            raise TypeError("The leaf node must be a RegExp instance!")
        else:
            self.regexp = regular_exp
        return

    def parse(self,s):
        return self.regexp.parse(s)


class LLParser():
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

    def process_cfg_rule(self,line,symbol_table,nonterminal_list):
        for symbol in line[2:]:
            # Symbol is a terminal
            if symbol not in nonterminal_list:
                # Symbol is a reference to the RegBuilder
                if symbol[0] == '@':
                    if not reg_dict.has_key(symbol[1:]):
                        raise ValueError("""There is not a predefined terminal
                                            %s\n""" % (symbol[1:]))
                    # Create a new non-terminal node
                    nt = Nonterminal(line[0])
                    
                    

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
        
