# Simple pluralization via rule "states"
def pluralize(noun: str) -> str:
    vowels = "aeiou"
    # States: END_Y, SIBILANT, DEFAULT
    if noun.endswith("y") and (len(noun) > 1 and noun[-2].lower() not in vowels):
        # consonant + y -> ies
        return noun[:-1] + "ies"
    elif noun.endswith(("s", "sh", "ch", "x", "z")):
        # sibilant -> es
        return noun + "es"
    else:
        return noun + "s"

tests = ["city", "dog", "box", "buzz", "dish", "boy"]
for t in tests:
    print(t, "->", pluralize(t))
