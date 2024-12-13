# -*- coding: utf-8 -*-

reserved={
        'print':'PRINT',
        'if':'IF',
        'else':'ELSE',
        'while':'WHILE',
        'for':'FOR',
        'fonction':'FUNCTIONDEF',
        'return':'RETURN',
    }

tokens = [ 'NUMBER','MINUS', 'PLUS','TIMES','DIVIDE', 'MODULO', 'LPAREN', 'LBRA', 'RBRA',
          'RPAREN', 'OR', 'AND', 'SEMI', 'EGAL', 'NAME', 'INF', 'SUP', 'SUPEG',
          'EGALEGAL','INFEG', 'COMMA']+ list(reserved.values())

t_PLUS = r'\+' 
t_MINUS = r'-' 
t_TIMES = r'\*' 
t_DIVIDE = r'/' 
t_MODULO = r'%'
t_LPAREN = r'\(' 
t_RPAREN = r'\)' 
t_LBRA = r'\{'
t_RBRA = r'\}'
t_OR = r'\|'
t_AND = r'\&'
t_SEMI = r';'
t_EGAL = r'\='
t_INF = r'\<'
t_SUP = r'>'
t_SUPEG = r'\>\='
t_INFEG = r'\<\='
t_EGALEGAL = r'\=\='
t_COMMA = r'\,'

DEBUG_WRAPPER, DEBUG_TIME, DEBUG_MEMORY = False, False, False

from sys import argv
debug_flags = {
    'DEBUG_WRAPPER': ['--debug-wrapper', '-w'],
    'DEBUG_TIME': ['--debug-time', '-t'],
    'DEBUG_MEMORY': ['--debug-memory', '-m']
}

# Flatten the arguments in argv, checking each individual character for matching flags
for key, flags in debug_flags.items():
    globals()[key] = any(any(flag in arg for flag in flags) for arg in argv)

def wrapper(f):
    def wrap(*args, **kwargs):
        if DEBUG_WRAPPER:
            print(f"\033[32m{f.__name__}\033[0m")
            for arg in args:
                print(f"\t\033[33m{arg}\033[0m")
        res = f(*args, **kwargs)
        if DEBUG_WRAPPER:
            print(f"\033[34m  {f.__name__} -> {res}\033[0m")
        return res
    return wrap

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

