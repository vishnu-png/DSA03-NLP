# pip install nltk
import nltk
from nltk.grammar import CFG
from nltk.parse import RecursiveDescentParser

# nltk.download('punkt')

grammar = CFG.fromstring("""
S -> NP VP
NP -> Det N | Det Adj N | N
VP -> V NP | V
Det -> 'the' | 'a'
Adj -> 'big' | 'small'
N -> 'dog' | 'cat' | 'bone'
V -> 'eats' | 'runs'
""")

parser = RecursiveDescentParser(grammar)
sent = "the big dog eats a bone"
tokens = nltk.word_tokenize(sent)
for tree in parser.parse(tokens):
    print(tree)
