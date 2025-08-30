# Very small parser for terms, predicates, connectives: ~, &, |, -> and quantifiers: forall, exists
# Example: "forall x (Human(x) -> Mortal(x)) & Human(Socrates)"

import re
from collections import namedtuple

Var     = namedtuple("Var", "name")
Const   = namedtuple("Const", "name")
Pred    = namedtuple("Pred", "name args")
Not     = namedtuple("Not", "phi")
And     = namedtuple("And", "left right")
Or      = namedtuple("Or", "left right")
Imply   = namedtuple("Imply", "left right")
ForAll  = namedtuple("ForAll", "var phi")
Exists  = namedtuple("Exists", "var phi")

TOKENS = r"\s*(forall|exists|[A-Za-z_]\w*|->|[(),~&|])"
def tokenize(s): return [t for t in re.findall(TOKENS, s) if t.strip()]

class Parser:
    def __init__(self, toks): self.toks, self.i = toks, 0
    def peek(self): return self.toks[self.i] if self.i < len(self.toks) else None
    def eat(self, t=None):
        tok = self.peek()
        if tok is None or (t and tok != t): raise ValueError(f"Expected {t}, got {tok}")
        self.i += 1; return tok

    def parse(self): return self.implication()

    def implication(self):
        left = self.disjunction()
        if self.peek() == "->":
            self.eat("->")
            right = self.implication()
            return Imply(left, right)
        return left

    def disjunction(self):
        left = self.conjunction()
        while self.peek() == "|":
            self.eat("|")
            right = self.conjunction()
            left = Or(left, right)
        return left

    def conjunction(self):
        left = self.unary()
        while self.peek() == "&":
            self.eat("&")
            right = self.unary()
            left = And(left, right)
        return left

    def unary(self):
        tok = self.peek()
        if tok == "~":
            self.eat("~")
            return Not(self.unary())
        if tok == "forall":
            self.eat("forall"); var = Var(self.eat())
            self.eat("("); phi = self.parse(); self.eat(")")
            return ForAll(var, phi)
        if tok == "exists":
            self.eat("exists"); var = Var(self.eat())
            self.eat("("); phi = self.parse(); self.eat(")")
            return Exists(var, phi)
        if tok == "(":
            self.eat("("); phi = self.parse(); self.eat(")"); return phi
        # predicate or variable/constant
        name = self.eat()
        if self.peek() == "(":
            self.eat("("); args = []
            if self.peek() != ")":
                while True:
                    args.append(self.term())
                    if self.peek() == ",":
                        self.eat(","); continue
                    break
            self.eat(")")
            return Pred(name, args)
        return Var(name) if name[0].islower() else Const(name)

    def term(self):
        name = self.eat()
        return Var(name) if name[0].islower() else Const(name)

s = "forall x (Human(x) -> Mortal(x)) & Human(Socrates)"
ast = Parser(tokenize(s)).parse()
print(ast)
