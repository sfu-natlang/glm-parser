
from regular_expression import *
#reg_dict is the dictionary that contains some important regular expressions

nonterminal_func_dict = {
    # Default processor for nonterminal nodes
    None: lambda(x): x,
    }

class Nonterminal():
    concat_node = 0
    union_node = 1
    """
    Nonterminal node used by LL parser
    """
    def __init__(self,name="",node_type=concat_node,func_name=None):
        """
        Initialize a child list. The children will be trated in order, and
        we do not pick the longest one
        """
        self.child_list = []
        self.name = name
        self.func_name = func_name
        if node_type == Nonterminal.concat_node:
            self.parse = self.parse_concat
        elif node_type == Nonterminal.union_node:
            self.parse = self.parse_union
        else:
            raise TypeError("Nonterminal type unsupported: %d\n" % (node_type))
        return

    def set_func_name(self,func_name):
        self.func_name = func_name
        return

    def append(self,child_node):
        """
        Add a new alternative into its child_list.
        """
        self.child_list.append(child_node)
        return
    

    def parse_union(self,s):
        """
        Parse the union non-terminal. It acts as an intermediate level when
        there is multiple definition for a non-terminmal
        """
        s.push_index()
        print 'push: ',s.stack[-1]
        for i in self.child_list:
            # Save the state before parsing
            s.push_index()
            ret = i.parse(s)
            #print self.name,ret
            # We only return the first match, not the longest match
            if ret != None:
                return ret
            else:
                # If parsing fail then restore state and prepare for next try
                s.pop_index()
        s.pop_index()
        print 'pop: ', s.start_index
        return None

    def parse_concat(self,s):
        """
        Parse the concatenation non-terminal.
        """
        s.push_index()
        # Record the name as the first element
        parse_result = [self.name]
        for i in self.child_list:
            reg_dict['spaces'].parse(s)
            ret = i.parse(s)
            print self.name,ret
            if ret == None:
                s.pop_index()
                return None
            else:
                parse_result.append(ret)

        parse_result = nonterminal_func_dict[self.func_name](parse_result)
        return parse_result

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
        # We add the union node first, because we may have to refer to this
        # later. node_union is the union node for nonterminal line[0]
        if line[0] not in symbol_table:
            node_union = Nonterminal("union",node_type=Nonterminal.union_node)
            symbol_table[line[0]] = node_union
        else:
            node_union = symbol_table[line[0]]
        # Create the node for this line
        node_concat = Nonterminal(line[0])
        # Add the node into the union node for this nonterminal
        # (now the node is empty but we will add contents later)
        node_union.append(node_concat)
        
        # We start from the second element
        line_index = 2
        # The name of the function in nonterminal_func_dict to process
        # the returned list
        func_name = None
        
        for symbol in line[2:]:
            # In the loop line_index is always the index of the next symbol
            line_index += 1
            # The following is function declaration
            if symbol == '<-':
                # The next symbol must be function name
                func_name = line[line_index]
                # Register that function into the node
                node_concat.set_func_name(func_name)
                # The symbol after <- is a function name, and we assume the line
                # is over after that
                break
            # Symbol is a terminal
            elif symbol not in nonterminal_list:
                # Symbol is a reference to the RegBuilder
                if symbol[0] == '@':
                    if not reg_dict.has_key(symbol[1:]):
                        raise ValueError("""There is not a predefined terminal
                                            %s\n""" % (symbol[1:]))
                    # Push the RegExp into nonterminal node
                    node_concat.append(reg_dict[symbol[1:]])
                # Symbol is a string, also a terminal. So we need to wrap it
                else:
                    node_regexp = RegExp(symbol)
                    node_concat.append(node_regexp)
            # The symbol is a nonterminal, we need to look up the dict
            else:
                if symbol not in symbol_table:  # key in dict is allowed
                    raise ValueError("""You have not defined the nonterminal
                                        %s yet\n""" % (symbol))
                else:
                    node_concat.append(symbol_table[symbol])
                    
        return

    def parse_cfg(self,s,reverse=True):
        """
        :param reverse: If it is true then we will reverse the line list before
        we process it. This is useful if you want to do a top-down definition
        :type reverse: bool
        """
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
        self.check_cfg_arrow(line_list)
        nonterminal_list = self.extract_cfg_nonterminal(line_list)
        # Store all defined nonterminal
        symbol_table = {}

        if reverse == True:
            line_list.reverse()

        for line in line_list:
            self.process_cfg_rule(line,symbol_table,nonterminal_list)

        self.symbol_table = symbol_table
        self.nonterminal_list = nonterminal_list
        return
    
    def print_tree(self,tree_root,level=0):
        if not isinstance(tree_root,str):
            print tree_root[0]
            for i in tree_root[1:]:
                print "  " * level,
                self.print_tree(i,level + 1)
        else:
            print tree_root
        return

nonterminal_func_dict['func_func'] = lambda(x): x[:-2]
nonterminal_func_dict['func_func2'] = lambda(x): x[:3] + x[4:-1]

if __name__ == "__main__":
    cfg_str = """
    func -> type ident ( ) <- func_func
    func -> type ident ( type_list ) <- func_func2
    type_list -> type ident
    type_list -> type ident , type_list
    type -> void
    type -> int
    type -> char
    ident -> @c_ident
    """
    
    ll = LLParser()
    ll.parse_cfg(cfg_str)
    index_str = IndexedStr("void main(int argc,char argv)")
    is2 = IndexedStr("int argc,char argv")
    #ll.print_tree(ll.symbol_table['func'].parse(index_str))
    ll.symbol_table['type_list'].parse(is2)
    #print ll.symbol_table['N'].child_list[0].child_list[0].token_list
    print is2.s[is2.start_index:]
        
