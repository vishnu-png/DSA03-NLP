import re

SING_VERBS = {"runs", "eats", "is", "has", "likes"}
PLUR_VERBS = {"run", "eat", "are", "have", "like"}

def is_plural_noun(word):
    return word.endswith('s') and word.lower() not in {"is"}

def check_agreement(sentence: str):
    # super-simplified heuristic: pattern "<NP> <V>"
    tokens = re.findall(r"\w+", sentence.lower())
    if len(tokens) < 2:
        return False, "Too short"

    subj, verb = tokens[0], tokens[1]
    subj_plural = is_plural_noun(subj)
    if subj_plural and verb in PLUR_VERBS:
        return True, "Plural subject with plural verb ✔"
    if not subj_plural and verb in SING_VERBS:
        return True, "Singular subject with singular verb ✔"
    return False, f"Agreement error: subject={'plural' if subj_plural else 'singular'}, verb='{verb}'"

tests = ["cats are hungry", "cat eats", "cats eats", "dog run"]
for s in tests:
    print(s, "=>", check_agreement(s))