def t_NUMBER(t): 
    r'\d+' 
    t.value = int(t.value) 
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    errors.push(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    errors.crash()
    
import ply.lex as lex
lex.lex()

class pile:
    def __init__(self):
        self.p=[{}]
    
    def push(self,x):
        self.p.append(x)
    
    def pop(self):
        return self.p.pop()
    
    def top(self):
        return self.p[-1]
    
    def empty(self):
        return self.p==[]
    
    def search(self,x):
        for stack in self.p[::-1]:
            if x in stack:
                return stack[x]
        return None
    
    def setVar(self, name, value):
        self.top()[name] = value

    def reverse(self):
        self.p = self.p[::-1]
    
    def translate(self, linst):

        for elt in linst:
            if isinstance(elt, tuple):
                if elt[0] in self.block_keywords and elt[0] not in self.function_keywords:
                    self.push(elt)
                    continue
                self.translate(elt[1:])
    
    def __repr__(self):
        res = ""
        for i in self.p[::-1]:
            res += str(i) + "\n"
        return res

class Errors(pile):
    def __init__(self):
        super().__init__()
        self.p = []
    def crash(self):
        print(f"\033[31m{self}\033[0m", end="\033[37m")
        exit(1)

memoryStack = [pile()]

callPile = pile()
callPile.block_keywords = ['functions', 'if', 'for', 'while', 'assign', 'call', 'print']
callPile.function_keywords = ['main', 'linst']
errors = Errors()

functions={}

precedence = ( 
        ('left','OR' ), 
        ('left','AND'), 
        ('nonassoc', 'INF', 'INFEG', 'EGALEGAL', 'SUP'), 
        ('left','PLUS', 'MINUS' ), 
        ('left','TIMES', 'DIVIDE', 'MODULO'),
        )

def p_start(p):
    '''start : prog'''
    # printTreeGraph(p[1])
    errors.p = []

    callPile.p = []
    callPile.translate(p[1])
    callPile.reverse()

    if DEBUG_TIME:
        from time import time
        start = time()
    while not callPile.empty():
        evalInst(callPile.pop())
    if DEBUG_TIME:
        print(f"Execution time: {time() - start}")
    
    if DEBUG_MEMORY:
        print(f"Memory stack: {[str(i) for i in memoryStack]}")

@wrapper
def evalLinst(linst):
    for inst in linst:
        if evalInst(inst) == 'return': return 'return'

@wrapper
def evalInst(inst):

    if inst in ['empty', 'linst']:
        return

    if not isinstance(inst, tuple):
        errors.push(f"Instruction <{inst}> not recognized")
        errors.crash()

    if inst[0] == 'linst':
        return evalLinst(inst[1:])

    match inst[0]:
        case 'assign':
            memoryStack[-1].setVar(inst[1], evalExpr(inst[2]))
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
            print(evalExpr(inst[1]))
        case 'return':
            if inst[1] == 'empty': # No return value
                memoryStack[-2].setVar('$__return__$', None)
            else:
                memoryStack[-2].setVar('$__return__$', evalExpr(inst[1]))
            memoryStack.pop()
            return "return"
        case _:
            errors.push(f"Instruction <{inst[0]}> not recognized")
            errors.crash()

    return inst
    
@wrapper
def flatten(tup):

    if not isinstance(tup, tuple):
        return ()

    result = []
    for item in tup[1:]:
        if isinstance(item, tuple):
            result.extend(flatten(item))
        else:
            result.append(item)
    return tuple(result)

with open('test.txt', 'r') as file:
    s = file.read()

@wrapper
def evalCond(inst):
    if evalExpr(inst[1]):
        return evalLinst(inst[2])
    elif inst[-1] != 'empty':
        return evalLinst(inst[-1][1])
    
@wrapper
def evalFor(inst):
    memoryStack[-1].push({})
    evalInst(inst[1])
    while evalExpr(inst[2]):
        evalLinst(inst[4])
        evalInst(inst[3])

    memoryStack[-1].pop()

@wrapper
def evalWhile(inst):
    memoryStack[-1].push({})
    while evalExpr(inst[1]):
        evalLinst(inst[2])

    memoryStack[-1].pop()

@wrapper
def evalCallFunction(inst):
    if inst[1] in functions:

        callParams = flatten(inst[2])
        funcParams = flatten(functions[inst[1]][0])

        if len(funcParams) != len(callParams):
            errors.push(f"Function <{inst[1]}> takes {len(funcParams)} arguments, {len(callParams)} given\n{inst[1]}({', '.join((str(c) for c in callParams))}) -> {inst[1]}({', '.join(funcParams)})")
            errors.crash()

        tmpPile = pile()
        for fParam, cParam in zip(funcParams, callParams):
            tmpPile.top()[fParam] = evalExpr(cParam)

        memoryStack.append(tmpPile)

        if (functions[inst[1]][1][0] == 'return'):
            res =  evalInst(functions[inst[1]][1])
        else:
            res = evalLinst(functions[inst[1]][1])
            # memoryStack.pop()
        return res
    else:
        errors.push(f"Function <{inst[1]}> not defined")
        errors.crash()

@wrapper
def evalExpr(t):

    if isinstance(t, int):
        return t
    
    if isinstance(t, str):
        if memoryStack[-1].search(t) is None:
            errors.push(f"Variable <{t}> not defined in this scope\nStack:\n{memoryStack[::-1]}")
            errors.crash()
        return memoryStack[-1].search(t)

    if t[0] == 'call':
        evalCallFunction(t)
        if memoryStack[-1].search('$__return__$') is None:
            errors.push(f"Function <{t[1]}> does not return a value")
            errors.crash()
        return memoryStack[-1].search('$__return__$')

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
        '||'    : lambda x, y: x or y
    }

    if op in ['/', '%'] and y == 0:
        errors.push(f"Division by zero")
        errors.crash()

    return var[op](x, y)

def p_prog(p):
    '''prog : functions main functions
    | functions main
    | main functions
    | main
    | functions'''

    if len(p)==2 : 
        p[0] = ('prog', p[1], 'empty')
    else : 
        p[0] = ('prog', p[1], p[2])
    
def p_functions(p):
    '''functions : functions function
    | function'''
    if len(p)==2 : 
        p[0] = ('functions', p[1])
    else : 
        p[0] = ('functions', p[1], p[2])
    
def p_return(p):
    '''return : RETURN expression SEMI
    | RETURN SEMI'''
    if len(p)==3 : 
        p[0] = ('return', 'empty')
    else : 
        p[0] = ('return', p[2])

def p_expression_return(p):
    '''expression : RETURN expression
    | RETURN'''
    if len(p)==2 : 
        p[0] = ('return', 'empty')
    else : 
        p[0] = ('return', p[2])

def flatten_tuple(t):
    flat_tuple = ()
    for item in t:
        if isinstance(item, tuple):
            flat_tuple += flatten_tuple(item)
        else:
            flat_tuple += (item,)
    return flat_tuple

