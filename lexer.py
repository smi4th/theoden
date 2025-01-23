# lexer.py

from utils import prog

import ply.lex as lex

reserved={
        'print':'PRINT',
        'if':'IF',
        'else':'ELSE',
        'while':'WHILE',
        'for':'FOR',
        'fonction':'FUNCTIONDEF',
        'return':'RETURN',
    }

tokens = [ 'INTEGER', 'FLOAT', 'CHAR', 'MINUS', 'PLUS','TIMES','DIVIDE', 'MODULO', 'LPAREN', 'LBRA', 'RBRA', 'LBRACKET', 'RBRACKET',
          'RPAREN', 'OR', 'AND', 'SEMI', 'EGAL', 'NAME', 'INF', 'SUP', 'SUPEG',
          'EGALEGAL','INFEG', 'COMMA','INC','DEC']+ list(reserved.values())

t_PLUS = r'\+' 
t_MINUS = r'-' 
t_TIMES = r'\*' 
t_DIVIDE = r'/' 
t_MODULO = r'%'
t_LPAREN = r'\(' 
t_RPAREN = r'\)' 
t_LBRA = r'\{'
t_RBRA = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
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
t_INC = r'\+\+'
t_DEC = r'\-\-'


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

def t_INTEGER(t): 
    r'(?<!\.)\b\d+\b(?!\.)'
    t.value = int(t.value) 
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CHAR(t):
    r'\'[a-zA-Z0-9]\''
    t.value = t.value[1]
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    prog.error.push(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    prog.error.crash()
    
lex.lex()