# main.py

from utils import printTreeGraph, prog
from evals import evalInst
from parser import *
import argparse

from time import time

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

    parser = argparse.ArgumentParser(description='Run a program written in the language')
    parser.add_argument('-f', '--file', type=str, help='File to run', required=False)
    parser.add_argument('-t', '--test', action='store_true', help='Run in test mode', required=False)
    parser.add_argument('-w', '--wrapper', action='store_true', help='Debug wrapper', required=False)
    parser.add_argument('-s', '--time', action='store_true', help='Debug time', required=False)
    parser.add_argument('-m', '--memory', action='store_true', help='Debug memory', required=False)
    parser.add_argument('-a', '--ast', action='store_true', help='Debug AST', required=False)

    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, 'r') as file:
                entry = file.read()
        except:
            prog.error.push("File not found")
            prog.error.crash()
    else:
        with open('test.txt', 'r') as file:
            entry = file.read()
    
    prog.TEST_MODE = args.test
    prog.DEBUG_WRAPPER = args.wrapper
    prog.DEBUG_TIME = args.time
    prog.DEBUG_MEMORY = args.memory
    prog.DEBUG_AST = args.ast
    
    main(entry)