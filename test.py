ch1= ('prog', ('main', ('linst', ('linst', ('assign', 'a', 1), 'empty'), ('if', ('>', 'a', 1), ('linst', ('assign', 'a', 2), 'empty'), ('else', ('linst', ('assign', 'a', 3), 'empty'))))), 'empty')
"""
a=1;
if (a>1) {
    a=2;
}
"""
class Pile:

    def __init__(self):
        self.pile = []
        self.block_keywords = ['functions', 'if', 'for', 'while', 'assign', 'call']
        self.function_keywords = ['main', 'linst']

    def push(self, element):
        self.pile.append(element)

    def pop(self):
        return self.pile.pop()

    def top(self):
        return self.pile[-1]

    def is_empty(self):

        return len(self.pile) == 0

    def __str__(self):

        return "---CALL STACK---\n" + "\n".join([str(elt) for elt in self.pile]) + "\n---END---"

    def translate(self, linst):

        for elt in linst:
            if isinstance(elt, tuple):
                if elt[0] in self.block_keywords and elt[0] not in self.function_keywords:
                    self.push(elt)
                    continue
                self.translate(elt[1:])


callStack = Pile()
callStack.translate(ch1)
print(callStack)