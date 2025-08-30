# pip install nltk
import nltk
# nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')

sent = "Time flies like an arrow; fruit flies like a banana."
tokens = nltk.word_tokenize(sent)
print(nltk.pos_tag(tokens))
