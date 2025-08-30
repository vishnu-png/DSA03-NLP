# FSA for strings over {a,b} that end with 'ab'
def accepts_end_ab(s: str) -> bool:
    # States: S0 (start), S1 (seen a), S2 (other), ACCEPT (ends with 'ab')
    state = "S0"
    for ch in s:
        if ch not in "ab":
            return False
        if state == "S0":
            state = "S1" if ch == "a" else "S2"
        elif state == "S1":
            state = "ACCEPT" if ch == "b" else "S1"
        elif state == "S2":
            state = "S1" if ch == "a" else "S2"
        elif state == "ACCEPT":
            state = "S1" if ch == "a" else "S2"
    return state == "ACCEPT"

tests = ["", "ab", "aab", "aba", "b", "aaab", "ba"]
for t in tests:
    print(t, accepts_end_ab(t))
