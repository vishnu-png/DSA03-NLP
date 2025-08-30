# pip install nltk
import nltk
from nltk import PCFG
from nltk.parse import ViterbiParser

pcfg = PCFG.fromstring("""
S -> NP VP [1.0]
NP -> Det N [0.6] | N [0.4]
VP -> V NP [0.7] | V [0.3]
Det -> 'the' [0.6] | 'a' [0.4]
N -> 'dog' [0.5] | 'cat' [0.5]
V -> 'sees' [0.5] | 'runs' [0.5]
""")

parser = ViterbiParser(pcfg)
sent = "the dog sees a cat".split()
for tree in parser.parse(sent):
    print(tree, f"\n(logprob={tree.logprob():.3f})")
