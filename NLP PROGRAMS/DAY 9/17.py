# pip install nltk
import nltk
from nltk.corpus import wordnet as wn

# nltk.download('wordnet'); nltk.download('omw-1.4')

word = "bank"
for syn in wn.synsets(word):
    print("Synset:", syn.name())
    print("  Lemmas:", [l.name() for l in syn.lemmas()])
    print("  Definition:", syn.definition())
    print("  Examples:", syn.examples())
    print()
