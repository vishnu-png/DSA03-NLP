# pip install nltk
import nltk
from nltk.grammar import CFG
from nltk.parse import EarleyChartParser

grammar = CFG.fromstring("""
S -> S Conj S | NP VP
Conj -> 'and'
NP -> Det N | N
VP -> V NP | V
Det -> 'the' | 'a'
N -> 'dog' | 'cat' | 'park'
V -> 'sees' | 'runs'
""")

parser = EarleyChartParser(grammar)
sentence = "the dog sees the cat and the cat runs"
for tree in parser.parse(sentence.split()):
    print(tree)
