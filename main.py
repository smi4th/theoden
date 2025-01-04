# main.py

from utils import printTreeGraph, prog
from evals import evalInst
from parser import *

from time import time
from sys import argv

def main(entry):

    AST = parse(entry)

    if AST == None:
        prog.error.push("Syntax error")
        prog.error.crash()

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

    if prog.TEST_MODE:
        prog.testOutput()


if __name__ == "__main__":

    if '-f' in argv:
        try:
            with open(argv[argv.index('-f') + 1], 'r') as file:
                entry = file.read()
        except:
            prog.error.push("File not found")
            prog.error.crash()
    else:
        with open('test.txt', 'r') as file:
            entry = file.read()
    
    main(entry)