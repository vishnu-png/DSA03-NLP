# pip install nltk
import nltk
from nltk.tag import RegexpTagger

# nltk.download('punkt')
rules = [
    (r'\d+(\.\d+)?$', 'NUM'),
    (r'.*ing$', 'VBG'),
    (r'.*ed$', 'VBD'),
    (r'.*ly$', 'ADV'),
    (r'.*ness$', 'NOUN'),
    (r'(The|the|A|a|An|an)$', 'DET'),
    (r'.*', 'NOUN')
]
tagger = RegexpTagger(rules)

text = "The quickly moving clouds darkened suddenly"
tokens = nltk.word_tokenize(text)
print(tagger.tag(tokens))
