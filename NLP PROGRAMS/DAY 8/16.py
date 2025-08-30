# pip install spacy
# python -m spacy download en_core_web_sm
import spacy
nlp = spacy.load("en_core_web_sm")

doc = nlp("Apple is looking at buying U.K. startup for $1 billion, said Tim Cook in London.")
for ent in doc.ents:
    print(ent.text, ent.label_)
