# evals.py

from utils import wrapper, flatten, Pile, prog, flatten_tuple

@wrapper
def evalLinst(linst):
    for inst in linst:
        if evalInst(inst) == 'return': return 'return'

@wrapper
def evalInst(inst):

    if inst in ['empty', 'linst']:
        return

    if not isinstance(inst, tuple):
        prog.error.push(f"Instruction <{inst}> not recognized")
        prog.error.crash()

    if inst[0] == 'linst':
        return evalLinst(inst[1:])

    match inst[0]:
        case 'assign':
            assign(inst)
        case 'if':
            return evalCond(inst)
        case 'for':
            return evalFor(inst)
        case 'while':
            return evalWhile(inst)
        case 'call':
            return evalFunction(inst)
        case 'functions':
            pass # function definition are already handled in the parser
        case 'print':
            return evalPrint(inst[1])
        case 'return':
            prog.memoryStack[-1].setVar('return', evalExpr(inst[1]))
            return 'return'
        case _:
            prog.error.push(f"Instruction <{inst[0]}> not recognized")
            prog.error.crash()

    return inst

@wrapper
def assign(inst):
    if inst[1][0] != 'array_access' and inst[2][0] != 'array':
        prog.memoryStack[-1].setVar(inst[1], evalExpr(inst[2]))
        return
    
    if inst[2][0] == 'array':
        # a = []
        array = transformArray(inst[2][1])
        if array[0] == 'expr':
            array = array[1:]

        if not isinstance(array[0], tuple):
            array = (array,)

        if array[0][0] == 'empty':
            prog.memoryStack[-1].setVar(inst[1], array)
            return

        array = list(array)

        for i in range(len(array)):
            array[i] = evalExpr(array[i])

        prog.memoryStack[-1].setVar(inst[1], tuple(array))
        return

    # a[0] = 1
    array = prog.memoryStack[-1].search(inst[1][1])
    if array is None:
        prog.error.push(f"Variable <{inst[1][1]}> not defined in this scope")
        prog.error.crash()

    index = evalExpr(inst[1][2])

    if index[0] != 'int':
        prog.error.push(f"Index must be an integer")
        prog.error.crash()

    if len(array) <= index[1] or array[0] == ('empty',):
        prog.error.push(f"Index out of range")
        prog.error.crash()

    array = list(array)
    array[index[1]] = evalExpr(inst[2])

    prog.memoryStack[-1].setVar(inst[1][1], tuple(array))
        
def transformArray(inst):
    def extract_expressions(expr):
        """
        Fonction récursive pour extraire les sous-expressions d'une structure imbriquée.
        Gère également les structures 'array'.
        """
        if expr[0] == 'expr':
            # Parcours récursif sur les sous-éléments, en excluant le premier niveau ('expr').
            expressions = []
            for sub_expr in expr[1:]:
                expressions.extend(extract_expressions(sub_expr))
            return expressions
        elif expr[0] == 'array':
            # Si c'est une structure 'array', transformer les sous-éléments en tuples imbriqués.
            arrays = []
            for sub_expr in expr[1:]:
                arrays.append(tuple(extract_expressions(sub_expr)))
            return arrays
        else:
            # Si ce n'est ni 'expr' ni 'array', c'est une sous-expression valide.
            return [expr]

    # Extraire toutes les sous-expressions
    flat_expressions = extract_expressions(inst)

    # Reconstruire la structure finale
    if len(flat_expressions) == 1 and isinstance(flat_expressions[0], tuple):
        return flat_expressions[0]  # Cas où on obtient une seule structure 'array'.
    return ('expr', *flat_expressions)

dataPrint = []

def dataToPrint(inst):

    if len(inst) == 2:
        dataPrint.append(evalExpr(inst[1]))
        return
    else:

        dataPrint.append(evalExpr(inst[2]))

        return evalPrint(inst[1])

@wrapper
def evalPrint(inst):
    global dataPrint

    dataToPrint(inst)

    print(*dataPrint[::-1])

    dataPrint = []

    return

@wrapper
def evalCond(inst):
    prog.memoryStack[-1].push({})
    res = None

    if evalExpr(inst[1])[1]:
        res = evalLinst(inst[2])
    elif inst[-1] != 'empty':
        res = evalLinst(inst[-1][1])

    returnValue = prog.memoryStack[-1].search('return')
    prog.memoryStack[-1].pop()
    
    if returnValue is not None:
        prog.memoryStack[-1].setVar('return', returnValue)
        return 'return'
    
    return res
    
