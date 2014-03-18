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
    if tree_node[0] != 'const_value':
        raise TypeError("Only evaluates const value")
    return int(tree_node[1])

def eva_exp(tree_node):
    """
    Evaluate an expression and return its value
    """
    node_len = len(tree_node)
    # Const value
    if tree_node[0] == 'value' and tree_node[1][0] == 'const_value':
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

def eva_rvalue(tree_node):
    if tree_node[0] != 'r_value':
        raise TypeError("Only evaluates r_value")
    
    if tree_node[1][0] == 'exp':
        return eva_exp(tree_node[1])
    elif tree_node[1][0] == 'const-value':
        return eva_const(tree_node[1])
    elif tree_node[1][0] == 'ident':
        return eva_ident(tree_node[1])
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
    else:
        raise ValueError("Unsuppoted type decl")
    return

def eva_assign(tree_node):
    if tree_node[0] != 'assign_stmt':
        raise TypeError("Only evaluates const value")
    rvalue = eva_rvalue(tree_node[3])
    
    # lvalue is identifier
    if tree_node[1][0] == 'ident':
        assign_ident(rvalue)
    else:
        raise TypeError("Unknown assignment type")

def eva_stmt(tree_node):
    if tree_node[1][0] == 'type_dec':
        eva_type_decl(tree_node[1])
    elif tree_node[1][0] == 'assign_stmt':
        eva_assign(tree_node[1])
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

    type_dec -> type ident
    type_dec -> type ident_list
    type_dec -> type ident = r_value
    
    ident_list -> @c_ident
    ident_list -> @c_ident , ident_list
    
    assign_stmt -> l_value = r_value
    
    exp -> add_exp
    exp -> ( add_exp )
    value -> ( add_exp )
    add_exp -> multi_exp
    add_exp -> multi_exp - add_exp
    add_exp -> multi_exp + add_exp
    multi_exp -> value
    multi_exp -> value / multi_exp
    multi_exp -> value * multi_exp
    value -> const_value
    
    value -> ident
    value -> ident ( )
    
    const_value -> @c_decimal
    
    r_value -> ident
    r_value -> ident ( )
    l_value -> ident
    r_value -> const_value
    r_value -> exp
    ident -> @c_ident
    type -> void
    type -> int
"""



s = IndexedStr("""
void main(int argc,int argv)
{
    int a = 2 + (3 * 6);
    int b = a * a;

    return b;
}
""")

test = IndexedStr(""" int a,b,c,d; int f = 99 + (5 * 9);int g = f * 2;
int h = g - 100; a = h;""")

if __name__ == '__main__':
    lp = LLParser()
    lp.parse_cfg(simple_cfg)
    t = lp.symbol_table['stmts'].parse(test)
    lp.print_tree(t)
    eva_stmts(t)
    
