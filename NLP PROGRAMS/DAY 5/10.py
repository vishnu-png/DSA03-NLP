# Start with all words as NOUN, then apply simple transformations (toy example)
import nltk
# nltk.download('punkt')

def transform_tags(tokens):
    tags = ["NOUN"] * len(tokens)

    # Rule 1: exact word 'to' -> 'PRT' (particle)
    for i, w in enumerate(tokens):
        if w.lower() == "to":
            tags[i] = "PRT"

    # Rule 2: words ending with 'ing' -> VBG
    for i, w in enumerate(tokens):
        if w.lower().endswith("ing"):
            tags[i] = "VBG"

    # Rule 3: word after 'the' -> NOUN
    for i in range(len(tokens)-1):
        if tokens[i].lower() == "the":
            tags[i+1] = "NOUN"

    return list(zip(tokens, tags))

sent = "The dog is going to the running track"
tokens = nltk.word_tokenize(sent)
print(transform_tags(tokens))
