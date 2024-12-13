# main.py

from utils import printTreeGraph, prog
from evals import evalInst
from parser import *

from time import time

def main():

    AST = parse(ENTRY)
    prog.ast = AST

    prog.generateCallStack()

    if prog.DEBUG_AST:
        printTreeGraph(AST)
        print(prog.callPile)


    if prog.DEBUG_TIME:
        start = time()

    while not prog.callPile.empty():
        evalInst(prog.callPile.pop())
    
    if prog.DEBUG_TIME:
        print(f"Execution time: {time() - start}")


    if prog.DEBUG_MEMORY:
        print(f"Memory stack: {[str(i) for i in prog.memoryStack]}")


with open('test.txt', 'r') as file:
    ENTRY = file.read()

if __name__ == "__main__":
    main()