def p_function(p):
    '''function : FUNCTIONDEF NAME LPAREN param RPAREN LBRA linst RBRA
                | FUNCTIONDEF NAME LPAREN RPAREN LBRA linst RBRA
                '''
    
    has_param = isinstance(p[4], tuple)
    has_instructions = (has_param and 'linst' in flatten_tuple(p[7])) or (not has_param and 'linst' in flatten_tuple(p[6]))
    has_return = (has_param and 'return' in flatten_tuple(p[7])) or (not has_param and 'return' in flatten_tuple(p[6]))
    
    if has_param and has_instructions and has_return:
        p[0] = (p[2], p[4], p[7][0], p[7][1])
        functions[p[2]] = (p[4], p[7])
    elif has_param and has_instructions and not has_return:
        p[0] = (p[2], p[4], p[7])
        functions[p[2]] = (p[4], p[7])
    elif has_param and not has_instructions and has_return:
        p[0] = (p[2], p[4], 'empty', p[7])
        functions[p[2]] = (p[4], p[7])
    elif not has_param and has_instructions and has_return:
        p[0] = (p[2], 'empty', p[6][0], p[6][1])
        functions[p[2]] = ('empty', p[6])
    elif not has_param and has_instructions and not has_return:
        p[0] = (p[2], 'empty', p[6])
        functions[p[2]] = ('empty', p[6])
    elif not has_param and not has_instructions and has_return:
        p[0] = (p[2], 'empty', 'empty', p[6])
        functions[p[2]] = ('empty', p[6])

def p_paramdef(p):
    '''param : param COMMA NAME
    | NAME'''
    if len(p)==2 : 
        p[0] = ('param',p[1])
    else : 
        p[0] = ('param',p[1], p[3])

def p_paramcall(p):
    '''paramcall : paramcall COMMA expression
    | expression'''
    if len(p)==2 : 
        p[0] = ('exp',p[1])
    else : 
        p[0] = ('exp',p[1],p[3] )

def p_main(p):
    '''main : linst'''
    p[0] = ('main', p[1])

def p_linst(p):
    '''linst : linst statement SEMI
    | statement SEMI
    | linst controlStruct
    | controlStruct
    | controlStruct linst
    | linst expression SEMI
    | expression SEMI
    | linst return
    | return'''
    if len(p)==2 : 
        p[0] = ('linst', p[1])
    else : 
        p[0] = ('linst', p[1], p[2] if p[2] != ';' else 'empty')

def p_controlStruct(p):
    '''controlStruct : for
    | while
    | if'''
    p[0] = p[1]

def p_expression_function(p):
    '''expression : NAME LPAREN paramcall RPAREN
    | NAME LPAREN RPAREN'''
    if len(p)==4:
        p[0] = ('call', p[1], 'empty')
    else:
        p[0] = ('call', p[1], p[3])

def p_statement_expr(p): 
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = ('print',p[3] )

def p_for(p):
    'for : FOR LPAREN statement SEMI expression SEMI statement RPAREN LBRA linst RBRA'
    p[0] = ('for', p[3], p[5], p[7], p[10])

def p_while(p):
    'while : WHILE LPAREN expression RPAREN LBRA linst RBRA'
    p[0] = ('while', p[3], p[6])

def p_if(p):
    '''if : IF LPAREN expression RPAREN LBRA linst RBRA
    | IF LPAREN expression RPAREN LBRA linst RBRA ELSE LBRA linst RBRA'''
    if len(p)==8 : 
        p[0] = ('if', p[3], p[6], 'empty')
    else : 
        p[0] = ('if', p[3], p[6], ('else', p[10]))
    
def p_statement_assign(p):
    'statement : NAME EGAL expression'
    p[0] = ('assign',p[1],p[3] )
    
def p_expression_binop_inf(p): 
    '''expression : expression INF expression
    | expression INFEG expression
    | expression EGALEGAL expression
    | expression AND expression
    | expression OR expression
    | expression PLUS expression
    | expression TIMES expression
    | expression MINUS expression
    | expression DIVIDE expression
    | expression MODULO expression
    | expression SUP expression
    | expression SUPEG expression'''
    p[0] = (p[2],p[1],p[3])
 
def p_expression_group(p): 
    'expression : LPAREN expression RPAREN' 
    p[0] = p[2] 
    
def p_expression_number(p): 
    'expression : NUMBER' 
    p[0] = p[1] 
    
def p_expression_name(p): 
    'expression : NAME' 
    p[0] =  p[1]

def p_error(p):
    print("Syntax error in input!", p)

import ply.yacc as yacc
import ply.yacc as yacc
import uuid
import graphviz as gv

def printTreeGraph(t):
    graph = gv.Digraph(format='pdf')
    graph.attr('node', shape='circle')
    addNode(graph, t)
    graph.render(filename='img/graph.dot') #Pour Sauvegarder
    graph.view() #Pour afficher

def addNode(graph, t):
    myId = uuid.uuid4()
    if type(t) != tuple:
        graph.node(str(myId), label=str(t))
        return myId
    
    graph.node(str(myId), label=str(t[0]))
    for i in range(1, len(t)):
         graph.edge(str(myId), str(addNode(graph, t[i])), arrowsize='0')

    return myId

yacc.yacc()
yacc.parse(s)