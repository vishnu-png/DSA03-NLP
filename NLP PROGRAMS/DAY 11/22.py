# pip install spacy
# python -m spacy download en_core_web_sm
# Note: spaCy v3 does not have built-in coref; for simple demo we do heuristic pronoun resolution.

import spacy
nlp = spacy.load("en_core_web_sm")

text = "Alice went to the park. She was very happy."
doc = nlp(text)

entities = [ent.text for ent in doc.ents]
print("Entities:", entities)

for token in doc:
    if token.pos_ == "PRON":
        print(f"Pronoun '{token.text}' may refer to:", entities[-1] if entities else "Unknown")
