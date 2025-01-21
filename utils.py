# utils.py

import uuid
import graphviz as gv
from sys import argv

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

def wrapper(f):
    def wrap(*args, **kwargs):
        if prog.DEBUG_WRAPPER:
            print(f"\033[32m{f.__name__}\033[0m")
            for arg in args:
                print(f"\t\033[33m{arg}\033[0m")
        res = f(*args, **kwargs)
        if prog.DEBUG_WRAPPER:
            print(f"\033[34m  {f.__name__} -> {res}\033[0m")
        return res
    return wrap

def flatten_tuple(t):
    flat_tuple = ()
    for item in t:
        if isinstance(item, tuple):
            flat_tuple += flatten_tuple(item)
        else:
            flat_tuple += (item,)
    return flat_tuple

@wrapper
def isTailRecursion(linst):
    for ret in extract_returns(linst):
        # if the return is a call to the same function
        if ret[1][0] == 'call' and ret[1][1] == linst[0][0]:
            return True
        
        # if the return is just a variable or a value
        if isinstance(ret[1], str) or isinstance(ret[1], int):
            return True
        
    return False

def extract_returns(tup):
    result = []
    if isinstance(tup, tuple):
        if tup[0] == 'return':
            result.append(tup)
        # Recursively process the rest of the tuple
        for item in tup[1:]:
            result.extend(extract_returns(item))
    return result

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

class Pile:
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
        for stack in self.p[::-1]:
            if name in stack:
                stack[name] = value
                return
        self.p[-1][name] = value

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
        return "---CALL STACK---\n" + "\n".join([str(elt) for elt in self.p[::-1]]) + "\n---END---"
    
class Errors(Pile):
    def __init__(self):
        super().__init__()
        self.p = []
    def crash(self):
        if prog.TEST_MODE:
            print(self)
        else:
            print(f"\033[31m{self}\033[0m", end="\033[37m")
        exit(1)

    def __repr__(self):
        return "---ERRORS---\n" + "\n".join([str(elt) for elt in self.p]) + "\n---END---"

class Program:
    def __init__(self):
        self.callPile = Pile()
        self.callPile.block_keywords = ['functions', 'if', 'for', 'while', 'assign', 'call', 'print']
        self.callPile.function_keywords = ['main', 'linst']

        self.error = Errors()
        self.memoryStack = [Pile()]
        self.functions = {}

        self.ast = None

        self.DEBUG_WRAPPER = False
        self.DEBUG_TIME = False
        self.DEBUG_MEMORY = False
        self.DEBUG_AST = False
        self.TEST_MODE = False

    def generateCallStack(self):
        self.callPile.p = []
        self.callPile.translate(self.ast)
        self.callPile.reverse()

    def testOutput(self):
        print("---TEST OUTPUT---")
        print("---MEMORY---")
        for stack in self.memoryStack:
            for s in stack.p:
                for key, value in s.items():
                    print(f"{key} = {value}")

        print("---FUNCTIONS---")
        for key, value in self.functions.items():
            print(f"{key} = {value}")

prog = Program()