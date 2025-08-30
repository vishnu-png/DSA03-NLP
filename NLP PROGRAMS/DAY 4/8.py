# pip install nltk
import nltk
from collections import Counter, defaultdict

# nltk.download('brown'); nltk.download('universal_tagset'); nltk.download('punkt')

# Train a very simple unigram tagger from Brown
tag_counts = defaultdict(Counter)
from nltk.corpus import brown
for sent in brown.tagged_sents(tagset='universal'):
    for w, t in sent:
        tag_counts[w.lower()][t] += 1

def most_likely_tag(word):
    counts = tag_counts.get(word.lower())
    if counts:
        return counts.most_common(1)[0][0]
    return "NOUN"  # default backoff

text = "I will book a table tonight and watch birds fly."
tokens = nltk.word_tokenize(text)
tags = [(w, most_likely_tag(w)) for w in tokens]
print(tags)
