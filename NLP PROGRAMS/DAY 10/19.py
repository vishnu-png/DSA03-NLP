# pip install nltk
import nltk
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

# nltk.download('punkt'); nltk.download('wordnet'); nltk.download('omw-1.4')

sentence = "I went to the bank to deposit money"
tokens = nltk.word_tokenize(sentence)
sense = lesk(tokens, 'bank')  # best synset for 'bank' in context
print("Best sense:", sense, "-", sense.definition() if sense else None)
