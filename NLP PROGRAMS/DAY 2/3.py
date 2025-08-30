# pip install nltk
import nltk
from nltk.stem import WordNetLemmatizer

# one-time downloads (uncomment on first run)
# nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet'); nltk.download('omw-1.4')

text = "The cats were running faster than the mice."
tokens = nltk.word_tokenize(text)
pos = nltk.pos_tag(tokens)

lemm = WordNetLemmatizer()

# Simple POS->WordNet POS mapping
def wn_pos(tag):
    return {'J':'a','V':'v','N':'n','R':'r'}.get(tag[0], 'n')

morph = [(w, p, lemm.lemmatize(w, wn_pos(p))) for (w, p) in pos]
print(morph)
