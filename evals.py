# evals.py

from utils import wrapper, flatten, Pile, prog, isTailRecursion

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
            prog.memoryStack[-1].setVar(inst[1], evalExpr(inst[2]))
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
    if evalExpr(inst[1]):
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
    while evalExpr(inst[2]):
        evalLinst(inst[4])
        evalInst(inst[3])

    prog.memoryStack[-1].pop()

@wrapper
def evalWhile(inst):
    prog.memoryStack[-1].push({})
    while evalExpr(inst[1]):
        res = evalLinst(inst[2])
        if res == 'return':
            prog.memoryStack[-1].pop()
            return 'return'
    prog.memoryStack[-1].pop()

@wrapper
def evalExpr(t):

    if isinstance(t, int):
        return t
    
    if isinstance(t, str):
        if prog.memoryStack[-1].search(t) is None:
            prog.error.push(f"Variable <{t}> not defined in this scope\nStack:\n{prog.memoryStack[::-1]}")
            prog.error.crash()
        return prog.memoryStack[-1].search(t)

    if t[0] == 'expr':
        return evalExpr(t[1])

    if len(t) == 2 and t[0] in ['++', '--']:

        return evalOpertor(t[0], evalExpr(t[1]), 0)

    if len(t) != 3:

        prog.error.push(f"Expression <{t}> not recognized, expected 3 elements")
        prog.error.crash()

    if t[0] == 'call':
        return evalFunction(t)

    return evalOpertor(t[0], evalExpr(t[1]), evalExpr(t[2]))
    
@wrapper
def evalOpertor(op, x, y):
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

    return var[op](x, y)

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