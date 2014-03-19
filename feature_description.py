from ll_parser import *

eva_debug = True

# Store functions
function_table = {}
# Store local variable dictionaries
local_var_stack = []
local_var = {}

def eva_ident(tree_node):
    if tree_node[0] != 'ident':
        raise TypeError("Only evaluates identifiers")
    if not local_var.has_key(tree_node[1]):
        raise ValueError("Identifier not defined")
    else:
        # Stores tuple, only return value
        return local_var[tree_node[1]][1]

def assign_ident(tree_node,value):
    if tree_node[0] != 'ident':
        raise TypeError("Only evaluates identifiers")
    if not local_var.has_key(tree_node[1]):
        raise ValueError("Identifier not defined")
    else:
        # Stores tuple, only return value
        local_var[tree_node[1]][1] = value

def eva_const(tree_node):
    if tree_node[0] != 'const_value' and tree_node[0] != 'const_num':
        raise TypeError("Only evaluates const value")

    # If not string then must be an integer
    if tree_node[1][0] != '"':
        return int(tree_node[1])
    else:
        # Strip the quoters
        return tree_node[1][1:-1]

def eva_exp(tree_node):
    """
    Evaluate an expression and return its value
    """
    node_len = len(tree_node)
    node_name = tree_node[0]
    # Const value
    if tree_node[0] == 'value' and tree_node[1][0] == 'const_num':
        return eva_const(tree_node[1])
    # Identifiers
    elif tree_node[0] == 'value' and tree_node[1][0] == 'ident':
        return eva_ident(tree_node[1])
    # ( add_exp )
    elif tree_node[0] == 'value' and node_len == 4:
        return eva_exp(tree_node[2])
    elif tree_node[0] == 'const_value':
        return int(tree_node[1])
    elif tree_node[0] == 'add_exp' and len(tree_node) > 2:
        if tree_node[2] == '+':
            return eva_exp(tree_node[1]) + eva_exp(tree_node[3])
        elif tree_node[2] == '-':
            return eva_exp(tree_node[1]) - eva_exp(tree_node[3])
    elif node_name == 'logic_exp' and node_len > 2 and tree_node[1] != '!':
        op = tree_node[2]
        opr1 = eva_exp(tree_node[1])
        opr2 = eva_exp(tree_node[3])
        if op == '>':
            if opr1 > opr2: return 1
            else: return 0
        elif op == '<':
            if opr1 < opr2: return 1
            else: return 0
        elif op == '>=':
            if opr1 >= opr2: return 1
            else: return 0
        elif op == '<=':
            if opr1 <= opr2: return 1
            else: return 0
        elif op == '==':
            if opr1 == opr2: return 1
            else: return 0
        elif op == '!=':
            if opr1 != opr2: return 1
            else: return 0
        elif op == '&&':
            if opr1 != 0 and opr2 != 0: return 1
            else: return 0
        elif op == '||':
            if opr1 == 0 and opr2 == 0: return 1
            else: return 0
        else: raise TypeError("Unknown logic operand type")
    elif node_name == 'logic_exp' and tree_node[1] == '!':
        if eva_exp(tree_node[2]) == 0: return 1
        else: return 0
    elif node_name == 'logic_exp':
        return eva_exp(tree_node[1])
    elif tree_node[0] == 'add_exp':
        return eva_exp(tree_node[1])
    elif tree_node[0] == 'multi_exp' and len(tree_node) > 2:
        if tree_node[2] == '*':
            return eva_exp(tree_node[1]) * eva_exp(tree_node[3])
        elif tree_node[2] == '/':
            return int(eva_exp(tree_node[1]) / eva_exp(tree_node[3]))
    elif tree_node[0] == 'multi_exp':
        return eva_exp(tree_node[1])
    elif tree_node[0] == 'exp' and len(tree_node) == 2:
        return eva_exp(tree_node[1])
    elif tree_node[0] == 'exp':
        return eva_exp(tree_node[2])
    else:
        raise ValueError("Unknown type: %s\n" % (tree_node[0]))

def check_array(ident,index):
    """
    Check: 1. whether the ident exists 2. Whether it is an array 3. Index
    legal or not
    """
    if not local_var.has_key(ident):
        raise ValueError("Have not defined array %s yet" % (ident))
    var = local_var[ident]
    if var[0][-1] != ']':
        raise TypeError("Cannot use index on a non-index array")
    if index >= len(var[1]):
        raise ValueError("Index out of bound")
    return

def eva_index_array(tree_node):
    if tree_node[0] != 'index_array':
        raise "Only evaluates index array"
    index = eva_rvalue(tree_node[3])
    ident = tree_node[1][1]
    check_array(ident,index)
    var = local_var[ident]
    return var[1][index]

def eva_rvalue(tree_node):
    if tree_node[0] != 'r_value':
        raise TypeError("Only evaluates r_value")
    
    if tree_node[1][0] == 'exp':
        return eva_exp(tree_node[1])
    elif tree_node[1][0] == 'const_value' or tree_node[1][0] == 'const_num':
        return eva_const(tree_node[1])
    elif tree_node[1][0] == 'ident':
        return eva_ident(tree_node[1])
    elif tree_node[1][0] == 'index_array':
        return eva_index_array(tree_node[1])
    else:
        raise TypeError("Unknown r_value type")

