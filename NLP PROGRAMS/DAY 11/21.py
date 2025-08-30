# pip install spacy nltk
# python -m spacy download en_core_web_sm
import spacy
from nltk.corpus import wordnet as wn
import nltk
# nltk.download('wordnet'); nltk.download('omw-1.4')

nlp = spacy.load("en_core_web_sm")
sentence = "The quick brown fox jumps over the lazy dog."

doc = nlp(sentence)
for chunk in doc.noun_chunks:
    print("Noun Phrase:", chunk.text)
    head = chunk.root.text
    synsets = wn.synsets(head, pos=wn.NOUN)
    if synsets:
        print("  Meaning:", synsets[0].definition())
    else:
        print("  Meaning: not found")
