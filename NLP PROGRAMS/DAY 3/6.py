import random
import re
from collections import defaultdict

text = """
the cat sat on the mat . the cat ate a rat . the rat sat too .
the dog saw the cat . the dog chased the cat . the cat ran .
"""

# Build bigram model
tokens = re.findall(r"\w+|[.]", text.lower())
bigrams = defaultdict(list)
for w1, w2 in zip(tokens, tokens[1:]):
    bigrams[w1].append(w2)

def generate(start="the", max_len=30):
    w = start
    out = [w]
    for _ in range(max_len-1):
        nexts = bigrams.get(w) or ["."]
        w = random.choice(nexts)
        out.append(w)
        if w == ".":
            break
    return " ".join(out)

for _ in range(3):
    print(generate("the"))
