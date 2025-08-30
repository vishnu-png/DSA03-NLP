# Simple heuristic dialog act recognizer
def classify_dialog_act(utterance):
    utterance = utterance.lower()
    if utterance.endswith("?"):
        return "QUESTION"
    elif utterance.startswith(("hi", "hello", "hey")):
        return "GREETING"
    elif "thank" in utterance:
        return "THANKS"
    elif "bye" in utterance:
        return "CLOSING"
    else:
        return "STATEMENT"

dialog = [
    "Hello!",
    "How are you?",
    "I am doing fine.",
    "Thank you very much!",
    "Bye!"
]

for u in dialog:
    print(u, "=>", classify_dialog_act(u))
