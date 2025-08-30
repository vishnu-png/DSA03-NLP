# pip install nltk
from nltk.tree import Tree

# Manually creating a tree (as an example)
t = Tree('S', [
    Tree('NP', [Tree('Det', ['the']), Tree('N', ['cat'])]),
    Tree('VP', [Tree('V', ['eats']),
                Tree('NP', [Tree('Det', ['a']), Tree('N', ['fish'])])])
])
print(t)
t.pretty_print()  # renders an ASCII tree
