# pip install scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

docs = [
    "The cat sat on the mat.",
    "Dogs and cats are great pets.",
    "I love to play football at the park.",
    "The dog chased the cat near the park.",
]
query = "cat in the park"

vec = TfidfVectorizer(stop_words="english")
X = vec.fit_transform(docs)
q = vec.transform([query])

scores = linear_kernel(q, X).flatten()
ranked = sorted(enumerate(scores), key=lambda x: -x[1])

print("Query:", query)
print("Ranking (doc_index, score):")
for idx, sc in ranked:
    print(idx, round(sc, 4), "=>", docs[idx])