@wrapper
def evalFor(inst):
    prog.memoryStack[-1].push({})
    evalInst(inst[1])
    while evalExpr(inst[2])[1]:
        evalLinst(inst[4])
        evalInst(inst[3])

    prog.memoryStack[-1].pop()

@wrapper
def evalWhile(inst):
    prog.memoryStack[-1].push({})
    while evalExpr(inst[1])[1]:
        res = evalLinst(inst[2])
        if res == 'return':
            prog.memoryStack[-1].pop()
            return 'return'
    prog.memoryStack[-1].pop()

@wrapper
def evalExpr(t):

    match t[0]:
        case 'int':
            return t
        case 'var':
            var = prog.memoryStack[-1].search(t[1])
            if var is None:
                prog.error.push(f"Variable <{t[1]}> not defined in this scope\nStack:\n{prog.memoryStack[::-1]}")
                prog.error.crash()
            return var
        case 'float':
            return t
        case 'bool':
            return t
        case 'char':
            return t
        case 'array':
            return t

    if t[0] == 'expr':
        return evalExpr(t[1])

    if len(t) == 2 and t[0] in ['++', '--']:

        res = evalOpertor(t[0][0], evalExpr(t[1]), 1)

        prog.memoryStack[-1].setVar(t[1], res)
        return res

    if t[0] == 'call':
        return evalFunction(t)

    return evalOpertor(t[0], evalExpr(t[1]), evalExpr(t[2]))

@wrapper
def evalNumberOperator(op, x, y, type):
    var = {
        '+'     : lambda x, y: x + y,
        '-'     : lambda x, y: x - y,
        '*'     : lambda x, y: x * y,
        '/'     : lambda x, y: x / y,
        '%'     : lambda x, y: x % y,
        '<'     : lambda x, y: x < y,
        '<='    : lambda x, y: x <= y,
        '>='    : lambda x, y: x >= y,
        '=='    : lambda x, y: x == y,
        '>'     : lambda x, y: x > y,
        '&&'    : lambda x, y: x and y,
        '||'    : lambda x, y: x or y,
        '++'    : lambda x, y: x + 1,
        '--'    : lambda x, y: x - 1,
    }

    if op in ['/', '%'] and y == 0:
        prog.error.push(f"Division by zero")
        prog.error.crash()

    if op in ['<', '<=', '>=', '==', '>', '&&', '||']:
        return ('bool', var[op](x, y))
    
    if op in ['/', '%']:
        return ('float', var[op](x, y))

    return (type, var[op](x, y))

def evalBoolOperator(op, x, y):
    var = {
        '&&'    : lambda x, y: x and y,
        '||'    : lambda x, y: x or y,
        '=='    : lambda x, y: x == y,
    }

    return ('bool', var[op](x, y))

def evalCharOperator(op, x, y):
    var = {
        '<'     : lambda x, y: x < y,
        '<='    : lambda x, y: x <= y,
        '>='    : lambda x, y: x >= y,
        '=='    : lambda x, y: x == y,
        '>'     : lambda x, y: x > y,
    }

    return ('bool', var[op](x, y))

@wrapper
def evalOpertor(op, x, y):
    if x[0] == y[0] == 'int':
        return evalNumberOperator(op, x[1], y[1], 'int')
    if x[0] == y[0] == 'float':
        return evalNumberOperator(op, x[1], y[1], 'float')
    if x[0] == y[0] == 'bool':
        return evalBoolOperator(op, x[1], y[1])
    if x[0] == y[0] == 'char':
        return evalCharOperator(op, x[1], y[1])

@wrapper
def evalFunction(inst):

    # if the function is not defined
    if inst[1] not in prog.functions:
        prog.error.push(f"Function <{inst[1]}> not defined")
        prog.error.crash()

    # if the function is defined
    tmp = Pile()
    tmp.push({})

    # if the function has arguments
    if inst[2] != 'empty':
        # check if the number of arguments is correct
        
        args = inst[2][1:] # values passed to the function
        params = flatten(prog.functions[inst[1]][0])

        if len(args) != len(params):
            prog.error.push(f"Function <{inst[1]}> expected {len(params)} arguments, got {len(args)}")
            prog.error.crash()

        # assign the values to the parameters
        for i in range(len(args)):
            tmp.setVar(params[i], evalExpr(args[i]))

    prog.memoryStack.append(tmp)

    # execute the function
    evalLinst(prog.functions[inst[1]][1])

    # get the return value
    res = prog.memoryStack[-1].search('return')
    
    # pop the stack
    prog.memoryStack.pop()

    return res