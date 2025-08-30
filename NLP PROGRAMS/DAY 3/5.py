# pip install nltk
import nltk
from nltk.stem import PorterStemmer

# nltk.download('punkt')  # first time
ps = PorterStemmer()
words = nltk.word_tokenize("Caresses ponies caresser cats running agreed meetings")
print([(w, ps.stem(w)) for w in words])
