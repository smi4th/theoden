# parser.py

from utils import flatten_tuple, prog
from lexer import *

import ply.yacc as yacc

precedence = ( 
        ('left','OR' ), 
        ('left','AND'), 
        ('nonassoc', 'INF', 'INFEG', 'EGALEGAL', 'SUP'), 
        ('left','PLUS', 'MINUS' ), 
        ('left','TIMES', 'DIVIDE', 'MODULO'),
        )

AST = None

def p_start(p):
    '''start : prog'''
    global AST
    AST = p[1]

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

def p_function(p):
    '''function : FUNCTIONDEF NAME LPAREN param RPAREN LBRA linst RBRA
                | FUNCTIONDEF NAME LPAREN RPAREN LBRA linst RBRA
                '''
    has_param = isinstance(p[4], tuple)
    has_instructions = (has_param and 'linst' in flatten_tuple(p[7])) or (not has_param and 'linst' in flatten_tuple(p[6]))
    
    if has_param and has_instructions:
        p[0] = (p[2], p[4], p[7])
        prog.functions[p[2]] = (p[4], p[7])
    elif has_param and not has_instructions:
        p[0] = (p[2], p[4], p[6])
        prog.functions[p[2]] = (p[4], p[7])
    elif not has_param and has_instructions:
        p[0] = (p[2], 'empty', p[6])
        prog.functions[p[2]] = ('empty', p[6])
    elif not has_param and not has_instructions:
        p[0] = (p[2], 'empty', p[5])
        prog.functions[p[2]] = ('empty', p[6])

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
        p[0] = ('expr',p[1])
    else : 
        p[0] = ('expr',p[1],p[3] )

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
    '''statement : PRINT LPAREN paramcall RPAREN '''
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
    | expression SUPEG expression
    | expression INC
    | expression DEC '''
    if len(p)==4 :
        p[0] = (p[2],p[1],p[3])
    else :
        p[0] = (p[2],p[1])
 
def p_expression_group(p): 
    'expression : LPAREN expression RPAREN' 
    p[0] = p[2] 
    
def p_expression_integer(p): 
    '''expression : INTEGER
    | MINUS INTEGER'''
    if len(p)==2 :
        p[0] = ('int',p[1])
    else :
        p[0] = ('int',-p[2])    
    
def p_expression_float(p):
    '''expression : FLOAT
    | MINUS FLOAT'''
    if len(p)==2 :
        p[0] = ('float',p[1])
    else :
        p[0] = ('float',-p[2])

def p_expression_name(p):
    '''expression : NAME
    | MINUS NAME'''
    if len(p)==2 :
        p[0] = ('var',p[1])
    else :
        p[0] = ('var',-p[2])

def p_error(p):
    print("Syntax error in input!", p)

yacc.yacc()
def parse(data):
    global AST
    yacc.parse(data)
    return AST