def eva_type_list(tree_node):
    """
    Return a list, the element of which is a tuple, and the first element of the
    tuple is a type, the second element is the ident
    """
    if tree_node[0] != 'type_list':
        raise TypeError("Only evaluates type list")
    if len(tree_node) == 3:
        return [(tree_node[1][1],tree_node[2][1])]
    else:
        return [(tree_node[1][1],tree_node[2][1])] + eva_type_list(tree_node[4])

def eva_rvalue_list(tree_node):
    """
    Evaluate a list of rvalues from left to right. Return value is a list of
    values
    """
    if tree_node[0] != 'rvalue_list':
        raise TypeError("Only evaluates rvalue")
    if len(tree_node) == 2:
        return [eva_rvalue(tree_node[1])]
    else:
        return [eva_rvalue(tree_node[1])] + eva_rvalue_list(tree_node[3])

def register_func(tree_node):
    """
    When we parsed a function just register it to the function table
    """
    if tree_node[0] != 'func':
        raise TypeError("Only registers functions")
    func_ident = tree_node[2][1]
    # The registered item is a tuple. The first element is the function tree
    # node, and the second is the parameter table
    if tree_node[4] != ')':
        type_list = eva_type_list(tree_node[4])
    else:
        type_list = []
    function_table[func_ident] = (tree_node,type_list)
    
    if eva_debug == True:
        print "Register function: ",func_ident,type_list
        
    return tree_node

def eva_ident_list(tree_node):
    """
    Returns a list of identifiers in a list
    """
    if tree_node[0] != 'ident_list':
        raise TypeError("Only evaluates ident_list")
    if len(tree_node) == 2:
        return [tree_node[1]]
    else:
        return [tree_node[1]] + eva_ident_list(tree_node[3])

def add_local_var(var_type,var_ident,init_val=0):
    if local_var.has_key(var_ident):
            raise ValueError("Identifier already decleared: %s" % (var_ident))
    # Initialize it to 0
    local_var[var_ident] = [var_type,init_val]
    if eva_debug == True:
        print "Adding local var: ",var_type,var_ident,'=',init_val
    return

def eva_type_decl(tree_node):
    if tree_node[0] != 'type_dec':
        raise TypeError("Only evaluates type declarations")
    # This is all the same 
    var_type = tree_node[1][1]
    # Simple type ident
    if len(tree_node) == 3 and tree_node[2][0] == 'ident':
        ident = tree_node[2][1]
        add_local_var(var_type,ident,0)
    elif tree_node[2][0] == 'ident_list':
        ident_list = eva_ident_list(tree_node[2])
        for i in ident_list:
            add_local_var(var_type,i,0)
    elif tree_node[3] == '=':
        ident = tree_node[2][1]
        init_val = eva_rvalue(tree_node[4])
        add_local_var(var_type,ident,init_val)
    # Array declaration
    elif tree_node[3] == '[':
        ident = tree_node[2][1]
        # We go to const_num directly to fetch the size
        size = eva_const(tree_node[4])
        # Base type + '[]' to indicate it is an array type
        # Initialize it with an array of 0
        add_local_var(var_type + '[]',ident,[0] * size)
    else:
        raise ValueError("Unsuppoted type decl")
    return

def assign_index_array(tree_node,value):
    if tree_node[0] != 'index_array':
        raise TypeError("Only evaluates index array")
    ident = tree_node[1][1]
    index = eva_rvalue(tree_node[3])
    check_array(ident,index)
    var = local_var[ident]
    var[1][index] = value
    return

def assign_lvalue(tree_node,value):
    if tree_node[0] != 'l_value':
        raise TypeError("Only evaluates lvalue")
    
    if len(tree_node) == 2 and tree_node[1][0] == 'ident':
        assign_ident(tree_node[1],value)
    elif len(tree_node) == 2 and tree_node[1][0] == 'index_array':
        assign_index_array(tree_node[1],value)
    else:
        raise TypeError("Unknown lvalue type")
    return

        
def eva_assign(tree_node):
    if tree_node[0] != 'assign_stmt':
        raise TypeError("Only evaluates const value")
    rvalue = eva_rvalue(tree_node[3])
    
    assign_lvalue(tree_node[1],rvalue)
    return

def eva_print(tree_node):
    if tree_node[0] != 'print_stmt':
        raise TypeError("Only evaluates print statement")
    rvalue_list = eva_rvalue_list(tree_node[2])
    for i in rvalue_list:
        print i,
    print ''
    return

def eva_stmt(tree_node):
    if tree_node[1][0] == 'type_dec':
        eva_type_decl(tree_node[1])
    elif tree_node[1][0] == 'assign_stmt':
        eva_assign(tree_node[1])
    elif tree_node[1][0] == 'print_stmt':
        eva_print(tree_node[1])
    elif tree_node[1][0] == 'if_stmt':
        eva_if_stmt(tree_node[1])
    else:
        raise TypeError("Unknown stmt type: " + tree_node[1][0])

