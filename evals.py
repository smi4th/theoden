# evals/controlStructures.py

from utils import wrapper, flatten, flatten_tuple, Pile, prog

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
            return evalCallFunction(inst)
        case 'functions':
            # This is a function definition, we don't need to evaluate it, it is already in the functions dictionary
            pass
        case 'print':
            return evalPrint(inst[1])
            #print(evalExpr(inst[1]))
        case 'return':
            prog.memoryStack[-2].setVar('$__return__$', evalExpr(inst[1]))
            # prog.memoryStack.pop()
            return "return"
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
    prog.memoryStack[-1].pop()
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
        evalLinst(inst[2])

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
        evalCallFunction(t)
        if prog.memoryStack[-1].search('$__return__$') is None:
            prog.error.push(f"Function <{t[1]}> did not return any value")
            prog.error.crash()
        return prog.memoryStack[-1].search('$__return__$')

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
def evalCallFunction(inst):
    if inst[1] in prog.functions:

        callParams = [evalExpr(i) for i in inst[2][1:]] if inst[2] != 'empty' else []
        funcParams = flatten(prog.functions[inst[1]][0])


        if len(funcParams) != len(callParams):
            prog.error.push(f"Function <{inst[1]}> takes {len(funcParams)} arguments, {len(callParams)} given\n{inst[1]}({', '.join((str(c) for c in callParams))}) -> {inst[1]}({', '.join(funcParams)})")
            prog.error.crash()

        tmpPile = Pile()
        for fParam, cParam in zip(funcParams, callParams):
            tmpPile.top()[fParam] = evalExpr(cParam)

        prog.memoryStack.append(tmpPile)

        if (prog.functions[inst[1]][1][0] == 'return'):
            res = evalInst(prog.functions[inst[1]][1])
        else:
            res = evalLinst(prog.functions[inst[1]][1])
        return res
    else:
        prog.error.push(f"Function <{inst[1]}> not defined")
        prog.error.crash()