# pip install scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

text = [
    "The cat chased the mouse.",
    "It was very fast and hungry.",
    "The Eiffel Tower is in Paris."
]

vec = TfidfVectorizer(stop_words="english")
X = vec.fit_transform(text)

coherence_scores = []
for i in range(len(text)-1):
    sim = cosine_similarity(X[i], X[i+1])[0,0]
    coherence_scores.append(sim)

print("Coherence scores between sentences:", coherence_scores)
print("Overall coherence:", sum(coherence_scores)/len(coherence_scores))