def eva_stmts(tree_node):
    if tree_node[0] != 'stmts':
        raise ValueError("Only evaluates statements")
    if len(tree_node) == 3:
        eva_stmt(tree_node[1])
    else:
        eva_stmt(tree_node[1])
        eva_stmts(tree_node[3])
    return

def eva_if_stmt(tree_node):
    if tree_node[0] != 'if_stmt':
        raise TypeError("Only evaluates if statements")
    cond = eva_rvalue(tree_node[3])
    if cond == 0:
        if len(tree_node) == 8:
            return
        else:
            # The else part
            eva_stmts(tree_node[10])
    else:
        # The if part
        eva_stmts(tree_node[6])
    return
    
nonterminal_func_dict['register_func'] = register_func

simple_cfg = """
    program -> func
    program -> func program
    
    func -> type ident ( ) { stmts } <- register_func
    func -> type ident ( type_list ) { stmts } <- register_func
    
    type_list -> type ident
    type_list -> type ident , type_list

    stmts -> stmt ;
    stmts -> stmt ; stmts
    
    stmt -> assign_stmt
    stmt -> return
    stmt -> type_dec
    stmt -> return exp
    stmt -> print_stmt
    stmt -> if_stmt

    if_stmt -> if ( r_value ) { stmts }
    if_stmt -> if ( r_value ) { stmts } else { stmts }

    type_dec -> type ident
    type_dec -> type ident_list
    type_dec -> type ident = r_value
    type_dec -> type ident [ const_num ]
    
    ident_list -> @c_ident
    ident_list -> @c_ident , ident_list

    rvalue_list -> r_value
    rvalue_list -> r_value , rvalue_list
    
    assign_stmt -> l_value = r_value

    print_stmt -> #print rvalue_list
    
    exp -> logic_exp
    exp -> ( logic_exp )
    value -> ( logic_exp )
    
    logic_exp -> add_exp
    //logic_exp -> ! logic_exp
    //logic_exp -> add_exp || logic_exp
    //logic_exp -> add_exp && logic_exp
    
    logic_exp -> add_exp > logic_exp
    logic_exp -> add_exp < logic_exp
    logic_exp -> add_exp >= logic_exp
    logic_exp -> add_exp <= logic_exp
    logic_exp -> add_exp == logic_exp
    logic_exp -> add_exp != logic_exp
    
    add_exp -> multi_exp
    add_exp -> multi_exp - add_exp
    add_exp -> multi_exp + add_exp
    multi_exp -> value
    multi_exp -> value / multi_exp
    multi_exp -> value * multi_exp
    value -> const_num

    index_array -> ident [ r_value ]
    
    value -> ident
    value -> ident ( )

    const_num -> @c_decimal
    const_value -> @c_decimal
    const_value -> @c_str
    
    r_value -> ident
    r_value -> ident ( )
    l_value -> ident
    l_value -> index_array
    r_value -> const_value
    r_value -> exp
    r_value -> index_array
    
    ident -> @c_ident
    type -> void
    type -> int
    type -> string
"""


s = IndexedStr("""
void main(int argc,int argv)
{
    int a = 2 + (3 * 6);
    int b = a * a;

    return b;
}
""")

test = IndexedStr("""
    int a,b,c,d;
    int wzq[10];
    int f = 99 + (5 * 9);
    int g = f * 2;
    int h = g - 100;
    int str = "I am the king!";
    wzq[1] = 1024;
    a = wzq[1];
    if( (a == (1023 + 1)) )
    {
        #print "This is",a,h * 2,h * h;
    }
    else
    {
        #print str;
    };
    """)

class FeatureDescription():
    """
    Parse a feature description and generates features using dependency tree
    instances and position marks.
    """
    def __init__(self,dep_tree,cfg,program):
        """
        Initialize the parser, and use the parser to parse the input program
        and generate a parsing tree.

        :param dep_tree: A dependency tree instance
        :type dep_tree: DependencyTree
        :param cfg: A context-free grammar
        :type cfg: str
        :param program: A program string
        :type program: IndexedStr
        """
        self.parser = LLParser()
        self.dep_tree = dep_tree
        self.parser.parse_cfg(cfg)
        self.parse_tree = self.parser.symbol_table['stmts'].parse(program)
        self.parser.print_tree(self.parse_tree)
        #if not program.is_end():
        #    raise ValueError("Parse fail.")
        return

    def get_feature(self,head_index,dep_index):
        global local_var
        local_var['head_index'] = ('int',head_index)
        local_var['dep_index'] = ('int',dep_index)
        local_var['word_list'] = ('string[]',self.dep_tree.word_list)
        local_var['pos_list'] = ('string[]',self.dep_tree.pos_list)
        local_var['length'] = ('int',len(self.dep_tree.word_list))
        eva_stmts(self.parse_tree)
        # We assume the program write into this statement
        return local_var['result'][1]


if __name__ == '__main__':
    lp = LLParser()
    lp.parse_cfg(simple_cfg)
    t = lp.symbol_table['stmts'].parse(test)
    lp.print_tree(t)
    eva_stmts(t)
    
